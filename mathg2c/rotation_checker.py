
class rotation_checker():
    """
    rotation_checker proofs in which direction the C-Axis will rotate.
    Left way round or right way round
    :return
    """
    def __init__(self):
        self.full_rotation_degree = 360

    # ------------------------------------------------------------------------------------------------------------------
    def get_num_of_full_rotations(self, rotation_value):
        """
        We calculate teh number of full rotations we already did
        :param rotation_value: float
        :return: number of full rotation as int
        """
        num_rotations = int(float(rotation_value) / self.full_rotation_degree)

        return num_rotations

    # ------------------------------------------------------------------------------------------------------------------
    def get_degree_to_full_rotation(self, rotation_value):
        """
        Function calculates the remaining degrees to full rotation
        :param rotation_value: float
        :return: float
        """
        degree_to_full_rotation = self.full_rotation_degree - (rotation_value -
                                                               (self.get_num_of_full_rotations(rotation_value) *
                                                                self.full_rotation_degree))

        return degree_to_full_rotation

    # ------------------------------------------------------------------------------------------------------------------
    def get_degree_from_full_rotation(self, rotation_value):
        """
        Function calculates the remaining degrees from full rotation
        :param rotation_value:
        :return:
        """
        degree_from_full_rotation = self.full_rotation_degree - self.get_degree_to_full_rotation(rotation_value)

        return degree_from_full_rotation

    # ------------------------------------------------------------------------------------------------------------------
    def get_quadrant(self, angle):
        """
        Calculates the quadrant of angle value. angle in degree
        :param angle:
        :return:
        """

        Q = int(abs(angle) / 90)  # 0 to 3

        return Q

    # ------------------------------------------------------------------------------------------------------------------
    def get_angle_difference(self, current_pos, next_pos):
        """
        This one only works if the angles are in modulo
        Pass the angles as absolute positions
        :param current_pos:
        :param next_pos:
        :return: first return value is the shortest distance in degree to next angle and the second the longest run. delta in float
        """
        angle_delta_SD = abs(abs(current_pos) - abs(next_pos))  # SD for shortest distance
        if angle_delta_SD > 180:
            angle_delta_LD = angle_delta_SD
            angle_delta_SD = 360 - angle_delta_SD
            if abs(current_pos) > abs(next_pos):
                rotating_direction = 'L+'
            else:
                rotating_direction = 'R-'
        else:
            angle_delta_LD = 360 - angle_delta_SD
            if current_pos > next_pos:
                rotating_direction = 'R-'
            else:
                rotating_direction = 'L+'

        return angle_delta_SD, angle_delta_LD, rotating_direction

    # ------------------------------------------------------------------------------------------------------------------
    def get_modulo_angle(self, angle):
        """
        Calculate modulo of angle value
        :param angle:
        :return:
        """

        modulo_angle = angle - (self.get_num_of_full_rotations(angle)*self.full_rotation_degree)

        if modulo_angle < 0:
            modulo_angle = 360 + modulo_angle

        return modulo_angle

    # ------------------------------------------------------------------------------------------------------------------
    def set_next_angle_value(self, current_pos, delta_short, rotation_direction):
        """
        After detecting the rotation direction and shortest distance to next rotation point
        we decide if we have to correct the value of next angle value because we overran a full rotation
        :param delta_short:
        :param rotation_direction:
        :return: next angle value in float not modulo anymore
        """

        if rotation_direction == 'L+':
            next_pos = current_pos + delta_short
        else:
            next_pos = current_pos - delta_short

        return next_pos

    # ------------------------------------------------------------------------------------------------------------------
    def get_rotation_direction(self, angle_pos1, angle_pos2):
        """
        Calculates the rotation direction from point 1 to point 2 or current to next angle value
        :param angle_pos1: current pos
        :param angle_pos2: next pos
        :return: rotation direction as float
        """
        answer = self.get_angle_difference(self.get_modulo_angle(angle_pos1), self.get_modulo_angle(angle_pos2))

        return answer[2]

# ------------------------------------------------------------------------------------------------------------------
def get_next_pos(current_pos, next_pos):
    """
    Just give back the next rotation value considering full rotation overrun
    :param current_pos: abs angle value
    :param next_pos: abs angle value
    :return: corrected next value
    """

    RC = rotation_checker()
    delta_short, delta_long, rotation_direction = RC.get_angle_difference(RC.get_modulo_angle(current_pos),
                                                                          RC.get_modulo_angle(next_pos))

    next_pos = RC.set_next_angle_value(current_pos, delta_short, rotation_direction)

    #print RC.get_modulo_angle(current_pos)
    #print RC.get_modulo_angle(next_pos)

    #print delta_short
    #print rotation_direction

    return next_pos, rotation_direction

