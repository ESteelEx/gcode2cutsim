import sys, os, threading
from subprocess import Popen, PIPE

class runSimulation(threading.Thread):
    def __init__(self, corePath, pluginPath, silent=False, calc=True, simType='verifier'):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.silent = silent
        self.calc = calc
        self.simType = simType
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
            if self.calc:
                command = [self.corePath + r"\gcode2cutsimFDM.exe",
                           self.corePath + r"\Mesh.gcode",
                           self.corePath + r"\Mesh.ini"]

                process = Popen(command, stdout=PIPE, stderr=PIPE, stdin=PIPE)

            else:
                if self.simType == 'verifier':
                    command = [self.corePath + r"\bin\verifier\VerifierApplicationSample.exe",
                               self.corePath + r"\Mesh_SIMULATION.ini"]

                    process = Popen(command, stdout=PIPE, stderr=PIPE, stdin=PIPE)

                elif self.simType == 'machSim':
                    command = self.corePath + r'\gcode2cutsimFDM.exe'
                    params = self.corePath + r'\Mesh.gcode ' + self.corePath + r'\Mesh.ini ' + r'-MachSim'

                    print command
                    print 'Starting MachineSimulation'

                    # process = Popen(command, stdout=PIPE, stderr=PIPE, stdin=PIPE)

                    os.system(command + ' ' + params)


"""
import win32event, win32con, win32process

import win32com.shell.shell as shell
from win32com.shell import shellcon

showCmd = win32con.SW_HIDE  # SW_SHOWNORMAL

procInfo = shell.ShellExecuteEx(nShow=showCmd,
                                fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                                lpVerb='runas',
                                lpFile=exeFolder + executable,
                                lpParameters=params
                                )

procHandle = procInfo['hProcess']
obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
rc = win32process.GetExitCodeProcess(procHandle)
"""
