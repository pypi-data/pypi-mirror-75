import io
import platform
import os
import re
import tempfile
import base64
from contextlib import contextmanager
from enum import Enum, auto
from typing import Optional, List, Tuple, Set, Iterator, Sequence, Union
from urllib.error import HTTPError
from urllib.parse import unquote, quote
import urllib.request

from dataclasses import dataclass, fields as dataclass_fields

from .parser import compile_grammar
from .deserialize import deserialize
from .cmd import cmd as _cmd, cmd_devnull, cmd_pipe, cmd_pipe_stdout, expect, GPGError


@dataclass(frozen=True)
class Uid:
    """GPG User ID representation. The GPGP user ID format contains the user's
    name and email in the format shown in the example below.
    Example: Alice (Alice's test PGP key) <alice@example.com>
    """
    full_name: str
    email: str

    def __repr__(self):
        return f"{self.full_name} <{self.email}>"

    @staticmethod
    def from_str(s):
        if s is None or s[0] == "[" and s[-1] == "]":
            # Something like "[User ID not found]" (can be translated into other languages)
            return None
        try:
            full_name, email = s.rstrip(">").split(" <")
        except (AttributeError, ValueError):
            raise ValueError(f"Wrong uid format: '{s}'")
        return Uid(full_name=full_name, email=email)


class KeyType(Enum):
    """Representation of the GPG key type. Only two type of keys exist:
    public and secret (often also referred to as 'private')"""
    public = auto()
    secret = auto()


class TrustModel(Enum):
    pgp = "pgp"
    classic = "classic"
    tofu = "tofu"             # Trust on first use.
    tofu_pgp = "tofu+pgp"
    direct = "direct"
    always = "always"
    auto = "auto"


class Validity(Enum):
    unknown_new = "o"  # Unknown (this key is new to the system)
    invalid = "i"      # The key is invalid (e.g. missing self-signature)
    disabled = "d"     # The key has been disabled
    #                  # (deprecated - use the 'D' in field 12 instead)
    revoked = "r"      # The key has been revoked
    expired = "e"      # The key has expired
    unknown = "-"      # Unknown validity (i.e. no value assigned)
    undefined = "q"    # Undefined validity.  '-' and 'q' may safely be
    #                  # treated as the same value for most purposes
    not_valid = "n"    # The key is not valid
    marginal_valid = "m"    # The key is marginally valid.
    fully_valid = "f"       # The key is fully valid
    ultimately_valid = "u"  # The key is ultimately valid. This often means
    #                       # that the secret key is available, but any key
    #                       # may be marked as ultimately valid.
    well_known_private_part = "w"  # The key has a well known private part.
    special_validity = "s"         # The key has special validity.  This means
    #                              # that it might be self - signed and
    #                              # expected to be used in the STEED system.


class SignatureValidity(Enum):
    good = "!"
    bad = "-"
    no_public_key = "?"
    error = "%"


key_capabilities = {}


def key_capability(key: str):
    def decorator(cls):
        wrapped = dataclass(frozen=True)(cls)
        for variant in {key, key.upper()}:
            key_capabilities[variant] = wrapped(variant.isupper())
        return wrapped
    return decorator


@dataclass(frozen=True)
class KeyCapabilityBase:
    global_: bool


class KeyCapability:
    @key_capability("e")
    class Encrypt(KeyCapabilityBase):
        pass

    @key_capability("s")
    class Sign(KeyCapabilityBase):
        pass

    @key_capability("c")
    class Certify(KeyCapabilityBase):
        pass

    @key_capability("a")
    class Authentication(KeyCapabilityBase):
        pass

    @key_capability("?")
    class Unknown(KeyCapabilityBase):
        pass

    @key_capability("D")
    class Disabled(KeyCapabilityBase):
        pass


@dataclass(frozen=True)
class Signature:
    issuer_uid: Optional[Uid]
    issuer_key_id: str
    signature_class: str
    creation_date: str
    expiration_date: Optional[str] = None


@dataclass(frozen=True)
class RevocationSignature(Signature):
    reason: Optional[str] = None
    comment: Optional[str] = None


@dataclass(frozen=True)
class SubKey:
    key_id: str
    key_type: KeyType
    fingerprint: str
    key_length: int
    pub_key_algorithm: int
    creation_date: str
    validity: Validity = Validity.unknown
    expiration_date: Optional[str] = None
    key_capabilities: Set[KeyCapabilityBase] = frozenset()
    signatures: Tuple[Signature] = ()

    @property
    def valid_signatures(self) -> List[Signature]:
        rev_sig_ids = {s.issuer_key_id for s in self.signatures if isinstance(
            s, RevocationSignature)}
        return [s for s in self.signatures if s.issuer_key_id not in rev_sig_ids]


