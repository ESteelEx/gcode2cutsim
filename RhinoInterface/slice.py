import copy, os, subprocess, threading
import addPoints

# import win32ui
# import win32uiole
#
# if hasattr(win32uiole, 'SetMessagePendingDelay'):
#     win32uiole.AfxOleInit()
#     win32uiole.SetMessagePendingDelay(aBigDelay)
#     win32uiole.EnableNotRespondingDialog(False)
#     win32uiole.EnableBusyDialog(False)

try:
    import scriptcontext
    import rhinoscriptsyntax as rs
except:
    pass


def GetDAESettings():
    e_str = ""
    return e_str


def GetOBJSettings():
    e_str = "_Geometry=_Mesh "
    e_str += "_EndOfLine=CRLF "
    e_str += "_ExportRhinoObjectNames=_ExportObjectsAsOBJGroups "
    e_str += "_ExportMeshTextureCoordinates=_Yes "
    e_str += "_ExportMeshVertexNormals=_No "
    e_str += "_CreateNGons=_No "
    e_str += "_ExportMaterialDefinitions=_No "
    e_str += "_YUp=_No "
    e_str += "_WrapLongLines=Yes "
    e_str += "_VertexWelding=_Welded "
    e_str += "_WritePrecision=4 "
    e_str += "_Enter "

    e_str += "_DetailedOptions "
    e_str += "_JaggedSeams=_No "
    e_str += "_PackTextures=_No "
    e_str += "_Refine=_Yes "
    e_str += "_SimplePlane=_No "

    e_str += "_AdvancedOptions "
    e_str += "_Angle=50 "
    e_str += "_AspectRatio=0 "
    e_str += "_Distance=0.0"
    e_str += "_Density=0 "
    e_str += "_Density=0.45 "
    e_str += "_Grid=0 "
    e_str += "_MaxEdgeLength=0 "
    e_str += "_MinEdgeLength=0.0001 "

    e_str += "_Enter _Enter"

    return e_str


def GetSTLSettings():
    eStr = "_ExportFileAs=_Binary "
    eStr += "_ExportUnfinishedObjects=_Yes "
    eStr += "_UseSimpleDialog=_No "
    eStr += "_UseSimpleParameters=_No "
    eStr += "_Enter _DetailedOptions "
    eStr += "_JaggedSeams=_No "
    eStr += "_PackTextures=_No "
    eStr += "_Refine=_Yes "
    eStr += "_SimplePlane=_No "
    eStr += "_AdvancedOptions "
    eStr += "_Angle=15 "
    eStr += "_AspectRatio=0 "
    eStr += "_Distance=0.01 "
    eStr += "_Grid=16 "
    eStr += "_MaxEdgeLength=0 "
    eStr += "_MinEdgeLength=0.0001 "
    eStr += "_Enter _Enter"

    return eStr


class mesh_saver:
    def __init__(self, fileName, filePath, settingsList):
        self.fileName = fileName
        self.filePath = filePath
        print self.filePath
        self.settingsList = settingsList
        self.arrLayers = self.layerNames()

    # ------------------------------------------------------------------------------------------------------------------
    def layerNames(self, sort=False):

        rc = []
        for layer in scriptcontext.doc.Layers:
            if not layer.IsDeleted:
                rc.append(layer.FullPath)

        if sort:
            rc.sort()

        return rc

    # ------------------------------------------------------------------------------------------------------------------
    def initExportByLayer(self, fileType="obj", visibleonly=False, byObject=False):
        for layerName in self.arrLayers:
            layer = scriptcontext.doc.Layers.FindByFullPath(layerName, True)
            if layer >= 0:
                layer = scriptcontext.doc.Layers[layer]
                save = True
                if visibleonly:
                    if not layer.IsVisible:
                        save = False
                if rs.IsLayerEmpty(layerName):
                    save = False
                if save:
                    cutName = layerName.split("::")
                    cutName = cutName[len(cutName)-1]
                    objs = scriptcontext.doc.Objects.FindByLayer(cutName)
                    if len(objs) > 0:
                        if byObject:
                            i = 0
                            for obj in objs:
                                i += 1
                                self.saveObjectsToFile(cutName+"_"+str(i), [obj], fileType)
                        else:
                            self.saveObjectsToFile(cutName, objs, fileType)

    # ------------------------------------------------------------------------------------------------------------------
    def initExportBySelection(self, fileType="obj"):

        print 'SAVE1'
        self.saveSelectionToFile(self.filePath + self.fileName, fileType)

    # ------------------------------------------------------------------------------------------------------------------
    def saveObjectsToFile(self, name, objs, fileType):

        rs.EnableRedraw(False)

        if len(objs) > 0:
            settings = self.settingsList["Get" + fileType.upper() + "Settings"]()
            rs.UnselectAllObjects()
            for obj in objs:
                obj.Select(True)
            name = "".join(name.split(" "))
            command = '-_Export "{}{}{}" {}'.format(self.filePath, name, "." + fileType.lower(), settings)
            rs.Command(command, True)
            rs.EnableRedraw(True)

    # ------------------------------------------------------------------------------------------------------------------
    def saveSelectionToFile(self, name, fileType):

        settings = self.settingsList["Get" + fileType.upper() + "Settings"]()
        command = '-_Export "{}{}{}" {}'.format(self.filePath, self.fileName, "." + fileType.lower(), settings)

        rs.Command(command, True)

# ----------------------------------------------------------------------------------------------------------------------
def run_saver(corePath):
    print "//export run started/////////////"

    settingsList = {
        'GetDAESettings': GetDAESettings,
        'GetOBJSettings': GetOBJSettings,
        'GetSTLSettings': GetSTLSettings
    }

    fileName = r'\Mesh'
    MS = mesh_saver(fileName, corePath, settingsList)

    MS.initExportBySelection(fileType="stl")

    print "//export run ended/////////////"

