#!dev\python
"""
gcode2cutsim parser -> cutsim can read gcode data now.

"""

__author__ = 'mathiasr'
__version__= 1.0

import sys, os, win32con, numpy
import traceback, subprocess, fileinput
import win32com.shell.shell as shell
# from decimal import *
from CLUtilities import G2CLogging
from MachineConfig import Tools
from MachineConfig import JobSetup
from CLUtilities import CLFileWriter
from CLUtilities import ExtrusionUtil
from CLUtilities import StrManipulator
from CLUtilities import evaluateGCode
from CLUtilities import NCFileReader


def startVerification(CLFile, NCiniFile):
    """starting Verification"""
    command = 'bin/Verifier/VerifierApplicationSample.exe'
    params = ' ' + NCiniFile

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.Popen(command + params, startupinfo=startupinfo)
    shell.ShellExecuteEx(nShow=win32con.SW_SHOWNORMAL, lpFile='notepad', lpParameters=CLFile)

# ----------------------------------------------------------------------------------------------------------------------
def main():

    G2CLOG = G2CLogging.G2CLogging() # start logger

    try:
        # initialize classes
        Tool = Tools.Tools() # initialize Tools
        ExUtil = ExtrusionUtil.ExtrusionUtil()
        StrManipulate = StrManipulator.StrManipulator()
        JobS = JobSetup.JobSetup()
        evalGcode = evaluateGCode.evaluateGcode()
        NCFileR = NCFileReader.NCFileReader()

        # define constant vars
        SIMPRECISION = 0.1 # precision of simulation be careful here because of memory consumption

        # get all input parameters from user
        inputParams = sys.argv

        if len(inputParams) == 1:
            import UI.selectFile as fselect
            print 'Input file missing. Pass gcode file to process. [gcode2cutsim [GCODE-DATA] [-sim]]'
            print 'Opening from selection'

            path, filename = fselect.get_file_list()
            if filename is None:
                G2CLOG.wlog('INFO', 'File selection canceled ... Nothing to process')
                print 'Canceled'
                return

            inputf = path + '\\' + str(filename)[3:-2]
            inputParams += [inputf]
            inputParams += ['-sim']
        else:
            if not os.path.isfile(inputParams[1]):
                print 'no such file -> ' + str(inputParams[1])
                return
            else:
                inputf = str(inputParams[1])

        pointpos = inputf.rfind('.')
        if pointpos != -1:
            outputf = inputf[:pointpos+1] + 'cl'
        else:
            outputf = inputf + 'cl'

        CLWriter = CLFileWriter.CLFileWriter(outputf) # start CL File writer
        # open and create CL file
        CLWriter.openCLFile()

        startParsing = False
        zValMachine = 0
        LayerThickness = 0
        ExtrusionLineOverlap = 0.15 # percent
        LayerWidthMachine = 0.48
        lineLloop = None

        G2CLOG.wlog('INFO', 'Starting G2C conversion ...')

        # open NC file reader and get a block of code
        flNC = open(inputf, 'r')
        NCBlock = NCFileR.getNCBlock(flNC, blocklength=5) # get NC block code
        flNC.close()

        # get initial layer width. To calculate initial LW we need a few lines o code.
        # At least 2 consecutive G1 moves with extrusion value.
        LayerWidthMachine = ExUtil.getInitialLayerWidth(NCBlock)

        # write header
        stockDimStr = JobS.getStockDimensionStr()
        homePosStr = JobS.getHomePosStr()

        CLWriter.writeNCCode(stockDimStr)
        CLWriter.writeNCCode('ADDITIVEBOX') # place holder. We replace this line with calculated part dimensions. We know them after every line from G-Code is procecssed. We use this line to find the right line to replace
        CLWriter.writeNCCode(homePosStr)

        with open(inputf) as fidO:

            # start reading g-Code file
            # -----
            loopCounter = 0
            for line in fidO:
                loopCounter += 1
                # save line to lineC -> keeps original
                lineC = line

                # check where g-code actually starts and give green light to parsing functions True/False
                if line[0] == 'G':
                    startParsing = True
                else:
                    startParsing = False

                if line[0] == ';': # cancel/go back to loop if line is commented
                    continue

                # check if layer thickness changed during z-level change
                pos = line.find('Z')
                if pos != -1:
                    zValForerun = float(line[pos+1:pos+8]) # get z value # TODO automatic detection of white space i line string
                    LayerThicknessForerun = zValForerun - zValMachine
                    if numpy.isclose(LayerThicknessForerun, LayerThickness, 0.05) is False:
                        geometryStr, midpoint, radius = Tool.getGeometry(LayerThickness=LayerThicknessForerun,
                                                                         LayerWidth=LayerWidthMachine,
                                                                         ELOverlap=ExtrusionLineOverlap)
                        CLWriter.writeToolChange(geometryStr)
                        LayerThickness = 0.48 # LayerThicknessForerun
                    zValMachine = zValForerun

                # get geometry of extrusion lines and layers before proceeding with tool etc.
                if line[0:2] == 'G1' and line[0:3].find(' ') != -1: # find white space to intercept G commands over 10
                    if lineLloop is not None and LayerThicknessForerun != 0:
                        x, LayerWidth, extrusionLength = ExUtil.getExtrusionParams(line, lineLloop, LayerThicknessForerun) # calc extrusion length

                        if numpy.isclose(LayerWidthMachine, LayerWidth, 0.1) is False:
                            geometryStr, midpoint, radius = Tool.getGeometry(LayerThickness=LayerThicknessForerun,
                                                                             LayerWidth=LayerWidth,
                                                                             ELOverlap=ExtrusionLineOverlap)
                            if geometryStr is not None:
                                pass
                                # CLWriter.writeToolChange(geometryStr)

                        LayerWidthMachine = 0.48 #LayerWidth
                        lineLloop = line
                    else:
                        lineLloop = line

                # write g-code to cutsim format
                if startParsing == True:
                    line = line.rstrip('\n') # remove next line chars
                    line = StrManipulate.sepStr(line, 'F')
                    line = StrManipulate.sepStr(line, 'G')
                    line = StrManipulate.sepStr(line, 'E')
                    line = StrManipulate.insertWS(line, 'X')
                    line = StrManipulate.insertWS(line, 'Y')
                    line = StrManipulate.insertWS(line, 'Z')
                    if lineC[0:2] == 'G1':
                        CLWriter.writeNCCode('CUT ' + line + ' TX 0 TY 0 TZ 1 ROLL 0 ;')
                        evalGcode.saveAxValLimits('X', lineC)
                        evalGcode.saveAxValLimits('Y', lineC)

                    elif lineC[0:2] == 'G0': # rapid move
                        CLWriter.writeNCCode('MOVE ' + line + ' TX 0 TY 0 TZ 1 ROLL 0 ;')
                        evalGcode.saveAxValLimits('Z', lineC)

        CLWriter.closeNCFile() # close CL writer and close CL file

        AdditiveBoxDim = evalGcode.getSavedAxLimits()
        partDimStr = JobS.getPartDimensionStr(PARTDEFINITION=[AdditiveBoxDim[0]['X'], AdditiveBoxDim[0]['Y'],
                                                              AdditiveBoxDim[0]['Z'], AdditiveBoxDim[1]['X'],
                                                              AdditiveBoxDim[1]['Y'], AdditiveBoxDim[1]['Z']])

        for line in fileinput.input(outputf, inplace = 1):
            print line.replace("ADDITIVEBOX", partDimStr),

        print 'Done. CL file written - > ' + outputf

        if len(inputParams) == 3:
            if inputParams[2] == '-sim':
                print 'Starting verification'
                # writing configuration (start options) file for verifier
                # TODO create own def to write ini file

                # CLUtilities.INIFileWriter()

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

                startVerification(outputf, NCiniFile)

        G2CLOG.wlog('INFO', 'All jobs done ...')

    except Exception as e:
        message = traceback.format_exc().splitlines() # get last error and prepare to write it in logger
        for i in message:
            G2CLOG.wlog('ERROR', str(i))

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    G2CLOG = G2CLogging.G2CLogging()
    main()
    # G2CLOG.writeToLog('hehe')
    G2CLOG.closeLogging()

    # open log file
    params = 'MWG2C.log'
    shell.ShellExecuteEx(nShow=win32con.SW_SHOWNORMAL, lpFile='notepad', lpParameters=params)