import sys, os, threading

class runSimulation(threading.Thread):
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
        os.system(self.corePath + r"\gcode2cutsimFDM.exe " +
                  self.corePath + r"\Mesh.gcode " +
                  self.corePath + r"\Mesh.ini")