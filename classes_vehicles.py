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
        if self.state == "manual": color = BLUE
        elif self.state == "stop": color = GREEN
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
        self.state = "manual"

    def draw_bar(self, win, orgin):
        width = 110
        height = 30
        lenght = width - height - 10

        pygame.draw.rect(win, BLACK, [*orgin, width, height], 0)
        pygame.draw.rect(win, WHITE, [*orgin, width, height], 1)

        # draw state indicator
        if self.state == "manual": color = BLUE
        elif self.state == "stop": color = GREEN
        elif self.state == "move": color = YELLOW
        else: color = RED
        pygame.draw.circle(win, color, move_point(orgin, 15, 15, 1), 4, 0)

        # draw velocity indicator
        # target velocity
        pygame.draw.line(win, GREEN, move_point(orgin, height + lenght/2, 12, 1), move_point(orgin, height + (1+self.v_target/5)*lenght/2, 12, 1), 2)
        # current velocity
        pygame.draw.line(win, RED, move_point(orgin, height + lenght/2, 17, 1), move_point(orgin, height + (1+self.v_current/5)*lenght/2, 17, 1), 2)
        # ruler
        pygame.draw.line(win, WHITE, move_point(orgin, height, height/2, 1), move_point(orgin, height + lenght, height/2, 1)) # ---
        pygame.draw.line(win, WHITE, move_point(orgin, height + lenght/2, 11, 1), move_point(orgin, height + lenght/2, 19, 1)) # -|-
        pygame.draw.line(win, WHITE, move_point(orgin, height, 11, 1), move_point(orgin, 30, 19, 1)) # |--
        pygame.draw.line(win, WHITE, move_point(orgin, height + lenght, 11, 1), move_point(orgin, height + lenght, 19, 1)) # --|

    def is_bar_pressed(self, click):
    # check if the bar is pressed
        return self.rect.collidepoint(click)

    def press_bar(self, click, engine):
        if self.is_pressed(click):
            pass

class Carriage(Vehicle):
    def __init__(self, id, coord, angle, segment):
        Vehicle.__init__(self, id, coord, angle, segment)
        self.r = 1