# Value used to indicate a missing required field.
_no_default = object()


@dataclass(frozen=True)
class Key(SubKey):
    uids: Tuple[Uid] = _no_default
    owner_trust: str = "-"
    sub_keys: Tuple[SubKey] = ()
    origin: Optional[str] = None

    def __post_init__(self):
        """Raise error if there is any required field with no value."""
        missing_fields = [
            f.name
            for f in dataclass_fields(type(self))
            if getattr(self, f.name) is _no_default]
        if missing_fields:
            l = len(missing_fields)
            plural = "s" if l > 1 else ""
            fields = ", ".join(f"'{f}'" for f in missing_fields)
            raise TypeError(
                f"__init__ missing {l} required argument{plural}: {fields}")


@dataclass(frozen=True)
class KeyInfo:
    uid: Uid
    fingerprint: str
    key_algorithm: int
    key_length: int
    creation_date: str
    expiration_date: Optional[str]


def parse_key_capabilities(s: Optional[str]):
    if s is None:
        return frozenset()
    return frozenset(key_capabilities[c] for c in s)


@dataclass
class ColonRecordBase:
    """According to [gnupg.git]/doc/DETAILS
    """
    validity: Optional[Validity] = None  # 2
    key_length: Optional[int] = None  # 3
    pub_key_algorithm: Optional[int] = None
    key_id: Optional[str] = None  # 5
    creation_date: Optional[str] = None
    expiration_date: Optional[str] = None
    cert_S_N_uid_hash_trust_signature_info: Optional[str] = None
    owner_trust: Optional[str] = None
    user_id: Optional[str] = None  # 10
    signature_class: Optional[str] = None
    key_capabilities: parse_key_capabilities = frozenset()
    issuer: Optional[str] = None
    flag: Optional[str] = None
    token_S_N: Optional[str] = None  # 15
    hash_algorithm: Optional[str] = None
    curve_name: Optional[str] = None
    compliance_flags: Optional[str] = None
    last_update: Optional[str] = None
    origin: Optional[str] = None  # 20
    comment: Optional[str] = None

    def into(self):
        return self


unimplemented_col_rec_ids = (
    "crt",  # X.509 certificate
    "crs",  # X.509 certificate and secret key available
    "uat",  # User attribute (same as user id except for field 10).
    "rvs",  # Revocation signature (standalone) [since 2.2.9]
    "pkd",  # Public key data [*]
    "grp",  # Keygrip
    "rvk",  # Revocation key
    "tfs",  # TOFU statistics [*]
    "tru",  # Trust database information [*]
    "spk",  # Signature subpacket [*]
    "cfg"   # Configuration data [*]
)

col_rec_types = {}


def col_rec_type(identifier):
    def decorator(cls):
        col_rec_types[identifier] = cls
        return cls
    return decorator


def extract_key_fields(rec):
    fields = ("validity", "key_length", "pub_key_algorithm", "key_id",
              "creation_date", "expiration_date", "owner_trust",
              "key_capabilities", "origin")
    return {key: val for key, val in
            ((f, getattr(rec, f, None)) for f in fields)
            if val is not None
            }


@col_rec_type("sec")
class ColonRecordSec(ColonRecordBase):
    """Secret key"""

    def into(self):
        return Factory(key_type=KeyType.secret, **extract_key_fields(self))


@col_rec_type("pub")
class ColonRecordPub(ColonRecordBase):
    """Public key"""

    def into(self):
        return Factory(key_type=KeyType.public, **extract_key_fields(self))


@col_rec_type("sub")
class ColonRecordSub(ColonRecordBase):
    """ Subkey (secondary key) """

    def into(self):
        return SubKeyFactory(key_type=KeyType.public,
                             **extract_key_fields(self))


@col_rec_type("ssb")
class ColonRecordSsb(ColonRecordBase):
    """ Subkey (secondary key) """

    def into(self):
        return SubKeyFactory(key_type=KeyType.secret,
                             **extract_key_fields(self))


@col_rec_type("uid")
class ColonRecordUid(ColonRecordBase):
    """User id"""

    def into(self):
        return Uid.from_str(self.user_id)


@col_rec_type("fpr")
class ColonRecordFpr(ColonRecordBase):
    """Fingerprint"""

    def into(self):
        if self.user_id is None:
            raise ValueError("Field 'user_id' missing in record")
        return self.user_id


