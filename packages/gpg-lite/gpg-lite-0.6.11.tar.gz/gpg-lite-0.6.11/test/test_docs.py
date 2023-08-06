import unittest
from pathlib import Path
from unittest import mock
import io
from contextlib import contextmanager


class TestDocs(unittest.TestCase):
    @staticmethod
    def test_gen_key():
        """Read the python code snippets from README and exec"""
        read = False
        code = ""
        with open(Path(__file__).parent.parent / "README.md") as doc:
            for line in doc:
                if line == "```python\n":
                    read = True
                    continue
                if line == "```\n":
                    read = False
                    continue
                if read:
                    code += line

        @contextmanager
        def mock_cmd(cmd, *_, **__):
            if "--version" in cmd:
                yield mock.Mock(stdout=io.BytesIO(b"""gpg (GnuPG) 2.2.19
libgcrypt 1.8.5
Copyright (C) 2019 F..."""))
            elif "--list-public-keys" in cmd:
                yield mock.Mock(stdout=io.BytesIO(b"""tru::1:1571400791:0:3:1:5
pub:u:2048:1:FDC66B7A5F6FFD4B:1550241679:::u:::scESC::::::23:1571230031:1 http\\x3a//keyserver.dcc.sib.swiss\\x3a11371:
fpr:::::::::CB5A3A5C2C4419BB09EFF879D6D229C51AB5D107:
uid:u::::1550241679::B1E8D4565D26BED47D1EB8BB2B5733AEC1F154B5::Chuck Norris <chuck.norris@roundhouse.gov>::::::::::0:
sig:::1:FDC66B7A5F6FFD4B:1550241679::::Chuck Norris <chuck.norris@roundhouse.gov>:13x::CB5A3A5C2C4419BB09EFF879D6D229C51AB5D107:::8:
sig:::1:3A6500D5C1DE39AC:1571225229::::DCC Test (Test key for transferprotocol) <dcc@sib.swiss>:13x:::::2:
sig:?::1:2E3E7FE28FE412AE:1573661452::::[User ID not found]:13x::2866A142A16F54E06EB73CF92E3E7FE28FE412AE:::8:
sub:u:2048:1:D892C41917B20115:1550241679::::::e::::::23:
fpr:::::::::55C5314BB9EFD19AE7CC4774D892C41917B20115:"""))
            else:
                yield mock.Mock(stdout=io.BytesIO(b"[GNUPG:] KEY_CREATED aaaaaaaaaaaa"))
        with mock.patch("gpg_lite.cmd_pipe", mock_cmd), \
                mock.patch("gpg_lite.cmd_pipe_stdout", mock.Mock()), \
                mock.patch("gpg_lite.cmd_devnull", mock.Mock()), \
                mock.patch("builtins.print", mock.Mock()):
            exec(code)  # pylint: disable=exec-used
