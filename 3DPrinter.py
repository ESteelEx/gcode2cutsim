#!/usr/bin/env python
# sysTrayIcon.py
# main script
# Multi Threaded Test Stage for 3D Printer module.

"""
3D Printer is a multifunctional module. Test a bunch of processed STL sets with comparable output. What is called Test stage.
Slice and calc single STLs + additional simulation with verifier
"""

import sys, logging
from CLUtilities import G2CLogging
from Utilities.console import bcolors
from Utilities.ini_worker import get_section_from_ini
from Utilities import help
from TestStage.test_stage import TestStage
from TestStage.thread_manager import thread_manager

__author__ = 'mathiasr'

# ----------------------------------------------------------------------------------------------------------------------
def main():
    """Main module admins the additional arguments passed with 3DPrinter.exe

    Here is decided if test stage will be executed or just a single STL file is processed.
    Also all exceptions when passing wrong commands are handled here.
    """

    _TS_LOGGER = G2CLogging.G2CLogging() # start logger

    _ABS_TEST_FODLER = r'\\OFFICE-AACHEN\projects\07_Products\06_3D-Printing\TestStage'

    _TS_LOGGER.wlog('INFO', 'WORKING DIRECTORY: ' + _ABS_TEST_FODLER)

    _COMMAND_LIST_TEST_STAGE = [{'TS': {'TS': False, 'MT': True, 'GT': False, 'TF': True }}, ]
    _COMMAND_LIST_SINGLE_FILE = [{'STL': {'STL': True, 'SIM': True}},
                                 {'SIM': {'P': True}}]

    _H = help.helper()
    TS = TestStage()

    print '\n' + bcolors.UNDERLINE + bcolors.BOLD + 'MW 3DPRINTER MULTIOPERATOR ... ' + bcolors.END
    print 'INIT ...' + '\n'

    if len(sys.argv) == 1:  # this is a default case with no passed command
        print bcolors.WARNING + 'No STL passed. Starting with STL file name in config.ini' + bcolors.END
        section_dict = get_section_from_ini('bin\\3DPrintModule\\config.ini', 'MESH')  # read all parameters related to MESH
        TS.start3DPrintJob(STL_file=section_dict['fileName'])  # not necessary to pass over stl. default is None
    else:

        bool_list = ['-' in s for s in sys.argv]  # proof if commands are complete or if a command is given

        if bool_list[1]:  # we expect an command with prefix '-' here

            command_dict = {}
            if sys.argv[1][1:] == 'TS':  # this is test stage

                if len(sys.argv) > 2:

                    for i in range(2, len(sys.argv)):
                        # check command list
                        TS_DICT = _COMMAND_LIST_TEST_STAGE[0]['TS']

                        if sys.argv[i][1:] in TS_DICT:

                            if TS_DICT[sys.argv[i][1:]]:
                                if len(sys.argv)-1 > i:
                                    if sys.argv[i+1][0] == '-':
                                        print 'Input for parameter ' + sys.argv[i] + ' expected.'
                                        return
                                    else:
                                        # command_dict.append(sys.argv[i][1:] + '=' + sys.argv[i+1])
                                        command_dict[sys.argv[i][1:]] = sys.argv[i+1]
                                else:
                                    print 'Input for parameter ' + sys.argv[i] + ' expected.'
                                    return
                            else:
                                # command_dict.append(sys.argv[i][1:] + '=True')
                                command_dict[sys.argv[i][1:]] = True

                    TM = thread_manager(TF=_ABS_TEST_FODLER, command_dict=command_dict)
                    TM.controller()

                else:
                    # seems there is only one command. So start test stage with default parameters
                    TM = thread_manager(TF=_ABS_TEST_FODLER)
                    TM.controller()

            elif sys.argv[1][1:] == 'STL':  # process a single STL

                for i in range(1, len(sys.argv)):
                    print sys.argv[i]


            # if sys.argv[i][0] == '-':
            #     if len(sys.argv[i]) > 1:
            #         if sys.argv[i][1:] == 'TS':
            #             file_list = os.listdir(_RELATIVEFOLDERTESTFILES)  # get directory list
            #             test_file_list = []
            #             for i in file_list:
            #                 if i.find('.stl') != -1:
            #                     test_file_list.append(i)
            #
            #             print '\n' + bcolors.BOLD + 'TESTNG STL SET:' + '-'*60 + '\n' + bcolors.END
            #
            #             for i, j in zip(test_file_list, range(len(test_file_list)) ):
            #                 print bcolors.DARKGREY + '+-> ' + str(j) + ' ' + i + bcolors.END
            #
            #             print '-'*60 + '\n'
            #
            #             jj = 0
            #             while 1:
            #                 if (threading.activeCount() - 1) <= _MAXTHREADS:
            #                     i = test_file_list[jj]
            #                     message = '\n' + 'TS<=: Starting test ' + str(jj + 1) + ' of ' + str(len(test_file_list)) + \
            #                               ' with: ' + i + ' - Running threads [' + str(threading.activeCount()-1) + ']'
            #                     print bcolors.UNDERLINE + bcolors.BOLD + message + bcolors.END + '\n'
            #                     TestStage(path=_RELATIVEFOLDERTESTFILES, fileName=i).start()
            #                     jj += 1
            #                     if jj >= len(test_file_list):
            #                         break
            #
            #             print bcolors.BOLD + '<ALL THREADS AND TESTING STAGES RUNNING>' + bcolors.END
            #
            #         elif sys.argv[i][1:] == 'SF':  # SF for single file [STL]
            #             # we passed a storage place to a stl file
            #             if len(sys.argv) == 3:
            #                 if not os.path.isfile(sys.argv[2]):
            #                     print bcolors.FAIL + 'No such STL file -> "' + str(sys.argv[2]) + '" ... Please proof INPUT' + bcolors.END
            #                 else:
            #                     print 'Processing >> ' + sys.argv[2] + '\n'
            #                     TestStage(sys.argv[2]).start3DPrintJob(sys.argv[2])
            #             else:
            #                 print bcolors.RED + 'Please provide STL file' + bcolors.END
            #
            #         else:
            #             print bcolors.RED + 'No known command.' + bcolors.END + '\n'
            #             _H.print_help()
            #     else:
            #         print bcolors.RED + 'No command.' + bcolors.END + '\n'
            #         _H.print_help()
            # else:
            #     print bcolors.RED + 'If you want to pass a command use the - operator with following commandline' \
            #           + bcolors.END + '\n'
            #     _H.print_help()

    print bcolors.DARKGREY +'TS<=:DONE' + bcolors.END

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
