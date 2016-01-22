from math import cos, sin, radians

def trig(angle):
  r = radians(angle)
  return cos(r), sin(r)

def matrix(rotation=(0,0,0), translation=(0,0,0)):
  xC, xS = trig(rotation[0])
  yC, yS = trig(rotation[1])
  zC, zS = trig(rotation[2])
  dX = translation[0]
  dY = translation[1]
  dZ = translation[2]
  return [[yC*xC, -zC*xS+zS*yS*xC, zS*xS+zC*yS*xC, dX],
    [yC*xS, zC*xC+zS*yS*xS, -zS*xC+zC*yS*xS, dY],
    [-yS, zS*yC, zC*yC, dZ],
    [0, 0, 0, 1]]

def transform(point=(0,0,0), vector=(0,0,0)):
  p = [0,0,0]
  for r in range(3):
    p[r] += vector[r][3]
    for c in range(3):
      p[r] += point[c] * vector[r][c]
  return p

if __name__ == '__main__':
  point = (7, 12, 8)
  rotation = (0, -45, 0)
  translation = (0, 0, 5)
  matrix = matrix(rotation, translation)
  print (transform(point, matrix))