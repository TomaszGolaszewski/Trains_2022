import math

from settings import *

def move_point(point, offset_x, offset_y, scale = 1):
# function that change coordinates of point by offset and scale

    # new_point = (point[0] + OFFSET_HORIZONTAL, point[1] + OFFSET_VERTICAL)
    return ((point[0] + offset_x)*scale, (point[1] + offset_y)*scale)

def move_point_back(point, offset_x, offset_y, scale = 1):
# function that change back coordinates of point by offset and scale

    # new_point = (point[0] + OFFSET_HORIZONTAL, point[1] + OFFSET_VERTICAL)
    return (point[0]/scale - offset_x, point[1]/scale - offset_y)

def move_point_by_angle(point, offset, angle):
# function that change coordinates of point by angle and offset
    return (point[0] + offset * math.cos(angle), point[1] + offset * math.sin(angle))

def dist_two_points(point1, point2):
# function that calculate distance between two points
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

def dist_two_points_square(point1, point2):
# function that calculate square of distance between two points
    return (point1[0]-point2[0])**2 + (point1[1]-point2[1])**2

def dist_to_segment(segment, test_point):
# function that calculate shortest distance between point and segment of the line
    l = dist_two_points(segment.point1, segment.point2)
    ls = dist_two_points_square(segment.point1, segment.point2)
    d1 = dist_two_points(segment.point1, test_point)
    ds1 = dist_two_points_square(segment.point1, test_point)
    d2 = dist_two_points(segment.point2, test_point)
    ds2 = dist_two_points_square(segment.point2, test_point)

    # print()
    # print(str(l))
    # print(str(d1))
    # print(str(d2))
    # print(str(ds1 - (0.5*(ds1-ds2)/l + 0.5*l) ** 2))
    # return 0
    if ds1 - ds2 > ls: return d2
    elif ds2 - ds1 > ls: return d1
    else: return math.sqrt(abs(ds1 - (0.5*(ds1-ds2)/l + 0.5*l) ** 2)) # abs is for numerical errors around 0

def myround(x, target = 5):
# round x to target
    return target * round(x / target)

def myround_point(point):
# round coordinates of the point to 5
    return (myround(point[0]), myround(point[1]))
