try:
    import rhinoscriptsyntax as rs
    import copy
except:
    pass

_FILE = r'D:\Development\GitRep\gcode2cutsim_V2\bin\3DPrintModule\Bottle_Opener.gcode'

X1 = 0
Y1 = 0
Z1 = 0

X2 = 0
Y2 = 0
Z2 = 0

radius = 0.4

_z_level_change = False
_layer = 0
LayerPoints = []

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

            LayerPoints.append((X1, Y1, Z1))

        break

    for line in fid:

        if line[0:3] == 'G1 ' or line[0:3] == 'G0 ':

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

            pos_Z = line.find('Z')
            if pos_Z != -1:
                pos_ws = line[pos_Z:].find(' ')
                if pos_ws == -1:
                    Z2 = float(line[pos_Z + 1:])
                else:
                    Z2 = float(line[pos_Z + 1:pos_ws + pos_Z + 1])
                _z_level_change = True

            LayerPoints.append((X2, Y2, Z2))

        if _z_level_change:
            try:
                # rs.AddPoint(X,Y,Z)
                # rs.AddCylinder((X1, Y1, Z1), (X2, Y2 ,Z2), radius)
                if len(LayerPoints) > 1:
                    # rs.AddPolyline(LayerPoints)
                    rs.AddPointCloud(LayerPoints)
                LayerPoints = []
                _z_level_change = False
                _layer += 1
                print _layer
            except:
                raise
                pass

        X1 = copy.deepcopy(X2)
        Y1 = copy.deepcopy(Y2)
        Z1 = copy.deepcopy(Z2)

        if _layer == 150:
            break

