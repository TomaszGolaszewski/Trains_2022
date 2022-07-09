import pygame

from settings import *
from functions_math import *

class Engine_bar:
# object with interface to control engine

    width = 100
    height = 30
    def __init__(self, engine_id, orgin):
        self.orgin = orgin
        self.engine_id = engine_id
        self.rect = pygame.Rect(*orgin, Engine_bar.width, Engine_bar.height)

    def draw(self, win, engine):
        pygame.draw.rect(win, BLACK, self.rect, 0)
        pygame.draw.rect(win, WHITE, self.rect, 1)

        # draw state indicator
        if engine.state == "stop": color = GREEN
        elif engine.state == "move": color = YELLOW
        else: color = RED
        pygame.draw.circle(win, color, move_point(self.orgin, 15, 15, 1), 4, 0)

        # draw velocity indicator
        pygame.draw.line(win, WHITE, move_point(self.orgin, 30, 15, 1), move_point(self.orgin, Engine_bar.width-15, 15, 1))
        pygame.draw.line(win, WHITE, move_point(self.orgin, 30+(Engine_bar.width-45)/2, 12, 1), move_point(self.orgin, 30+(Engine_bar.width-45)/2, 18, 1))
        pygame.draw.line(win, WHITE, move_point(self.orgin, 30, 12, 1), move_point(self.orgin, 30, 18, 1))
        pygame.draw.line(win, WHITE, move_point(self.orgin, Engine_bar.width-15, 12, 1), move_point(self.orgin, Engine_bar.width-15, 18, 1))


    def is_pressed(self, click):
    # check if the bar is pressed
        return self.rect.collidepoint(click)

    def press(self, click, engine):
        if self.is_pressed(click):
            pass
