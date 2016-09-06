import os, sys, threading

class openSettings(threading.Thread):
    def __init__(self, pluginPath, corePath, configFile):
        self.pluginPath = pluginPath
        print self.pluginPath
        self.corePath = corePath
        self.INI_CONFIG = self.corePath + configFile
        threading.Thread.__init__(self)

    def run(self):
        self.open_config_ini()

    def open_config_ini(self):
        sys.path.append(self.pluginPath)
        os.system(r"notepad.exe " + self.INI_CONFIG)
