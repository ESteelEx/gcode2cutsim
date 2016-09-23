import sys, os, threading

class runparameterGuard(threading.Thread):
    def __init__(self, corePath, pluginPath):
        self.pluginPath = pluginPath
        self.corePath = corePath
        threading.Thread.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        self.execute()

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self):
        sys.path.append(self.pluginPath)
        os.system(self.corePath + r"\paramGuard.exe")