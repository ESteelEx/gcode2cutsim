"""This module checks consistency of config file"""
import hashlib, filecmp
from difflib import SequenceMatcher
from Utilities import ini_worker
from Utilities.console import bcolors

__version__ = '1.0.0'

# ----------------------------------------------------------------------------------------------------------------------
class config_checker():
    """"""
    def __init__(self, config_orig, config_test):
        self.config_orig = config_orig
        self.config_test = config_test

        self.config_orig_MD5 = self.checksum_md5(self.config_orig)
        self.config_test_MD5 = self.checksum_md5(self.config_test)

        self.section_list_orig = []
        self.section_list_test = []

        self.section_param_orig = {}
        self.section_param_test = {}

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
        self.section_list_orig = ini_worker.get_sections_list_from_ini(self.config_orig)
        self.section_list_test = ini_worker.get_sections_list_from_ini(self.config_test)

        print '\nMATCHING SECTIONS'

        for section in self.section_list_orig:
            if section not in self.section_list_test:
                self.warning['section'] = True
                print bcolors.RED + section + ' -> MISSING' + bcolors.END
            else:
                print bcolors.GREEN + section + ' -> MATCH' + bcolors.END

        return self.warning

    # ------------------------------------------------------------------------------------------------------------------
    def get_similarity(self, a, b):

        return SequenceMatcher(a, b).ratio()

    # ------------------------------------------------------------------------------------------------------------------
    def compare_parameters(self):
        """

        :return:
        """
        print bcolors.BOLD + '\nMATCHING SECTION PARAMETER' + bcolors.END

        for section in self.section_list_orig:
            self.section_param_orig[section] = ini_worker.get_section_from_ini(self.config_orig, section)

        for section in self.section_list_test:
            self.section_param_test[section] = ini_worker.get_section_from_ini(self.config_test, section)

        intersection_list = list(set(self.section_list_orig).intersection(self.section_list_test))

        differ_list_orig = list(set(self.section_list_orig).difference(self.section_list_test))
        differ_list_test = list(set(self.section_list_test).difference(self.section_list_orig))

        # proof -> seen from original MASTER document
        if len(differ_list_orig) != 0:
            print bcolors.RED + str(differ_list_orig) + ' -> MISSING' + bcolors.END

        # proof -> seen from WANT TO COMMIT document
        if len(differ_list_test) != 0:
            print bcolors.LIGHTRED + str(differ_list_test) + ' -> COMMIT REQUEST' + bcolors.END

        # proof parameters of sections
        section_differ = []
        for key in intersection_list:

            print bcolors.BOLD + 'TESTING: ' + key + bcolors.END

            # from MASTER side
            differ_params_orig = list(set(self.section_param_orig[key]).
                                 difference(self.section_param_test[key]))

            # from TESTER side
            differ_params_test = list(set(self.section_param_test[key]).
                                      difference(self.section_param_orig[key]))

            if len(differ_params_orig) == 0 and len(differ_params_test) == 0:
                print bcolors.GREEN + key + ' -> MATCH' + bcolors.END
            else:
                if len(differ_params_orig) != 0:

                    section_differ.append(key)

                    differ_param_list = list(set(self.section_param_orig[key]).
                                             difference(self.section_param_test[key]))

                    print bcolors.RED + key + ' -> MISSING -> ' + str(differ_param_list) + bcolors.END

                if len(differ_params_test) != 0:

                    section_differ.append(key)

                    differ_param_list = list(set(self.section_param_test[key]).
                                             difference(self.section_param_orig[key]))

                    print bcolors.LIGHTRED + key + ' -> REQUEST -> ' + str(differ_param_list) + bcolors.END



# ------------------------------------------------------------------------------------------------------------------
def init_plugin():
    """

    :return:
    """
    print bcolors.BOLD + 'INIT CONFIG CHECKER' + bcolors.END
    print bcolors.BOLD + 'VERSION: ' + __version__ + bcolors.END


# ------------------------------------------------------------------------------------------------------------------
def main():
    """

    :return:
    """
    init_plugin()
    CC = config_checker('config_MASTER.ini', 'config_TESTER.ini')
    if CC.compare_hashtags():
        # continue here with code
        CC.compare_sections()
        CC.compare_parameters()
    else:
        # nothing changed so stage must not compare. We safe time here.
        print bcolors.BOLD + 'NOTHING CHANGED. FILES ARE THE SAME' + bcolors.END
        pass

main()

