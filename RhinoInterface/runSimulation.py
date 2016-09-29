import sys, os, threading

class runSimulation(threading.Thread):
    def __init__(self, corePath, pluginPath, silent=False):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.silent = silent
        threading.Thread.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        self.execute()

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self):
        sys.path.append(self.pluginPath)

        if self.silent:
            os.system(self.corePath + r"\gcode2cutsimFDM.exe " +
                      self.corePath + r"\Mesh.gcode " +
                      self.corePath + r"\Mesh.ini " +
                      "-silent")
        else:
            os.system(self.corePath + r"\gcode2cutsimFDM.exe " +
                      self.corePath + r"\Mesh.gcode " +
                      self.corePath + r"\Mesh.ini")