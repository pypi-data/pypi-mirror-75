#!python3

import unittest
import os
import sys
import subprocess

sys.path.insert(0, os.getcwd())
os.environ["WITH_GPG"] = "true"
os.environ["KEY_SERVER"] = "hkp://fl-8-188.zhdk.cloud.switch.ch:80"


def main():
    from test import test_gpg

    # DOWNLOAD_URL = "https://www.gnupg.org/ftp/gcrypt/binary/"

    INSTALLERS = (
        ("2.2.8", "gnupg-w32-2.2.8_20180613.exe"),
        ("2.2.9", "gnupg-w32-2.2.9_20180712.exe"),
        ("2.2.10", "gnupg-w32-2.2.10_20180830.exe"),
        ("2.2.11", "gnupg-w32-2.2.11_20181106.exe"),
        ("2.2.12", "gnupg-w32-2.2.12_20181214.exe"),
        ("2.2.13", "gnupg-w32-2.2.13_20190212.exe"),
        ("2.2.14", "gnupg-w32-2.2.14_20190319.exe"),
        ("2.2.15", "gnupg-w32-2.2.15_20190326.exe"),
        ("2.2.16", "gnupg-w32-2.2.16_20190528.exe"),
        ("2.2.17", "gnupg-w32-2.2.17_20190709.exe")
    )

    try:
        installer_path = sys.argv[1]
    except IndexError:
        print("please provide a path containing the installers")
        sys.exit(1)

    test_loader = unittest.TestLoader()
    for version, installer in INSTALLERS:
        print("Installing version", version, installer)
        subprocess.run(
            (os.path.join(installer_path, installer), "/S"), shell=True)
        subprocess.run(("gpg", "--version"))
        print("Testing version", version)
        test_suite = test_loader.loadTestsFromModule(test_gpg)
        unittest.TextTestRunner().run(test_suite)


main()
