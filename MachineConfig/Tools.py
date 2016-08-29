#######################################################################################################################
# Define Tools
########################################################################################################################
__author__ = 'Mathias Rohler'
__version__= 1.0

from decimal import *

# ----------------------------------------------------------------------------------------------------------------------
class Tools:
    def __init__(self, configData=None):
        self.CD = configData

    def getGeometry(self, LayerThickness=0.2, LayerWidth=0.48, ELOverlap=0.15):
        """calculation of tool parameters
        :returns
        midpoint: mid point of extrusion line as vector
        radius: radius of extrusion line
        geometrieStr: complete NC string to be used for CL file
        """

        # SLM
        # LayerThickness = 0.03
        # LayerWidth = 0.04
        # ELOverlap = 0
        #
        # Renishaw
        # LayerThickness = 0.1
        # LayerWidth = 0.20
        # ELOverlap = 0.15

        getcontext().prec = 4 # set precision for decimal class

        R = Decimal(LayerThickness) / 2
        x = (Decimal(LayerWidth) - 2 * Decimal(R)) / 2
        xWithOverlap = Decimal(x) + (Decimal(x) * Decimal(ELOverlap))
        RWithOverlap = Decimal(R) + Decimal(R) * Decimal(ELOverlap)

        sim_data = self.CD.get_simulation_data()

        revolve_shape = sim_data['sweepShape']

        if xWithOverlap >= 0:

            if revolve_shape == 'real_extrusion':
                # rectangle with rounded faces.
                geometryStr = 'arc pc ' + str(Decimal(xWithOverlap)) + ' ' + str(Decimal(RWithOverlap)) + ' ra ' + \
                              str(Decimal(RWithOverlap)) + \
                              ' astart 270 asweep 180'

            elif revolve_shape == 'rhomb':
                # rhombus - two lines that mark an arrow
                geometryStr = 'line ps ' + \
                              str(Decimal(xWithOverlap)) + \
                              ' 0 ' + \
                              ' pe ' + \
                              str(Decimal(xWithOverlap) + Decimal(RWithOverlap)) + ' ' + \
                              str(Decimal(RWithOverlap)) + '\n' + \
                              'line ps ' + \
                              str(Decimal(xWithOverlap) + Decimal(RWithOverlap)) + ' ' + \
                              str(Decimal(RWithOverlap)) + \
                              ' pe ' + \
                              str(Decimal(xWithOverlap)) + ' ' + \
                              str(2 * Decimal(RWithOverlap))

            elif revolve_shape == 'rectangle':
                # rectangle - vertical line
                geometryStr = 'line ps ' + \
                              str(Decimal(xWithOverlap) + Decimal(RWithOverlap)) + \
                              ' 0 ' + \
                              ' pe ' + \
                              str(Decimal(xWithOverlap) + Decimal(RWithOverlap)) + ' ' + \
                              str(2 * Decimal(RWithOverlap))

        else:
            geometryStr = None

        midPoint = Decimal(xWithOverlap), Decimal(R)
        radius = Decimal(R)

        return geometryStr, midPoint, radius