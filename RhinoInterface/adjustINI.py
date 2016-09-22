import sys

class adjustINI():
    def __init__(self, pluginPath, corePath):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.configFile = 'Mesh.ini'

    def adjust_abs_folder(self):
        sys.path.append(self.pluginPath)
        from Utilities import ini_worker

        abs_path_file = self.corePath + '\\' + self.configFile

        print abs_path_file

        ini_worker.write_to_section(abs_path_file,
                                    'MESH',
                                    'filename',
                                    self.corePath + '\\' + 'Mesh.stl')

        ini_worker.write_to_section(abs_path_file,
                                    'GCODE',
                                    'filename',
                                    self.corePath + '\\' + 'Mesh.gcode')