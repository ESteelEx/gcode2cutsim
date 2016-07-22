"""This module checks on consistency of config file"""
import hashlib


# ----------------------------------------------------------------------------------------------------------------------
class config_checker():
    def __init__(self, config_test, config_orig):
        self.config_test = config_test
        self.config_orig = config_orig

    # ------------------------------------------------------------------------------------------------------------------
    def load_hash(self, file):

        hash_number = hashlib.sha256()

    # ------------------------------------------------------------------------------------------------------------------
    def checksum_md5(self, filename):
        md5 = hashlib.md5()
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                md5.update(chunk)

        return md5.digest()


CC = config_checker('config_checker.py', 'config_checker.py')
print CC.checksum_md5('config_checker.py')