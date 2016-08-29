import os, sys


class openSettings():
    def __init__(self, pluginPath, corePath):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.INI_CONFIG = self.corePath + r'\Mesh.ini'

    def open_config_ini(self):
        sys.path.append(self.pluginPath)
        os.system(r"notepad.exe " + self.INI_CONFIG)