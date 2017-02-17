import math

class arcsuite():
    def __init__(self):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def toDegree(self, arc_in_radian):
        arc_in_degree = arc_in_radian * 180.0 / math.pi

        return arc_in_degree

    # ------------------------------------------------------------------------------------------------------------------
    def toRadian(self, arc_in_degree):
        arc_in_radian = arc_in_degree * math.pi / 180.0

        return arc_in_radian

    # ------------------------------------------------------------------------------------------------------------------
    def proof_angle_change(self, arcFrom, arcTo):

        if abs(arcTo - arcFrom) > 170:
            print arcFrom
            print arcTo
            arc_in_degree = arcTo + 180
            print 'correction ' + str(arc_in_degree)
        else:
            arc_in_degree = arcTo

        return arc_in_degree

    # ------------------------------------------------------------------------------------------------------------------
    def arc_from_points(self, p1, p2):
        try:
            arc_in_radian = math.atan((p2[1] - p1[1]) / (p2[0] - p1[0]))
        except:
            arc_in_radian = 0

        return self.toDegree(arc_in_radian)