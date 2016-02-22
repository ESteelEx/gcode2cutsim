#######################################################################################################################
# MW PPLogging Module
#######################################################################################################################

from math import pi

__author__ = 'Mathias Rohler'
__version__ = '1.0'

class ExtrusionUtil():
    def __init__(self):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def getCoordinates(self, NCline):
        """extract X,Y,Z,F,E coordinates from NCline when available"""

        posG = NCline.find('G')
        posX = NCline.find('X')
        posY = NCline.find('Y')
        posZ = NCline.find('Z')
        posF = NCline.find('F')
        posE = NCline.find('E')

        if NCline[posG:].find(' ') != -1:
            GMove = NCline[0:NCline[posG:].find(' ')]
        else:
            GMove = None
            return None

        if NCline[posX:].find(' ') != -1:
            valX1 = float(NCline[posX+1:NCline[posX:].find(' ') + posX])
        else:
            valX1 = float(NCline[posX+1:])

        if NCline[posY:].find(' ') != -1:
            valY1 = float(NCline[posY+1:NCline[posY:].find(' ') + posY])
        else:
            valY1 = float(NCline[posY+1:])

        if posZ != -1:
            if NCline[posZ:].find(' ') != -1:
                valZ1 = float(NCline[posZ+1:NCline[posZ:].find(' ') + posZ])
            else:
                valZ1 = float(NCline[posZ+1:NCline[posZ:]])
        else:
            valZ1 = None

        if posF != -1:
            if NCline[posF:].find(' ') != -1:
                valF1 = float(NCline[posF+1:NCline[posF:].find(' ') + posF])
            else:
                valF1 = float(NCline[posF+1:])
        else:
            valF1 = None

        if posE != -1:
            if NCline[posE:].find(' ') != -1:
                valE1 = float(NCline[posE+1:NCline[posE:].find(' ') + posE])
            else:
                valE1 = float(NCline[posE+1:])
        else:
            valE1 = None

        return GMove, valX1, valY1, valZ1, valF1, valE1

    # ------------------------------------------------------------------------------------------------------------------
    def getExtrusionLength(self, XYpairs):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def getMoveLength(self, valX, valY):

        moveLength = pow(pow((valX[1] - valX[0]), 2) + pow((valY[1] - valY[0]), 2), 0.5)

        return moveLength

    # ------------------------------------------------------------------------------------------------------------------
    def getExtrusionParams(self, line, lineLloop, LayerThicknessT):

        """
        calculate all important parameters from gcode input.
            Layer width, thickness, radius from circle elements outside the extrusion line
        line: current NC line from gcode
        lineLloop: gcode NC line from previous loop run
        """

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
            areaExtrusionLine = abs(valE2-valE1) / extrusionLength
        else:
            areaExtrusionLine = abs(valE2-valE1)

        areaExtrusionLineRect = areaExtrusionLine - (pi * ((LayerThicknessT/2)**2))
        x = (areaExtrusionLineRect / LayerThicknessT)
        LayerWidth = x + LayerThicknessT

        return x, LayerWidth, extrusionLength

    # ------------------------------------------------------------------------------------------------------------------
    def calcLayerThickness(self, NCData):
        for i in range(len(NCData)):
            if NCData[i][3] is not None:
                LayerThickness = NCData[i][3]

        return LayerThickness

    # ------------------------------------------------------------------------------------------------------------------
    def getOverlap(self, ExtrusionVolume, LayerWidth):
        overlap = None
        return overlap

    # ------------------------------------------------------------------------------------------------------------------
    def getExtrusionDelta(self, E1, E2):
        if E2 is not None and E1 is not None:
            EDelta = E2 - E1
        else:
            return None

        return EDelta

    # ------------------------------------------------------------------------------------------------------------------
    def getInitialLayerWidth(self, NCBlock, LayerThickness=0.2):
        """get initial Layer width"""
        NCData = []
        arrayMoveLength = []
        arrayEDelta= []
        LayerWidth = 0
        for i in NCBlock:
            # split up NClineand store G,X,Y,Z,F,E data
            NCData.append(self.getCoordinates(i))

        LayerThickness = self.calcLayerThickness(NCData)

        for i in range(1, len(NCData)):
            arrayMoveLength.append(self.getMoveLength([NCData[i-1][1], NCData[i][1]], [NCData[i-1][2], NCData[i][2]]))
            arrayEDelta.append(self.getExtrusionDelta(NCData[i-1][5], NCData[i][5]))

        # calculate extrusion width
        numCalc = 0
        for i in range(len(arrayMoveLength)):
            if arrayEDelta[i] is not None:
                numCalc += 1
                areaExtrusionLine = arrayEDelta[i] / arrayMoveLength[i]
                areaExtrusionLineRect = areaExtrusionLine - (pi * ((LayerThickness/2)**2))
                x = (areaExtrusionLineRect / LayerThickness)
                LayerWidth += x + LayerThickness

        initialLayerWidth = LayerWidth / numCalc
        print initialLayerWidth

        return initialLayerWidth
