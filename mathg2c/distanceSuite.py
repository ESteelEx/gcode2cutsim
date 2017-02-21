import math

class distanceSuite():
    def __init__(self):
       self.unit = 'mm'

    # ------------------------------------------------------------------------------------------------------------------
    def get_distance_between_points(self, p1, p2):

        distance = math.sqrt(math.pow((float(p1[0]) - float(p2[0])), 2) + math.pow((float(p1[1]) - float(p2[1])), 2))

        return distance