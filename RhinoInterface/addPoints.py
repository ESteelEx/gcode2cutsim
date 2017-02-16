import threading

try:
    import Rhino
    import rhinoscriptsyntax as rs
    import scriptcontext
    import mathg2c
    import System.Guid, System.Array, System.Enum
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


# ----------------------------------------------------------------------------------------------------------------------
def getRGBfromI(RGBint):
    blue = RGBint & 255
    green = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255
    return red, green, blue

# ----------------------------------------------------------------------------------------------------------------------
def getIfromRGB(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    RGBint = (red << 16) + (green << 8) + blue
    return RGBint

# ----------------------------------------------------------------------------------------------------------------------
def AddPolyline(points, layer, replace_id=None, objColor=(0, 0, 0), segment=''):
    """Adds a polyline to the current CAD scene
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
        rc = Polyline(points)
        attributes = ObjectAttributes()
        attributes.ObjectColor = ColorTranslator.FromOle(getIfromRGB(objColor))
        attributes.ColorSource = ObjectColorSource.ColorFromObject
        zero_str = '000000'
        objName = 'Layer: ' + zero_str[:-len(str(layer))] + str(layer) + ' ' + segment  # str(layer)
        attributes.Name = objName
        lIdx = scriptcontext.doc.Layers.Find('MW 3D Printer Perimeter', 1)
        attributes.LayerIndex = lIdx
        doc.Objects.AddPolyline(rc, attributes)

    if rc == System.Guid.Empty:
        raise Exception("Unable to add polyline to document")

    return rc

# ----------------------------------------------------------------------------------------------------------------------
def proof_z_level_change(line, first_move_in_layer):
    pass

# ----------------------------------------------------------------------------------------------------------------------
class addPoints(threading.Thread):
    def __init__(self, pluginPath, corePath):
        self.pluginPath = pluginPath
        self.corePath = corePath
        self.INI_CONFIG = self.corePath + r'\Mesh.ini'
        self.runstat = True
        self.segmentIdxDict = {}
        self.colorDict = {'Wall': (0, 0, 0),
                          'DenseInfill': (255, 0, 255),
                          'SparseInfill': (0, 255, 255),
                          'Brim': (100, 100, 100),
                          'Skirt': (180, 180, 180),
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

        print 'Adding polylines to CAD environment ... wait'

        _FILE = self.corePath + r'\Mesh.gcode'

        pl = []  # polyline list
        pc = []  # pointcloud list
        poly_fail = 0

        _add_point_cloud = False

        _z_level_change = False
        first_z_move_in_layer = True

        # it is possible to define a layer range that is displayed in CAD
        # default is layer 1 to end -> [1, -1]
        layer_start = 0
        layer_end = -1
        _from_to_layer = [layer_start, layer_end]

        _layer = 1
        LayerPoints = {}
        line_in_file = 0

        end_of_file = False

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

        # open G-Code
        fid = open(_FILE, 'r')
        # Begin G-Code processing
        last_pos = []
        last_pos.append(fid.tell())
        for line in fid:
            last_pos.append(fid.tell())
            line_in_file += 1

            if len(line) == 1:
                continue

            if self.runstat:  # external functions can inject a command to stop threading

                # proof if there is a comment with layer information
                if line.strip()[0] == ';':

                    if line.find('gCode file finished') != -1:
                        end_of_file = True

                    if line.find('WARNING') == -1:  # if we do NOT find a WARNING
                        split_line = line.split(',')
                        _segment = split_line[0][1:].strip().rstrip()

                        if _segment not in self.segmentIdxDict:
                            self.segmentIdxDict[_segment] = 0

                        segment = _segment + str(self.segmentIdxDict[_segment])
                    else:
                        pass
                        # print 'WARNING'

                # coordinates of G1 and G0 moves are processed
                if line[0:3] == 'G1 ' or line[0:3] == 'G0 ':

                    # filter z coordinates and proof if its the first inital or the next layer
                    pos_Z = line.find('Z')
                    if pos_Z != -1:
                        pos_ws = line[pos_Z:].find(' ')
                        if pos_ws == -1:
                            Z = float(line[pos_Z + 1:])
                        else:
                            try:
                                Z = float(line[pos_Z + 1:pos_ws + pos_Z + 1])
                            except:
                                Z = float(line[pos_Z + 1:pos_ws + pos_Z + 1])
                        if first_z_move_in_layer:
                            first_z_move_in_layer = False
                        else:
                            _z_level_change = True
                            fid.seek(last_pos[-3])  # revert file position
                            last_pos.pop()
                            last_pos.pop()
                            last_pos.pop()
                            line_in_file = line_in_file - 2


                    if not _z_level_change:
                        # filter coordinates from G1 move
                        if line[0:3] == 'G1 ':
                            pos_X = line.find('X')
                            if pos_X != -1:
                                pos_ws = line[pos_X:].find(' ')
                                X = float(line[pos_X+1:pos_ws+pos_X+1])

                            pos_Y = line.find('Y')
                            if pos_Y != -1:
                                pos_ws = line[pos_Y:].find(' ')
                                if pos_ws == -1:
                                    Y = float(line[pos_Y + 1:])
                                else:
                                    Y = float(line[pos_Y + 1:pos_ws + pos_Y+1])

                        # filter coordinates from G0 move
                        elif line[0:3] == 'G0 ':
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

                        # add coordinates to layer dictionary
                        if _layer >= _from_to_layer[0]:
                            if line[0:3] == 'G0 ':
                                if _segment in self.segmentIdxDict:
                                    self.segmentIdxDict[_segment] += 1
                                else:
                                    self.segmentIdxDict[_segment] = 0

                                segment = _segment + str(self.segmentIdxDict[_segment])
                                LayerPoints[segment] = [[X_G0, Y_G0, Z]]  # first point of next segment
                            else:
                                if len(LayerPoints) == 0:
                                    LayerPoints[segment] = [[X, Y, Z]]
                                else:
                                    if segment in LayerPoints:
                                        LayerPoints[segment].append([X, Y, Z])

                # add lines and points to Rhino environment
                if _z_level_change and self.runstat or end_of_file:

                    try:
                        if _layer >= _from_to_layer[0]:
                            if len(LayerPoints) > 1:
                                for segment, points in LayerPoints.iteritems():
                                    if self.runstat:
                                        if len(points) > 1:
                                            try:
                                                # .NET
                                                try:
                                                    int(segment[-1])
                                                    lenIdx = 1
                                                    int(segment[-2:])
                                                    lenIdx = 2
                                                    int(segment[-3:])
                                                    lenIdx = 3
                                                    int(segment[-4:])
                                                    lenIdx = 4
                                                except:
                                                    pass

                                                if segment[:-lenIdx] in self.colorDict:
                                                    pl.append(AddPolyline(points,
                                                                          _layer,
                                                                          objColor=self.colorDict[segment[:-lenIdx]],
                                                                          segment=segment))
                                                else:
                                                    pl.append(AddPolyline(points,
                                                                          _layer,
                                                                          objColor=(255, 0, 0),
                                                                          segment=segment))

                                                    # print 'Segment not found'

                                                # add point cloud
                                                if _add_point_cloud:
                                                    pc.append(rs.AddPointCloud(points))

                                            except:
                                                raise
                                                poly_fail += 1

                        LayerPoints = {}  # clear point information from dict
                        self.segmentIdxDict = {}  # clear segment counter dict
                        _z_level_change = False
                        _layer += 1
                        first_z_move_in_layer = True

                    except:
                        raise
                        pass

                if _from_to_layer[1] != -1:
                    if _layer == _from_to_layer[1]:
                        break

        scriptcontext.doc.Views.Redraw()
        # rs.ObjectLayer(pl, layer='MW 3D Printer Perimeter')

        print 'Flushing path data finished.'
        print 'Polylines ignored: ' + str(poly_fail)
