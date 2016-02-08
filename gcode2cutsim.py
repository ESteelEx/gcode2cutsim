#!dev\python
"""
gcode2cutsim parser -> cutsim can read gcode data now.

"""

import sys, os, win32con
import traceback
import win32com.shell.shell as shell
from decimal import *
from CLUtilities import G2CLogging
from MachineConfig import Tools
from CLUtilities import CLFileWriter

__author__ = 'mathiasr'

# ----------------------------------------------------------------------------------------------------------------------
def sepStr(line, char):
    """delete a string from a string. Starting with char and ends with white space"""
    posChar = line.find(char)
    if posChar == -1:
        return line

    if posChar != None:
        for i in range(posChar, len(line)):
            if line[i:i+1] == ' ' or i == len(line)-1:
                # line.find('F')
                line = line[:posChar] + line[i+1:]
                break

    return line

# ----------------------------------------------------------------------------------------------------------------------
def insertWS(line, char):
    """inserts a white space after user given character"""
    posChar = line.find(char)
    line = line[:posChar+1] + ' ' + line[posChar+1:]
    return line

# ----------------------------------------------------------------------------------------------------------------------
def calcLayerThickness(zVal):
    pass

# ----------------------------------------------------------------------------------------------------------------------
def getExtrusionParams(line, lineLloop, LTT):

    # print LTT

    # if LTT >= 1.0:
       # print 'here it changed'
       # print line
       # print lineLloop

    posX1 = line.find('X')
    posX2 = lineLloop.find('X')
    posY1 = line.find('Y')
    posY2 = lineLloop.find('Y')
    posE1 = line.find('E')
    posE2 = lineLloop.find('E')

    valX1 = float(line[posX1+1:line[posX1:].find(' ') + posX1])
    valY1 = float(line[posY1+1:line[posY1:].find(' ') + posY1])
    valE1 = float(line[posE1+1:])
    valX2 = float(lineLloop[posX2+1:lineLloop[posX2:].find(' ') + posX2])
    valY2 = float(lineLloop[posY2+1:lineLloop[posY2:].find(' ') + posY2])
    valE2 = float(lineLloop[posE2+1:])

    eLength = pow(pow((valX2 - valX1), 2) + pow((valY2 - valY1), 2), 0.5)

    # avoid devision by zero
    if eLength != 0:
        areaL = (abs(valE2-valE1)*2) / eLength
    else:
        areaL = (abs(valE2-valE1)*2)

    x = (areaL/LTT) - LTT

    LW = x + LTT

    """
    print LW

    print LW + (LW*0.15)

    print '---'
    """

    return x, LW, eLength


