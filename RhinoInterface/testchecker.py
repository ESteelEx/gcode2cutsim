try:
    import rhinoscriptsyntax as rs
    import Rhino, scriptcontext
    import System.Drawing, System.Guid

    from System.Drawing import *
    from Rhino import *
    from Rhino.DocObjects import *
    from Rhino.DocObjects.Tables import *
    from Rhino.Geometry import *
    from Rhino.Input import *
    from Rhino.Commands import *
    from Rhino.UI.Dialogs import ShowColorDialog
    from scriptcontext import doc

except:
    pass


def get_num_layer():
    count = 0
    objID = []
    while 1:
        count += 1
        zero_str = '000000'
        objName = 'Layer: ' + zero_str[:-len(str(count))] + str(count) + ' Wall1'
        objID.append(rs.ObjectsByName(objName))
        if objID[-1] == []:
            # rs.HideObjects(objID[:])
            return count - 1

_NUM_LAYER = get_num_layer()


def FindObjectsByName(name):
    settings = Rhino.DocObjects.ObjectEnumeratorSettings()
    settings.NameFilter = name
    ids = [rhobj.Id for rhobj in scriptcontext.doc.Objects.GetObjectList(settings)]
    if not ids:
        print "No objects with the name", name
        return Rhino.Commands.Result.Failure
    else:
        print "Found", len(ids), "objects"

    return Rhino.Commands.Result.Success


def GetPointDynamicDrawFunc(sender, args):
    # pt1 = Rhino.Geometry.Point3d(0,0,0)
    # pt2 = Rhino.Geometry.Point3d(10,10,0)
    # args.Display.DrawLine(pt1, args.CurrentPoint, System.Drawing.Color.Red, 2)
    # args.Display.DrawLine(pt2, args.CurrentPoint, System.Drawing.Color.Blue, 2)

    rs.UnselectAllObjects()

    # redraw = rs.EnableRedraw(True)

    cursPos = rs.GetCursorPos()
    viewSize = rs.ViewSize()
    stepSize = int(viewSize[1] / _NUM_LAYER)

    obj_Layer1 = 'Layer: 000001 Wall1'
    obj_Layer2 = 'Layer: 000002 Wall1'
    settings = Rhino.DocObjects.ObjectEnumeratorSettings()

    settings.NameFilter = obj_Layer1
    ids_L1 = [rhobj.Id for rhobj in scriptcontext.doc.Objects.GetObjectList(settings)]

    settings.NameFilter = obj_Layer2
    ids_L2 = [rhobj.Id for rhobj in scriptcontext.doc.Objects.GetObjectList(settings)]

    z_L1 = rs.BoundingBox(ids_L1[0])[0][2]
    z_L2 = rs.BoundingBox(ids_L2[0])[0][2]

    zVal = viewSize[1] - cursPos[3][1]

    z_level = int(zVal / stepSize)

    # print scriptcontext.doc.Objects.GetObjectList(settings)
    # z_level = int(args.CurrentPoint[2] / (z_L2 - z_L1))
    # z_level = int(cursPos[2][1] / (z_L2 - z_L1))

    zero_str = '000000'
    obj_LayerZ = 'Layer: ' + zero_str[:-len(str(z_level))] + str(z_level) + ' Wall1'

    settings = Rhino.DocObjects.ObjectEnumeratorSettings()

    settings.NameFilter = obj_LayerZ
    ids_LZ = [rhobj.Id for rhobj in scriptcontext.doc.Objects.GetObjectList(settings)]

    args.Display.DrawDot(args.CurrentPoint, 'Layer ' + str(z_level) + ' - Distance ' + str(z_L2 - z_L1) + ' mm')

    # print dir(ids_LZ)

    # rs.ShowObject(ids_LZ)
    rs.SelectObject(ids_LZ)
    # try:
        # RhinoObject.IsHidden(ids_LZ)
        # ids_LZ.RhinoObject.Select

    # except:
    #    raise

    print obj_LayerZ

    # viewport = Rhino.Display.RhinoView.ActiveViewport
    # Rhino.Display.RhinoView.EnableDrawing
    Rhino.Display.RhinoView.Redraw


class testchecker():
    def __init__(self):
        pass

    def draw_line(self):
        # Create an instance of a GetPoint class and add a delegate for the DynamicDraw event
        gp = Rhino.Input.Custom.GetPoint()
        # gp = Rhino.Input.Custom.PickContext()
        gp.DynamicDraw += GetPointDynamicDrawFunc
        gp.Get()

        # print gp.Point()