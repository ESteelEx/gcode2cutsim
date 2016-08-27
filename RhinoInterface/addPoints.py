try:
    import rhinoscriptsyntax as rs
    import copy
except:
    pass

def getRGBfromI(RGBint):
    blue = RGBint & 255
    green = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255
    return red, green, blue

_FILE = r'D:\StoreDaily\Mesh.gcode'

X1 = 0
Y1 = 0
Z1 = 0

X2 = 0
Y2 = 0
Z2 = 0

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

    g_zero_move = int(0)

    for line in fid:
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
                    Z2 = float(line[pos_Z + 1:pos_ws + pos_Z + 1])
                _z_level_change = True

            if _layer >= _from_to_layer[0] and not _z_level_change:
                if line[0:3] == 'G0 ':
                    #if g_zero_move >= 1:
                    #    LayerPoints[g_zero_move].append(LayerPoints[g_zero_move][0])
                    g_zero_move += 1
                    LayerPoints[g_zero_move] = [[X_G0, Y_G0, Z2]] # first point of next segment
                else:
                    if len(LayerPoints) == 0:
                        LayerPoints[g_zero_move] = [[X2, Y2, Z2]]
                    else:
                        LayerPoints[g_zero_move].append([X2, Y2, Z2])

        if _z_level_change:
            try:
                obj = []
                obj_poly = []
                if _layer >= _from_to_layer[0]:
                    if len(LayerPoints) > 1:
                        for segment, points in LayerPoints.iteritems():
                            if len(points) > 1:
                                obj.append(rs.AddPointCloud(points))
                                rs.ObjectName(obj[segment], 'Line: ' + str(line_in_file))
                                rs.ObjectColor(obj[segment], (getRGBfromI(100000 + _layer * 100)))
                                rs.ObjectLayer(obj[segment], layer='MW 3D Printer PointCloud')

                                try:
                                    obj_poly.append(rs.AddPolyline(points))

                                    # rs.ObjectColor(obj_poly[segment], (getRGBfromI(100000 + _layer * 100)))
                                    rs.ObjectColor(obj_poly[segment], (180, 190, 200) )
                                    rs.ObjectLayer(obj_poly[segment], layer='MW 3D Printer Perimeter')
                                    rs.ObjectName(obj_poly[segment], 'Layer: ' + str(_layer))

                                    # fill up with volume
                                    # rs.AddPipe(obj_poly, 0, 0.3, blend_type=0, cap=2, fit=True)

                                except:
                                    print 'Point ignored. No polyline possible'


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
                g_zero_move = 0
                _z_level_change = False
                _layer += 1

            except:
                raise
                pass

        if _from_to_layer[1] != -1:
            if _layer == _from_to_layer[1]:
                break

