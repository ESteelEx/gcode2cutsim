try:
    import rhinoscriptsyntax as rs
except:
    pass

_BEDCENTER = [125, 110, 0]

rs.UnselectAllObjects()
objects = rs.OpenFileNames(title='Enter or select STL', filter='STL|*.stl', extension='stl')

for objSTL in objects:
    print objSTL
    if objSTL is not None:
        objSTL = '"' + objSTL + '"'
        rs.Command(r'-_Import ' + objSTL + ' _Enter')
        meshName = objSTL.split('\\')
        obj = rs.SelectedObjects()

        if len(obj) != 0:
            centroid = rs.MeshVolumeCentroid(obj)
            rs.AddLayer(name=meshName[-1].split('.')[0])
            rs.ObjectLayer(obj, layer=meshName[-1].split('.')[0])
            if centroid:
                vector = rs.VectorCreate(_BEDCENTER, centroid)
                rs.MoveObject(obj, vector)
                BB = rs.BoundingBox(obj)
                rs.MoveObject(obj, [0, 0, -BB[0][2]])
                rs.UnselectAllObjects()