@col_rec_type("sig")
@dataclass
class ColonRecordSig(ColonRecordBase):
    """Signature"""
    validity: Optional[SignatureValidity]  # 2

    def into_dict(self):
        uid = Uid.from_str(self.user_id)
        return dict(
            issuer_uid=uid,
            issuer_key_id=self.key_id,
            creation_date=self.creation_date,
            expiration_date=self.expiration_date,
            signature_class=self.signature_class)

    def into(self):
        return Signature(**self.into_dict())


@col_rec_type("rev")
@dataclass
class ColonRecordRev(ColonRecordSig):
    """Revocation Signature"""

    def into(self):
        sig = self.into_dict()
        sig_class = sig.pop("signature_class")
        try:
            sig_class, revocation_reason = sig_class.split(",")
        except ValueError:
            revocation_reason = None
        return RevocationSignature(
            comment=self.comment,
            signature_class=sig_class,
            reason=revocation_reason,
            **sig)


def parse_data_class(T: type, args: tuple):
    fields = (f.type for f in dataclass_fields(T))
    return T(*(deserialize(f_type)(arg) for f_type, arg in zip(fields, args)))


def lex_colon(payload: io.IOBase) -> Iterator:
    """Tokenizes the output of a call to the gpg command to list keys (payload)
    one line at a time. Works for both commands to list public or secret keys.
    Example of payload:
        tru::1:1574434353:0:3:1:5
        pub:u:4096:1:12477DE52DAD86CC:1574434343:::u:::escaESCA:
        fpr:::::::::621A2A449F234A0E9246CF8212477DE52DAD86CC:
        uid:u::::1574434343::9F08B014A8964D2FCA0B04A7B11CF5FDFD12DF13::bob <bob@example.com>:
        sub:u:4096:1:CFAF4D7B40DAF86B:1574434343::::::esa:
        fpr:::::::::39D91E3C8C9C2C0677F1A74BCFAF4D7B40DAF86B:

    :param payload: stream of bytes corresponding to the output of the gpg
        command.
    :return: generator of "token" that are either a "Factory" object or string.
    :raises ValueError:
    """
    # Loop through the output of the GPG command one line at a time.
    for rec in payload:
        rec = rec.rstrip(b"\n")
        if not rec:
            continue

        # Split line by ':' separator. The first element of the line is the
        # "type of record" (e.g. pub = public key, sub = sub key)
        t_id, *args = map(lambda s: s if s else None,
                          rec.decode("utf-8", "replace").split(":"))
        args = args[:len(dataclass_fields(ColonRecordBase))]
        if t_id in unimplemented_col_rec_ids:
            continue
        try:
            token = parse_data_class(col_rec_types[t_id], args).into()
        except BaseException as e:
            raise ValueError(f"Error while parsing row of type {t_id}"
                             f"\n{format(e)}"
                             f"\ncolumns: {args}")
        if token is not None:
            yield token


class Factory:
    type_ = Key

    def __init__(self, origin: Optional[str] = None, **kwargs):
        self.kwargs = kwargs
        if origin:
            origin = origin.replace("\\x3a", ":").lstrip("0123456789 ")
            self.kwargs["origin"] = origin or None

    def append(self, key, val):
        self.kwargs[key] = self.kwargs.get(key, ()) + (val,)
        return self

    def append_subkey(self, val):
        if self.kwargs["key_type"] != val.key_type:
            raise ValueError(f"Wrong sub key type '{val.key_type}'")
        return self.append("sub_keys", val)

    def set(self, key, val):
        if key in self.kwargs:
            raise ValueError(f"Key '{key}' already set")
        self.kwargs[key] = val
        return self

    def build(self):
        try:
            return self.type_(**self.kwargs)
        except (TypeError, ValueError) as e:
            raise type(e)(e.args[0].replace("__init__", self.type_.__name__))


class SubKeyFactory(Factory):
    type_ = SubKey


