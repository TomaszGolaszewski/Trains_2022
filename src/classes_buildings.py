import pygame
import math

from settings import *
from functions_math import *


class Harbor:
    def __init__(self, orgin, angle):
        self.orgin = orgin
        self.angle = angle

        self.LIST_WITH_MACHINES=[
            Ship([orgin[0] + 200*math.cos(angle) + 28*math.sin(angle), orgin[1] + 200*math.sin(angle) - 28*math.cos(angle)], angle),
            Ship([orgin[0] + 600*math.cos(angle) + 28*math.sin(angle), orgin[1] + 600*math.sin(angle) - 28*math.cos(angle)], angle)]

        for i in range(4):
            for j in range(3):
                self.LIST_WITH_MACHINES.append(Containers([orgin[0] - (80 + 50*j)*math.sin(angle) + (100 + 200*i)*math.cos(angle), orgin[1] + (80 + 50*j)*math.cos(angle) + (100 + 200*i)*math.sin(angle)], angle))

        for i in range(6):
            self.LIST_WITH_MACHINES.append(Big_portal_crane([orgin[0] - 10*math.sin(angle) + 130*i*math.cos(angle), orgin[1] + 10*math.cos(angle) + 130*i*math.sin(angle)], angle))
        for i in range(4):
            self.LIST_WITH_MACHINES.append(Portal_crane([orgin[0] - 220*math.sin(angle) + (200 + 100*i)*math.cos(angle), orgin[1] + 220*math.cos(angle) + (200 + 100*i)*math.sin(angle)], angle))


    def draw(self, win, offset_x, offset_y, scale):
        for machine in self.LIST_WITH_MACHINES:
            machine.draw(win, offset_x, offset_y, scale)

        pygame.draw.line(win, BLUE, move_point(self.orgin, offset_x, offset_y, scale), move_point([self.orgin[0] + 800*math.cos(self.angle), self.orgin[1] + 800*math.sin(self.angle)], offset_x, offset_y, scale), 1)
        pygame.draw.circle(win, RED, move_point(self.orgin, offset_x, offset_y, scale), 5*scale, 0)

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

        pygame.draw.circle(win, YELLOW, move_point(self.orgin, offset_x, offset_y, scale), 5*scale, 0)

    def run(self):
        pass

class Containers(Building):
    path = CONTAINERS_PATH
    def __init__(self, orgin, angle):
        Building.__init__(self, orgin, angle)

class Portal_crane(Building):
    path = PORTAL_CRANE_PATH
    def __init__(self, orgin, angle):
        Building.__init__(self, orgin, angle)

    # def draw(self, win, offset_x, offset_y, scale):
    #     pass
    #
    # def run(self):
    #     pass


class Big_portal_crane(Portal_crane):
    path = BIG_PORTAL_CRANE_PATH
    def __init__(self, orgin, angle):
        Portal_crane.__init__(self, orgin, angle)

    # def draw(self, win, offset_x, offset_y, scale):
    #     pass
    #
    # def run(self):
    #     pass


class Ship(Building):
    path = SHIP_PATH
    def __init__(self, orgin, angle):
        Building.__init__(self, orgin, angle)
