import unittest
import os
import tempfile
import io

import gpg_lite as gpg

WITH_GPG = os.environ.get("WITH_GPG", None) == "true"
KEY_SERVER = os.environ.get("KEY_SERVER", None)

CN_UID = gpg.Uid(full_name="Chuck Norris",
                 email="chuck.norris@roundhouse.gov")

UMLAUTS_UID = gpg.Uid(full_name="With Umläuts",
                      email="with.umlauts@umlauts.info")


class TestUtils(unittest.TestCase):
    def test_split_url(self):
        self.assertEqual(
            gpg.split_host("http://keyserver.dcc.sib.swiss:11371"),
            ("http://", "keyserver.dcc.sib.swiss", ":11371"))
        self.assertEqual(
            gpg.split_host("hkp://keyserver.dcc.sib.swiss:11371"),
            ("hkp://", "keyserver.dcc.sib.swiss", ":11371"))
        self.assertEqual(
            gpg.split_host("keyserver.dcc.sib.swiss:11371"),
            (None, "keyserver.dcc.sib.swiss", ":11371"))
        self.assertEqual(
            gpg.split_host("http://keyserver.dcc.sib.swiss"),
            ("http://", "keyserver.dcc.sib.swiss", None))
        self.assertEqual(
            gpg.split_host("keyserver.dcc.sib.swiss"),
            (None, "keyserver.dcc.sib.swiss", None))
        with self.assertRaises(ValueError):
            gpg.split_host("keyserver.dcc:sib.swiss")

    def test_uid_from_str(self):
        self.assertEqual(gpg.Uid.from_str("[User ID not found]"), None)
        self.assertEqual(gpg.Uid.from_str("[User-ID nicht gefunden]"), None)
        self.assertEqual(gpg.Uid.from_str("[Identité introuvable]"), None)
        self.assertEqual(gpg.Uid.from_str("Chuck Norris <chucknorris@roundhouse.gov"),
                         gpg.Uid(full_name="Chuck Norris", email="chucknorris@roundhouse.gov"))

    def test_normalize_fingerprint(self):
        for length in (8, 16, 32, 40):
            fp = "A" * length
            self.assertEqual(gpg.normalize_fingerprint(fp), f"0x{fp}")
            self.assertEqual(gpg.normalize_fingerprint(f"0x{fp}"), f"0x{fp}")
        self.assertEqual(gpg.normalize_fingerprint(
            "123 af  47a"), "0x123af47a")
        with self.assertRaises(ValueError):
            gpg.normalize_fingerprint("A" * 7)
        with self.assertRaises(ValueError):
            gpg.normalize_fingerprint("Z" * 8)