# Factory, type : rule how to transform subsequences of tokens
# into reduced token sequences. For example, in:
#  -> (Factory, str): lambda fac, fpr: [fac.set("fingerprint", fpr)]
# the rule (lambda function) defines how to add the string (fingerprint) to
# the Factory (i.e. the main key object).
key_parser = compile_grammar({
    ((Factory, SubKeyFactory), Uid): lambda fac, uid: [fac.append("uids", uid)],
    ((Factory, SubKeyFactory), str): lambda fac, fpr: [fac.set("fingerprint", fpr)],
    ((Factory, SubKeyFactory), (Signature, RevocationSignature)):
    lambda fac, sig: [fac.append("signatures", sig)],
    (Factory, SubKey): lambda fac, sub: [fac.append_subkey(sub)],
    ((Factory, SubKeyFactory), list): lambda fac, lst: [fac.build(), lst],
    (SubKeyFactory, SubKey): lambda fac, key: [fac.build(), key],
    (Key, list): lambda key, lst: [[key] + lst],
}, list)


def parse_keys(payload: io.IOBase):
    return key_parser(list(lex_colon(payload)) + [[]])


def parse_search_keys(source: io.IOBase) -> List[KeyInfo]:
    """According to https://tools.ietf.org/html/draft-shaw-openpgp-hkp-00"""
    try:
        line = next(source).rstrip(b"\r\n")
    except StopIteration:
        return
    if not line.startswith(b"info:"):
        raise ValueError("Unknown response format from gpg, starting with\n" +
                         line.decode('utf-8', 'replace'))
    for line in source:
        line = line.decode('utf-8', 'replace').rstrip("\r\n")
        if not line:
            continue
        try:
            hdr_key, fingerprint, algorithm, key_length, \
                creation_date, expiration_date, _ = line.split(":")
        except ValueError:
            raise ValueError(f"Wrong format for search_key: {line}")
        try:
            hdr_uid, uid, uid_creation_date, uid_expiration_date, _ = next(
                source).decode('utf-8', 'replace').rstrip("\n").split(":")
        except StopIteration:
            raise ValueError("Unexpected end of source. Expected 'uid:' line")
        if hdr_key != "pub":
            raise ValueError(f"Unknown response format from gpg: "
                             f"expected 'pub:', got '{hdr_key}'")
        if hdr_uid != "uid":
            raise ValueError(f"Unknown response format from gpg: "
                             f"expected 'uid:', got '{hdr_uid}'")
        if creation_date and uid_creation_date and creation_date != uid_creation_date:
            raise ValueError(
                f"Key {fingerprint}: Mismatch in creation date")
        if expiration_date and uid_expiration_date and expiration_date != uid_expiration_date:
            raise ValueError(
                f"Key {fingerprint}: Mismatch in expiration date")
        yield KeyInfo(
            uid=Uid.from_str(unquote(uid)),
            fingerprint=fingerprint,
            key_algorithm=int(algorithm),
            creation_date=creation_date,
            expiration_date=expiration_date or None,
            key_length=int(key_length))


def normalize_fingerprint(fp: str):
    valid_len = (8, 16, 32, 40)
    s = re.sub(r"^0[xX]", "", re.sub(r"\s", "", fp))
    if len(s) not in valid_len:
        raise ValueError("Invalid fingerprint length. "
                         f"Allowed lengths {valid_len}")
    try:
        int(s, 16)
    except ValueError:
        raise ValueError("Fingerprint contains invalid characters. "
                         "Allwed characters: 0-9A-Fa-f")
    return f"0x{s}"


GPG_DEFAULT_DIR_BY_OS = {
    'Linux': ('.gnupg',),
    'Darwin': ('.gnupg',),
    'Windows': ('AppData', 'Roaming', 'gnupg')
}


def get_default_gpg_config_dir() -> str:
    """Path of the directory where GnuPG stores the user's keyrings.
    The location of this directory is platform dependent.
    """
    return os.path.join(os.path.expanduser('~'),
                        *GPG_DEFAULT_DIR_BY_OS[platform.system()])


