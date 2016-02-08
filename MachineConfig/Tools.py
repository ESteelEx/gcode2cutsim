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

    def getGeometrie(self, LayerThickness = 0.2, LayerWidth = 0.48):
        """calculation of tool parameters"""

        getcontext().prec = 2 # set precision for decimal class

        LayerWidth = Decimal(LayerWidth) / 1
        LayerThickness = Decimal(LayerThickness) / 1

        # avoid division b zero
        if LayerWidth < 0:
            LayerWidth = 0

        # fidW.write('GENERICTOOL\nADDING\nCUTTING\n')

        geometry = 'arc pc ' + str(LayerWidth) + ' ' + str(LayerThickness) + ' ra ' + str(Decimal(LayerThickness)/2)
        # geometry = 'arc pc 0.5 0 ' + ' ra 0.48'

        # fidW.write(geometry + ' astart 270 asweep 180\n')
        # fidW.write('NONCUTTING\n')
        # fidW.write('line ps 0.6 0 pe 3 3 ;\n')

        midPoint = (LayerWidth, LayerThickness)
        radius = LayerThickness / 2

        return midPoint, radius,



    def calcExtrusionParams(self):
        pass