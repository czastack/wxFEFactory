import math
PI = math.pi

def degreeToRadian(degrees):
    return degrees * (PI / 180.0)

def radianToDegree(radian):
    return radian / PI * 180.0

def headingToDirection(heading):
    heading = degreeToRadian(heading)
    return -math.sin(heading), math.cos(heading)