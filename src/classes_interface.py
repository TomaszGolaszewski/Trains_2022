import pygame

from settings import *
from functions_math import *

class Control_panel:
    width_S = 100
    width_L = 150
    width_train_box = 40
    height = 30


    def __init__(self, id, orgin):
        self.id = id
        self.size = "S"
        self.orgin = orgin # main orgin - top right corner
        self.orgin_S = (orgin[0] - Control_panel.width_S, orgin[1]) # orgin of small bar
        self.rect_bar_S = pygame.Rect([*self.orgin_S, Control_panel.width_S, Control_panel.height]) # rect for small bar
        self.rect_train_box_S = pygame.Rect([*self.orgin_S, Control_panel.width_train_box, Control_panel.height]) # rect for train box inside small bar

        self.orgin_L = (orgin[0] - Control_panel.width_L, orgin[1]) # orgin of large bar


        # from old
        width = 100
        height = 30
        lenght = width - height - 10
        self.bar = pygame.Rect([*orgin, width, height])
        self.bar_auto_button = pygame.Rect([*move_point(orgin, 5, 5), 20, 20])
        self.bar_slower = pygame.Rect([self.bar_auto_button.right+10, self.bar_auto_button.top, lenght/2, 20])
        self.bar_faster = pygame.Rect([*self.bar_slower.topright, lenght/2, 20])

    def draw_engine(self, win, engine):
        if self.size == "S":
            center_point = self.rect_train_box_S.center
        elif self.size == "L":
            # center_point = self.rect_train_box_L.center
            center_point = (0, 0)
        else:
            center_point = (0, 0)

        # draw state indicator bottom
        if engine.state == "manual": color = BLUE
        elif engine.state == "stop": color = GREEN
        elif engine.state == "move": color = YELLOW
        else: color = RED
        pygame.draw.circle(win, color, center_point, 10, 0)

        # draw engine indicator
        rotated_image = pygame.transform.rotate(engine.imgs, -math.degrees(engine.angle))
        new_rect = rotated_image.get_rect(center = center_point)
        win.blit(rotated_image, new_rect.topleft)

        # draw state indicator top
        pygame.draw.circle(win, color, center_point, 2, 0)


    def draw(self, win, engine):
        self.draw_bar_S_manual(win, engine)

        self.draw_engine(win, engine)

    def draw_bar_S_manual(self, win, engine):
        width = self.bar.width
        height = self.bar.height
        lenght = width - height - 10
        orgin = self.bar.topleft

        pygame.draw.rect(win, BLACK, self.rect_bar_S, 0) # black background
        pygame.draw.rect(win, WHITE, self.rect_bar_S, 1) # white frame

        # pygame.draw.rect(win, YELLOW, self.bar_auto_button, 0)
        # pygame.draw.rect(win, BLUE, self.bar_slower, 0)
        # pygame.draw.rect(win, RED, self.bar_faster, 0)



        # draw velocity indicator
        # target velocity
        pygame.draw.line(win, GREEN, move_point(orgin, height + lenght/2, 12, 1), move_point(orgin, height + (1+engine.v_target/5)*lenght/2, 12, 1), 2)
        # current velocity
        pygame.draw.line(win, RED, move_point(orgin, height + lenght/2, 17, 1), move_point(orgin, height + (1+engine.v_current/5)*lenght/2, 17, 1), 2)
        # ruler
        pygame.draw.line(win, WHITE, move_point(orgin, height, height/2, 1), move_point(orgin, height + lenght, height/2, 1)) # ---
        pygame.draw.line(win, WHITE, move_point(orgin, height + lenght/2, 11, 1), move_point(orgin, height + lenght/2, 19, 1)) # -|-
        pygame.draw.line(win, WHITE, move_point(orgin, height, 11, 1), move_point(orgin, 30, 19, 1)) # |--
        pygame.draw.line(win, WHITE, move_point(orgin, height + lenght, 11, 1), move_point(orgin, height + lenght, 19, 1)) # --|
