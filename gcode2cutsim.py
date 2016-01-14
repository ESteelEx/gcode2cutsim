"""gcode2cutsim is a parser so that cutsim can read gcode data.

STOCK -30 -40 -20 28 33 20 ;
ADDITIVEBOX 0 0 0 200 200 100 ;

---- This is the geometry of the nozzle with a diameter of 0.4 mm

GENERICTOOL
CUTTING
arc pc 0 0.4 ra 0.2 astart 270 asweep 90
NONCUTTING
line ps 0.4 0 pe 3 6 ;"""

__author__ = 'mathiasr'

inputf = 'AachenerDom_15122015.gcode'
outputf = 'out_DOM_AC.nc'

fidW = open(outputf, 'w')

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

def insertWS(line, char):
    """inserts a white space after a character"""
    posChar = line.find(char)
    line = line[:posChar+1] + ' ' + line[posChar+1:]
    return line


########################################################################################################################
j = 0
with open(inputf) as fidO:
    fidW.write('STOCK -30 -40 -20 28 33 20 ;\n')
    fidW.write('ADDITIVEBOX 0 0 0 300 300 100 ;\n')
    fidW.write('GENERICTOOL\nADDING\nCUTTING\narc pc 0 0.4 ra 0.2 astart 270 asweep 90\nNONCUTTING\nline ps 0.4 0 pe 3 6 ;\n')
    fidW.write('MOVE  X 0.00000000 Y -50.34838486 Z 19.21260071 TX 0.00000000 TY 0.1 TZ 0.9 ROLL 0.00000000 ;\n\n')

    for line in fidO:
        j += 1
        if line[0] == ';':
            continue

        if j >= 4:
            if line[0:2] == 'G1':
                line = line.rstrip('\n')
                line = sepStr(line, 'F')
                line = sepStr(line, 'G')
                line = sepStr(line, 'E')
                line = insertWS(line, 'X')
                line = insertWS(line, 'Y')
                line = insertWS(line, 'Z')
                if len(line) > 5:
                    machSimStr = 'CUT ' + line + ' TX 0.0 TY 0.0 TZ 1.0 ROLL 0 ;\n'
                    fidW.write(machSimStr)
            else:
                line = line.rstrip('\n')
                line = sepStr(line, 'F')
                line = sepStr(line, 'G')
                line = sepStr(line, 'E')
                line = insertWS(line, 'X')
                line = insertWS(line, 'Y')
                line = insertWS(line, 'Z')
                if len(line) > 5:
                    machSimStr = 'MOVE ' + line + ' TX 0.0 TY 0.0 TZ 1.0 ROLL 0 ;\n'
                    fidW.write(machSimStr)

