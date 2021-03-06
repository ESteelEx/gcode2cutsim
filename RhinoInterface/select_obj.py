import copy
import scriptcontext
try:
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
def run_saver(objId):
    print "//export run started/////////////"

    settingsList = {
        'GetDAESettings': GetDAESettings,
        'GetOBJSettings': GetOBJSettings,
        'GetSTLSettings': GetSTLSettings
    }

    fileName = r'Mesh'
    filePath = r'D:\StoreDaily\\'
    MS = mesh_saver(fileName, filePath, settingsList)

    # MS.initExportByLayer("stl", True, False)
    MS.initExportBySelection(fileType="stl")

    print "//export run ended/////////////"

try:
    rs.UnselectAllObjects()
    objId = rs.GetObjects(message='Please select an Object: ', select=True)

    print 'SAVING STL'
    run_saver(objId)

except:
    raise
    pass