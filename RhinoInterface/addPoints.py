import threading
import time

try:
    import Rhino
    import rhinoscriptsyntax as rs
    import scriptcontext
    import math
    import System.Guid, System.Array, System.Enum
except:
    pass

# ----------------------------------------------------------------------------------------------------------------------
def getRGBfromI(RGBint):
    blue = RGBint & 255
    green = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255
    return red, green, blue


def AddPolyline(points, layer, replace_id=None, objColor=(0, 0, 0)):
    """Adds a polyline curve to the current model
    Parameters:
      points = list of 3D points. Duplicate, consecutive points found in
               the array will be removed. The array must contain at least
               two points. If the array contains less than four points,
               then the first point and the last point must be different.
      replace_id[opt] = If set to the id of an existing object, the object
               will be replaced by this polyline
    Returns:
      id of the new curve object if successful
    """

    points = rs.coerce3dpointlist(points, True)
    if replace_id:
        replace_id = rs.coerceguid(replace_id, True)

    rc = System.Guid.Empty
    if replace_id:
        pl = Rhino.Geometry.Polyline(points)
        plColor = Rhino.Input.Custom.GetObject.Color
        if scriptcontext.doc.Objects.Replace(replace_id, pl):
            rc = replace_id
    else:
        rc = scriptcontext.doc.Objects.AddPolyline(points)
        rs.ObjectColor(rc, objColor)

    if rc == System.Guid.Empty:
        raise Exception("Unable to add polyline to document")

    zero_str = '000000'
    objName = 'Layer: ' + zero_str[:-len(str(layer))] + str(layer)  # str(layer)

    rs.ObjectName(rc, objName)

    return rc