class GPGStore:
    """Main class providing functionality. Representation of a GPG 'home'
    directory that contains the user's keyrings
    """

    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = config_dir
        self._gpg_bin = None
        for _bin in ("gpg", "gpg2"):
            self._gpg_bin = _bin
            try:
                cmd_devnull((_bin, "--version"))
                break
            except FileNotFoundError:
                continue
        else:
            raise FileNotFoundError("gpg executable not found")
        self._version = self.version()
        self._pw_args_t = ("--passphrase-fd", "0")
        if self._version >= (2, 2, 0):
            self._pw_args_t = ("--pinentry-mode", "loopback") + self._pw_args_t
        else:
            # Specific to older versions of gpg: the --batch option must be
            # added in order for the --passphrase-fd option to be used.
            self._pw_args_t = ("--batch",) + self._pw_args_t

    def _pw_args(self, pw):
        if pw is not None:
            return self._pw_args_t
        return ()

    @property
    def _base_args(self):
        args = (self._gpg_bin,)
        if self.config_dir is not None:
            args += ("--homedir", self.config_dir)
        return args

    def default_key(self) -> Optional[str]:
        config_file = os.path.join(
            self.config_dir or get_default_gpg_config_dir(),
            "gpg.conf")
        try:
            with open(config_file) as f_cfg:
                default_key = next(
                    line for line in f_cfg if line.startswith("default-key "))
            return default_key.split(" ")[1].rstrip("\r\n")
        except (FileNotFoundError, StopIteration):
            try:
                return self.list_sec_keys()[0].fingerprint
            except IndexError:
                return None

    def list_pub_keys(self, sigs: bool = False,
                      keys: Optional[Sequence[str]] = None) -> List[Key]:
        return self._list_keys(option="--list-public-keys",
                               sigs=sigs, keys=keys)

    def list_sec_keys(self, keys: Optional[Sequence[str]] = None) -> List[Key]:
        return self._list_keys(option="--list-secret-keys", keys=keys)

    def _list_keys(self, option: str,
                   sigs: bool = False,
                   keys: Optional[Iterator[str]] = None) -> List[Key]:
        """Ask gpg to list keys with the selected options.

        :param option: argument to pass to gpg, e.g. "--list-public-keys" to
            list the public keys in the user's keyring.
        :param sigs: if True, show signatures appended on keys.
        :param keys: key name, key ID or fingerprint to search for. If an
            empty list is passed, no key is returned.
            If keys is None, return all keys.
        :return: list of keys matching the search criteria.
        :raise GPGError:
        """
        if keys is None:
            keys = ()
        else:
            keys = tuple(keys)
            if not keys:
                return []
        # Add arguments that are always required for gpg to produce the
        # correct output. Note that for gpg versions < 2.1, the
        # --with-fingerprint option is required to be passed twice. If passed
        # only once the fingerprint of the subkeys are not printed.
        args = (option, "--fingerprint", "--fingerprint", "--with-colons")
        if sigs:
            args += ("--with-sig-list",)
        args += keys
        try:
            with cmd_pipe(self._base_args + args) as proc:
                return parse_keys(proc.stdout)
        except GPGError as e:
            if "error reading key" in str(e).lower():
                return []
            raise

    def encrypt(self,
                source: io.IOBase,
                recipients: List[str],
                output: Optional[io.IOBase] = None,
                passphrase: Optional[str] = None,
                trust_model: TrustModel = TrustModel.pgp,
                sign: Optional[str] = None):
        # Generate list of recipients for the encrypted file.
        args = sum((('--recipient', rcp) for rcp in recipients), ())
        args += ("--no-tty", "--trust-model", trust_model.name, "--encrypt")
        if sign is not None:
            args += ("--sign", "--local-user", sign)
        return _cmd(self._base_args + self._pw_args(passphrase) + args,
                    out=output, src=source, passphrase=passphrase)

    @contextmanager
    def decrypt(self,
                source: io.IOBase,
                output: Optional[io.IOBase] = None,
                trust_model: TrustModel = TrustModel.pgp,
                passphrase: Optional[str] = None
                ) -> str:
        """Decrypt file and, if present, retrieve the signature appended to
        the encrypted file.

        :param source: file to decrypt.
        :param output: file to save the decrypted output to.
        :param trust_model: trust model to be followed by gpg.
        :param passphrase: passphrase of the private key to be used to decrypt
            the data.
        :return: fingerprint or keyid of the signee's key.
        """

        # Note: the '--keyid-format', 'long' argument is only needed for
        # backwards compatibility with gpg versions < 2.1.0
        args = ("--batch", "--no-tty", "--status-fd", "2", "--trust-model",
                trust_model.name, "--decrypt")
        maybe_stdout = {}
        if output is not None:
            maybe_stdout["stdout"] = output
        with cmd_pipe(self._base_args + self._pw_args(passphrase) + args,
                      **maybe_stdout, src=source, passphrase=passphrase) as proc:
            fprs = capture_fpr(proc.stderr.read())
            if proc.stdout is not None:
                proc.stdout.sender_sig_fingerprints = fprs
                yield proc.stdout
            else:
                yield type("FingerprintCarrier",
                           (object,),
                           {"sender_sig_fingerprints": fprs})

    def gen_key(self, full_name: str,
                email: str,
                passphrase: str,
                key_length: int = 4096,
                key_type: str = "RSA"):
        args = ("--batch", "--status-fd", "1", "--gen-key")
        with cmd_pipe(self._base_args + args, src=f"""
%echo Generating a basic OpenPGP key
Key-Type: {key_type}
Key-Length: {key_length}
Subkey-Type: {key_type}
Subkey-Length: {key_length}
Name-Real: {full_name}
Name-Email: {email}
Expire-Date: 0
Passphrase: {passphrase}
%commit
%echo done
""".encode()) as proc:
            l = next(line for line in proc.stdout if line.startswith(
                b"[GNUPG:] KEY_CREATED"))
            return l.rstrip(b"\r\n").split(b" ")[-1].decode("utf-8", "replace")

    def send_keys(self, *fingerprints: str, keyserver: str,
                  url_opener=urllib.request.urlopen):
        """Following https://tools.ietf.org/html/draft-shaw-openpgp-hkp-00#page-6, Section 4"""
        with self.export(*fingerprints) as stream:
            data = stream.read()
        post(build_host(keyserver) + "/pks/add", b"keytext=" + quote(data).encode(),
             url_opener=url_opener)

    def recv_keys(self, *fingerprints: str, keyserver: str, **kwargs):
        for fingerprint in fingerprints:
            with download_key(keyserver=keyserver,
                              fingerprint=fingerprint, **kwargs) as key:
                self.import_file(key.read())

    def delete_keys(self, *fingerprints: str):
        cmd_devnull(self._base_args + ("--batch", "--yes",
                                       "--delete-keys") + fingerprints)

    def import_file(self, source: io.IOBase, *,
                    passphrase: Optional[str] = None):
        cmd_devnull(self._base_args + self._pw_args(passphrase) +
                    ("--import", "--batch", "-"),
                    src=source, passphrase=passphrase)

    def export(self, *fingerprints: str, armor: bool = True):
        return cmd_pipe_stdout(self._base_args + ("--export",) +
                               (("--armor",) if armor else ()) + fingerprints)

    def version(self):
        with cmd_pipe(self._base_args + ("--version",)) as proc:
            return tuple(map(int,
                             proc.stdout.readline().rstrip(b"\n").split(b" ")[-1].split(b".")))

    def gen_revoke(self, fingerprint: str, passphrase) -> bytes:
        args = self._base_args + self._pw_args(passphrase) + (
            "--no-tty", "--status-fd", "2", "--command-fd", "0",
            "--gen-revoke", fingerprint)
        with expect(args) as proc:
            try:
                proc.put(passphrase.encode() + b"\n")
                proc.expect(b"[GNUPG:] GET_BOOL gen_revoke.okay\n")
                proc.put(b"y\n")
                proc.expect(b"[GNUPG:] GET_LINE ask_revocation_reason.code\n")
                proc.put(b"0\n")
                proc.expect(b"[GNUPG:] GET_LINE ask_revocation_reason.text\n")
                proc.put(b"\n")
                proc.expect(b"[GNUPG:] GET_BOOL ask_revocation_reason.okay\n")
                proc.put(b"y\n")
            except ValueError:
                raise GPGError("Failed to generate a revocation certificate")
            return proc.stdout.read()

    def revoke(self, fingerprint: str, *, keyserver: Optional[str] = None,
               passphrase: str):
        self.import_file(self.gen_revoke(fingerprint, passphrase))
        if keyserver is not None:
            self.send_keys(fingerprint, keyserver=keyserver)

    def detach_sig(self, src: Union[bytes, io.IOBase], passphrase: str,
                   user: Optional[str] = None):
        return cmd_pipe_stdout(
            self._base_args + self._pw_args(passphrase) +
            (("--local-user", user) if user is not None else ()) +
            ("--detach-sig", "-"),
            src=src,
            passphrase=passphrase)

    def verify(self, src: Union[bytes, io.IOBase], sig: bytes) -> str:
        """Verify and retrieve the pgp signature made to a file in detached
        signature mode - i.e. the signed file and the signature are in separate
        files.

        :param src: file that was signed.
        :param sig: detached signature file.
        :return: fingerprint or keyid of the signee's key.
        :raises GPGError:
        """
        f = tempfile.NamedTemporaryFile(delete=False)
        try:
            f.write(sig)
            f.seek(0)
            f.close()
            # Note: the '--keyid-format', 'long' argument is only needed for
            # backwards compatibility with gpg versions < 2.1.0
            with cmd_pipe(
                self._base_args +
                ("--status-fd", "2", "--verify", f.name, "-"),
                    src=src) as proc:
                gpg_out = proc.stderr.read()
                fprs = capture_fpr(gpg_out)
                try:
                    fpr, = fprs
                except ValueError:
                    if not fprs:
                        raise GPGError(
                            "No fingerprint found in the output of gpg:\n" +
                            gpg_out.decode('utf-8', 'replace'))
                    raise GPGError(
                        "Multiple fingerprints found in the output of gpg:\n" +
                        gpg_out.decode('utf-8', 'replace'))
                return fpr
        finally:
            os.remove(f.name)


