import sys, os, threading
from subprocess import Popen, PIPE


class runSimulation():
    def __init__(self, corePath, pluginPath, silent=False, calc=True, simType='verifier'):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.silent = silent
        self.calc = calc
        self.simType = simType
        # threading.Thread.__init__(self)

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
            if self.calc:
                os.system(self.corePath + r"\gcode2cutsimFDM.exe " +
                          self.corePath + r"\Mesh.gcode " +
                          self.corePath + r"\Mesh.ini")
            else:
                if self.simType == 'verifier':
                    os.system(self.corePath + r"\bin\verifier\VerifierApplicationSample.exe " +
                              self.corePath + r"\Mesh_SIMULATION.ini")
                elif self.simType == 'machSim':
                    # os.system(self.corePath + r'\bin\MachSim\mwMachineSimulator_App\mwMachineSimulator.exe')
                    #os.system(self.corePath + r"\gcode2cutsimFDM.exe " +
                    #          self.corePath + r"\Mesh.gcode " +
                    #          self.corePath + r"\Mesh.ini")

                    rel_command = [self.corePath + r"\gcode2cutsimFDM.exe ",
                                   self.corePath + r"\Mesh.gcode ",
                                   self.corePath + r"\Mesh.ini"]

                    process = Popen(rel_command, stdout=PIPE, stderr=PIPE)
