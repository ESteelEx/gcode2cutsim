try:
    import Rhino
    import System.Drawing
except:
    pass

def GetPointDynamicDrawFunc( sender, args ):
    # pt1 = Rhino.Geometry.Point3d(0,0,0)
    # pt2 = Rhino.Geometry.Point3d(10,10,0)
    # args.Display.DrawLine(pt1, args.CurrentPoint, System.Drawing.Color.Red, 2)
    # args.Display.DrawLine(pt2, args.CurrentPoint, System.Drawing.Color.Blue, 2)

    print dir(args.Source)

    args.Display.DrawDot(args.CurrentPoint, str(args.CurrentPoint[2]))

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