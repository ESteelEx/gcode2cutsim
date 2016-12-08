#!dev\python
"""
G-Code parser -> Cutsim and MachSim can read gcode data now.

"""

__author__ = 'mathiasr'
__version__= 2.0

import sys, os, win32con, numpy, warnings, wx, copy
import traceback, subprocess, fileinput
import win32com.shell.shell as shell
from subprocess import Popen, PIPE

# from decimal import *
from CLUtilities import G2CLogging
from MachineConfig import Tools
from MachineConfig import JobSetup
from CLUtilities import CLFileWriter
from CLUtilities import ExtrusionUtil
from CLUtilities import StrManipulator
from CLUtilities import evaluateGCode
from CLUtilities import NCFileReader
from CLUtilities import configData
from Utilities import ini_worker
from Utilities import compare

# warnings.filterwarnings("ignore")

# ----------------------------------------------------------------------------------------------------------------------
def startVerification(CLFile, NCiniFile, WD, simType='Verifier'):
    """starting Verification"""

    command = []
    params = ''
    print 'Working directory: ' + WD
    if WD == '':
        if simType == 'MachSim':
            command.append(r'\bin\MachSim\mwMachineSimulator_App\mwMachineSimulator.exe')
            command.append(r'C:\MW3DPrinting\bin\MachSim\mwMachineSimulator_App\mwMachineSimulator.exe')
        else:
            command.append(r'\bin\Verifier\VerifierApplicationSample.exe')
            command.append(r'C:\MW3DPrinting\bin\Verifier\VerifierApplicationSample.exe ')
            params = copy.deepcopy(NCiniFile)
    else:
        if simType == 'MachSim':
            command.append(WD + r'\bin\MachSim\mwMachineSimulator_App\mwMachineSimulator.exe')
        else:
            command.append(WD + r'\bin\Verifier\VerifierApplicationSample.exe')
            params = copy.deepcopy(NCiniFile)

    # starting
    for com in command:
        if os.path.isfile(com):
            try:
                if simType == 'Verifier':
                    process = Popen([com, params], stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
                else:
                    process = Popen(com, stdout=PIPE, stderr=PIPE, stdin=PIPE, shell=True)
                break
            except:
                pass

# ----------------------------------------------------------------------------------------------------------------------
def getSimulationPrecision(fileName):

    sim_params = ini_worker.get_section_from_ini(fileName, 'SIMULATION')

    return sim_params['precision']

# ----------------------------------------------------------------------------------------------------------------------
def main():
    """
    gcode2cutsim needs to be compiled to exe
    :return: Nothing
    """

    G2CLOG = G2CLogging.G2CLogging() # start logger

    try:
        # initialize classes
        WD = ''
        Tool = Tools.Tools() # initialize Tools
        ExUtil = ExtrusionUtil.ExtrusionUtil()
        StrManipulate = StrManipulator.StrManipulator()
        JobS = JobSetup.JobSetup()
        evalGcode = evaluateGCode.evaluateGcode()
        NCFileR = NCFileReader.NCFileReader()
        # define constant vars
        SIMPRECISION = 0.2 # default precision of simulation. precision is increased when layer thickness is smaller
        # TODO define number of layer by a layer interval -> slider
        SLIDERPOSITION_START = 25  # percentage
        SLIDERPOSITION_END = 33  # percentage
        silent_process = False

        # get all input parameters from user
        inputParams = sys.argv

        if len(inputParams) == 1:
            import UI.selectFile as fselect
            print 'Input file missing. Pass gcode file to process. [gcode2cutsim [GCODE-DATA] [-sim]]'
            print 'Opening from selection'

            path, filename = fselect.get_file_list()
            if filename is None:
                G2CLOG.wlog('INFO', 'File selection canceled ... Nothing to process')
                print 'Canceled'
                return

            inputf = path + '\\' + str(filename)[3:-2]
            inputParams += [inputf]
            inputParams += ['-sim']
        elif len(inputParams) >= 2:
            if not os.path.isfile(inputParams[1]):
                print 'no such file -> ' + str(inputParams[1])
                return
            else:
                inputf = str(inputParams[1])

            if len(inputParams) >= 3:
                if not os.path.isfile(inputParams[2]):
                    print 'no config file -> ' + str(inputParams[1])
                    return
                else:
                    CD = configData.configData(inputParams[2])

                    # get working directory when Mesh.ini was passed via command line
                    splittedStr = inputParams[2].split('\\')[:-1]
                    for item in splittedStr:
                        WD = WD + item + '\\'

                    Tool = Tools.Tools(configData=CD)  # initialize Tools
                    # read simulation precision
                    SIMPRECISION = getSimulationPrecision(inputParams[2])

                if len(inputParams) == 4:
                    if inputParams[3][1:].strip() == 'silent':
                        silent_process = True
                        print 'Silent parsing'
                    else:
                        inputParams += ['-sim']
                else:
                    inputParams += ['-sim']

        pointpos = inputf.rfind('.')
        if pointpos != -1:
            outputf = inputf[:pointpos+1] + 'cl'
            outputfMS = inputf[:pointpos+1] + 'sim'
        else:
            outputf = inputf + 'cl'
            outputfMS = inputf + 'sim'

        if compare.sim_files(inputf, outputf) or compare.sim_files(inputf, outputfMS):

            CLWriter = CLFileWriter.CLFileWriter(outputf) # start CL File writer
            CLMSWriter = CLFileWriter.CLFileWriter(outputfMS)
            # open and create CL file
            CLWriter.openCLFile()
            CLMSWriter.openCLFile()

            # initialize const
            # ------------------------------------------------------------------------------------------------------------
            startParsing = False
            zValMachine = 0
            LayerThickness = 0
            # EXTRUSIONLINEOVERLAP = 0 # [mm]
            ExtrusionLineOverlap = 0 # percent
            # EXTENDADDITIVEBOX = 1 # [mm]
            extendAdditiveBox = 1 # [mm]
            lineLloop = None
            # ------------------------------------------------------------------------------------------------------------

            G2CLOG.wlog('INFO', 'Starting G2C conversion ...')

            # open NC file reader and get a block of code
            flNC = open(inputf, 'r') # read only
            NCBlock, flNC = NCFileR.getNCBlock(flNC, blocklength=15) # get NC block code
            flNC.close()

            # get initial layer width. To calculate initial LW we need a few lines of code.
            # At least 2 consecutive G1 moves with extrusion value.
            LayerWidthMachine = ExUtil.getInitialLayerWidth(NCBlock)
            currentExtrusionVal = ExUtil.getInitialExtrusionVal(NCBlock)

            # write header
            # stockDimStr = JobS.getStockDimensionStr()
            homePosStr = JobS.getHomePosStr()

            # CLWriter.writeNCCode(stockDimStr)
            CLWriter.writeNCCode('STOCK')
            CLWriter.writeNCCode('ADDITIVEBOX') # place holder. We replace this line with calculated part dimensions.
                                                # We know them after every line from G-Code is procecssed.
                                                # We use this line to find the right line to replace
            CLWriter.writeNCCode(homePosStr)


            # write information in MachSim File
            CLMSWriter.writeNCCode('MW_UNITS_METRIC 1')

            if not silent_process:

                app = wx.App(False)

                pulse_dlg = wx.ProgressDialog(title="G2C Converting ...",
                                              message="Initializing ...",
                                              maximum=int(101),
                                              style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)

            num_lines = sum(1 for line in open(inputf))

            # line_start

            next_update_block = 0
            keepGoin = 1
            with open(inputf) as fidO:

                # start reading g-Code file
                # -----
                loopCounter = 0
                for line in fidO:
                    loopCounter += 1
                    # save line to lineC -> keeps original
                    lineC = line

                    perc = round((loopCounter / float(num_lines) * 100))
                    if  perc > next_update_block:
                        next_update_block += 0.1

                        if not silent_process:
                            updmessage = 'Line ' + str(loopCounter) + ' of ' + str(num_lines) + ' - ' + str(perc) + '%'

                            (keepGoin, skip) = pulse_dlg.Update(perc, updmessage)
                            if not keepGoin:
                                G2CLOG.wlog('INFO', 'User canceled at line: ' + str(loopCounter) + ' - ' + str(perc) + '%')
                                existent = 2
                                break
                        #else:
                        #    print str(perc) + ' [%]'

                    # check where g-code actually starts and give green light to parsing functions True/False
                    if line[0] == 'G':
                        startParsing = True
                    else:
                        startParsing = False

                    if line[0] == ';': # cancel/go back to loop if line is commented
                        continue

                    # zLevelChange = evalGcode.proofZlevelChange(line) # True or False

                    # check if layer thickness changed during z-level change
                    pos = line.find('Z')
                    if pos != -1:
                        posShifter = 8
                        while 1:
                            try:
                                zValForerun = float(line[pos+1:pos+posShifter]) # get z value # TODO automatic detection of white space in line string
                                break
                            except:
                                posShifter -= 1

                        LayerThicknessForerun = zValForerun - zValMachine
                        if numpy.isclose(LayerThicknessForerun, LayerThickness, 0.05) is False:  # check if in tolerance after subtraction
                            geometryStr, midpoint, radius, width = Tool.getGeometry(LayerThickness=LayerThicknessForerun,
                                                                             LayerWidth=LayerWidthMachine,
                                                                             ELOverlap=ExtrusionLineOverlap)

                            CLWriter.writeToolChange(geometryStr)
                            CLMSWriter.writeToolChange(str(width), NC_Style='MachSim')
                            CLMSWriter.writeNCCode('MW_MACHMOVE RAPID Z' + str(zValMachine))

                            LayerThickness = LayerThicknessForerun
                            if LayerThickness < SIMPRECISION:
                                SIMPRECISION = LayerThickness
                        zValMachine = zValForerun
                        CLMSWriter.Z_level = zValMachine
                        CLWriter.Z_level = zValMachine
                        CLWriter.layerNr += 1
                        CLMSWriter.layerNr += 1
                        CLMSWriter.path_area_index = 0

                    # get geometry of extrusion lines and layers before proceeding with tool etc.
                    if line[0:2] == 'G1' and line[0:3].find(' ') != -1: # find white space to intercept G commands over and equal 10
                        if lineLloop is not None and LayerThicknessForerun != 0:
                            # x, LayerWidth, extrusionLength = ExUtil.getExtrusionParams(line, lineLloop, LayerThicknessForerun) # calc extrusion length

                            # get current positions and extrusion values
                            forerunMachinePos = ExUtil.getCoordinates(line)
                            if forerunMachinePos is not None:
                                forerunMachinePos = (forerunMachinePos[1], forerunMachinePos[2])

                            forerunExtrusionVal = ExUtil.getExtrusionVal(line)
                            LayerWidth = ExUtil.getLayerWidth(currentMachinePos, forerunMachinePos, currentExtrusionVal,
                                                              forerunExtrusionVal, LayerThicknessForerun)

                            if numpy.isclose(LayerWidthMachine, LayerWidth, 0.05) is False:  # check if in tolerance after subtraction
                                geometryStr, midpoint, radius, width = Tool.getGeometry(LayerThickness=LayerThicknessForerun,
                                                                                 LayerWidth=LayerWidth,
                                                                                 ELOverlap=ExtrusionLineOverlap)
                                if geometryStr is not None:
                                    if float(geometryStr.split(' ')[2]) >= 1:
                                        # LayerThickness = 0.2, LayerWidth = 0.48, ELOverlap = 0.15
                                        print '---'
                                        print geometryStr

                                    CLWriter.writeToolChange(geometryStr)
                                    CLMSWriter.writeToolChange(str(width), NC_Style='MachSim')
                                    CLMSWriter.writeNCCode('MW_MACHMOVE FEED X' + str(currentMachinePos[0]) + ' Y' + str(currentMachinePos[1]) + ' Z' + str(zValMachine))

                            LayerWidthMachine = LayerWidth
                            lineLloop = line
                            currentExtrusionVal = ExUtil.getExtrusionVal(line)
                        else:
                            lineLloop = line

                    if line[0:3] == "G1 " or line[0:3] == 'G0 ':
                        # get current machine position from NC line
                        currentMachinePos = ExUtil.getCoordinates(line)
                        if currentMachinePos is not None:
                            currentMachinePos = (currentMachinePos[1], currentMachinePos[2]) # X,Y

                    # write g-code to cutsim format
                    if startParsing == True:
                        line = line.rstrip('\n') # remove next line chars
                        line = StrManipulate.sepStr(line, 'G')
                        line = StrManipulate.sepStr(line, 'E')
                        lineMS = copy.deepcopy(line)
                        lineMS = StrManipulate.vartype(line, 'F', 'int')
                        line = StrManipulate.sepStr(line, 'F')
                        line = StrManipulate.insertWS(line, 'X')
                        line = StrManipulate.insertWS(line, 'Y')
                        line = StrManipulate.insertWS(line, 'Z')

                        if lineC[0:3] == 'G1 ':
                            if line.find('G') == -1:
                                CLWriter.writeNCCode('CUT ' + line + ' TX 0 TY 0 TZ 1 ROLL 0 ;')
                                CLMSWriter.writeNCCode('MW_MACHMOVE FEED ' + lineMS)
                                evalGcode.saveAxValLimits('X', lineC)
                                evalGcode.saveAxValLimits('Y', lineC)

                        elif lineC[0:3] == 'G0 ': # rapid move
                            CLWriter.writeNCCode('MOVE ' + line + ' TX 0 TY 0 TZ 1 ROLL 0 ;')
                            CLMSWriter.writeNCCode('MW_MACHMOVE RAPID ' + lineMS)
                            evalGcode.saveAxValLimits('Z', lineC)

            CLWriter.closeNCFile() # close CL writer and close CL file
            CLMSWriter.writeNCCode('MW_OP_END')
            CLMSWriter.closeNCFile()

            AdditiveBoxDim = evalGcode.getSavedAxLimits()

            ADDITIVEBOX = [AdditiveBoxDim[0]['X'] - extendAdditiveBox, AdditiveBoxDim[0]['Y'] - extendAdditiveBox,
                              AdditiveBoxDim[0]['Z'] - extendAdditiveBox, AdditiveBoxDim[1]['X'] + extendAdditiveBox,
                              AdditiveBoxDim[1]['Y'] + extendAdditiveBox, AdditiveBoxDim[1]['Z'] + extendAdditiveBox]

            JobS.ADDITIVEBOX = ADDITIVEBOX

            partDimStr = JobS.getABDimensionStr()

            for line in fileinput.input(outputf, inplace=1):
                print line.replace("ADDITIVEBOX", partDimStr),

            # find position of stock model
            JobS.set_stock_position()

            for line in fileinput.input(outputf, inplace=1):

                stockDimStr = JobS.getStockDimensionStr()
                print line.replace("STOCK", stockDimStr),

            print 'Done. CL file written - > ' + outputf

        # gcode2cutsimFDM D:\MW3DPrinting_MachSim\Mesh.gcode D:\MW3DPrinting_MachSim\Mesh.ini -MachSim

        print inputParams

        if len(inputParams) >= 3:
            if inputParams[-1] == '-sim':
                print 'Starting verification'
                # writing configuration (start options) file for verifier
                # TODO create own def to write ini file

                # CLUtilities.INIFileWriter()

                posDir = outputf.rfind('\\')
                posPoint = outputf[posDir+1:].rfind('.')
                iniFileName = outputf[posDir+1:posDir+1+posPoint]
                iniFileName = iniFileName + '_SIMULATION.ini'
                iniDirName = outputf[0:posDir+1]
                NCiniFile = iniDirName + iniFileName

                fh = open(NCiniFile, 'w')

                fh.write('nc=' + outputf[posDir+1:] + '\n')
                fh.write('precision=' + str(SIMPRECISION) + '\n')
                fh.write('model=3\n')
                fh.close()

                if inputParams[-2] == '-MachSim' or inputParams[-2] == '-Verifier':
                    startVerification(outputf, NCiniFile, WD, simType=inputParams[-2][1:])
                else:
                    startVerification(outputf, NCiniFile, WD)

        G2CLOG.wlog('INFO', 'All jobs done ...')

    except Exception as e:
        raise
        message = traceback.format_exc().splitlines() # get last error and prepare to write it in logger
        for i in message:
            G2CLOG.wlog('ERROR', str(i))

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    G2CLOG = G2CLogging.G2CLogging()
    main()
    # G2CLOG.writeToLog('hehe')
    G2CLOG.closeLogging()

    # open log file
    # params = 'MWG2C.log'
    # shell.ShellExecuteEx(nShow=win32con.SW_SHOWNORMAL, lpFile='notepad', lpParameters=params)