#!dev\python
"""
gcode2cutsim parses -> cutsim can read gcode data now.

STOCK -30 -40 -20 28 33 20 ;
ADDITIVEBOX 0 0 0 200 200 100 ;

---- This is the geometry of the nozzle with a diameter of 0.4 mm

GENERICTOOL
CUTTING
arc pc 0 0.4 ra 0.2 astart 270 asweep 90
NONCUTTING
line ps 0.4 0 pe 3 6 ;
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
    """inserts a white space after a character"""
    posChar = line.find(char)
    line = line[:posChar+1] + ' ' + line[posChar+1:]
    return line


# ----------------------------------------------------------------------------------------------------------------------
def main():

    if len(sys.argv) == 1:
        print 'no input. EXIT'
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
    with open(inputf) as fidO:
        fidW.write('STOCK -30 -40 -20 28 33 20 ;\n')
        fidW.write('ADDITIVEBOX 0 0 0 300 300 200 ;\n')
        fidW.write('GENERICTOOL\nADDING\nCUTTING\n')
        fidW.write('line ps 0 0 pe 2 2') # arc pc 0 0.4 ra 0.2 astart 270 asweep 90\n')
        fidW.write('NONCUTTING\nline ps 0.4 0 pe 3 6 ;\n')
        fidW.write('MOVE  X 0.00000000 Y -50.34838486 Z 19.21260071 TX 0.00000000 TY 0.1 TZ 0.9 ROLL 0.00000000 ;\n\n')

        for line in fidO:
            j += 1
            lineC = line
            if line[0] == ';':
                continue

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

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()