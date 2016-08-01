try:
    import rhinoscriptsyntax as rs
    import copy
except:
    pass

def getRGBfromI(RGBint):
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return red, green, blue

#_FILE = r'D:\Development\GitRep\gcode2cutsim_V2\bin\3DPrintModule\Bottle_Opener.gcode'
#_FILE = r'D:\Development\GitRep\gcode2cutsim_V2\bin\3DPrintModule\bench_5-4-2016.gcode'
_FILE = r'C:\StoreDaily\Mesh.gcode'
#_FILE = r'C:\Users\ModuleWoks\Documents\Development\GitRep\gcode2cutsim\bin\3DPrintModule\bench_5-4-2016.gcode'
#_FILE = r'C:\Users\ModuleWoks\Documents\Development\GitRep\gcode2cutsim\bin\3DPrintModule\Figure_of_man.gcode'

X1 = 0
Y1 = 0
Z1 = 0

X2 = 0
Y2 = 0
Z2 = 0

radius = 0.4

_z_level_change = False

layer_start = 1
layer_end = -1

# layer_start = raw_input('Please define start layer: ')
# if len(layer_start) == 0:
#     layer_start = 1
# layer_end = raw_input('Please define end layer: ')
# if len(layer_end) == 0:
#     layer_end = -1

_from_to_layer = [layer_start, layer_end]

_layer = 0
LayerPoints = []
LayerPoints[0].append('fgf')

with open(_FILE) as fid:

    for line in fid:

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

            LayerPoints[0].append((X1, Y1, Z1))

        break

    rs.AddLayer(name='MW 3D Printer PointCloud')
    rs.AddLayer(name='MW 3D Printer Perimeter')
    g_zero_move = 0

    for line in fid:

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


            if _layer >= _from_to_layer[0]:
                if line[0:3] == 'G0 ':
                    LayerPoints.append([])
                    # g_zero_move += 1
                    LayerPoints[-1].append((X2, Y2, Z2))
                else:
                    print len(LayerPoints)
                    LayerPoints[-1].append((X2, Y2, Z2))

        # if _z_level_change:
        #     _layer += 1

        if _z_level_change:
            try:
                # rs.AddPoint(X,Y,Z)
                # rs.AddCylinder((X1, Y1, Z1), (X2, Y2 ,Z2), radius)
                if _layer >= _from_to_layer[0]:
                    if len(LayerPoints) > 1:
                        #rs.AddPolyline(LayerPoints)
                        obj = rs.AddPointCloud(LayerPoints)
                        rs.ObjectColor(obj, (getRGBfromI(100000 + _layer * 100)))
                        rs.ObjectLayer(obj, layer='MW 3D Printer PointCloud')

                        obj_poly = rs.AddPolyline(LayerPoints)
                        #rs.ObjectColor(obj_poly, (getRGBfromI(100000 + _layer * 100)))
                        rs.ObjectLayer(obj_poly, layer='MW 3D Printer Perimeter')

                        # rs.AddPipe(obj_poly, 0, 0.3, blend_type=0, cap=2, fit=False)


                    # if _layer == 1:
                    #     rs.AddLayer(name=str(_layer), parent='MW 3D Printer Slices')
                    # else:
                    #     rs.AddLayer(name=str(_layer), visible=True, parent='MW 3D Printer Slices')
                    #
                    # rs.ObjectLayer(obj, layer=str(_layer))

                    #if _layer == 1:
                    #    rs.AddLayer(name=str(_layer), parent='MW 3D Printer PointCloud')

                    # rs.ObjectLayer(obj, layer=str(_layer))

                LayerPoints = []
                g_zero_move = 0
                _z_level_change = False
                _layer += 1
                # print _layer
            except:
                raise
                pass

        if _from_to_layer[1] != -1:
            if _layer == _from_to_layer[1]:
                break