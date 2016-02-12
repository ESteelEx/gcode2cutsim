#######################################################################################################################
# MW PPLogging Module
#######################################################################################################################
__author__ = 'Mathias Rohler'
__version__ = '1.0'

from math import pi

class ExtrusionUtil():
    def __init__(self):
        pass

    # ----------------------------------------------------------------------------------------------------------------------
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

    # ----------------------------------------------------------------------------------------------------------------------
    def calcLayerThickness(self, zVal):
        pass

    def getOverlap(self, ExtrusionVolume, LayerWidth):
        overlap = None
        return overlap
