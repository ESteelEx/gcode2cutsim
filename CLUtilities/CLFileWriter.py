########################################################################################################################
# CL File Writer
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
        self.operationNr = 1
        self.Number = 0
        self.INC = 1

    def initializeCLFileWriter(self, filename):
        """Initialize CL File writer"""
        type(self).__init__(filename)
        return CLFileWriter

    def openCLFile(self):
        """open a new CLFile"""
        try:
            self.fn = open(self.filename, 'w')
            self.fn.write('')
            self.fn.close()
            self.fn = open(self.filename, 'a')
        except:
            self.logger.wlog('ERROR','CLFileWriter: File could not be open for writing ...  Try again...')

    def incrNCLineCounter(self):
        """Increment NC File Line Counter"""
        self.Number = self.Number + self.INC

    def writeNCCodeN(self, NCLine):
        """Write NC code with line numbering"""
        try:
            self.fn.write('N{0} '.format(self.Number) + NCLine + "\n")
            self.incrNCLineCounter()
        except:
            self.logger.wlog('ERROR', 'CLFileWriter.writeNCCodeN: Error while writing NC-code')

    def writeNCCode(self, NCLine):
        """Write NC code line without line numbering"""
        try:
            self.fn.write(NCLine + "\n")
            self.incrNCLineCounter()
        except:
            self.logger.wlog('ERROR', 'CLFileWriter.writeNCCode: Error while writing NC-code')

    def writeToolChange(self, geometryStr, NC_Style='CL'):
        """Write new tool geometry to CL file"""
        if NC_Style == 'CL':
            self.writeNCCode('GENERICTOOL')
            self.writeNCCode('ADDING')
            self.writeNCCode('CUTTING')
            self.writeNCCode(geometryStr)
            self.writeNCCode('NONCUTTING')
            self.writeNCCode('line ps 0.6 0 pe 3 3 ;')
        elif NC_Style == 'MachSim':
            if self.operationNr > 1:
                self.writeNCCode('MW_OP_END')

            self.writeNCCode('MW_OP_START')
            self.writeNCCode('MW_OP_NUMBER ' + str(self.operationNr))
            self.writeNCCode('MW_OP_COMMENT "Dummy op"')
            self.writeNCCode('MW_TOOL_ID 0')  # + str(self.operationNr))
            self.writeNCCode('MW_TOOL_NUMBER 100000')
            self.writeNCCode('MW_TOOL_COMMENT "Dummy tool"')
            self.writeNCCode('MW_TOOL_CUT_PART_DEF ' + geometryStr + ' 0 ' + geometryStr + ' 2')
            self.writeNCCode('MW_TOOL_NON_CUT_PART_DEF 0 0 0 0')
            self.writeNCCode('MW_TOOL_ARB_DEF 0 0 0 0')
            self.writeNCCode('MW_TOOL_HLD_DEF 0 0 0 0')
            self.writeNCCode('MW_TOOL_PROFILE_CHORDAL_TOL ' + geometryStr)
            self.writeNCCode('MW_TOOL_LEN_COMPENSATION 0')
            self.operationNr += 1

    def readNCCodeN(self):
        """Read the NC file"""
        rf = open(self.File, 'r')
        for line in rf.read():
            print(" " + str(line))
        rf.close()

    def closeNCFile(self):
        """Close the NC File"""
        try:
            self.fn.close()
        except:
            self.logger.wlog('ERROR', 'Error while closing CL-file' + self.File)





