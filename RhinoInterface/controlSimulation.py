import sys

sys.path.append(r'C:\Users\ModuleWoks\Documents\Development\GitRep\gcode2cutsim')

import rhinoscriptsyntax as rs
from Utilities import ini_worker

reload(ini_worker)

class controlSimulation():
    def __init__(self, feature, pluginPath, corePath):
        self.feature = feature  # string defines what to control on 1st Layer. Use as specified in INI file
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.INI_CONFIG = self.corePath + r'\Mesh.ini'

    # ------------------------------------------------------------------------------------------------------------------
    def set_sweep_shape(self, sweepShape='rectangle'):

        section_params = ini_worker.get_section_from_ini(self.INI_CONFIG, 'SIMULATION')

        for key, value in section_params.iteritems():
            if key == 'sweepShape':
                print 'SIMULATION SWEEP SHAPE SWITCHED TO ' + sweepShape
                ini_worker.write_to_section(self.INI_CONFIG, 'SIMULATION', 'sweepShape', sweepShape)
