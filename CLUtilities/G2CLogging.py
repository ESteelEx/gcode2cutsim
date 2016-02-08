#######################################################################################################################
# MW PPLogging Module
#######################################################################################################################
__author__ = 'Mathias Rohler'
__version__ = '1.0'

import logging
import sys
import os
from datetime import *

#help(logging)

class G2CLogging:
    def __init__(self, LOGDIR = os.getcwd(), MWPP_Version = '0.1'):
        """
        Create an instance of PPLogging
        :param LOGDIR: String of the logging directory e.g. "c:\\temp"
        """
        # intialize logging counters
        self.MWPP_WarningCount = 0
        self.MWPP_ErrorCount = 0
        self.MWPP_InfoCount = 0
        self.MWPP_Version = MWPP_Version

        # Start of logger
        #  open log file if logging folder exists
        if os.path.isdir(LOGDIR):
           self.LOGFILE = LOGDIR + '/MWG2C.log'
           self.lf = open(self.LOGFILE, 'w')
           self.lf.close()
        # register error and print
        else:
           #self.PPResults = {'successful':0, 'error':1, 'warning':2}
           #MB("PP Error: Logging folder does not exist!")
           self.MWPP_ErrorCount += 1
           #print( "PP Error: Logging folder does not exist!" )
           #print("MWPP: fatal error->Logging folder does not exist!" , file=sys.stderr)
           sys.stderr.write("MWPP: fatal error->Logging folder does not exist! \n")

        # setup logger
        logging.basicConfig(filename=self.LOGFILE, level=logging.DEBUG)
        # Add Basic messages to MWPP logger
        self.log = logging.getLogger('MWG2C')
        self.log.info("***** G2C Logger started ***********************************")
        self.log.info("** " + self.MWPP_Version)
        self.log.info("** Logging started @ : " + str(datetime.now()))
        self.log.info("** Log-File : " + self.LOGFILE)
        self.log.info("************************************************************")

    def writeToLog(self,LogText):
        """
        Write Logging text to File
        :param LogText: String to log
        :return: None
        """
        try:
            self.lf = open(self.LOGFILE, 'a')
            self.lf.write(LogText + '\n')
            self.lf.close()
        except:
            print("Error while writing to PP-LOG!")

    def wlog(self,level, logtext):
        """
        Write logging content to file, dependent on type of log
        and log number of logging events per type
        :param level: 'INFO', 'WARNING', 'ERROR'
        :param logtext: String to log
        :return: True (if logging was successful) ; 'False' else
        """
        timeinfo = ' @ : ' + str(datetime.now())
        if level == 'INFO':
            self.log.info(logtext + timeinfo)
            self.MWPP_InfoCount += 1
            return True
        elif level == 'WARNING':
            #self.log.warning('  %s', logtext , exc_info=1)
            self.log.warning(logtext)
            self.MWPP_WarningCount += 1
            return True
        elif level == 'ERROR':
            #self.log.error('  %s', logtext , exc_info=1)
            self.log.error(logtext)
            self.MWPP_ErrorCount += 1
            return True
        else:
           return False

    def closeLogging(self):
        """
        Close MWPP Logging facility
        """
        try:
            now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.log.info("** Logging stopped @ : " + now)
            handlers = self.log.root.handlers[:]
            for handler in handlers:
                handler.close()
                self.log.removeHandler(handler)
            #self.log.shutdown()
            #logging.shutdown()
        except:
            sys.stderr.write("Error while closing MWPP-LOG!\n")
            return False

        return True

    def getLogfileName(self):
        """returns name of the log file"""
        return self.LOGFILE



