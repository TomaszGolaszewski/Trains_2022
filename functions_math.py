from settings import *

def move_point(point, offset_x, offset_y, scale):
# function that change coordinates of point by display offset and scale

    # new_point = (point[0] + OFFSET_HORIZONTAL, point[1] + OFFSET_VERTICAL)
    return ((point[0] + offset_x)*scale, (point[1] + offset_y)*scale)
