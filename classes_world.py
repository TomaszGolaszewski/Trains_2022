import pygame

from settings import *
from functions_math import *

class Point:
    def __init__(self, number, coord, segment1, segment2):
        self.number = number
        self.coord = coord
        self.segment1 = segment1
        self.segment2 = segment2

class Segment:
    def __init__(self, id, point1, point2, segment1, segment2):
        self.id = id
        self.point1 = point1 # coordinates of point before
        self.point2 = point2 # coordinates of point after
        self.segment1 = segment1 # id of point before
        self.segment2 = segment2 # id of point after
        self.state = "active"

    def draw(self, win, offset_x, offset_y, scale):
        if self.state == "active": color = (255,255,255)
        elif self.state == "passive": color = (0,0,255)
        else: color = (255,0,0)
        pygame.draw.line(win, color, move_point(self.point1, offset_x, offset_y, scale), move_point(self.point2, offset_x, offset_y, scale), 1)


class Track_switch:
    def __init__(self, number, coord, first, active, passive):
        self.number = number
        self.coord = coord
        self.first = first
        self.active = active
        self.passive = passive

    def draw(self, win, offset_x, offset_y, scale):
        pygame.draw.circle(win, (0, 0, 255), move_point(self.coord, offset_x, offset_y, scale), 4*scale, 0)
