"""This module checks consistency of config file"""
import hashlib
from Utilities import ini_worker
import global_parameter

__version__ = '1.0.0'

# ----------------------------------------------------------------------------------------------------------------------
class config_checker():
    def __init__(self, config_orig, config_test):
        self.config_orig = config_orig
        self.config_test = config_test

        self.config_orig_MD5 = self.checksum_md5(self.config_orig)
        self.config_test_MD5 = self.checksum_md5(self.config_test)

        self.section_list_org = []
        self.section_list_test = []

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
        """

        :return:
        """
        self.section_list_org = ini_worker.get_sections_list_from_ini(self.config_orig)
        self.section_list_test = ini_worker.get_sections_list_from_ini(self.config_test)

        for section in self.section_list_org:
            if section not in self.section_list_test:
                self.warning['section'] = True
            else:
                print section + ' FOUND -> OK'

        return self.warning

    # ------------------------------------------------------------------------------------------------------------------
    def compare_parameters(self):

        for section in self.section_list_org:
            section_param = ini_worker.get_section_from_ini(self.config_orig, section)
            print section_param

# ------------------------------------------------------------------------------------------------------------------
def init_plugin():
    print 'INIT CONFIG CHECKER'
    print 'VERSION: ' + __version__


# ------------------------------------------------------------------------------------------------------------------
def main():
    init_plugin()
    CC = config_checker('config.ini', 'config - Copy.ini')
    if CC.compare_hashtags():
        # continue here with code
        CC.compare_sections()
        CC.compare_parameters()
    else:
        # nothing changed so stage must not compare. We safe time here.
        pass

main()

