#######################################################################################################################
# MW PPLogging Module
#######################################################################################################################
__author__ = 'Mathias Rohler'
__version__ = '1.0'

class ExtrusionUtil():
    def __init__(self):
        pass

    # ----------------------------------------------------------------------------------------------------------------------
    def getExtrusionParams(self, line, lineLloop, LayerThicknessT):

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

        extrusionLength = pow(pow((valX2 - valX1), 2) + pow((valY2 - valY1), 2), 0.5)

        # avoid devision by zero
        if extrusionLength != 0:
            areaExtrusionLine = (abs(valE2-valE1)*2) / extrusionLength
        else:
            areaExtrusionLine = (abs(valE2-valE1)*2)

        x = (areaExtrusionLine / LayerThicknessT) - LayerThicknessT

        LayerWidth = x + LayerThicknessT

        """
        print LW

        print LW + (LW*0.15)

        print '---'
        """

        return x, LayerWidth, extrusionLength