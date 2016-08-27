import sys, os

class runSimulation():
    def __init__(self, corePath, pluginPath):
        self.pluginPath = pluginPath
        self.corePath = corePath

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self):
        os.system(self.corePath + r"\gcode2cutsimFDM.exe " +
                  self.corePath + r"\Mesh.gcode " +
                  self.corePath + r"\Mesh.ini")