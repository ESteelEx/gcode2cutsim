#!dev\python
"""
This is the job setup. Where to place the part, machine limits etc.
"""

__author__ = 'mathiasr'
__version__= 1.0

# ######################################################################################################################
class JobSetup:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        # TODO py for machine configuration read out (XML)
        self.MACHINENAME = 'ULTIMAKER2'
        self.FILAMENTDIAMETER = 0.285 # [mm] diameter
        self.HOMEPOSITION = [0, 0, 0]
        self.BEDDEFINITION = [230, 250, 200] # Dimensions of Ultimaker 2 print area [mm^3]
        self.STOCKDEFINITION = [0.1, 0.1, 0.1, 0.2, 0.2, 0.2] # size of stock. Is needed for cutsim set up.

    # ------------------------------------------------------------------------------------------------------------------
    def getStockDimensionStr(self):

        stockdimstr = 'STOCK '
        for i in self.STOCKDEFINITION:
            stockdimstr += str(i) + ' '

        return stockdimstr

    # ------------------------------------------------------------------------------------------------------------------
    def getBedDimensionStr(self):

        beddimstr = 'ADDITIVEBOX 0 0 0 '
        for i in self.BEDDEFINITION:
            beddimstr += str(i) + ' '

        beddimstr += ' ;'

        return beddimstr

    # ------------------------------------------------------------------------------------------------------------------
    def getHomePosStr(self):
        homeposstr = 'MOVE  X 0 Y 0 Z 0 TX 0 TY 0 TZ 1 ROLL 0 ;'

        return homeposstr
