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
    def set_path_distance(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define path distance [mm]: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'pathDistance', num)
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
    def set_support_overhang_angle(self):
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

    # ------------------------------------------------------------------------------------------------------------------
    def set_rotation_angle(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define rotation angle of pattern [deg]: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'angle', num)
        except:
            raise

    # ------------------------------------------------------------------------------------------------------------------
    def set_connection_angle(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define connection angle of pattern [deg]. Set to zero to disable connections: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'maxConnectionAngle', num)
        except:
            raise

    # ------------------------------------------------------------------------------------------------------------------
    def set_support_head_height(self, num=None):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        if num is None:
            num = raw_input('Define head height of support tower [mm]: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'headHeight', num)
        except:
            raise

        return num

    # ------------------------------------------------------------------------------------------------------------------
    def set_support_foot_height(self, num=None):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        if num is None:
            num = raw_input('Define foot height of support tower [mm]: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'footHeight', num)
        except:
            raise

        return num

    # ------------------------------------------------------------------------------------------------------------------
    def set_support_head_area(self, num=None):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        if num is None:
            num = raw_input('Define head connection area of support tower (define one side here) [mm]: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'headWidth', num)
        except:
            raise

        return num

    # ------------------------------------------------------------------------------------------------------------------
    def set_support_foot_area(self, num=None):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        if num is None:
            num = raw_input('Define foot connection area of support tower (define one side here) [mm]: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'footWidth', num)
        except:
            raise

        return num

    # ------------------------------------------------------------------------------------------------------------------
    def set_support_grid(self, num=None):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        if num is None:
            num = raw_input('Define grid square area of support tower (define one side here) [mm]: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'fieldWidth', num)
        except:
            raise

        return num


    # ------------------------------------------------------------------------------------------------------------------
    def set_feed_rate(self, num=None):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        if num is None:
            num = raw_input('Define feed rate [mm\min] > ' + self.feature)
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'feedrate', num)
        except:
            raise

        return num

    # ------------------------------------------------------------------------------------------------------------------
    def set_roof_layers(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define number of solid roof layer: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'solidRoofLayers', num)
        except:
            raise


    # ------------------------------------------------------------------------------------------------------------------
    def set_floor_layers(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define number of solid floor layer: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'solidFloorLayers', num)
        except:
            raise

    # ------------------------------------------------------------------------------------------------------------------
    def set_outer_path_width(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define outer path width: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'outerPathWidth', num)
        except:
            raise

    # ------------------------------------------------------------------------------------------------------------------
    def set_inner_path_width(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define inner path width: ')
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
    def set_global_path_width(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define global path width: ')
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
    def set_min_segment_length(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define min segment length: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'minLength', num)
            print 'DONE'
        except:
            raise

    # ------------------------------------------------------------------------------------------------------------------
    def set_filter_tolerance(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define filter tolerance: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'filterTolerance', num)
            print 'DONE'
        except:
            raise

    # ------------------------------------------------------------------------------------------------------------------
    def set_minimum_sparse_ratio(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Define ratio of sparse to solid: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'minimumSparseRatio', num)
            print 'DONE'
        except:
            raise

    # ------------------------------------------------------------------------------------------------------------------
    def set_connection_sparse_onoff(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker
        reload(ini_worker)

        num = raw_input('Switch connections to on or off: ')
        try:
            num = float(num)
        except:
            print 'This is not a valid number'
            return

        try:
            ini_worker.write_to_section(self.INI_CONFIG, self.feature, 'connectSparse', num)
            print 'DONE'
        except:
            raise
