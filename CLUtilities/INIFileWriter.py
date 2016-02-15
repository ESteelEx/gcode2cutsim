########################################################################################################################
# INI File Writer
########################################################################################################################
__author__ = 'Mathias Rohler'
__version__= 1.0

import logging
import G2CLogging

class CLFileWriter:
    def __init__(self, filename='clfile.cl'):
        self.filename = filename
        # self.logger = logging.getLogger('MWG2C')
        self.logger = G2CLogging.G2CLogging()
        self.Number = 0
        self.INC = 1

        posDir = outputf.rfind('\\')
        posPoint = outputf[posDir+1:].rfind('.')
        iniFileName = outputf[posDir+1:posDir+1+posPoint]
        iniFileName = iniFileName + '.ini'
        iniDirName = outputf[0:posDir+1]
        NCiniFile = iniDirName + iniFileName

        fh = open(NCiniFile, 'w')

        fh.write('nc=' + outputf[posDir+1:] + '\n')
        fh.write('precision=' + str(SIMPRECISION) + '\n')
        fh.write('model=3\n')
        fh.close()