from math import *

class Preprocessor(object):

    VERSION = 1
    TYPE = "move"
    AXIS = ["X" , "Y" , "U" , "V" , "Z", "R1", "LBYR1", "LBYR2", "LBXR1", "LBXR2" ]  

    def ProcessMove(self, environment, operation, move): 
        move["axisValue"]["U"] = move["axisValue"]["X"]
        move["axisValue"]["V"] = move["axisValue"]["Y"]
        move["axisValue"]["R1"] = move["axisValue"]["Z"]*240
        move["axisValue"]["LBYR1"] = move["axisValue"]["Y"]*-9.59
        move["axisValue"]["LBYR2"] = move["axisValue"]["Y"]*-9.59
        move["axisValue"]["LBXR1"] = move["axisValue"]["X"]*9.59
        move["axisValue"]["LBXR2"] = move["axisValue"]["X"]*9.59

preprocessor = Preprocessor()
