try:
    import rhinoscriptsyntax as rs
    import Rhino, scriptcontext
    import System.Drawing, System.Guid
except:
    pass

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

def GetPointDynamicDrawFunc( sender, args ):
    # pt1 = Rhino.Geometry.Point3d(0,0,0)
    # pt2 = Rhino.Geometry.Point3d(10,10,0)
    # args.Display.DrawLine(pt1, args.CurrentPoint, System.Drawing.Color.Red, 2)
    # args.Display.DrawLine(pt2, args.CurrentPoint, System.Drawing.Color.Blue, 2)
    rs.UnselectAllObjects()

    obj_Layer1 = 'Layer: 1'
    obj_Layer2 = 'Layer: 2'
    settings = Rhino.DocObjects.ObjectEnumeratorSettings()

    settings.NameFilter = obj_Layer1
    ids_L1 = [rhobj.Id for rhobj in scriptcontext.doc.Objects.GetObjectList(settings)]

    settings.NameFilter = obj_Layer2
    ids_L2 = [rhobj.Id for rhobj in scriptcontext.doc.Objects.GetObjectList(settings)]

    z_L1 = rs.BoundingBox(ids_L1[0])[0][2]
    z_L2 = rs.BoundingBox(ids_L2[0])[0][2]

    z_level = int(args.CurrentPoint[2] / (z_L2 - z_L1))

    obj_LayerZ = 'Layer: ' + str(z_level)
    settings = Rhino.DocObjects.ObjectEnumeratorSettings()

    settings.NameFilter = obj_LayerZ
    ids_LZ = [rhobj.Id for rhobj in scriptcontext.doc.Objects.GetObjectList(settings)]

    args.Display.DrawDot(args.CurrentPoint, 'Layer ' + str(z_level))

    Rhino.Display.RhinoView.Redraw

    rs.SelectObjects(ids_LZ)

    # scriptcontext.doc.Views.Redraw()

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