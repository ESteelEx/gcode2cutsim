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

    # ------------------------------------------------------------------------------------------------------------------
    def set_simulation_precision(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define simulation precision [mm]. Press ESC for automated calculation: ')
        try:
            num = float(num)
        except:
            print 'Simulation set to automatic solution'
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'precision', 'auto')
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'precision', num)
        except:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'precision', 'auto')

