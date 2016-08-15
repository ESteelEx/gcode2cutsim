"""
-_RunPythonScript (
import sys
import MW_printer_global_parameter
import rhinoscriptsyntax as rs
reload(MW_printer_global_parameter)
MWP = MW_printer_global_parameter.MW_printer_paths()
sys.path.append(MWP._ABS_FOLDER_SCRIPTS)
import visibility
reload(visibility)
VI = visibility.visibility(MWP._ABS_FOLDER_PLUGIN, MWP._ABS_FOLDER_CORE)
VI.set_extrusion_lines()
)
"""
import sys
import rhinoscriptsyntax as rs

class visibility:
    def __init__(self, pluginPath, corePath):
        self.pluginPath = pluginPath
        self.corePath = corePath

    # ------------------------------------------------------------------------------------------------------------------
    def set_extrusion_lines(self):
        sys.path.append(self.pluginPath)

        if rs.IsLayerVisible('MW 3D Printer Perimeter'):
            rs.LayerVisible('MW 3D Printer PointCloud', visible=False)
            rs.LayerVisible('MW 3D Printer Perimeter', visible=False)
        else:
            rs.LayerVisible('MW 3D Printer PointCloud', visible=False)
            rs.LayerVisible('MW 3D Printer Perimeter', visible=True)