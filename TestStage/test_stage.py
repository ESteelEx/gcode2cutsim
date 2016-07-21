"""test stage is initialized"""
import threading, subprocess, os, time, filecmp
from Utilities.console import bcolors


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
                print bcolors.RED + 'TS<=:<' + self.fileName[:-3] + '> - was not processed before.\nAdd a how to be process to test stage.' + bcolors.END


        except:
            print 'Something went wrong with: ' + self.fileName


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