def search_keys(name: str, keyserver: str,
                url_opener=urllib.request.urlopen) -> Iterator[KeyInfo]:
    try:
        queries = {normalize_fingerprint(name), name}
    except ValueError:
        queries = {name}
    for query in queries:
        try:
            with query_keyserver(keyserver=keyserver,
                                 query=query,
                                 op="index",
                                 url_opener=url_opener) as response:
                yield from parse_search_keys(response)
        except HTTPError as e:
            if e.code != 404:
                raise e


def download_key(fingerprint: str, keyserver: str, **kwargs) -> bytes:
    return query_keyserver(keyserver=keyserver,
                           query=normalize_fingerprint(fingerprint),
                           op="get",
                           exact="on",
                           **kwargs)


def query_keyserver(keyserver: str, query: str, op: str,
                    url_opener=urllib.request.urlopen,
                    **parameters):
    url = build_host(keyserver)

    query_url = (
        f"{url}/pks/lookup?search={quote(query)}&op={op}&options=mr" +
        "".join(f"?{key}={val}" for key, val in parameters.items()))
    return url_opener(query_url)  # nosec


def split_host(url: str) -> Tuple[Optional[str], str, Optional[str]]:
    match = re.fullmatch(r"(https?://|hkp://)?([^:]+)(:[0-9]+)?", url)
    if not match:
        raise ValueError(f"Invalid URL: {url}")
    return match.groups()


