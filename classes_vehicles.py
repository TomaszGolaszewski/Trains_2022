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

        if self.state == "stop" and self.v_current != 0: self.state = "move"
        elif self.state == "move" and self.v_target == 0 and self.v_current == 0: self.state = "stop"

    def move(self):
        self.coord[0] += self.v_current
        # if self.v_target == self.v_current:
        #     self.v_target = -self.v_target

class Engine(Vehicle):
    def __init__(self, id, coord, angle, segment):
        Vehicle.__init__(self, id, coord, angle, segment)
        self.r = 0
        self.state = "manual"

        # control bar
        self.orgin = [0, 0] # bar orgin
        self.set_new_bar_orgin(self.orgin)

    def set_new_bar_orgin(self, orgin):
        width = 110
        height = 30
        lenght = width - height - 10
        self.bar = pygame.Rect([*orgin, width, height])
        self.bar_auto_button = pygame.Rect([*move_point(orgin, 10, 10), 10, 10])
        self.bar_slower = pygame.Rect([self.bar_auto_button.right+10, self.bar_auto_button.top, lenght/2, 10])
        self.bar_faster = pygame.Rect([*self.bar_slower.topright, lenght/2, 10])

    def draw_bar(self, win):
        width = self.bar.width
        height = self.bar.height
        lenght = width - height - 10
        orgin = self.bar.topleft

        pygame.draw.rect(win, BLACK, self.bar, 0)
        pygame.draw.rect(win, WHITE, self.bar, 1)

        # pygame.draw.rect(win, YELLOW, self.bar_auto_button, 0)
        # pygame.draw.rect(win, BLUE, self.bar_slower, 0)
        # pygame.draw.rect(win, RED, self.bar_faster, 0)

        # draw state indicator
        if self.state == "manual": color = BLUE
        elif self.state == "stop": color = GREEN
        elif self.state == "move": color = YELLOW
        else: color = RED
        pygame.draw.circle(win, color, self.bar_auto_button.center, 4, 0)

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
        return self.bar.collidepoint(click)

    def press_bar(self, click):
        if self.bar_auto_button.collidepoint(click):
            if self.state == "manual": self.state = "stop"
            elif self.state == "stop" or self.state == "move": self.state = "manual"
        if self.bar_faster.collidepoint(click):
            if self.state == "manual":
                self.v_target += 0.5
                if self.v_target >= 5: self.v_target = 5
        if self.bar_slower.collidepoint(click):
            if self.state == "manual":
                self.v_target -= 0.5
                if self.v_target <= -5: self.v_target = -5

class Carriage(Vehicle):
    def __init__(self, id, coord, angle, segment):
        Vehicle.__init__(self, id, coord, angle, segment)
        self.r = 1
