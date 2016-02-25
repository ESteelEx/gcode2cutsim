#######################################################################################################################
# NC FILE READER
#######################################################################################################################
__author__ = 'Mathias Rohler'
__version__ = '1.0'

class NCFileReader:
    def __init__(self):
        pass

    def getNCBlock(self, NCfileHandler, blocklength=10, rewindHandler=False):
        # get current file position
        filePos = NCfileHandler.tell()
        # NC forerun to get initial layer width
        loopCounter = 0
        NCBlock = []
        for line in NCfileHandler:
            if line[0] == ';' or line[0] != 'G':
                continue
            loopCounter += 1
            NCBlock += [line]
            if loopCounter == blocklength:
                break

        if rewindHandler:
            NCfileHandler.seek(filePos)

        return NCBlock, NCfileHandler