# ----------------------------------------------------------------------------------------------------------------------
def get_objects(corePath):
    try:
        rs.UnselectAllObjects()

        # make 3D Printer layer invisible
        layerNames = rs.LayerNames()
        for layerName in layerNames:
            if layerName.find('MW 3D Printer') != -1:
                rs.LayerVisible(layerName, visible=False)

        objIds = rs.GetObjects(message='Please select Objects: ', select=True)

        run_saver(corePath) # save Object as STL

    except:
        print 'Could not select Objects'
        objIds = None

    return objIds


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class slicer(threading.Thread):
    def __init__(self, objIds, pluginPath, corePath):
        self.objIds = objIds
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.correctplacement = True
        threading.Thread.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):

        if self.objIds is not None:
            self.proof_placement()
        else:
            print 'No Objects selected'
            return

        if self.correctplacement:
            self.nesting()

        if self.correctplacement:
            pass
            # self.save_stl()
        else:
            print 'Please place the parts correct in build space'
            rs.UnselectAllObjects()
            return

        slice_stat = self.slicing()
        if slice_stat:
            AP = addPoints.addPoints(self.pluginPath, self.corePath)
            AP.start()

    # ------------------------------------------------------------------------------------------------------------------
    def proof_placement(self):

        # color objects
        self.correctplacement = True
        print 'Checking positioning'
        for obj in self.objIds:
            BB = rs.BoundingBox(obj)
            rs.MoveObject(obj, [0, 0, -BB[0][2]])
            BB = rs.BoundingBox(obj)

            for point in BB:
                if point[0] < 0 or point[0] > 241:
                    rs.ObjectColor(obj, (255, 0, 0))
                    self.correctplacement = False
                    break
                else:
                    rs.ObjectColor(obj, (0, 255, 0))

                if point[1] < 0 or point[1] > 209:
                    rs.ObjectColor(obj, (255, 0, 0))
                    self.correctplacement = False
                    break
                else:
                    rs.ObjectColor(obj, (0, 255, 0))

                if point[2] < 0 or point[2] > 205:
                    rs.ObjectColor(obj, (255, 0, 0))
                    self.correctplacement = False
                    break
                else:
                    rs.ObjectColor(obj, (0, 255, 0))

    # ------------------------------------------------------------------------------------------------------------------
    def nesting(self):

        auto_nesting = True

        if len(self.objIds) > 1:
            print 'Checking intersections'
            # proof if objects have intersections
            bBoxCo = []
            for obj, i in zip(self.objIds, range(len(self.objIds))):
                bBoxCo.append(rs.BoundingBox(obj))

            for obj, i in zip(self.objIds, range(len(self.objIds))):
                rs.ObjectColor(obj, (0, 255, 0))
                objIds_tmp = copy.deepcopy(self.objIds)
                objIds_tmp.remove(obj)
                for objCompare in objIds_tmp:
                    intersect = rs.MeshMeshIntersection(obj, objCompare)
                    if intersect is not None:
                        rs.ObjectColor(obj, (255, 0, 0))
                        rs.ObjectColor(objCompare, (255, 0, 0))
                        self.correctplacement = False

                        if auto_nesting:
                            BB = rs.BoundingBox(obj)
                            BBComp = rs.BoundingBox(objCompare)

                            xmin_BB = BB[0][0]
                            xmax_BB = BB[1][0]
                            ymin_BB = BB[0][1]
                            ymax_BB = BB[3][1]

                            xmin_BBComp = BBComp[0][0]
                            xmax_BBComp = BBComp[1][0]
                            ymin_BBComp = BBComp[0][1]
                            ymax_BBComp = BBComp[3][1]

                            if xmin_BBComp >= xmin_BB and xmin_BBComp <= xmax_BB:
                                print 'Correcting x value'
                                # x_delta_to_min = xmin_BBComp - xmin_BB
                                x_delta_to_max = xmin_BBComp - xmax_BB
                                rs.MoveObject(objCompare, [abs(x_delta_to_max), 0, 0])

                            if xmax_BBComp >= xmin_BB and xmax_BBComp <= xmax_BB:
                                print 'Correcting xvalue 2'

                            if ymin_BBComp >= ymin_BB and ymin_BBComp <= ymax_BB:
                                print 'Correcting y value'
                                # y_delta_to_min = ymin_BBComp - ymin_BB
                                y_delta_to_max = ymin_BBComp - ymax_BB
                                rs.MoveObject(objCompare, [0, abs(y_delta_to_max), 0])

                            if ymax_BBComp >= ymin_BB and ymax_BBComp <= ymax_BB:
                                print 'Correcting y value 2'


    # ------------------------------------------------------------------------------------------------------------------
    def save_stl(self):
        run_saver(self.corePath)

    # ------------------------------------------------------------------------------------------------------------------
    def slicing(self):

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW

        abscommand = self.corePath + r'\mwAdditive3DPrinter.exe'

        absargs = self.corePath + r'\Mesh.stl'
        command_string = abscommand + ' ' + absargs

        print 'Starting slicer ...'

        output = subprocess.Popen(command_string, startupinfo=startupinfo, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, stdin=subprocess.PIPE).communicate()

        output_list = str(output)
        output_list_splitted = output_list.split('\\r\\n')
        for message in output_list_splitted:
            print message

        slice = True
        if output_list.find('exception') != -1:
            print 'SLICING FAILED. CONTROL SETTINGS.'
            slice = False

        return slice
