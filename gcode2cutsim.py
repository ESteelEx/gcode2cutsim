#!dev\python
"""
gcode2cutsim parser -> cutsim can read gcode data now.

"""

import sys, os
import win32com.shell.shell as shell
import win32con

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
def getExtrusionParams(line, lineLloop):

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

    eLength = ((valX2 - valX1)**2 + (valY2 - valY1)**2)**0.5

    lWidth = abs(valE1-valE2) / eLength

    print lWidth

    return None

# ----------------------------------------------------------------------------------------------------------------------
def defineTool(fidW, LT, LW):

    fidW.write('GENERICTOOL\nADDING\nCUTTING\n')

    geometry = 'arc pc ' + str(LW) + ' ' + str(LT) + ' ra ' + str(LT/2)

    fidW.write(geometry + ' astart 270 asweep 180\n')
    fidW.write('NONCUTTING\n')
    fidW.write('line ps 0.6 0 pe 3 3 ;\n')


# ----------------------------------------------------------------------------------------------------------------------
def main():

    # define constant vars
    FILDIAMETER = 0.285 # [mm]

    if len(sys.argv) == 1:
        print 'Input file missing. Pass gcode file to process. [gcode2cutsim [GCODE-DATA] [-sim]]'
        return
    else:
        if not os.path.isfile(sys.argv[1]):
            print 'no such file -> ' + str(sys.argv[1])
            return

    inputf = str(sys.argv[1])
    pointpos = inputf.rfind('.')
    if pointpos != -1:
        outputf = inputf[:pointpos+1] + 'cl'
    else:
        outputf = inputf + 'cl'

    fidW = open(outputf, 'w')

    startParsing = False
    zVal = float(0)
    LT = float(0)
    LWT = 0.095
    lineLloop = None
    with open(inputf) as fidO:
        # write header
        fidW.write('STOCK -30 -40 -20 28 33 20 ;\n')
        fidW.write('ADDITIVEBOX 0 0 0 300 300 200 ;\n')
        fidW.write('MOVE  X 0 Y 0 Z 0 TX 0 TY 0 TZ 1 ROLL 0 ;\n')

        for line in fidO:
            # save line to lineC to keep original
            lineC = line

            # check where g-code actually starts
            if line[0:1] == 'G':
                startParsing = True

            if line[0] == ';': # cancel/go back to loop if line is commented
                continue

            # get geometry of extrusion lines and layers before proceeding with tool etc.
            if line[0:2] == 'G1' and line[0:3].find(' ') != -1:
                if lineLloop is not None:
                    eLength = getExtrusionParams(line, lineLloop) # calc extrusion length
                    lineLloop = line
                else:
                    lineLloop = line


            # check if layer thickness changed during z-level change
            pos = line.find('Z')
            if pos != -1:
                zValT = float(line[pos+1:pos+4])
                LTT = abs(zValT - zVal)
                if LTT != LT:
                    defineTool(fidW, LTT, LWT)
                    LT = LTT
                zVal = zValT


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
                        machSimStr = 'CUT ' + line + ' TX 0 TY 0 TZ 1 ROLL 0 ;\n'
                        fidW.write(machSimStr)
                elif lineC[0:2] == 'G0': # rapid move
                    if len(line) > 5:
                        machSimStr = 'MOVE ' + line + ' TX 0 TY 0 TZ 1 ROLL 0 ;\n'
                        fidW.write(machSimStr)

    print 'Done. CL file written - > ' + outputf

    if len(sys.argv) == 3:
        if sys.argv[2] == '-sim':
            print 'starting verification'
            command = 'daily/VerifierApplicationSample.exe'
            params = outputf
            abscommand = os.path.abspath(command)
            shell.ShellExecuteEx(nShow=win32con.SW_SHOWNORMAL, lpFile=abscommand, lpParameters=params)
            shell.ShellExecuteEx(nShow=win32con.SW_SHOWNORMAL, lpFile='notepad', lpParameters=outputf)

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()