########################################################################################################################
# Evaluate G-Code
########################################################################################################################
__author__ = 'Mathias Rohler'
__version__= 1.0

from CLUtilities import G2CLogging

class evaluateGcode:
    def __init__(self):
        # initialize axes dict
        self.G2CLOG = G2CLogging.G2CLogging()
        self.G2CLOG.wlog('INFO', 'G-Code Evaluation started')
        self.minAxVal = {}
        self.maxAxVal = {}

    def saveAxValLimits(self, axToSave, NCline):
        pos = NCline.find(axToSave)
        if pos != -1: # only proceed if axToSave str was found in NCline
            posValueEnd = NCline[pos:].find(' ')
            if posValueEnd != -1:
                axValue = NCline[pos+1:posValueEnd + pos]
            else:
                axValue = NCline[pos+1:]

            try:
                axValue = float(axValue)
            except:
                self.G2CLOG.wlog('WARNING', 'String to float conversion failed')
                return False

            self.proofKeyEntry(axToSave) # proof if axe was already stored in dict

            if axValue > self.maxAxVal[axToSave]:
                self.maxAxVal[axToSave] = axValue

            if axValue < self.minAxVal[axToSave]:
                self.minAxVal[axToSave] = axValue

    def getSavedAxLimits(self):
        self.G2CLOG.wlog('INFO', 'Additivebox calculated')
        return self.minAxVal, self.maxAxVal

    def proofKeyEntry(self, axToSave):
        if axToSave not in self.maxAxVal:
            self.maxAxVal[axToSave] = 0

        if axToSave not in self.minAxVal:
            # value is random set. Needs to be a value that will never be reached by machine
            self.minAxVal[axToSave] = 100000