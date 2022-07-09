import pygame

from settings import *
from functions_math import *

class Vehicle:
    acceleration = 0.02

    def __init__(self, id, coord, angle, segment):
        self.id = id
        self.coord = coord
        self.angle = angle
        self.state = "stop"
        self.v_target = 0
        self.v_current = 0
        self.segment = segment
        # self.type

    def draw(self, win, offset_x, offset_y, scale):
        if self.state == "stop": color = GREEN
        elif self.state == "move": color = YELLOW
        else: color = RED
        pygame.draw.circle(win, color, move_point(self.coord, offset_x, offset_y, scale), 4*scale, self.r)

    def accelerate(self):
        if self.v_target > self.v_current:
            self.v_current += Vehicle.acceleration
            if self.v_target < self.v_current: self.v_current = self.v_target
        if self.v_target < self.v_current:
            self.v_current -= Vehicle.acceleration
            if self.v_target > self.v_current: self.v_current = self.v_target

    def move(self):
        self.coord[0] += self.v_current
        if self.v_target == self.v_current:
            self.v_target = -self.v_target

class Engine(Vehicle):
    def __init__(self, id, coord, angle, segment):
        Vehicle.__init__(self, id, coord, angle, segment)
        self.r = 0

class Carriage(Vehicle):
    def __init__(self, id, coord, angle, segment):
        Vehicle.__init__(self, id, coord, angle, segment)
        self.r = 1
