#!/usr/bin/env python
# sysTrayIcon.py
# main script

import sys, os, subprocess, threading, time, filecmp

__author__ = 'mathiasr'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[99m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class TestStage(threading.Thread):
    def __init__(self, path='\\bin\\3DPrintModule\\', fileName=''):
        threading.Thread.__init__(self)
        self.path = path
        self.fileName = fileName
        self.WORKINGDIR = os.getcwd() + '\\' + self.path
        self.RELATIVEFODLERTOCOMPARE = 'WORKINGCOPYTESTING\\'

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        try:
            self.start3DPrintJob()
            print 'TS<=: COMPARING ' + bcolors.WARNING
            if os.path.isfile(self.path + self.fileName[:-3] + 'gcode') and  \
                    os.path.isfile(self.WORKINGDIR + self.RELATIVEFODLERTOCOMPARE + self.fileName[:-3] + 'gcode'):

                answer = filecmp.cmp(self.WORKINGDIR + self.RELATIVEFODLERTOCOMPARE + self.fileName[:-3] + 'gcode',
                                     self.path + self.fileName[:-3] + 'gcode')



                if answer:
                    print bcolors.OKGREEN + 'TS<=: NO CHANGES'
                else:
                    print bcolors.WARNING + 'TS<=: CHANGES'

        except:
            pass

        print '' + bcolors.HEADER

        return 0

    # ----------------------------------------------------------------------------------------------------------------------
    def start3DPrintJob(self):
        command = 'bin/3DPrintModule/mw3DPrinter.exe'
        abscommand = os.path.abspath(command)
        startTime = time.time()
        FNULL = open(os.devnull, 'w')
        p = subprocess.Popen(abscommand + ' ' + self.path + self.fileName, stdout=FNULL, stderr=subprocess.STDOUT).wait()

        stopTime = time.time()
        delta = stopTime - startTime
        print 'TS<=: Duration: ' + str(delta) + ' sec' + ' -> ' + self.fileName


# ----------------------------------------------------------------------------------------------------------------------
def main():

    print 'TESTING STAGE INITIALIZING ...  ' + bcolors.HEADER

    _MAXTHREADS = 5
    _RELATIVEFOLDERTESTFILES = 'bin\\3DPrintModule\\'

    if len(sys.argv) == 1:
        print 'no input. EXIT. Starting with config.ini'
        TestStage('').start3DPrintJob()
    else:
        if sys.argv[1] == 'testing':
            file_list = os.listdir(_RELATIVEFOLDERTESTFILES) # get directory list
            j = 0
            test_file_list = []
            for i in file_list:
                if i.find('.stl') != -1:
                    test_file_list.append(i)
                    j += 1

            j = 0
            jj = 0
            print 'TESTNG STL SET:'
            print '-'*60
            j = 0
            for i in test_file_list:
                j += 1
                print '+-> ' + str(j) + ' ' + i
            print '-'*60
            while 1:
                TR = threading.enumerate()
                j = len(TR)
                if j <= _MAXTHREADS:
                    i = test_file_list[jj]
                    print 'TS<=: Starting test ' + str(jj+1) + ' of ' + str(len(test_file_list)) + ' with: ' + i
                    TestStage(path=_RELATIVEFOLDERTESTFILES, fileName=i).start()
                    jj += 1
                    if jj >= len(test_file_list):
                        break

        else:
            if not os.path.isfile(sys.argv[1]):
                print 'no such STL file -> ' + str(sys.argv[1])
            else:
                TestStage(sys.argv[1]).start3DPrintJob()


    print '<ALL THREADS AND TESTING STAGE RUNNING>'



# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()