import os, sys

class openSettings():
    def __init__(self, pluginPath, corePath, configFile):
        self.pluginPath = pluginPath
        print self.pluginPath
        self.corePath = corePath
        self.INI_CONFIG = self.corePath + configFile

    def open_config_ini(self):
        sys.path.append(self.pluginPath)



        os.system(r"notepad.exe " + self.INI_CONFIG)