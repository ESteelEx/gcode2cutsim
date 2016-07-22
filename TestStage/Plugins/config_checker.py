"""This module checks on consistency of config file"""
import hashlib
from Utilities import ini_worker
import global_parameter

# ----------------------------------------------------------------------------------------------------------------------
class config_checker():
    def __init__(self, config_orig, config_test):
        self.config_orig = config_orig
        self.config_test = config_test

        self.config_orig_MD5 = self.checksum_md5(self.config_orig)
        self.config_test_MD5 = self.checksum_md5(self.config_test)

        self.warning = {}

    # ------------------------------------------------------------------------------------------------------------------
    def checksum_md5(self, filename):
        md5 = hashlib.md5()
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                md5.update(chunk)

        return md5.digest()

    # ------------------------------------------------------------------------------------------------------------------
    def compare_hashtags(self):
        """

        :return: bool
        """
        if self.config_orig_MD5 == self.config_test_MD5:
            changes = False
        else:
            changes = True

        return changes

    # ------------------------------------------------------------------------------------------------------------------
    def compare_sections(self):
        section_list_org = ini_worker.get_sections_list_from_ini(self.config_orig)
        section_list_test = ini_worker.get_sections_list_from_ini(self.config_test)

        for section in section_list_org:
            if section not in section_list_test:
                self.warning['section'] = True

        return

def main():
    CC = config_checker('config.ini', 'config - Copy.ini')
    print CC.config_orig_MD5
    print CC.config_test_MD5
    if CC.compare_hashtags():
        # continue here with code
        CC.compare_sections()
    else:
        # nothing changed so stage must not compare. We safe time here.
        pass


main()

