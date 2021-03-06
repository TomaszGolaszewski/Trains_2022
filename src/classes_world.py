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

    def save(self):
        return str(self.id) + "\t" + str(self.point1[0]) + "\t" + str(self.point1[1]) + "\t" + str(self.point2[0]) + "\t" + str(self.point2[1]) + "\t" + str(self.segment1) + "\t" + str(self.segment2) + "\n"

    def draw(self, win, offset_x, offset_y, scale):
        if self.state == "active": color = WHITE
        elif self.state == "passive": color = BLUE
        else: color = RED
        pygame.draw.line(win, color, move_point(self.point1, offset_x, offset_y, scale), move_point(self.point2, offset_x, offset_y, scale), 1)

    def draw_ends(self, win, offset_x, offset_y, scale):
        if self.segment1 == 9999: color = RED
        else: color = WHITE
        pygame.draw.circle(win, color, move_point(self.point1, offset_x, offset_y, scale), 4*scale, 0)

        if self.segment2 == 9999: color = RED
        else: color = WHITE
        pygame.draw.circle(win, color, move_point(self.point2, offset_x, offset_y, scale), 4*scale, 0)

class Track_switch:
    def __init__(self, number, coord, first, active, passive):
        self.number = number
        self.coord = coord
        self.first = first
        self.active = active
        self.passive = passive

    def save(self):
        return str(self.number) + "\t" + str(self.coord[0]) + "\t" + str(self.coord[1]) + "\t" + str(self.first) + "\t" + str(self.active) + "\t" + str(self.passive) + "\n"

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


class Semaphore:
    def __init__(self, number, light_coord, sensor_coord):
        self.number = number
        self.light_coord = light_coord
        self.sensor_coord = sensor_coord
        self.light = "red"
        self.light_used = False
        self.sensor_used = False
        self.light_on = False
        self.sensor_on = False

    def save(self):
        return str(self.number) + "\t" + str(self.light_coord[0]) + "\t" + str(self.light_coord[1]) + "\t" + str(self.sensor_coord[0]) + "\t" + str(self.sensor_coord[1]) + "\n"

    def is_pressed(self, click):
    # check if the light button is pressed
        return dist_two_points(self.light_coord, click) < 5

    def change_light(self):
    # change color of the light
        if self.light == "red": self.light = "green"
        elif self.light == "green": self.light = "red"

    def draw(self, win, offset_x, offset_y, scale):
        if self.light == "green": color = GREEN
        elif self.light == "yellow": color = YELLOW
        else: color = RED
        pygame.draw.circle(win, WHITE, move_point(self.sensor_coord, offset_x, offset_y, scale), 4*scale, 1)
        pygame.draw.circle(win, color, move_point(self.light_coord, offset_x, offset_y, scale), 4*scale, 0)

    def reset(self):
        self.light_used = False
        self.sensor_used = False
        self.light_on = False
        self.sensor_on = False

    def stop_train(self, position):
        if self.light == "red":
            if dist_two_points(self.light_coord, position) < 3 and not self.light_used:
                if self.sensor_on:
                    self.sensor_on = False
                    self.light_used = True
                    return True # train has to stop
                else:
                    self.light_on = True # train is moving from behind
                self.light_used = True

            elif dist_two_points(self.sensor_coord, position) < 3 and not self.sensor_used:
                if self.light_on:
                    self.light_on = False # train is moving from behind
                else:
                    self.sensor_on = True # train is moving from front
                self.sensor_used = True
        return False
