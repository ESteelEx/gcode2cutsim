import os, threading, string
from TestStage.test_stage import TestStage
from Utilities.console import bcolors


# ----------------------------------------------------------------------------------------------------------------------
class thread_manager():
    """the coordinator controls the maximum threads and starts one test stage after the other"""
    def __init__(self, TF='bin\\3DPrintModule\\', MT=2, GT=None, command_dict=[]):
        self.TF = TF
        self.MT = MT  # number of threads
        self.GT = GT
        if len(command_dict) != 0:
            for key, item in command_dict.iteritems():
                if 'MT' in key:
                    try:
                        int(item)
                        self.MT = int(item)
                    except:
                        print 'Expected an integer as input. Calculation with default value.'

                elif 'TF' in key:
                    if os.path.isdir(item):
                        self.TF = item
                    else:
                        print 'Path does not exist. Taking default.'

    # ------------------------------------------------------------------------------------------------------------------
    def controller(self):

        _MAXTHREADS = self.MT
        _RELATIVEFOLDERTESTFILES = self.TF

        test_file_list = []

        print 'SETTING UP TEST DB. SEARCHING FOR TEST FILES IN: ' + _RELATIVEFOLDERTESTFILES
        # iterate through all elements of root and subfolders
        for root, dirs, files in os.walk(_RELATIVEFOLDERTESTFILES):
            for name in files:
                if name.endswith((".stl")):
                    root = string.replace(root, '\\', '/')
                    test_file_list.append(root + '/' + name)

        print 'DONE'

        print '\n' + bcolors.BOLD + 'TESTING STL SET:' + '-'*60 + '\n' + bcolors.END

        for i, j in zip(test_file_list, range(len(test_file_list)) ):
            print bcolors.DARKGREY + '+-> ' + str(j) + ' ' + i + bcolors.END

        print '-'*60 + '\n'

        jj = 0
        while 1:
            if (threading.activeCount() - 1) <= _MAXTHREADS:
                i = test_file_list[jj]
                message = '\n' + 'TS<=: Starting test ' + str(jj + 1) + ' of ' + str(len(test_file_list)) + \
                          ' with: ' + i + ' - Running threads [' + str(threading.activeCount()-1) + ']'
                print bcolors.UNDERLINE + bcolors.BOLD + message + bcolors.END + '\n'
                TestStage(path=_RELATIVEFOLDERTESTFILES, fileName=i).start()
                jj += 1
                if jj >= len(test_file_list):
                    break

        print bcolors.BOLD + '<ALL THREADS AND TESTING STAGES RUNNING>' + bcolors.END