def build_host(url: str) -> str:
    scheme, host, port = split_host(url)
    if scheme not in {"http://", "https://"}:
        if port in {":80", ":8080", ":11371"}:
            scheme = "http://"
        else:
            scheme = "https://"
    if port is None:
        if scheme == "https://":
            port = ":443"
        else:
            port = ":80"
    return scheme + host + port


def extract_key_id(src: io.BytesIO) -> Iterator[str]:
    """Extract the public key_id from an encrypted message"""
    with preserve_pos(src):
        while True:
            fpr = extract_key_id_once(src)
            if fpr is None:
                break
            yield fpr


def public_key_encrypted_session_key_packet(src: io.BytesIO) -> bytes:
    """type 1: Public-Key Encrypted Session Key Packet"""
    _version = src.read(1)
    return src.read(8)


def signature_packet(src: io.BytesIO) -> bytes:
    """Type 2: Signature Packet"""
    version, = src.read(1)
    if version == 3:
        length, = src.read(1)
        if length != 5:
            raise ValueError(f"Invalid length: {length}. Should be 5")
        _sigtype = src.read(1)
        _creationtime = src.read(4)
        return src.read(8)
    if version == 4:
        # fpr stars at octet 12
        _sigtype = src.read(1)
        _pubkeyalgorithm = src.read(1)
        _hashalgorithm = src.read(1)
        hashed_octet_count = int.from_bytes(src.read(2), "big")
        src.read(hashed_octet_count)
        unhashed_octet_count = int.from_bytes(src.read(2), "big")
        subpackets_end = src.tell() + unhashed_octet_count
        while src.tell() < subpackets_end:
            key_id = read_subpacket(src)
            if key_id:
                return key_id
        _signedhash = src.read(2)
        raise ValueError("No issuer subpacket in signature packet")
    raise ValueError(
        f"Invalid version: {version}. Only 3 and 4 are supported")


def read_subpacket(src: io.BytesIO) -> Optional[bytes]:
    l = read_new_packet_len(src)
    pkg_tpye, = src.read(1)
    body = src.read(l-1)
    if pkg_tpye == 16:  # type 16: Issuer
        return body
    return None


PACKET_HANDLERS = {
    1: public_key_encrypted_session_key_packet,
    2: signature_packet
}


def read_new_packet_len(src: io.BytesIO) -> int:
    l, = src.read(1)
    if l < 192:  # 1 octet length
        return l
    if l <= 223:  # 2 octet length
        l2, = src.read(1)
        return ((l - 192) << 8) + l2 + 192
    # 224 <= l < 255: Partial Body Lengths (=> header has length 1)
    if l < 255:
        return None
    if l == 255:  # 5 octet length
        l2, l3, l4, l5 = src.read(4)
        return (l2 << 24) | (l3 << 16) | (l4 << 8) | l5
    raise ValueError(f"Invalid length: {l}")


