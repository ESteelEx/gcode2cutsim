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
                line.find('F')
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

    return layerT


# ----------------------------------------------------------------------------------------------------------------------
def defineTool(fidW, LT, LW):

    fidW.write('GENERICTOOL\nADDING\nCUTTING\n')

    geometry = 'arc pc ' + str(LW) + ' ' + str(LT) + ' ra ' + str(LT/2)

    fidW.write(geometry + ' astart 270 asweep 180\n')
    fidW.write('NONCUTTING\n')
    fidW.write('line ps 0.6 0 pe 3 3 ;\n\n')


# ----------------------------------------------------------------------------------------------------------------------
def main():

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

    j = 0
    zVal = float(0.0)
    LT = 0.0
    LWT = 0.095
    with open(inputf) as fidO:
        fidW.write('STOCK -30 -40 -20 28 33 20 ;\n')
        fidW.write('ADDITIVEBOX 0 0 0 300 300 200 ;\n')
        fidW.write('MOVE  X 0.00000000 Y 0.00000000 Z 0.00000000 TX 0.00000000 TY 0.00000000 TZ 1.00000000 ROLL 0.00000000 ;\n')

        for line in fidO:
            j += 1
            lineC = line
            if line[0] == ';':
                continue

            pos = line.find('Z')
            if pos != -1:
                zValT = float(line[pos+1:pos+4])
                LTT = zValT - zVal
                if LTT != LT:
                    defineTool(fidW, LTT, LWT)
                    LT = LTT
                zVal = zValT

            if j >= 4:
                line = line.rstrip('\n')
                line = sepStr(line, 'F')
                line = sepStr(line, 'G')
                line = sepStr(line, 'E')
                line = insertWS(line, 'X')
                line = insertWS(line, 'Y')
                line = insertWS(line, 'Z')
                if lineC[0:2] == 'G1':
                    if len(line) > 5:
                        machSimStr = 'CUT ' + line + ' TX 0.0 TY 0.0 TZ 1.0 ROLL 0 ;\n'
                        fidW.write(machSimStr)
                else:
                    if len(line) > 5:
                        machSimStr = 'MOVE ' + line + ' TX 0.0 TY 0.0 TZ 1.0 ROLL 0 ;\n'
                        fidW.write(machSimStr)

    print 'Done. CL file written to - > ' + outputf

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