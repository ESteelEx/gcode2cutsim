#######################################################################################################################
# Define Tools
########################################################################################################################
__author__ = 'Mathias Rohler'
__version__= 1.0

from decimal import *

# ----------------------------------------------------------------------------------------------------------------------
class Tools:
    def __init__(self):
        pass

    def getGeometry(self, LayerThickness=0.2, LayerWidth=0.48, ELOverlap=0.15):
        """calculation of tool parameters
        :returns
        midpoint: mid point of extrusion line as vector
        radius: radius of extrusion line
        geometrieStr: complete NC string to be used for CL file
        """

        # SLM
        LayerThickness = 0.03
        LayerWidth = 0.04
        ELOverlap = 0

        # Renishaw
        LayerThickness = 0.1
        LayerWidth = 0.20
        ELOverlap = 0.15

        getcontext().prec = 4 # set precision for decimal class

        R = Decimal(LayerThickness) / 2
        x = (Decimal(LayerWidth) - 2 * Decimal(R)) / 2
        xWithOverlap = Decimal(x) + (Decimal(x) * Decimal(ELOverlap))
        RWithOverlap = Decimal(R) + Decimal(R) * Decimal(ELOverlap)

        if xWithOverlap >= 0:
            geometryStr = 'arc pc ' + str(Decimal(xWithOverlap)) + ' ' + str(Decimal(RWithOverlap)) + ' ra ' + \
                          str(Decimal(RWithOverlap)) + \
                          ' astart 270 asweep 180'
        else:
            geometryStr = None

        midPoint = Decimal(xWithOverlap), Decimal(R)
        radius = Decimal(R)

        return geometryStr, midPoint, radius