class TestGPG(unittest.TestCase):
    def test_factory(self):
        class TestFactory(gpg.Factory):
            type_ = object
        fct = TestFactory()
        fct.append("keys", "A")
        self.assertEqual(fct.kwargs, {"keys": ("A",)})
        fct.append("keys", "B")
        self.assertEqual(fct.kwargs, {"keys": ("A", "B")})

    def test_parse_search_keys(self):
        response = io.BytesIO(b"""info:1:1
pub:CB5A3A5C2C4419BB09EFF879D6D229C51AB5D107:1:2048:1550241679::
uid:Chuck Norris <chuck.norris@roundhouse.gov>:1550241679::

pub:F119E26211119BB09EFF879D6D229C51AB5D107C:1:2048:1550241679::
uid:With Uml%C3%A4uts <with.umlauts@umlauts.info>:1550241679::
""")
        keys = list(gpg.parse_search_keys(response))
        self.assertEqual(keys, [
            gpg.KeyInfo(
                uid=CN_UID,
                fingerprint="CB5A3A5C2C4419BB09EFF879D6D229C51AB5D107",
                key_algorithm=1,
                key_length=2048,
                creation_date="1550241679",
                expiration_date=None),
            gpg.KeyInfo(
                uid=UMLAUTS_UID,
                fingerprint="F119E26211119BB09EFF879D6D229C51AB5D107C",
                key_algorithm=1,
                key_length=2048,
                creation_date="1550241679",
                expiration_date=None)])

    def test_parse_keys(self):
        key_payload = io.BytesIO(b"""tru::1:1571400791:0:3:1:5
pub:u:2048:1:FDC66B7A5F6FFD4B:1550241679:::u:::scESC::::::23:1571230031:1 http\\x3a//keyserver.dcc.sib.swiss\\x3a11371:
fpr:::::::::CB5A3A5C2C4419BB09EFF879D6D229C51AB5D107:
uid:u::::1550241679::B1E8D4565D26BED47D1EB8BB2B5733AEC1F154B5::Chuck Norris <chuck.norris@roundhouse.gov>::::::::::0:
sig:::1:FDC66B7A5F6FFD4B:1550241679::::Chuck Norris <chuck.norris@roundhouse.gov>:13x::CB5A3A5C2C4419BB09EFF879D6D229C51AB5D107:::8:
sig:::1:3A6500D5C1DE39AC:1571225229::::DCC Test (Test key for transferprotocol) <dcc@sib.swiss>:13x:::::2:
sig:?::1:2E3E7FE28FE412AE:1573661452::::[User ID not found]:13x::2866A142A16F54E06EB73CF92E3E7FE28FE412AE:::8:
sub:u:2048:1:D892C41917B20115:1550241679::::::e::::::23:
fpr:::::::::55C5314BB9EFD19AE7CC4774D892C41917B20115:
pub:-:4096:1:3A6500D5C1DE39AC:1565257866:::-:::scESC::::::23::0:
fpr:::::::::848FA2707A1AC6060FFE5D253A6500D5C1DE39AC:
uid:-::::1565257866::4D51176EBCDF1F58C3D7E0F76625B168A184BB8E::DCC Test (Test key for transferprotocol) <dcc@sib.swiss>::::::::::0:
sub:-:4096:1:A4C037FA518B5C4F:1565257866::::::e::::::23:
fpr:::::::::3AC9B4462D255449989A3D6EA4C037FA518B5C4F:
""")
        keys = gpg.parse_keys(key_payload)
        dcc_uid = gpg.Uid(full_name="DCC Test (Test key for transferprotocol)",
                          email="dcc@sib.swiss")
        self.assertEqual(
            keys, [
                gpg.Key(key_id="FDC66B7A5F6FFD4B",
                        fingerprint="CB5A3A5C2C4419BB09EFF879D6D229C51AB5D107",
                        validity=gpg.Validity.ultimately_valid,
                        key_length=2048,
                        pub_key_algorithm=1,
                        creation_date="1550241679",
                        signatures=(gpg.Signature(
                            issuer_uid=CN_UID, issuer_key_id="FDC66B7A5F6FFD4B",
                            creation_date="1550241679", signature_class="13x"),
                            gpg.Signature(
                            issuer_uid=dcc_uid, issuer_key_id="3A6500D5C1DE39AC",
                            creation_date="1571225229", signature_class="13x"),
                            gpg.Signature(
                            issuer_uid=None, issuer_key_id="2E3E7FE28FE412AE",
                            creation_date="1573661452", signature_class="13x")),
                        key_capabilities={
                            gpg.KeyCapability.Sign(True),
                            gpg.KeyCapability.Sign(False),
                            gpg.KeyCapability.Certify(True),
                            gpg.KeyCapability.Certify(False),
                            gpg.KeyCapability.Encrypt(True)},
                        key_type=gpg.KeyType.public,
                        uids=(CN_UID,),
                        owner_trust="u",
                        sub_keys=(gpg.SubKey(
                            key_type=gpg.KeyType.public,
                            key_id="D892C41917B20115",
                            fingerprint="55C5314BB9EFD19AE7CC4774D892C41917B20115",
                            validity=gpg.Validity.ultimately_valid,
                            key_length=2048,
                            pub_key_algorithm=1,
                            creation_date="1550241679",
                            key_capabilities={
                                   gpg.KeyCapability.Encrypt(False)},
                        ),),
                        origin="http://keyserver.dcc.sib.swiss:11371",
                        ),
                gpg.Key(key_id="3A6500D5C1DE39AC",
                        fingerprint="848FA2707A1AC6060FFE5D253A6500D5C1DE39AC",
                        validity=gpg.Validity.unknown,
                        key_length=4096,
                        pub_key_algorithm=1,
                        creation_date="1565257866",
                        key_capabilities={
                            gpg.KeyCapability.Sign(True),
                            gpg.KeyCapability.Sign(False),
                            gpg.KeyCapability.Certify(True),
                            gpg.KeyCapability.Certify(False),
                            gpg.KeyCapability.Encrypt(True)},
                        key_type=gpg.KeyType.public,
                        uids=(dcc_uid,),
                        owner_trust="-",
                        sub_keys=(gpg.SubKey(
                            key_type=gpg.KeyType.public,
                            key_id="A4C037FA518B5C4F",
                            fingerprint="3AC9B4462D255449989A3D6EA4C037FA518B5C4F",
                            validity=gpg.Validity.unknown,
                            key_length=4096,
                            pub_key_algorithm=1,
                            creation_date="1565257866",
                            key_capabilities={
                                gpg.KeyCapability.Encrypt(False)},
                        ),),
                        origin=None,
                        )
            ]
        )

    def test_parse_keys_revocation_sig(self):
        key_payload = io.BytesIO(b"""
pub:-:2048:1:0000000000000000:1587731664:::-:::scESC::::::23:1588834129:1 http\\x3a//keyserver.dcc.sib.swiss\\x3a11371:
fpr:::::::::1111111111111111111111110000000000000000:
uid:-::::1587731664::6350A25D9F42F55F19A335C67AFC54D0DF542625::Gunnery Sgt. Hartmann <hartmann@bullshit.gov>:::::::::1588834129:1:
sig:::1:0000000000000000:1587731664::::Gunnery Sgt. Hartmann <hartmann@bullshit.gov>:13x:::::2:
sig:::1:881685B5EE0FCBD3:1588064955::::SPHN Data Coordination Centre <dcc@sib.swiss>:13x::B37CE2A101EBFA70941DF885881685B5EE0FCBD3:::8:
rev:::1:881685B5EE0FCBD3:1588066811::::SPHN Data Coordination Centre <dcc@sib.swiss>:30x,00::B37CE2A101EBFA70941DF885881685B5EE0FCBD3:::8:::::revsig\\nInvalid email:
sub:-:2048:1:AAAAAAAAAAAAAAAA:1587731664::::::e::::::23:
fpr:::::::::BBBBBBBBBBBBBBBBBBBBBBBBAAAAAAAAAAAAAAAA:
""")
        keys = gpg.parse_keys(key_payload)
        dcc_uid = gpg.Uid(full_name="SPHN Data Coordination Centre",
                          email="dcc@sib.swiss")
        uid = SGT_HARTMANN_UID
        self.assertEqual(
            keys, [
                gpg.Key(key_id="0000000000000000",
                        fingerprint="1111111111111111111111110000000000000000",
                        validity=gpg.Validity.unknown,
                        key_length=2048,
                        pub_key_algorithm=1,
                        creation_date="1587731664",
                        signatures=(
                            gpg.Signature(issuer_uid=uid,
                                          issuer_key_id='0000000000000000',
                                          signature_class='13x',
                                          creation_date='1587731664'),
                            gpg.Signature(
                                issuer_uid=dcc_uid, issuer_key_id="881685B5EE0FCBD3",
                                creation_date="1588064955", signature_class="13x"),
                            gpg.RevocationSignature(
                                issuer_uid=dcc_uid, issuer_key_id="881685B5EE0FCBD3",
                                creation_date="1588066811", signature_class="30x",
                                reason="00",
                                comment="revsig\\nInvalid email")
                        ),
                        key_capabilities={
                            gpg.KeyCapability.Sign(True),
                            gpg.KeyCapability.Sign(False),
                            gpg.KeyCapability.Certify(True),
                            gpg.KeyCapability.Certify(False),
                            gpg.KeyCapability.Encrypt(True)},
                        key_type=gpg.KeyType.public,
                        uids=(uid,),
                        owner_trust="-",
                        sub_keys=(gpg.SubKey(
                            key_type=gpg.KeyType.public,
                            key_id="AAAAAAAAAAAAAAAA",
                            fingerprint="BBBBBBBBBBBBBBBBBBBBBBBBAAAAAAAAAAAAAAAA",
                            validity=gpg.Validity.unknown,
                            key_length=2048,
                            pub_key_algorithm=1,
                            creation_date="1587731664",
                            key_capabilities={
                                gpg.KeyCapability.Encrypt(False)},
                        ),),
                        origin="http://keyserver.dcc.sib.swiss:11371",
                        )
            ]
        )
        self.assertEqual(keys[0].valid_signatures, [
            gpg.Signature(issuer_uid=uid,
                          issuer_key_id='0000000000000000',
                          signature_class='13x',
                          creation_date='1587731664')])

    @staticmethod
    def test_parse_keys_w_rev():
        key_payload = io.BytesIO(b"""tru::1:1576574206:0:3:1:5
pub:-:2048:17:CCCCCCCCCCCCCCC:1282220531:1592219853::-:::scESC::::::23::0:
fpr:::::::::CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC:
uid:-::::1534238253::DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD::Roundhouse Team <team@roundhouse.gov>::::::::::0:
sig:::17:CCCCCCCCCCCCCCC:1534238253::::Roundhouse Team <team@roundhouse.gov>:13x::CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC:::10:
sig:?::1:AAAAAAAAAAAAAAAA:1512502244::::[User ID not found]:13x::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA:::8:
rev:?::1:BBBBBBBBBBBBBBBB:1521078619::::[User ID not found]:30x,00::BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB:::8:
""")
        gpg.parse_keys(key_payload)

    @staticmethod
    def test_parse_keys_w_sub_sub():
        key_payload = io.BytesIO(b"""tru::1:1576574206:0:3:1:5
pub:-:2048:17:CCCCCCCCCCCCCCC:1282220531:1592219853::-:::scESC::::::23::0:
fpr:::::::::CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC:
uid:-::::1534238253::FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF::Roundhouse Team <team@roundhouse.gov>::::::::::0:
sub:-:2048:16:DDDDDDDDDDDDDDDD:1282220531:1592219869:::::e:::::::
fpr:::::::::DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD:
sig:::17:CCCCCCCCCCCCCCC:1534238269::::Roundhouse Team <team@roundhouse.gov>:18x::CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC:::10:
sub:-:4096:1:AAAAAAAAAAAAAAAA:1396950003:1704188403:::::s::::::23:
fpr:::::::::AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA:
sig:::17:CCCCCCCCCCCCCCC:1396950003::::Roundhouse Team <team@roundhouse.gov>:18x:::::10:
""")
        gpg.parse_keys(key_payload)

    def test_extract_key_id(self):
        partial_msg = io.BytesIO(b'\x84\x8c\x03\xf3\rL3@z?c\x01\x03\xff]\xdf')
        pos = partial_msg.tell()
        key_id, = gpg.extract_key_id(partial_msg)
        self.assertEqual(key_id, "F30D4C33407A3F63")
        self.assertEqual(partial_msg.tell(), pos)

        wrong_msg = io.BytesIO(b'\x04\x8c\x03\xf3\rL3@z?c\x01\x03\xff]\xdf')
        with self.assertRaises(ValueError):
            list(gpg.extract_key_id(wrong_msg))

        partial_msg = io.BytesIO(
            b'\x85\x01\x0c\x03\xd8\x92\xc4\x19\x17\xb2\x01\x15\x01\x08'
            b'\x00\xafZ\xd8\x83\xba' +
            248 * b'\000' +
            b'c\x1d\x16\x85\x02\x0c\x032\xf9\xe2\xf8\rR!^\x01\x10\x00\x97c' +
            504 * b'\000' +
            b'\x1a\xa2\xf2&\xc0\xe5\x85\x02\x0c\x03\xcc\xfa\xa7\xf4\x12\xb0m'
            b'\x83\x01\x10'
        )

        key_ids = list(gpg.extract_key_id(partial_msg))
        self.assertEqual(
            key_ids, ["D892C41917B20115", "32F9E2F80D52215E", "CCFAA7F412B06D83"])

    def test_extract_key_id_from_sig(self):
        sig = (
            b'\x89\x023\x04\x00\x01\x08\x00\x1d\x16!\x04\xa8\x05h*\x13\xa1\x08\xca'
            b'\xab\x07\xef\xd0k\xe5(\xb1&\xd3\xe13\x05\x02_\x05\xcfP\x00\n\t\x10k'
            b'\xe5(\xb1&\xd3\xe13\xf8\x8a\x10\x00\x97\xb8\x0bWU\x05B\xd5\x17\xba\xd2'
            b'\x9b\xe4o\xd4`\x86Id\x86\xc4m\xa6=\xf2\xf3\xc5\xec\x8b\x16?Q\xfe\x06'
            b'\xf9\xdc`\xfa\xe4\x9d~)\xcaYx\x16\x06t@\xc0\xc0\xe4\xd5\x94\x1a\x19'
            b'\xa5yL.r\xba\x01-\xe8\xc6\xaf \xa8\xc9\xbef\x0b:C\xa4\x83Ahn\x85R\xbe'
            b'\x81\x02\xb14\xce\x89\xef4\xa4\xb5\x96\xcc\x81t/x\x16_\xb1|\xcbb+3'
            b'\xf4`w_\x93\x8cl\xa0\x95$<&\x8fu<\n\xd1-9^\\\x98\x04\xa0F\x9fE\xeb{'
            b'\xc4\xda\x9f\x9f\xf0\xc9#>\xba\xb5\xa8\x99Od\xcdb\x9en\xa0\xb2\x1c\xd2'
            b'\xe8\xa8\x03k\x04o\xd5\x08\xb7W\x19UL\xa4\x14P\xba\x10}XS\x18\x86M'
            b'\xa3k\xdc\x0fO&\xe6J-\xca\x13\xac\xe8\xacb\xc5\x81x\xe3\xf0\x0b\xe1['
            b'\x1f\xc7\xd1b\x89\xb7\xe3E\x06\xa7n\x83\xe8\xc0.\x96\xd8\x19\x9d\xc3J'
            b'\xfcR\xc1%\x960\x95Y\n\x98`\xb1C(KAwO\xf6\xf5\xe1\xdcCk\x96j\xbbC\xd3?'
            b'\x05\x07r\xc1#\x97\x1d\x15~L\xb8HQ\xb4|=\x8dG\x987wN\xc8\xbfm\x889\xd5'
            b'\x9c\xfd\x90@#C\xef\xcf\x12\r\xc1\xdd\x1e\xd2\xc3\x97[\xad\xcc\x86\xbc'
            b'\xa2\xc6R\xce\xf6L\x8f5;\xe0\xc4|\xe2\xeb\xfe\xe5\xb0\xa2F\xc2\x8eX'
            b'\xab \xe7\xe3\xf3\xe9SN\x16K\x99\xb9S}\xa7\x02\xaa\xd6\x9c\xb3\xb8'
            b'\xcelO\xd3!/2r|\x06\x10\x88$L\x99\x15 \xff\xa7\x812\xb6\xf6I\xba\x10'
            b'\xfd\x94\xb6\x05:`*\xa3\xd0\xfb\xf8~\x0f\xedPx\t\x1fq\xe0\x8e\xf0\xcb'
            b'\xf1\xab\xa0yF\xc7iL\xba\xb7e\xfa\xba\xfb\x8e\xe5w\x8bF\xd3\x91\xc7G4'
            b'\x9c]\xcc\xb8\x10\x0c\xdc\x81\xc0_\x1e\x83c=x2\xd6\xa9:s\xc5\xf0\x04#'
            b'\x0c`\xa2\x0c\x95&\x08\xf5:\x12\xe0\x8a\xb6\x86\x9dE\xea\xa9\xd6\xff'
            b'\xe9~\x91_|\x14.\xcb\x14\xdd\xb9\tR\x1a)\x04\xaf\xf6\xb7\xd4(&%\xc4'
            b'\xe9\xea\xac\x00\x17\xe3Nf\xd6\xd1\xa0\xb9\x99\xe3[\xa1O?a\xd7\x06\x9fc')
        key_id = gpg.extract_key_id_from_sig(sig)
        self.assertEqual(key_id, "6BE528B126D3E133")
        sig = b"""-----BEGIN PGP SIGNATURE-----

iQIzBAABCAAdFiEEqAVoKhOhCMqrB+/Qa+UosSbT4TMFAl8YCiwACgkQa+UosSbT
4TMEvQ/5AaSlYmpQK1MWQbNHiL4AMl55GfVlSnQBCpk3lsltOnycEVxP67jawpd7
2DSFBzcF5wRUiMo85R9YkNxBjFwfU2xlT738ZWFQIoOvvwyGJgOlgngZ7+BEGEqP
130pEIGeDVt6kzVuwqB09SZCATGR0qnkB/84+pFimN0tiFkFWHXLHgJ++uMO2Pg+
j45HbZzYh0qqKfY+X9lP5JIuCsnFQv5AOgnUFfy1vKNZd6OGCZuxCla5M+RpOcFD
F3w004RK2p3SNS7ikoATRSDnSHwiWDay8WesmVkOXQurevEONGdvUY91ZW41wA5T
HR3qHWZyg4fWy4G2azCbGA3AEnd2m+sWdvptpbL7InxutLET5hLEXNsnL1Ixiqr/
DViv+hBaixAT0LRCdci3G/FfWAC38zZjo/A6JLpCGaqTuWl1OWkDPxQXPNYT4Wgk
Y9YJFrgF1MQ2BrUuYzrC+ClEvO/TBsVe2r9l4ElZs3rZBH1vOxyCyuAHreNw46R6
MfwW9lYob56DUTRBVrhZI46/LQD/dlwtYedN5p/CNpzavuzQHAmJD1G22WZHwTqV
SL/bsOqwOqJP1BpQloAR+jEnP6jPbQAmPEn3xU+3IPWjKFe95QUj3PIeeSqst2Mt
xERXJ/PqFoAktjU/mhNeDHovXdB+7378YkY3NHNSlFytYG0D5jo=
=qg97
-----END PGP SIGNATURE-----
"""
        key_id = gpg.extract_key_id_from_sig(sig)
        self.assertEqual(key_id, "6BE528B126D3E133")
        key_id = gpg.extract_key_id_from_sig(sig.replace(b"\n", b"\r\n"))
        self.assertEqual(key_id, "6BE528B126D3E133")

    def test_capture_fpr(self):
        b = b"""
[GNUPG:] NEWSIG
gpg: Signature made Tue 10 Mar 2020 11:29:27 CET
gpg:                using RSA key AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
[GNUPG:] KEY_CONSIDERED AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA 0
[GNUPG:] SIG_ID PaAuiNMUyUDRMsctXpV+7rX+0CI 2020-03-10 1583836167
[GNUPG:] KEY_CONSIDERED AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA 0
[GNUPG:] GOODSIG 066E042415D8FD9C Chuck Norris <chucknorris@roundhouse.gov>
gpg: Good signature from "Chuck Norris <chucknorris@roundhouse.gov>" [undefined]
[GNUPG:] VALIDSIG AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA 2020-03-10 1583836167 0 4 0 1 8 00 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
[GNUPG:] TRUST_UNDEFINED 0 pgp
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
"""
        self.assertEqual(gpg.capture_fpr(
            b), ["AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"])
        b = b"""
gpg: Signature made Mi 12 Feb 2020 15:34:46 CET
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
"""
        self.assertEqual(gpg.capture_fpr(
            b), [])
        b = b"""
[GNUPG:] NEWSIG
gpg: Signature made Tue 10 Mar 2020 11:29:27 CET
gpg:                using RSA key AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
[GNUPG:] KEY_CONSIDERED AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA 0
[GNUPG:] SIG_ID PaAuiNMUyUDRMsctXpV+7rX+0CI 2020-03-10 1583836167
[GNUPG:] KEY_CONSIDERED AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA 0
[GNUPG:] GOODSIG 066E042415D8FD9C Chuck Norris <chucknorris@roundhouse.gov>
gpg: Good signature from "Chuck Norris <chucknorris@roundhouse.gov>" [undefined]
[GNUPG:] VALIDSIG AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA 2020-03-10 1583836167 0 4 0 1 8 00 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
[GNUPG:] TRUST_UNDEFINED 0 pgp
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
[GNUPG:] NEWSIG
gpg: Signature made Tue 10 Mar 2020 11:29:27 CET
gpg:                using RSA key BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
[GNUPG:] KEY_CONSIDERED BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB 0
[GNUPG:] SIG_ID PaAuiNMUyUDRMsctXpV+7rX+0CI 2020-03-10 1583836167
[GNUPG:] KEY_CONSIDERED BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB 0
[GNUPG:] GOODSIG 066E042415D8FD9C Gunnery Sgt. Hartmann <hartmann@bullshit.gov>
gpg: Good signature from "Gunnery Sgt. Hartmann <hartmann@bullshit.gov" [undefined]
[GNUPG:] VALIDSIG BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB 2020-03-10 1583836167 0 4 0 1 8 00 BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
[GNUPG:] TRUST_UNDEFINED 0 pgp
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
"""
        self.assertEqual(gpg.capture_fpr(
            b), ["AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                 "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"])


class IntegrationTest(unittest.TestCase):
    def _setup_key(self):
        self.s.import_file(CN_SEC_KEY, passphrase="test")
        self.s.import_file(CN_PUB_KEY)
        key, = self.s.list_sec_keys()
        return key

    def setUp(self):
        gpg_homedir = tempfile.TemporaryDirectory()
        self.gpg_homedir = gpg_homedir
        d = gpg_homedir.__enter__()
        self.s = gpg.GPGStore(d)

    def tearDown(self):
        try:
            self.gpg_homedir.__exit__(None, None, None)
        except FileNotFoundError:
            pass


@unittest.skipUnless(WITH_GPG, "Integration tests")
class TestGPGIntegration(IntegrationTest):
    def test_revoke(self):
        key = self._setup_key()
        self.assertTrue(key.validity != gpg.Validity.revoked)
        self.s.revoke(key.fingerprint, passphrase="test")
        key, = self.s.list_sec_keys()
        self.assertEqual(key.validity, gpg.Validity.revoked)

    def test_list_keys(self):
        self._setup_key()
        self.s.import_file(UMLAUTS_PUB_KEY)

        def extract_keys(**kwargs):
            keys = self.s.list_pub_keys(**kwargs)
            if keys[0].uids == (CN_UID,):
                key_1, key_2 = keys
            else:
                key_2, key_1 = keys
            return key_1, key_2

        pub_key, umlauts_key = extract_keys()

        self.assertEqual(pub_key.uids, (CN_UID,))
        self.assertEqual(pub_key.key_type, gpg.KeyType.public)
        self.assertFalse(pub_key.signatures)
        self.assertEqual(umlauts_key.uids, (UMLAUTS_UID,))
        self.assertEqual(umlauts_key.key_type, gpg.KeyType.public)
        self.assertFalse(umlauts_key.signatures)

        pub_key, umlauts_key = extract_keys(sigs=True)
        self.assertEqual(pub_key.uids, (CN_UID,))
        self.assertEqual(pub_key.key_type, gpg.KeyType.public)
        self.assertTrue(pub_key.signatures)
        self.assertEqual(umlauts_key.uids, (UMLAUTS_UID,))
        self.assertEqual(umlauts_key.key_type, gpg.KeyType.public)
        self.assertTrue(umlauts_key.signatures)

        keys = self.s.list_pub_keys(sigs=True, keys=(pub_key.fingerprint,))
        self.assertEqual(keys, [pub_key])

        sec_key, = self.s.list_sec_keys()
        self.assertEqual(sec_key.uids, (CN_UID,))
        self.assertEqual(sec_key.key_type, gpg.KeyType.secret)

        keys = self.s.list_pub_keys(sigs=True, keys=())
        self.assertEqual(keys, [])

    def test_gen_key(self):
        self.s.gen_key(full_name=CN_UID.full_name,
                       email=CN_UID.email, passphrase="test", key_length=1024)
        pub_key, = self.s.list_pub_keys()
        self.assertEqual(pub_key.uids, (CN_UID,))
        self.assertEqual(pub_key.key_length, 1024)
        self.assertEqual(pub_key.key_type, gpg.KeyType.public)
        sec_key, = self.s.list_sec_keys()
        self.assertEqual(sec_key.uids, (CN_UID,))
        self.assertEqual(sec_key.key_length, 1024)
        self.assertEqual(sec_key.key_type, gpg.KeyType.secret)

    def test_decrypt(self):
        message = b"a"
        self.s.import_file(CN_SEC_KEY, passphrase="test")
        with self.assertRaises(BaseException):
            with self.s.decrypt(source=io.BytesIO(ENCRYPTED_MESSAGE),
                                passphrase="wrongpass"):
                pass
        with self.s.decrypt(source=io.BytesIO(ENCRYPTED_MESSAGE),
                            passphrase="test") as decrypted:
            msg = decrypted.read()
            self.assertEqual(msg, message)

    def test_encrypt_decrypt(self):
        key = self._setup_key()
        message = b"a"

        with self.s.encrypt(source=message,
                            recipients=(key.fingerprint,),
                            trust_model=gpg.TrustModel.always) as e:
            with self.s.decrypt(source=e,
                                passphrase="test") as decrypted, \
                    self.subTest("decrypt"):
                self.assertEqual(decrypted.read(), message)

    def test_delete_keys(self):
        self.s.import_file(SGT_HARTMANN_PUB_KEY)
        key, = self.s.list_pub_keys()
        self.assertEqual(
            key.fingerprint, SGT_HARTMANN_FPRT)
        self.s.delete_keys(key.fingerprint)
        self.assertFalse(self.s.list_pub_keys())

    def test_detach_sig(self):
        self.s.import_file(CN_SEC_KEY, passphrase="test")
        cn_key, = self.s.list_pub_keys()
        cn_key, = self.s.list_sec_keys()
        msg = b"Camelot! ... It's only a model."
        with self.s.detach_sig(msg, passphrase="test") as out:
            sig = out.read()
        fpr = self.s.verify(sig=sig, src=msg)
        self.assertEqual(fpr, cn_key.sub_keys[0].fingerprint)
        with self.assertRaises(gpg.GPGError):
            self.s.verify(sig=sig, src=b"Wrong message")


def to_info(key):
    return gpg.KeyInfo(uid=key.uids[0],
                       fingerprint=key.fingerprint,
                       key_algorithm=key.pub_key_algorithm,
                       creation_date=key.creation_date,
                       expiration_date=key.expiration_date,
                       key_length=key.key_length)


@unittest.skipUnless(KEY_SERVER is not None and WITH_GPG,
                     "Key Server Tests")
class TestGPGKeyserver(IntegrationTest):
    def test_send_search(self):
        self.s.import_file(CN_PUB_KEY)
        self.s.import_file(UMLAUTS_PUB_KEY)
        key_a, key_b = self.s.list_pub_keys()

        self.s.send_keys(key_a.key_id, key_b.key_id,
                         keyserver=KEY_SERVER)

        keys = gpg.search_keys(
            key_a.uids[0].full_name, keyserver=KEY_SERVER)
        self.assertEqual(list(keys), [to_info(key_a)])

        keys = gpg.search_keys(
            key_b.uids[0].full_name, keyserver=KEY_SERVER)
        self.assertEqual(list(keys), [to_info(key_b)])

        # By fingerprint
        keys = gpg.search_keys(
            key_b.fingerprint, keyserver=KEY_SERVER)
        self.assertEqual(list(keys), [to_info(key_b)])

        # By ID
        keys = gpg.search_keys(
            key_b.key_id, keyserver=KEY_SERVER)
        self.assertEqual(list(keys), [to_info(key_b)])

    def test_recv_keys(self):
        try:
            with tempfile.TemporaryDirectory() as gpg_temp_dir:
                temp_store = gpg.GPGStore(gpg_temp_dir)
                temp_store.import_file(SGT_HARTMANN_PUB_KEY)
                temp_store.import_file(UMLAUTS_PUB_KEY)
                key_a, key_b = temp_store.list_pub_keys(sigs=True)
                self.assertTrue(key_a.signatures or key_b.signatures)
                temp_store.send_keys(key_a.key_id, key_b.key_id,
                                     keyserver=KEY_SERVER)
        except FileNotFoundError:
            pass
        self.s.recv_keys(key_a.key_id, key_b.fingerprint,
                         keyserver=KEY_SERVER)
        keys = set(self.s.list_pub_keys(sigs=True))
        self.assertEqual({key_a, key_b}, keys)


CN_PUB_KEY = b"""-----BEGIN PGP PUBLIC KEY BLOCK-----


mI0EXcPQFwEEAMm1d9jlC5Zw1y/buUV6MuT5ABp4H8Sr3+MUf/GMFKPvd4Qboitd
Yf3eX753y0MNgzFlsSl8CtSO9pd+lqEt4WNMbIVWti04JAM6tD4lqeSzW57vlQlb
sGRf70fg9Qt1dc2LR0HcUi6bw46eWbSGGR3ZM7jbxB9F/VjpaTKI9S69ABEBAAG0
KkNodWNrIE5vcnJpcyA8Y2h1Y2subm9ycmlzQHJvdW5kaG91c2UuZ292PojOBBMB
CAA4FiEEKGahQqFvVOButzz5Lj5/4o/kEq4FAl3D0BcCGy8FCwkIBwIGFQoJCAsC
BBYCAwECHgECF4AACgkQLj5/4o/kEq59GQP+ONPvcLBccHAYbf0utUCiWZux9EwH
BN/TfOo1Vpgbq/DiBZcPoVeDvGTJDPg3dSUxsQzMHztp1UAi6o5Q6XCAGALMlxU9
QIHb4fyfbTQX1QrtB2EyLD/9O8nePrhqTqAd+xpdyvAw8L+hMoTyk0JnVW/UBVLH
RK4L9NaBxhSapfS4jQRdw9AXAQQAsuju5Ccwg3mDJcV+bR9yHIc+XyXcsbzFW0VU
lgNXiQoVHKJQ+X/SgElmxKwik8yeQ4CiM3/GeKmjhKB7JZnp4U+61Dfew+qc6Net
uAdNu7f26x5q237tjU9zx4JzhdnDMhrXkuYl/VR95S7CHlt1QlVxP1/Psx11a/Ej
xB+7ZDsAEQEAAYkBawQYAQgAIBYhBChmoUKhb1Tgbrc8+S4+f+KP5BKuBQJdw9AX
AhsuAL8JEC4+f+KP5BKutCAEGQEIAB0WIQRK0g8wPkscJLLIn7rzDUwzQHo/YwUC
XcPQFwAKCRDzDUwzQHo/YzIkA/4m5TWu7yvVzxjtybqHpShxrrZeTzWRrSu/SiCQ
bR8pGWP9NhnRDcfH/zMX6sMMorE6BBHI8fFMzJB974Lv0q2S8njVMuv+tIH7t+Um
KxlTY2Nz+uzFjuv2rDvPL4ozb4iZfOFq1WOwrml3fpE3qQzqLypd4OBj4H+ITghJ
DiJ55n2eBACItELQ3PcTXeh7XmXTeV3/lVhGHWlhUvcQUCNZCo9AFoX9aYBPX6OF
arsEzjNcZilc/R+r3xYF4kV2kspQQPGoslHN0Zq4Wxp0tOh/IevqjJ3bSzcCqwGz
c9fhdV81kJHiCZUFT03X+D5LrOJJ857/vwL1Roi5UgjRjX1jMFV/tg ==
=0f3v
-----END PGP PUBLIC KEY BLOCK-----
"""

CN_SEC_KEY = b"""-----BEGIN PGP PRIVATE KEY BLOCK-----

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
T03X+D5LrOJJ857/vwL1Roi5UgjRjX1jMFV/tg ==
=G52m
-----END PGP PRIVATE KEY BLOCK-----
"""


UMLAUTS_PUB_KEY = b"""-----BEGIN PGP PUBLIC KEY BLOCK-----

mI0EXcQPZwEEAMFLJh5nhUL3e2cIIEHw2lUwleWu/FMgy5GVVGho1pzSjqxc2cML
0PTLePd5/w/BOHH7tx2404CcwNVF8NrdPgFLV7mZu0Q4eUJNG+yz4EpUBCVK2si/
vNijeF3YH2vO18cyTCGiCW6vXi1cJqf6k73PCrSOPqj7QuNi41Ahkr5FABEBAAG0
KVdpdGggVW1sw6R1dHMgPHdpdGgudW1sYXV0c0B1bWxhdXRzLmluZm8+iM4EEwEI
ADgWIQS1Rlqvu4FLhxmgfbVt8x+lbBrrcQUCXcQPZwIbLwULCQgHAgYVCgkICwIE
FgIDAQIeAQIXgAAKCRBt8x+lbBrrca0uA/9Dj+s3F4FzO2MsDGaD8WXuZ8LPFSRW
zehWewIeRS6hT7L9+LNF3m0GVOueXCPrHj/8iBstc5UbFuph3Pu/3Cgw5YnnSkcC
/LPFGRlc5Z6oRF259qZNW8NafOoi1E4o/LAN1QG5SChYUS2jcyDrosJekGEaPP3n
0KqQQPYC7Smu3riNBF3ED2cBBADClqvryRmApeYO8tQcGWaiFa27vFmM4FCAzbPK
tt88N1GaHWgycgVV/dChhWDVVkEDnas+WwVMz39ZZi8tejBrk1mtoIIBctn8AWJL
W7VH9ZOrfPm1UuqLE7YMhu9hl7i4ANIJnJMsjYnOnb/Z9ButzIobZdigV7a1j47t
pXHnuwARAQABiQFrBBgBCAAgFiEEtUZar7uBS4cZoH21bfMfpWwa63EFAl3ED2cC
Gy4AvwkQbfMfpWwa63G0IAQZAQgAHRYhBHW94ZPbXFu5K4+7zYDWfVUAnJDMBQJd
xA9nAAoJEIDWfVUAnJDMBb4EAKt1sMe/6MhTsn3weshU5U6T217W/lxXmz5vErnO
yd0WaMWOsGN7WEV/UtoVMZ/EBBdIqswUiujDPd8oL3yCsNBZNDigyCGX6shqCeRP
AAUkpC/0KWDP33PNenGSMFzoBcghYBRUuVucvamzskDfidsKbLv+/7FkRwzstg7L
5/GUKGkD/2LlSZlm+qDBzDt5q+tQaGOQnJmebF7o4FQ8feY7GNcFQ9DMV9lR5vuZ
jV4OTQVS2Prv2ASuN7rPRbUYeJD5t7Mko9DzL+6XGgjPim6Wg1xlRSRkskksbX3y
QndrRiimeh43nPBLOBRN9HQoaywkc6hoAZTQAvCgOZli507dp8Mz
=sfjX
-----END PGP PUBLIC KEY BLOCK-----
"""

SGT_HARTMANN_UID = gpg.Uid(full_name="Gunnery Sgt. Hartmann",
                           email="hartmann@bullshit.gov")

SGT_HARTMANN_FPRT = "DA1A363BC5E11DA73806A8A4E3E4024A0E56221E"

SGT_HARTMANN_PUB_KEY = b"""-----BEGIN PGP PUBLIC KEY BLOCK-----

mQENBF3MKrABCACw6ZFUve5lTSCtDfhcuDH0pFd7AF0uM1o4kEBLKfcEImrgGo7S
LX7tooxsx2gNv4ARHW4XL5pixLj4itRBDeUGczdDzNwQeE6HmWNW2JtqF7/h1TTr
iw3UwS3eOG8sNrZxx2yLoIF/JZP2CDLz7jXDhuAvLdoK8hzNX82PVUkoVKtPYhbk
1gw3y1coH2Z6rdAp6EwrMSg95vbwzKjuhcyYlxRodwlvmJhDBRxr86QCCRNiA6R8
7Nugtt/wP5XbxcxgNBmciX10NPR4eIoQk4acyGlDvOdrF50h2DPAw3HUdOw513xN
4b7NOHlJJk0+Uo4yKcZ2LXmeiSNU6TY93moLABEBAAG0LUd1bm5lcnkgU2d0LiBI
YXJ0bWFubiA8aGFydG1hbm5AYnVsbHNoaXQuZ292PokBVAQTAQgAPhYhBNoaNjvF
4R2nOAaopOPkAkoOViIeBQJdzCqwAhsDBQkDwmcABQsJCAcCBhUKCQgLAgQWAgMB
Ah4BAheAAAoJEOPkAkoOViIeSIEH/RDXmilCOkoR6uxJgNm7MUqavL2/s3ks57uk
qDrldJm3T5SKBCgrUSP3UaiBIwq+M32k23+CLNl8RQBVwhFAnJcHmMK/fEVcSK8G
HKy4CS8yu1xwDIgWWeDBtbo6r4IEah19dBSLOrxeyBFoI65pRHP18AWMaHnKv5nz
GXdGiLlRl6rKbyBxnesXweR+IIZJhciphhzuV8HtnyHsess0Toq2kjiCGp7Kjkz1
6YQSiHawAj3nV+/RK0kNLZsuQOgY7X2WVw4HAU//Ap1XdtMbOxberLcUU7Rzeudg
uiWfkmTMM36mhojOjtPhgB1J9ZZZCe5KM7hRB2VFuJE45r3S5LCIswQTAQgAHRYh
BChmoUKhb1Tgbrc8+S4+f+KP5BKuBQJdzCsMAAoJEC4+f+KP5BKuz3oD/inKIFnX
KzFblhnLeHf+tW7JQ9EVu+7rTKKyHHay7sgzVQ2KfySemFYwn2fgXUOuZtuk0axe
BHV0qTgL0vfnadxXF96tjFQ14xhBym6KR2ccvQN+/GLM5c0iBbp59azMy0q4VyJH
5c435C3Yq9ownEvJRRdYdJgaFTU1wjwQs7qZuQENBF3MKrABCADguI7FCLGtG6rZ
/EJv58Bnihfz9OuUSc/R6DaFbGGtolTzpTskX3pK1daYigPDDv4iMN5KnO1eeJyp
wmyRpC2yKBLw70z87QGPSviQHWTvyj22YF9ByywFKAuZeY2tpWwkLW2bbVm38LLT
hwmDRkQ8nQZPufvpDOHq6AC84ymW5TuHKEYTfF//14hyonOK40HNjSdEC6ZvfN2n
N80y9g3IvaNGsPOo3MW4z877W9v/IAvFlTEVnyRA0hXEykFnUYk//Eh6cnDTlrCO
hLwd9bbcivPPpjiGYLjgvDghyXK/qv2T4ahiMq2qxp5F8c4x/aTq8U//9GIEU7nd
danxrHsZABEBAAGJATwEGAEIACYWIQTaGjY7xeEdpzgGqKTj5AJKDlYiHgUCXcwq
sAIbDAUJA8JnAAAKCRDj5AJKDlYiHiyUB/9ZH1ZUF/lHsFjFgypyv1BfqFIyYZk9
1/zSHdwUl7svtBrc8XewisxgCBywbzJWHCooAAkSmwSrCFnqVfoUFCdAYxd3lrX1
DA2WEDcIr3Im2wUOKw0fB5yyBcep5QAzoRFl3uZwOcAYrqq38L7xAoRka991oPIk
nzY4GfcR+7ftmzKDPcXjTIbLQwmDNR0vDy7kNBB7ycHWwrMfadWGrGmeQ8pgTnP4
Egfkuv5fEQ3njiV3QcRwmTtqPEVPmA1G/TStAPZa9cBfYHTxH1JzxwVhYvBWXoA3
vwMVdh5kI53+JxM0k7OS6SI8cpf4pmiyLypdkyOCql2HYe7iPuRk0IYi
=lmDh
-----END PGP PUBLIC KEY BLOCK-----
"""

ENCRYPTED_MESSAGE = (
    b'\x84\x8c\x03\xf3\rL3@z?c\x01\x03\xff\\\t\xea;f\xb4`b\x05\xfeJ(\xdf'
    b'^`"\x87B/\x8b\xdfYD\xb4^\x03\x99R\x0bn\x1c\x12\xca6Ju\x8e\x03\x1fI'
    b'U|~\x89>w\x18\'\xad\xbb\xa0\x86\x85\x1a\r\x93\xe8$\xd0H\xf8\xef\xfa'
    b'\x16\x87\x17K|\x9d$\xeb<\xbd\x0e3N\xbd{\xf1bT\xcd\xa3-\xc6\x83\x0e'
    b'\x96\xc5\xcb--\x93P\x15\xe7@\x84\x8fR\xfa\t\xc2\x99\x1f\xc4\xf0`\xfc'
    b'\x87v\x04\x1c\x9ef\x03\xc7Jh\x840\x112/\x1b\x06L\xf4\xd2<\x01\xbb'
    b'\xd2\x80=\x17\x9d\xc5ww\n\xd9\xf7%\x9fpzg\\\x1fz\x02\xf8$\x17\xe7V'
    b'\x825\xdd\n\xedu\x12\xa9\xac\xab5\x99\x9b\x7f\x9a\x8f\\\xd1\xa8\xb2'
    b'\xe9!\x1dH\xa3\x1c\xd9\xf9\xd1l\x86\xe7\x12'
)
ENCRYPTED_MESSAGE_CN = (
    b'\x84\x8c\x03\xf3\rL3@z?c\x01\x03\xffw\x058f\x95\xbd\xe5\x8d1q'
    b'\xdd\x80\xbd\x8d\xb5v5\xb3\xcf\x92\xb9?6\x8a \xfc\xc9\xc9\xad'
    b'\xccI\xd7\xc1@\xe3\xb3]\xbag\xcb\xae\x99\xbdkB\xdd\xcaS\x86598'
    b'\x00\xdd\xe1C\xad$1<\xe0\xac\xd5\x9b4\xc0w\xb5O\xf6\x8a/\x88\x7f'
    b'\x1b!\xb7\x08x\x0cUV\xd3\x1e\xaba\xe8\x03]\xc79\xea\x05\x0f*\xdc'
    b'\xa5\x88\xac\xa3Y\xa0\xfb\xd24\xf4\xa0hD\xe3\xaa\x11\xd1\xf9o'
    b'\xf7\xf7\xc3\xc8:\x0c\x16\xd5W\xfa%\x8f7\xd2F\x01q\x07\xd0\xde'
    b'~\xe1V\x00h\xc0O=ls?\x13\xfc\x9e\x8aY>e\x10$\xd2\xdb;\x18\xc0'
    b'\xf7]\xa2)r\xfe\xf8\xd9\x05\xcb\xcc\r8\xb5\xaf\x8b\xa0\xff.\xa1T'
    b'&_\x17\xdb\x0bi\x04\xd0\xa3\xa2\x9c\x8b\x80\x96\xb5\x10I\xea`'
)