class addPoints(threading.Thread):
    def __init__(self, pluginPath, corePath):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.INI_CONFIG = self.corePath + r'\Mesh.ini'
        self.runstat = True
        self.segmentIdxDict = {}
        self.colorDict = {'Wall': (50, 50, 50),
                          'DenseInfill': (255, 0, 255),
                          'SparseInfill': (255, 255, 0),
                          'Brim': (150, 100, 100),
                          'Skirt': (250, 20, 200),
                          'Support': (250, 250, 250)}

        threading.Thread.__init__(self)

    # ------------------------------------------------------------------------------------------------------------------
    def run(self):
        self.flush_data()

    # ------------------------------------------------------------------------------------------------------------------
    def inject_runstat(self, status):
        self.runstat = status

    # ------------------------------------------------------------------------------------------------------------------
    def flush_data(self):
        _FILE = self.corePath + r'\Mesh.gcode'

        X1 = 0
        Y1 = 0
        Z1 = 0

        X2 = 0
        Y2 = 0
        Z2 = 0

        pl = [] # polyline list
        poly_fail= 0

        radius = 0.4

        _z_level_change = False

        # it is possible to define a layer range that is displayed in CAD
        # default is layer 1 to end -> [1, -1]
        layer_start = 1
        layer_end = -1
        _from_to_layer = [layer_start, layer_end]

        _layer = 0
        LayerPoints = {}
        line_in_file = 0

        with open(_FILE) as fid:

            for line in fid:

                if line.strip()[0] == ';':
                    if line.find('WARNING') == -1:  # if we do NOT find
                        split_line = line.split(',')
                        _segment = split_line[0][1:].strip().rstrip()
                        if _segment in self.segmentIdxDict:
                            self.segmentIdxDict[_segment] += 1
                        else:
                            self.segmentIdxDict[_segment] = 0

                        segment = _segment + str(self.segmentIdxDict[_segment])

                line_in_file += 1

                if line[0:3] == 'G1 ' or line[0:3] == 'G0 ':

                    pos_X = line.find('X')
                    if pos_X != -1:
                        pos_ws = line[pos_X:].find(' ')
                        X1 = float(line[pos_X+1:pos_ws+pos_X+1])

                    pos_Y = line.find('Y')
                    if pos_Y != -1:
                        pos_ws = line[pos_Y:].find(' ')
                        if pos_ws == -1:
                            Y1 = float(line[pos_Y + 1:])
                        else:
                            Y1 = float(line[pos_Y + 1:pos_ws + pos_Y+1])

                    pos_Z = line.find('Z')
                    if pos_Z != -1:
                        pos_ws = line[pos_Z:].find(' ')
                        if pos_ws == -1:
                            Z1 = float(line[pos_Z + 1:])
                        else:
                            Z1 = float(line[pos_Z + 1:pos_ws + pos_Z + 1])

                    LayerPoints[0] = [[X1, Y1, Z1]]

                break

            # check if a previous calculation exists
            if rs.IsLayer('MW 3D Printer PointCloud'):
                if rs.IsLayer('MW 3D Printer PointCloud_OLD'):
                    rs.PurgeLayer('MW 3D Printer PointCloud_OLD')
                    rs.RenameLayer('MW 3D Printer PointCloud', 'MW 3D Printer PointCloud_OLD')
                    rs.LayerVisible('MW 3D Printer PointCloud_OLD', visible=False)
                else:
                    rs.RenameLayer('MW 3D Printer PointCloud', 'MW 3D Printer PointCloud_OLD')
                    rs.LayerVisible('MW 3D Printer PointCloud_OLD', visible=False)
                rs.AddLayer(name='MW 3D Printer PointCloud', visible=False)
            else:
                rs.AddLayer(name='MW 3D Printer PointCloud', visible=False)

            if rs.IsLayer('MW 3D Printer Perimeter'):
                if rs.IsLayer('MW 3D Printer Perimeter_OLD'):
                    rs.PurgeLayer('MW 3D Printer Perimeter_OLD')
                    rs.RenameLayer('MW 3D Printer Perimeter', 'MW 3D Printer Perimeter_OLD')
                    rs.LayerVisible('MW 3D Printer Perimeter_OLD', visible=False)
                else:
                    rs.RenameLayer('MW 3D Printer Perimeter', 'MW 3D Printer Perimeter_OLD')
                    rs.LayerVisible('MW 3D Printer Perimeter_OLD', visible=False)
                rs.AddLayer(name='MW 3D Printer Perimeter', visible=True)
            else:
                rs.AddLayer(name='MW 3D Printer Perimeter', visible=True)

            first_move_in_layer = True

            for line in fid:

                if self.runstat:

                    if line.strip()[0] == ';':
                        if line.find('WARNING') == -1:  # if we do NOT find
                            split_line = line.split(',')
                            _segment = split_line[0][1:].strip().rstrip()
                            if _segment in self.segmentIdxDict:
                                self.segmentIdxDict[_segment] += 1
                                # print self.segmentIdxDict
                            else:
                                self.segmentIdxDict[_segment] = 0
                                # print self.segmentIdxDict

                            segment = _segment + str(self.segmentIdxDict[_segment])

                    line_in_file += 1
                    if line[0:3] == 'G1 ' or line[0:3] == 'G0 ':
                        if line[0:3] == 'G1 ':
                            pos_X = line.find('X')
                            if pos_X != -1:
                                pos_ws = line[pos_X:].find(' ')
                                X2 = float(line[pos_X+1:pos_ws+pos_X+1])

                            pos_Y = line.find('Y')
                            if pos_Y != -1:
                                pos_ws = line[pos_Y:].find(' ')
                                if pos_ws == -1:
                                    Y2 = float(line[pos_Y + 1:])
                                else:
                                    Y2 = float(line[pos_Y + 1:pos_ws + pos_Y+1])
                        else:
                            pos_X = line.find('X')
                            if pos_X != -1:
                                pos_ws = line[pos_X:].find(' ')
                                X_G0 = float(line[pos_X + 1:pos_ws + pos_X + 1])

                            pos_Y = line.find('Y')
                            if pos_Y != -1:
                                pos_ws = line[pos_Y:].find(' ')
                                if pos_ws == -1:
                                    Y_G0 = float(line[pos_Y + 1:])
                                else:
                                    Y_G0 = float(line[pos_Y + 1:pos_ws + pos_Y + 1])

                        pos_Z = line.find('Z')
                        if pos_Z != -1:
                            pos_ws = line[pos_Z:].find(' ')
                            if pos_ws == -1:
                                Z2 = float(line[pos_Z + 1:])
                            else:
                                try:
                                    Z2 = float(line[pos_Z + 1:pos_ws + pos_Z + 1])
                                except:
                                    print line[pos_Z + 1:pos_ws + pos_Z + 1]
                                    Z2 = float(line[pos_Z + 1:pos_ws + pos_Z + 1])
                            _z_level_change = True

                        if _layer >= _from_to_layer[0] and not _z_level_change or first_move_in_layer:
                            if line[0:3] == 'G0 ':

                                if _segment in self.segmentIdxDict:
                                    self.segmentIdxDict[_segment] += 1
                                else:
                                    self.segmentIdxDict[_segment] = 0

                                segment = _segment + str(self.segmentIdxDict[_segment])
                                LayerPoints[segment] = [[X_G0, Y_G0, Z2]]  # first point of next segment
                                # print LayerPoints
                                first_move_in_layer = False

                            else:
                                if len(LayerPoints) == 0:
                                    LayerPoints[segment] = [[X2, Y2, Z2]]
                                    first_move_in_layer = False
                                else:
                                    if segment in LayerPoints:
                                        LayerPoints[segment].append([X2, Y2, Z2])

                    if _z_level_change and self.runstat:
                        try:
                            obj = []
                            obj_poly = []
                            if _layer >= _from_to_layer[0]:
                                if len(LayerPoints) > 1:
                                    for segment, points in LayerPoints.iteritems():
                                        if self.runstat:
                                            # print len(points)
                                            if len(points) > 1:
                                                #obj.append(rs.AddPointCloud(points))
                                                #rs.ObjectName(obj[segment], 'Line: ' + str(line_in_file))
                                                #rs.ObjectColor(obj[segment], (getRGBfromI(100000 + _layer * 100)))
                                                #rs.ObjectLayer(obj[segment], layer='MW 3D Printer PointCloud')
                                                try:
                                                    # .NET
                                                    try:
                                                        int(segment[-1])
                                                        lenIdx = 1
                                                        int(segment[-2:])
                                                        lenIdx = 2
                                                        int(segment[-3:])
                                                        lenIdx = 3
                                                    except:
                                                        pass

                                                    # print LayerPoints
                                                    # print points

                                                    if segment[:-lenIdx] in self.colorDict:
                                                        pl.append(AddPolyline(points,
                                                                              _layer,
                                                                              objColor=self.colorDict[segment[:-lenIdx]]))

                                                    # pl.append(AddPolyline(points, _layer))
                                                    # rhino python script - very slow
                                                    #obj_poly.append(rs.AddPolyline(points))

                                                    #rs.ObjectColor(pl, (getRGBfromI(100000 + _layer * 100)))
                                                    #rs.ObjectColor(pl, (180, 190, 200))
                                                    #rs.ObjectLayer(pl, layer='MW 3D Printer Perimeter')
                                                    #rs.ObjectName(pl, 'Layer: ' + str(_layer))

                                                    # fill up with volume
                                                    # rs.AddPipe(obj_poly, 0, 0.3, blend_type=0, cap=2, fit=True)

                                                except:
                                                    poly_fail += 1

                                    # if _layer == 1:
                                    #     rs.AddLayer(name=str(_layer), parent='MW 3D Printer Slices')
                                    # else:
                                    #     rs.AddLayer(name=str(_layer), visible=True, parent='MW 3D Printer Slices')
                                    #
                                    # rs.ObjectLayer(obj, layer=str(_layer))

                                    #if _layer == 1:
                                    #    rs.AddLayer(name=str(_layer), parent='MW 3D Printer PointCloud')

                                    # rs.ObjectLayer(obj, layer=str(_layer))

                            LayerPoints = {}
                            self.segmentIdxDict = {}
                            _z_level_change = False
                            _layer += 1
                            first_move_in_layer = True

                        except:
                            raise
                            pass

                    if _from_to_layer[1] != -1:
                        if _layer == _from_to_layer[1]:
                            break

        scriptcontext.doc.Views.Redraw()
        rs.ObjectLayer(pl, layer='MW 3D Printer Perimeter')

        print 'Flushing path data finished.'
        print 'Polylines ignored: ' + str(poly_fail)
