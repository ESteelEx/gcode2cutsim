########################################################################################################################
# INI File Writer
########################################################################################################################
__author__ = 'Mathias Rohler'
__version__= 1.0

import logging
import G2CLogging

class CLFileWriter:
    def __init__(self, filename='clfile.cl'):
        self.filename = filename
        # self.logger = logging.getLogger('MWG2C')
        self.logger = G2CLogging.G2CLogging()
        self.Number = 0
        self.INC = 1