"""
This is what has to be deposited in button instance in Rhino (SKIRT switch example)

-_RunPythonScript (
import sys
import MW_printer_global_parameter
import rhinoscriptsyntax as rs
reload(MW_printer_global_parameter)
MWP = MW_printer_global_parameter.MW_printer_paths()
sys.path.append(MWP._ABS_FOLDER_SCRIPTS)
import control1stLayer
reload(control1stLayer)
CS = control1stLayer.control1stLayer('SKIRT', MWP._ABS_FOLDER_PLUGIN, MWP._ABS_FOLDER_CORE)
CS.switch()
)


-_RunPythonScript (
import sys
import MW_printer_global_parameter
import rhinoscriptsyntax as rs
reload(MW_printer_global_parameter)
MWP = MW_printer_global_parameter.MW_printer_paths()
sys.path.append(MWP._ABS_FOLDER_SCRIPTS)
import control1stLayer
reload(control1stLayer)
CS = control1stLayer.control1stLayer('INFILL', MWP._ABS_FOLDER_PLUGIN, MWP._ABS_FOLDER_CORE)
CS.set_infill(pattern='parallel')
)

"""

import sys
import rhinoscriptsyntax as rs


class controlLayer:
    def __init__(self, feature, pluginPath, corePath):
        self.feature = feature  # string defines what to control on 1st Layer. Use as specified in INI file
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.INI_CONFIG = self.corePath + r'\Mesh.ini'

    # ------------------------------------------------------------------------------------------------------------------
    def switch(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        section_params = ini_worker.get_section_from_ini(self.INI_CONFIG, self.feature)

        for key, value in section_params.iteritems():
            if key == 'create':
                if int(value) == 0:
                    print self.feature + ' SWITCHED TO ON'
                    ini_worker.write_to_section(self.INI_CONFIG,  self.feature, 'create', 1)
                else:
                    print  self.feature + ' SWITCHED TO OFF'
                    ini_worker.write_to_section(self.INI_CONFIG,  self.feature, 'create', 0)

    # ------------------------------------------------------------------------------------------------------------------
    def set_num(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define the number of perimeter: ')
        try:
            num = int(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'perimeterCount', num)
        except:
            raise

    # ------------------------------------------------------------------------------------------------------------------
    def set_path_width(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define path width: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'pathWidth', num)
        except:
            raise

    # ------------------------------------------------------------------------------------------------------------------
    def set_distance(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define the distance to object: ')
        try:
            num = int(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'distance', num)
        except:
            raise

    # ------------------------------------------------------------------------------------------------------------------
    def set_support_angle(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define overhang angle [deg]: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'overhangAngleThreshold', num)
        except:
            raise

    # ------------------------------------------------------------------------------------------------------------------
    def set_infill_pattern(self, pattern='cross'):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        if pattern == 'parallel':
            print 'Infill pattern set to parallel'
            try:
                ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'cross', 0)
            except:
                raise
        elif pattern == 'cross':
            print 'Infill pattern set to cross'
            try:
                ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'cross', 1)
            except:
                raise

    # ------------------------------------------------------------------------------------------------------------------
    def set_slicer_height(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define layer height [mm]: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'layerHeight', num)
        except:
            raise

    # ------------------------------------------------------------------------------------------------------------------
    def set_first_layer_slicer_height(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define first layer height [mm]: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'firstLayerHeight', num)
        except:
            raise