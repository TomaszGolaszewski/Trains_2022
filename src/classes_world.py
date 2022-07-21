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

    def __str__(self):
        return str(self.segment1) + " " + str(self.point1) + " " + str(self.id) + " " + str(self.point2) + " " + str(self.segment2)


    def draw(self, win, offset_x, offset_y, scale):
        if self.state == "active": color = WHITE
        elif self.state == "passive": color = BLUE
        else: color = RED
        pygame.draw.line(win, color, move_point(self.point1, offset_x, offset_y, scale), move_point(self.point2, offset_x, offset_y, scale), 1)


class Track_switch:
    def __init__(self, number, coord, first, active, passive):
        self.number = number
        self.coord = coord
        self.first = first
        self.active = active
        self.passive = passive

    def draw(self, win, offset_x, offset_y, scale):
        pygame.draw.circle(win, BLUE, move_point(self.coord, offset_x, offset_y, scale), 4*scale, 0)

    def is_switch_pressed(self, click):
    # check if the switch button is pressed
        return dist_two_points(self.coord, click) < 10

    def switch_switch(self, dict_with_segments):
    # switch the track switch
        if dict_with_segments[self.first].segment1 == self.active:
            dict_with_segments[self.first].segment1 = self.passive
        elif dict_with_segments[self.first].segment2 == self.active:
            dict_with_segments[self.first].segment2 = self.passive

        dict_with_segments[self.active].state = "passive"
        dict_with_segments[self.passive].state = "active"
        self.active, self.passive = self.passive, self.active
