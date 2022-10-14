import pygame
import math
import random

from settings import *
from functions_math import *


class Harbor:
    def __init__(self, orgin, angle):
        self.orgin = orgin
        self.angle = angle

        self.LIST_WITH_MACHINES=[
            Ship([orgin[0] + 200*math.cos(angle) + 28*math.sin(angle), orgin[1] + 200*math.sin(angle) - 28*math.cos(angle)], angle),
            Ship([orgin[0] + 600*math.cos(angle) + 28*math.sin(angle), orgin[1] + 600*math.sin(angle) - 28*math.cos(angle)], angle),
            Ship([orgin[0] + 1000*math.cos(angle) + 28*math.sin(angle), orgin[1] + 1000*math.sin(angle) - 28*math.cos(angle)], angle)]

        for i in range(6):
            for j in range(3):
                if not ( j == 2 and i >= 4 ):
                    self.LIST_WITH_MACHINES.append(Containers([orgin[0] - (80 + 50*j)*math.sin(angle) + (100 + 200*i)*math.cos(angle), orgin[1] + (80 + 50*j)*math.cos(angle) + (100 + 200*i)*math.sin(angle)], angle))

        for i in range(9):
            self.LIST_WITH_MACHINES.append(Big_portal_crane([orgin[0] - 10*math.sin(angle) + 130*i*math.cos(angle), orgin[1] + 10*math.cos(angle) + 130*i*math.sin(angle)], angle))
        for i in range(4):
            self.LIST_WITH_MACHINES.append(Portal_crane([orgin[0] - 210*math.sin(angle) + (200 + 100*i)*math.cos(angle), orgin[1] + 210*math.cos(angle) + (200 + 100*i)*math.sin(angle)], angle))


    def draw(self, win, offset_x, offset_y, scale):
        for machine in self.LIST_WITH_MACHINES:
            machine.draw(win, offset_x, offset_y, scale)

        pygame.draw.line(win, BLUE, move_point(self.orgin, offset_x, offset_y, scale), move_point([self.orgin[0] + 1180*math.cos(self.angle), self.orgin[1] + 800*math.sin(self.angle)], offset_x, offset_y, scale), 1)
        # pygame.draw.circle(win, RED, move_point(self.orgin, offset_x, offset_y, scale), 5*scale, 0)

    def run(self):
        for machine in self.LIST_WITH_MACHINES:
            machine.run()

class Building:
    path = BIG_PORTAL_CRANE_PATH
    def __init__(self, orgin, angle):
        self.orgin = orgin
        self.angle = angle

        self.body = pygame.image.load(os.path.join(*self.path))
        self.body.convert()
        self.rotated_image = pygame.transform.rotate(self.body, -math.degrees(self.angle))

    def draw(self, win, offset_x, offset_y, scale):
        body = self.rotated_image.get_rect()
        scaled_image = pygame.transform.scale(self.rotated_image, (scale*body.width, scale*body.height))
        new_rect = scaled_image.get_rect(center = move_point(self.orgin, offset_x, offset_y, scale))
        win.blit(scaled_image, new_rect.topleft)
        # win.blit(scaled_image, move_point(self.orgin, offset_x, offset_y, scale))

        # pygame.draw.circle(win, YELLOW, move_point(self.orgin, offset_x, offset_y, scale), 5*scale, 0)

    def run(self):
        pass

class Containers(Building):
    def __init__(self, orgin, angle):

        temp = random.randint(0,2)
        if temp == 0: self.path = CONTAINERS_PATH
        elif temp == 1: self.path = CONTAINERS2_PATH
        else: self.path = CONTAINERS3_PATH

        Building.__init__(self, orgin, angle)

class Portal_crane(Building):
    path = PORTAL_CRANE_PATH

    track_lenght = 100
    track_width = 50
    orgin_to_track = 14
    margin = 20

    portal_max_speed = 0.25

    def __init__(self, orgin, angle):
        Building.__init__(self, orgin, angle)

        self.position = random.randint(self.margin, self.track_lenght-self.margin)
        temp = random.randint(0,2) - 1
        self.current_speed = temp * self.portal_max_speed
        if temp:
            temp = random.randint(0,1)
            self.current_speed = temp * self.portal_max_speed

    def draw(self, win, offset_x, offset_y, scale):

        pygame.draw.line(win, GRAY, move_point(self.orgin, offset_x, offset_y, scale),
            move_point([self.orgin[0] + self.track_lenght*math.cos(self.angle), self.orgin[1] + self.track_lenght*math.sin(self.angle)], offset_x, offset_y, scale), 1)

        pygame.draw.line(win, GRAY, move_point([self.orgin[0] - self.track_width*math.sin(self.angle), self.orgin[1] + self.track_width*math.cos(self.angle)], offset_x, offset_y, scale),
            move_point([self.orgin[0] - self.track_width*math.sin(self.angle) + self.track_lenght*math.cos(self.angle), self.orgin[1] + self.track_width*math.cos(self.angle) + self.track_lenght*math.sin(self.angle)], offset_x, offset_y, scale), 1)

        body = self.rotated_image.get_rect()
        scaled_image = pygame.transform.scale(self.rotated_image, (scale*body.width, scale*body.height))
        new_orgin = [self.orgin[0] - self.orgin_to_track*math.sin(self.angle) + self.position*math.cos(self.angle), self.orgin[1] + self.orgin_to_track*math.cos(self.angle) + self.position*math.sin(self.angle)]
        new_rect = scaled_image.get_rect(center = move_point(new_orgin, offset_x, offset_y, scale))
        win.blit(scaled_image, new_rect.topleft)

        # pygame.draw.circle(win, RED, move_point(self.orgin, offset_x, offset_y, scale), 5*scale, 0)

    def run(self):
        self.position += self.current_speed
        if self.position < self.margin:
            self.position = self.margin
            self.current_speed = -self.current_speed
        if self.position > self.track_lenght-self.margin:
            self.position = self.track_lenght-self.margin
            self.current_speed = -self.current_speed


class Big_portal_crane(Portal_crane):
    path = BIG_PORTAL_CRANE_PATH

    track_lenght = 130
    track_width = 40
    orgin_to_track = 4
    margin = 25

    portal_max_speed = 0.2

    def __init__(self, orgin, angle):
        Portal_crane.__init__(self, orgin, angle)


class Ship(Building):
    path = SHIP_PATH
    def __init__(self, orgin, angle):
        Building.__init__(self, orgin, angle)
