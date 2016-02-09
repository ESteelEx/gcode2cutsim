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
        midpoint: mid point of extrusion line as tuple
        radius: radius of extrusion line
        geometrieStr: complete NC string to be used for CL file
        """

        getcontext().prec = 4 # set precision for decimal class

        R = Decimal(LayerThickness / 2)
        x = Decimal(LayerWidth - 2*R)
        xWithOverlap = Decimal(x + x * (2*ELOverlap))
        RWithOverlap = Decimal(R + R * ELOverlap)

        geometryStr = 'arc pc ' + str(Decimal(xWithOverlap)) + ' ' + str(Decimal(R)) + ' ra ' + str(Decimal(RWithOverlap)) \
                      + ' astart 270 asweep 180'

        midPoint = Decimal(xWithOverlap), Decimal(R)
        radius = Decimal(R)

        return geometryStr, midPoint, radius