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
        self.MACHINENAME = 'ULTIMAKER2'
        self.FILAMENTDIAMETER = 0.285 # [mm] diameter
        self.HOMEPOSITION = [0, 0, 0]
        self.BEDDEFINITION = [220, 220, 200] # Dimensions of Ultimaker 2 print area [mm^3]
        self.ADDITIVEBOX = [0, 0, 0, 10, 10, 10]
        self.STOCKDEFINITION = [5, 5, 5, 5.1, 5.1, 5.1] # size of stock. Is needed for cutsim set up. placeit middle of additive box
        self.STOCKDICEDIM = 0.2

    # ------------------------------------------------------------------------------------------------------------------
    def getBedDimensionStr(self):
        beddimstr = 'ADDITIVEBOX -50 -50 0 '
        for i in self.BEDDEFINITION:
            beddimstr += str(i) + ' '

        beddimstr += ' ;'

        return beddimstr

    # ------------------------------------------------------------------------------------------------------------------
    def getHomePosStr(self):
        homeposstr = 'MOVE  X 0 Y 0 Z 0 TX 0 TY 0 TZ 1 ROLL 0 ;'

        return homeposstr

    # ------------------------------------------------------------------------------------------------------------------
    def getABDimensionStr(self):
        partdimstr = 'ADDITIVEBOX '
        for i in self.ADDITIVEBOX:
            partdimstr += str(i) + ' '

        partdimstr += ' ;'

        return partdimstr

    # ------------------------------------------------------------------------------------------------------------------
    def getStockDimensionStr(self):
        stockdimstr = 'STOCK '
        for i in self.STOCKDEFINITION:
            stockdimstr += str(i) + ' '

        return stockdimstr

    # ------------------------------------------------------------------------------------------------------------------
    def set_stock_position(self):
        X_MID = ((self.ADDITIVEBOX[3] - self.ADDITIVEBOX[0]) / float(2)) + self.ADDITIVEBOX[0]
        Y_MID = ((self.ADDITIVEBOX[4] - self.ADDITIVEBOX[1]) / float(2)) + self.ADDITIVEBOX[1]
        Z_MID = ((self.ADDITIVEBOX[5] - self.ADDITIVEBOX[2]) / float(2)) + self.ADDITIVEBOX[2]

        self.STOCKDEFINITION = [X_MID, Y_MID, 0, X_MID + self.STOCKDICEDIM, Y_MID + self.STOCKDICEDIM, self.STOCKDICEDIM]