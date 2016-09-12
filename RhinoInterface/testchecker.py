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
    z_level = int(args.CurrentPoint[2] / 0.2)
    # objs = FindObjectsByName('Layer: ' + str(z_level))
    rs.ObjectsByName('Layer: ' + str(z_level), True)

    args.Display.DrawDot(args.CurrentPoint, 'Layer ' + str(z_level))
    Rhino.Display.RhinoView.Redraw
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