#!/usr/bin/env python
# sysTrayIcon.py
# main script
# Multi Threaded Test Stage for 3D Printer module.

"""
3D Printer is a multifunctional module. Test a bunch of processed STL sets with comparable output. What is called Test stage.
Slice and calc single STLs
"""

import sys, os, subprocess, threading, time, filecmp
from Utilities.console import bcolors
from Utilities.ini_worker import get_section_from_ini
from Utilities import help

__author__ = 'mathiasr'

class TestStage(threading.Thread):
    """

    """
    def __init__(self, path='\\bin\\3DPrintModule\\', fileName=''):
        threading.Thread.__init__(self)
        self.path = path
        self.fileName = fileName
        self.WORKINGDIR = os.getcwd() + '\\' + self.path
        self.RELATIVEFODLERTOCOMPARE = 'WORKINGCOPYTESTING\\'

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        """Main thread that starts
        :return:
        """
        try:
            self.start3DPrintJob(STL_file=self.path + self.fileName)

            print bcolors.DARKCYAN + 'TS<=: COMPARING <' + self.fileName[:-3] + 'gcode>' + bcolors.END

            if os.path.isfile(self.path + self.fileName[:-3] + 'gcode') and  \
                    os.path.isfile(self.WORKINGDIR + self.RELATIVEFODLERTOCOMPARE + self.fileName[:-3] + 'gcode'):

                gcode_original = self.WORKINGDIR + self.RELATIVEFODLERTOCOMPARE + self.fileName[:-3] + 'gcode'
                gcode_to_compare = self.path + self.fileName[:-3] + 'gcode'

                answer = filecmp.cmp( gcode_original, gcode_to_compare)

                if answer:
                    print bcolors.GREEN + 'TS<=: NO CHANGES <' + self.fileName[:-3] + 'gcode>' + bcolors.END
                else:
                    print bcolors.RED + 'TS<=: CHANGES <' + self.fileName[:-3] + 'gcode>' + bcolors.END

            else:
                print bcolors.RED + 'TS<=:<' + self.fileName[:-3] + '> - was not processed before. Add it.' + bcolors.END


        except:
            pass

        print ''

        return

    # ----------------------------------------------------------------------------------------------------------------------
    def start3DPrintJob(self, STL_file=None):
        """

        :param STL_file:
        :return:
        """
        startTime = time.time()

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW

        command = 'bin/3DPrintModule/mw3DPrinterSLM.exe'
        abscommand = os.path.abspath(command)

        if STL_file == None:
            absargs = ''
            command_string = abscommand
        else:
            absargs = os.path.abspath(STL_file)
            command_string = abscommand + ' ' + absargs

        output = subprocess.Popen(command_string, startupinfo=startupinfo, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, stdin=subprocess.PIPE).communicate()

        output = output[0].strip()  # filter version number from output

        print output

        stopTime = time.time()
        delta = stopTime - startTime

        print '\n' + bcolors.DARKGREY + 'TS<=:' + str(delta) + ' [sec]' + ' -> ' + STL_file + bcolors.END

        return output

# ----------------------------------------------------------------------------------------------------------------------
def main():
    """Main module admins the additional arguments passed with 3DPrinter.exe

    Here is decided if test stage will be executed or just a single STL file is processed.
    Also all exceptions when passing wrong commands are handled here.
    """

    _MAXTHREADS = 2
    _RELATIVEFOLDERTESTFILES = 'bin\\3DPrintModule\\'
    _H = help.helper()

    print '\n' + bcolors.UNDERLINE + bcolors.BOLD + 'MW 3DPRINTER MULTIOPERATOR ... ' + bcolors.END
    print 'INIT ...' + '\n'

    if len(sys.argv) == 1:  # this is a default case with no passed command
        print bcolors.WARNING + 'No STL passed. Starting with STL file name in config.ini' + bcolors.END
        section_dict = get_section_from_ini('bin\\3DPrintModule\\config.ini', 'MESH')
        TS = TestStage()
        TS.start3DPrintJob(STL_file=section_dict['fileName'])  # not necessary to pass over stl. default is None
    else:
        for i, j in zip(sys.argv, range(len(sys.argv))):

            if sys.argv[i][0] == '-':
                if len(sys.argv[1]) > 1:
                    if sys.argv[1][1:] == 'TS':
                        file_list = os.listdir(_RELATIVEFOLDERTESTFILES)  # get directory list
                        test_file_list = []
                        for i in file_list:
                            if i.find('.stl') != -1:
                                test_file_list.append(i)

                        print '\n' + bcolors.BOLD + 'TESTNG STL SET:' + '-'*60 + '\n' + bcolors.END

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

                    elif sys.argv[1][1:] == 'SF':  # SF for single file [STL]
                        # we passed a storage place to a stl file
                        if len(sys.argv) == 3:
                            if not os.path.isfile(sys.argv[2]):
                                print bcolors.FAIL + 'No such STL file -> "' + str(sys.argv[2]) + '" ... Please proof INPUT' + bcolors.END
                            else:
                                print 'Processing >> ' + sys.argv[2] + '\n'
                                TestStage(sys.argv[2]).start3DPrintJob(sys.argv[2])
                        else:
                            print bcolors.RED + 'Please provide STL file' + bcolors.END

                    else:
                        print bcolors.RED + 'No known command.' + bcolors.END + '\n'
                        _H.print_help()
                else:
                    print bcolors.RED + 'No command.' + bcolors.END + '\n'
                    _H.print_help()
            else:
                print bcolors.RED + 'If you want to pass a command use the - operator with following commandline' \
                      + bcolors.END + '\n'
                _H.print_help()


    print bcolors.DARKGREY +'TS<=:DONE' + bcolors.END
# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()