# ----------------------------------------------------------------------------------------------------------------------
def main():

    G2CLOG = G2CLogging.G2CLogging() # start logger


    try:

        Tool = Tools.Tools() # initialize Tools
        # define constant vars
        MACHINENAME = 'ULTIMAKER2'
        FILDIAMETER = 0.285 # [mm]
        BEDDIM = [230, 250, 220] # Dimensions of Ultimaker 2,
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

        # fidW = open(outputf, 'w')

        CLWriter = CLFileWriter.CLFileWriter(outputf) # start CL File writer
        # open and create CL file
        CLWriter.openCLFile()

        startParsing = False
        zVal = float(0)
        LT = float(0)
        LWT = 0.14
        lineLloop = None

        G2CLOG.wlog('INFO', 'Starting parser ...')

        with open(inputf) as fidO:
            # write header

            # fidW.write('STOCK ' + str(STOCKDEFINITION[0]) + ' ' + str(STOCKDEFINITION[1]) + ' ' + str(STOCKDEFINITION[2]) + ' ' + str(STOCKDEFINITION[3]) + ' ' + str(STOCKDEFINITION[4]) + ' ' + str(STOCKDEFINITION[5]) + ' ;\n')
            # fidW.write(ABstr)
            # fidW.write('MOVE  X 0 Y 0 Z 0 TX 0 TY 0 TZ 1 ROLL 0 ;\n')

            CLWriter.writeNCCode('STOCK ' + str(STOCKDEFINITION[0]) + ' ' + str(STOCKDEFINITION[1]) + ' ' + str(STOCKDEFINITION[2]) + ' ' + str(STOCKDEFINITION[3]) + ' ' + str(STOCKDEFINITION[4]) + ' ' + str(STOCKDEFINITION[5]) + ' ;')
            ABstr = 'ADDITIVEBOX 0 0 0 ' + str(BEDDIM[0]) + ' ' + str(BEDDIM[1]) + ' ' + str(BEDDIM[2]) + ' ;'
            CLWriter.writeNCCode(ABstr)
            CLWriter.writeNCCode('MOVE  X 0 Y 0 Z 0 TX 0 TY 0 TZ 1 ROLL 0 ;')

            for line in fidO:
                # save line to lineC to keep original
                lineC = line

                # check where g-code actually starts
                if line[0:1] == 'G':
                    startParsing = True

                if line[0] == ';': # cancel/go back to loop if line is commented
                    continue

                # check if layer thickness changed during z-level change
                pos = line.find('Z')
                if pos != -1:
                    zValT = float(line[pos+1:pos+4])
                    LTT = abs(zValT - zVal)
                    if LTT != LT:
                        Tool.getGeometrie(LayerThickness=LTT, LayerWidth=LWT)
                        LT = LTT
                    zVal = zValT

                # get geometry of extrusion lines and layers before proceeding with tool etc.
                if line[0:2] == 'G1' and line[0:3].find(' ') != -1: # to intercept G commands over 10
                    if lineLloop is not None and LTT != 0:
                        x, LWcomp, eLength = getExtrusionParams(line, lineLloop, LTT) # calc extrusion length
                        LWT = x/2
                        lineLloop = line
                    else:
                        lineLloop = line

                # write g-code to cutsim format
                if startParsing == True:
                    line = line.rstrip('\n') # remove next line chars
                    line = sepStr(line, 'F')
                    line = sepStr(line, 'G')
                    line = sepStr(line, 'E')
                    line = insertWS(line, 'X')
                    line = insertWS(line, 'Y')
                    line = insertWS(line, 'Z')
                    if lineC[0:2] == 'G1':
                        if len(line) > 5: # feedrate move
                            NCLine = 'CUT ' + line + ' TX 0 TY 0 TZ 1 ROLL 0 ;'
                            CLWriter.writeNCCode(NCLine)
                    elif lineC[0:2] == 'G0': # rapid move
                        if len(line) > 5:
                            NCLine = 'MOVE ' + line + ' TX 0 TY 0 TZ 1 ROLL 0 ;'
                            CLWriter.writeNCCode(NCLine)

        print 'Done. CL file written - > ' + outputf

        if len(inputParams) == 3:
            if inputParams[2] == '-sim':
                print 'starting verification'
                command = 'daily/VerifierApplicationSample.exe'
                params = outputf
                abscommand = os.path.abspath(command)
                shell.ShellExecuteEx(nShow=win32con.SW_SHOWNORMAL, lpFile=abscommand, lpParameters=params)
                shell.ShellExecuteEx(nShow=win32con.SW_SHOWNORMAL, lpFile='notepad', lpParameters=outputf)
    except Exception as e:
        top = traceback.extract_stack()[-1]
        errStr = ', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])])
        G2CLOG.wlog('ERROR', ' Error in main program: ' + str(e.message) + ' ' + errStr)

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    G2CLOG = G2CLogging.G2CLogging()
    main()
    # G2CLOG.writeToLog('hehe')
    G2CLOG.closeLogging()

    # open log file
    params = 'MWG2C.log'
    shell.ShellExecuteEx(nShow=win32con.SW_SHOWNORMAL, lpFile='notepad', lpParameters=params)
