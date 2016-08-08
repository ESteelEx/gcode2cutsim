import rhinoscriptsyntax as rs

CP = rs.AddClippingPlane(rs.WorldXYPlane(), 220.0, 220.0)
rs.RotateObject(CP, (110, 110, 0), 180, axis=(1, 0, 0))
