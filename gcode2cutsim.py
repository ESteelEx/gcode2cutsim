#!dev\python
"""
gcode2cutsim parser -> cutsim can read gcode data now.

"""

__author__ = 'mathiasr'
__version__= 1.0

import sys, os, win32con, numpy
import traceback, subprocess
import win32com.shell.shell as shell
# from decimal import *
from CLUtilities import G2CLogging
from MachineConfig import Tools
from CLUtilities import CLFileWriter
from CLUtilities import ExtrusionUtil
from CLUtilities import StrManipulator

# ----------------------------------------------------------------------------------------------------------------------
def main():

    G2CLOG = G2CLogging.G2CLogging() # start logger

    try:
        # initialize classes
        Tool = Tools.Tools() # initialize Tools
        ExUtil = ExtrusionUtil.ExtrusionUtil()
        StrManipulate = StrManipulator.StrManipulator()

        # define constant vars
        MACHINENAME = 'ULTIMAKER2'
        FILDIAMETER = 0.285 # [mm]
        BEDDIM = [230, 250, 20] # Dimensions of Ultimaker 2,
        STOCKDEFINITION = [0.1, 0.1, 0.1, 0.2, 0.2, 0.2] # size of stock

        # get all input parameters from user
        inputParams = sys.argv

        if len(inputParams) == 1:
            import UI.selectFile as fselect
            path, filename = fselect.get_file_list()
            print 'Input file missing. Pass gcode file to process. [gcode2cutsim [GCODE-DATA] [-sim]]'
            print 'opening from selection'
            inputf = path + '\\' + str(filename)[3:-2]
            # sys.argv = '-sim'
            # print inputf
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
        ExtrusionLineOverlap = 0.0 # percent
        LayerWidthMachine = 0.48
        lineLloop = None

        G2CLOG.wlog('INFO', 'Starting parser ...')

        with open(inputf) as fidO:
            # write header
            CLWriter.writeNCCode('STOCK ' + str(STOCKDEFINITION[0]) + ' ' + str(STOCKDEFINITION[1]) + ' ' + str(STOCKDEFINITION[2]) + ' ' + str(STOCKDEFINITION[3]) + ' ' + str(STOCKDEFINITION[4]) + ' ' + str(STOCKDEFINITION[5]) + ' ;')
            CLWriter.writeNCCode('ADDITIVEBOX 0 0 0 ' + str(BEDDIM[0]) + ' ' + str(BEDDIM[1]) + ' ' + str(BEDDIM[2]) + ' ;')
            CLWriter.writeNCCode('MOVE  X 0 Y 0 Z 0 TX 0 TY 0 TZ 1 ROLL 0 ;')
            loopCounter = 0
            for line in fidO:
                loopCounter += 1
                # save line to lineC to keep original
                lineC = line

                # check where g-code actually starts
                if line[0] == 'G':
                    startParsing = True
                else:
                    startParsing = False

                if line[0] == ';': # cancel/go back to loop if line is commented
                    continue

                # check if layer thickness changed during z-level change
                pos = line.find('Z')
                if pos != -1:
                    # TODO automatic detection of white space
                    zValForerun = float(line[pos+1:pos+8]) # get z value
                    LayerThicknessForerun = zValForerun - zValMachine
                    if numpy.isclose(LayerThicknessForerun, LayerThickness, 0.05) is False:
                        geometryStr, midpoint, radius = Tool.getGeometry(LayerThickness=LayerThicknessForerun,
                                                                         LayerWidth=LayerWidthMachine,
                                                                         ELOverlap=ExtrusionLineOverlap)
                        print 'tool change'
                        print '-'*10
                        CLWriter.writeNCCode('GENERICTOOL')
                        CLWriter.writeNCCode('ADDING')
                        CLWriter.writeNCCode('CUTTING')
                        CLWriter.writeNCCode(geometryStr)
                        CLWriter.writeNCCode('NONCUTTING')
                        CLWriter.writeNCCode('line ps 0.6 0 pe 3 3 ;')
                        LayerThickness = LayerThicknessForerun
                    zValMachine = zValForerun

                # get geometry of extrusion lines and layers before proceeding with tool etc.
                if line[0:2] == 'G1' and line[0:3].find(' ') != -1: # to intercept G commands over 10
                    if lineLloop is not None and LayerThicknessForerun != 0:
                        x, LayerWidth, extrusionLength = ExUtil.getExtrusionParams(line, lineLloop, LayerThicknessForerun) # calc extrusion length
                        LayerWidthMachine = x/2
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
                        if len(line) > 5: # feedrate move
                            NCLine = 'CUT ' + line + ' TX 0 TY 0 TZ 1 ROLL 0 ;'
                            CLWriter.writeNCCode(NCLine)
                    elif lineC[0:2] == 'G0': # rapid move
                        if len(line) > 5:
                            NCLine = 'MOVE ' + line + ' TX 0 TY 0 TZ 1 ROLL 0 ;'
                            CLWriter.writeNCCode(NCLine)

        CLWriter.closeNCFile()

        print 'Done. CL file written - > ' + outputf

        if len(inputParams) == 3:
            if inputParams[2] == '-sim':
                print 'starting verification'
                # writing configuration (start options) file for verifier
                # TODO create own def to write ini file
                posDir = outputf.rfind('\\')
                posPoint = outputf[posDir+1:].rfind('.')
                iniFileName = outputf[posDir+1:posDir+1+posPoint]
                iniFileName = iniFileName + '.ini'
                iniDirName = outputf[0:posDir+1]
                NCiniFile = iniDirName + iniFileName

                fh = open(NCiniFile, 'w')

                fh.write('nc=' + outputf[posDir+1:] + '\n')
                fh.write('precision=0.05\n')
                fh.write('model=3\n')
                fh.close()

                command = 'bin/Verifier/VerifierApplicationSample.exe'
                params = ' ' + NCiniFile

                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                # abscommand = os.path.abspath(command)
                subprocess.Popen(command + params, startupinfo=startupinfo)

                # shell.ShellExecuteEx(nShow=win32con.SW_SHOWNORMAL, lpFile=abscommand, lpParameters=params)
                shell.ShellExecuteEx(nShow=win32con.SW_SHOWNORMAL, lpFile='notepad', lpParameters=outputf)

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
