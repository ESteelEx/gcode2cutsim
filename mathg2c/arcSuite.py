import math
import rotation_checker

class arcsuite():
    def __init__(self, unit='degree'):
        self.unit = unit
        self.full_rotations = 0
        self.current_arc = 0
        self.first_move = True
        self.RC = rotation_checker.rotation_checker()

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
        if p1[0] >= 0 and p1[1] >= 0:
            quadrant = 1
        elif p1[0] <= 0 and p1[1] >= 0:
            quadrant = 2
        elif p1[0] <= 0 and p1[1] <= 0:
            quadrant = 3
        elif p1[0] >= 0 and p1[1] <= 0:
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
    def adapt_full_rotation(self, arc, type='realValue'):

        current_arc_relative = self.current_arc - (self.full_rotations * 360)

        answer = self.RC.get_angle_difference(current_arc_relative, arc)

        if answer[2] == 'L+':
            arc_in_degree = self.current_arc + answer[0]
        elif answer[2] == 'R-':
            arc_in_degree = self.current_arc - answer[0]

        self.full_rotations = int(arc_in_degree / 360.0)

        return arc_in_degree

    # ------------------------------------------------------------------------------------------------------------------
    def arc_from_points(self, p1, p2):

        quadrant = self.get_quadrant(self.get_movement_direction(p1, p2))

        try:
            arc_in_radian = math.atan((float(p2[1]) - float(p1[1])) / float((p2[0]) - float(p1[0])))
        except:
            # division by zero will result in exception.
            # is only possible when x-component doesn't change
            # -> possible arcs are 90 or 270 degree (PI/2 or 3/2*PI)
            arc_in_radian = quadrant * (math.pi / 2)
            return self.toDegree(arc_in_radian)

        arc_in_degree = self.toDegree(arc_in_radian)

        if quadrant == 1 or quadrant == 3:
            arc_in_degree += (quadrant - 1) * 90
        else:
            arc_in_degree = (90 + arc_in_degree) + ((quadrant - 1) * 90)

        return arc_in_degree