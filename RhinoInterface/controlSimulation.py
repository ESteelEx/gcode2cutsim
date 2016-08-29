import os, sys
import rhinoscriptsyntax as rs

class controlSimulation():
    def __init__(self, feature, pluginPath, corePath):
        self.feature = feature  # string defines what to control on 1st Layer. Use as specified in INI file
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.INI_CONFIG = self.corePath + r'\Mesh.ini'

    # ------------------------------------------------------------------------------------------------------------------
    def set_sweep_shape(self, sweepShape='rectangle'):
        sys.path.append(self.pluginPath)
        print self.pluginPath
        print os.getcwd()
        from Utilities import ini_worker
        reload(ini_worker)

        section_params = ini_worker.get_section_from_ini(self.INI_CONFIG, 'SIMULATION')

        for key, value in section_params.iteritems():
            if key == 'sweepShape':
                print 'SIMULATION SWEEP SHAPE SWITCHED TO ' + sweepShape
                ini_worker.write_to_section(self.INI_CONFIG, 'SIMULATION', 'sweepShape', sweepShape)
