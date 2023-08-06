import io
from typing import Optional, Tuple
from shutil import copyfileobj
from contextlib import contextmanager

import subprocess  # nosec
# Here bandit warns about:
# B404:blacklist import_subprocess
# B603:subprocess_without_shell_equals_true
# 1. We do not use shell=True in this package
# 2. All calls to subprocess start with gpg, so possibly unsanitized input would
#    only result in a gpg error message

if hasattr(subprocess, "STARTUPINFO"):
    def startupinfo():
        _startupinfo = subprocess.STARTUPINFO()
        _startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        _startupinfo.wShowWindow = subprocess.SW_HIDE
        return _startupinfo
else:
    def startupinfo():
        return None


class GPGError(BaseException):
    pass


def cmd(command: Tuple[str], out: Optional[io.IOBase] = None,
        **kwargs):
    if out is not None:
        return cmd_devnull(command, stdout=out, **kwargs)
    return cmd_pipe_stdout(command, **kwargs)


def cmd_devnull(command: Tuple[str], src=None,
                stdout=subprocess.DEVNULL, **kwargs):
    with cmd_pipe(command, src=src, stdout=stdout, **kwargs):
        pass


@contextmanager
def cmd_pipe_stdout(*args, **kwargs):
    with cmd_pipe(*args, **kwargs) as proc:
        yield proc.stdout


@contextmanager
def cmd_pipe(command: Tuple[str], src=None, stdout=subprocess.PIPE, passphrase=None, **kwargs):
    feed = None
    if src is not None:
        if has_fileno(src) and passphrase is None:
            kwargs["stdin"] = src
        else:
            kwargs["stdin"] = subprocess.PIPE
            if isinstance(src, bytes):
                feed = feed_from_str(src)
            else:
                feed = feed_from_stream(src)

    # For the bandit vulnerability suppressed here (nosec):
    # see info close the subprocess import
    with subprocess.Popen(command, stderr=subprocess.PIPE,  # nosec
                          stdout=stdout,
                          startupinfo=startupinfo(),
                          **kwargs) as proc:
        if passphrase is not None:
            proc.stdin.write(passphrase.encode() + b"\n")
        if feed is not None:
            feed(proc.stdin)
            proc.stdin.flush()
            proc.stdin.close()
        yield proc
        err = proc.stderr.read()
    if proc.returncode != 0:
        raise GPGError(err.decode('utf-8', 'replace'))


class ExpectProc:
    def __init__(self, proc):
        self.proc = proc
        self.source = proc.stderr
        self.dest = proc.stdin
        self.stdout = proc.stdout

    def expect(self, expected, prefix=b"[GNUPG:] GET_"):
        actual = b""
        while not actual.startswith(prefix):
            actual = self.source.read(len(prefix))
            c = True
            while c and c != b"\n":
                c = self.source.read(1)
                if c != b'\r':  # Skip '\r' (windows)
                    actual += c
            if not actual:
                raise ValueError("Unexpected end of source")
        if actual != expected:
            raise ValueError(
                f"Unexpected prompt from gpg:\n{expected}\n{actual}")

    def put(self, msg):
        self.dest.write(msg)
        self.dest.flush()


@contextmanager
def expect(command, **kwargs):
    # For the bandit vulnerability suppressed here (nosec):
    # see info close the subprocess import
    with subprocess.Popen(command, stdin=subprocess.PIPE,  # nosec
                          stderr=subprocess.PIPE, stdout=subprocess.PIPE, **kwargs) as proc:
        yield ExpectProc(proc)


def feed_from_str(src: str):
    def feed(stdin):
        stdin.write(src)
    return feed


def feed_from_stream(src: io.IOBase):
    def feed(stdin):
        copyfileobj(src, stdin)
    return feed


def has_fileno(s: io.FileIO) -> bool:
    if hasattr(s, "fileno"):
        try:
            s.fileno()
        except BaseException:
            return False
        return True
    return False
