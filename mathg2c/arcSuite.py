import math

class arcsuite():
    def __init__(self):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def toDegree(self, arc_in_radian):
        arc_in_degree = float(arc_in_radian) * 180.0 / float(math.pi)

        return arc_in_degree

    # ------------------------------------------------------------------------------------------------------------------
    def toRadian(self, arc_in_degree):
        arc_in_radian = float(arc_in_degree) * math.pi / 180.0

        return arc_in_radian

    # ------------------------------------------------------------------------------------------------------------------
    def get_quadrant(self, p1):
        if p1[0] > 0 and p1[1] > 0:
            quadrant = 1
        elif p1[0] < 0 and p1[1] > 0:
            quadrant = 2
        elif p1[0] < 0 and p1[1] < 0:
            quadrant = 3
        elif p1[0] > 0 and p1[1] < 0:
            quadrant = 4

        return quadrant

    # ------------------------------------------------------------------------------------------------------------------
    def get_movement_direction(self, p1, p2):
        direction = []
        direction.append(p1[0] - p2[0])
        direction.append(p1[1] - p2[1])

        magnitude = math.sqrt(math.pow(direction[0], 2) + math.pow(direction[1], 2))

        direction[0] = direction[0] / magnitude
        direction[1] = direction[1] / magnitude

        return direction

    # ------------------------------------------------------------------------------------------------------------------
    def proof_angle_change(self, arcFrom, arcTo, maxAngleChange=20):

        if abs(arcTo - arcFrom) > maxAngleChange:
            return True
        else:
            return False

    # ------------------------------------------------------------------------------------------------------------------
    def arc_from_points(self, p1, p2):
        try:
            arc_in_radian = math.atan((float(p2[1]) - float(p1[1])) / float((p2[0]) - float(p1[0])))
        except:
            arc_in_radian = 0

        arc_in_degree = self.toDegree(arc_in_radian)
        quadrant = self.get_quadrant(self.get_movement_direction(p1, p2))

        if quadrant == 1 or quadrant == 3:
            arc_in_degree += (quadrant - 1) * 90
        else:
            arc_in_degree = (90 + arc_in_degree) + ((quadrant - 1) * 90)

        return arc_in_degree