def extract_key_id_from_sig(src: bytes) -> Optional[str]:
    """Extract key id from a signature packet. Either ascii armored or binary"""
    if src[0] == b"-"[0]:
        src = ascii_armored_to_binary(src)
    return extract_key_id_once(io.BytesIO(src))


def extract_key_id_once(src: io.BytesIO) -> Optional[str]:
    """Reads one packet from src

    According to https://www.ietf.org/rfc/rfc4880.txt
    """
    try:
        packet_hdr, = src.read(1)
    except ValueError:
        return None
    # 1st bit must be 1
    if not packet_hdr & 0x80:
        raise ValueError("Not a valid packet tag")
    # 2nd bit is packet version (new / old)
    new_version = packet_hdr & 0x40
    packet_type = packet_hdr & 0b00111111
    if not new_version:
        packet_type >>= 2
    pkg_handler = PACKET_HANDLERS.get(packet_type)
    if pkg_handler is None:
        return None
    if not new_version:
        packet_length_type = packet_hdr & 0b11
        body_offs_by_len_type = {0: 2, 1: 3, 2: 5, 3: 1}
        try:
            packet_len_size = body_offs_by_len_type[packet_length_type] - 1
        except KeyError:
            raise ValueError(
                f"Invalid packet length type: {packet_length_type}")
        if packet_length_type == 3:  # The packet is of indeterminate length
            packet_len = None
        else:
            packet_len = int.from_bytes(src.read(packet_len_size), "big")
    else:
        packet_len = read_new_packet_len(src)
    if packet_len is not None and packet_len < 10:
        raise ValueError(f"Unexpected packet length of {packet_len}")
    body_start = src.tell()
    pub_key_id = pkg_handler(src)
    if packet_len:
        src.seek(body_start + packet_len)
    else:
        src.seek(0, 2)
    return pub_key_id.hex().upper()


def capture_fpr(b: bytes) -> List[str]:
    """Extract fingerprint from a standard output of gpg that looks like:
    [GNUPG:] NEWSIG
    gpg: Signature made Tue 10 Mar 2020 11:29:27 CET
    gpg:                using RSA key 3B3EB1983FAA63C1B05E072D066E042415D8FD9C
    [GNUPG:] KEY_CONSIDERED 3B3EB1983FAA63C1B05E072D066E042415D8FD9C 0
    [GNUPG:] SIG_ID PaAuiNMUyUDRMsctXpV+7rX+0CI 2020-03-10 1583836167
    [GNUPG:] KEY_CONSIDERED 3B3EB1983FAA63C1B05E072D066E042415D8FD9C 0
    [GNUPG:] GOODSIG 066E042415D8FD9C Chuck Norris <chucknorris@roundhouse.gov>
    gpg: Good signature from "Chuck Norris <chucknorris@roundhouse.gov>" [unknown]
    [GNUPG:] VALIDSIG 3B3EB1983FAA63C1B05E072D066E042415D8FD9C 2020-03-10 1583836167

    :param b: gpg stdout in binary form.
    :return: either a 40-char long fingerprint.
    """
    return [m.group(1).decode('utf-8', 'replace') for m in re.finditer(
        rb"\[GNUPG:\] VALIDSIG ([0-9A-F]{40})", b)
    ]


@contextmanager
def preserve_pos(src: io.BytesIO):
    pos = src.tell()
    yield src
    src.seek(pos)


default_opener = urllib.request.build_opener(
    urllib.request.HTTPSHandler(debuglevel=0)).open


def post(url, data, url_opener=default_opener):
    request = urllib.request.Request(
        url, data, method='POST',
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    with url_opener(request) as response:
        response_text = response.read()
        return response_text


def ascii_armored_to_binary(src: bytes):
    header, _, *lines, footer = src.splitlines()
    # If the last line is empty, continue to the last not empty line:
    while not footer:
        footer = lines.pop()
    if header != b"-----BEGIN PGP SIGNATURE-----":
        raise ValueError(
            "Invalid ascii armored signature header: '" + header.decode() + "'")
    if footer != b"-----END PGP SIGNATURE-----":
        raise ValueError(
            "Invalid ascii armored signature footer: '" + footer.decode() + "'")
    return base64.decodebytes(b"".join(l for l in lines if l))
