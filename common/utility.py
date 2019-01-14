M_PI = 3.141519


# This function converts an input angle from degree to radians
def deg2rad(degree):
    return (degree / 180.0) * M_PI


def rad2deg(angle):
    return angle * (180.0 / M_PI)
