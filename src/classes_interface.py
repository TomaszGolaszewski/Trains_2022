import pygame

from settings import *
from functions_math import *

class Control_panel:
    width_S = 100
    width_S_velocity_box = 25
    width_train_box = 40
    width_button = 29
    width_M = width_S + width_button*3
    width_L = width_S + width_button*5
    height = 30


    def __init__(self, id, orgin):
        self.id = id
        self.size = "S"
        self.orgin = orgin # main orgin - top right corner
        self.orgin_S = (orgin[0] - Control_panel.width_S, orgin[1]) # orgin of small bar
        self.rect_bar_S = pygame.Rect([*self.orgin_S, Control_panel.width_S, Control_panel.height]) # rect for small bar
        self.rect_train_box_S = pygame.Rect([*self.orgin_S, Control_panel.width_train_box, Control_panel.height]) # rect for train box inside small bar
        self.rect_bar_slower_S = pygame.Rect([*self.rect_train_box_S.topright, Control_panel.width_S_velocity_box, Control_panel.height])
        self.rect_bar_faster_S = pygame.Rect([*self.rect_bar_slower_S.topright, Control_panel.width_S_velocity_box, Control_panel.height])

        self.orgin_M = (orgin[0] - Control_panel.width_M, orgin[1]) # orgin of medium bar
        self.rect_bar_M = pygame.Rect([*self.orgin_M, Control_panel.width_M, Control_panel.height]) # rect for medium bar
        self.rect_train_box_M = pygame.Rect([*self.orgin_M, Control_panel.width_train_box, Control_panel.height]) # rect for train box inside medium bar
        self.rect_bar_slower_M = pygame.Rect([*self.rect_train_box_M.topright, Control_panel.width_S_velocity_box, Control_panel.height])
        self.rect_bar_faster_M = pygame.Rect([*self.rect_bar_slower_M.topright, Control_panel.width_S_velocity_box, Control_panel.height])

        self.rect_button_1 = pygame.Rect([orgin[0] - Control_panel.width_button, orgin[1], Control_panel.width_button, Control_panel.height]) # rect for first button
        self.rect_button_2 = pygame.Rect([orgin[0] - 2 * Control_panel.width_button, orgin[1], Control_panel.width_button, Control_panel.height]) # rect for second button
        self.rect_button_3 = pygame.Rect([orgin[0] - 3 * Control_panel.width_button, orgin[1], Control_panel.width_button, Control_panel.height]) # rect for third button
        self.rect_button_4 = pygame.Rect([orgin[0] - 4 * Control_panel.width_button, orgin[1], Control_panel.width_button, Control_panel.height]) # rect for fourth button
        self.rect_button_5 = pygame.Rect([orgin[0] - 5 * Control_panel.width_button, orgin[1], Control_panel.width_button, Control_panel.height]) # rect for fifth button

        self.orgin_L = (orgin[0] - Control_panel.width_L, orgin[1]) # orgin of large bar
        self.rect_bar_L = pygame.Rect([*self.orgin_L, Control_panel.width_L, Control_panel.height]) # rect for medium bar
        self.rect_train_box_L = pygame.Rect([*self.orgin_L, Control_panel.width_train_box, Control_panel.height]) # rect for train box inside medium bar
        self.rect_bar_slower_L = pygame.Rect([*self.rect_train_box_L.topright, Control_panel.width_S_velocity_box, Control_panel.height])
        self.rect_bar_faster_L = pygame.Rect([*self.rect_bar_slower_L.topright, Control_panel.width_S_velocity_box, Control_panel.height])

    def draw_engine(self, win, engine):
        if self.size == "S":
            center_point = self.rect_train_box_S.center
        elif self.size == "M":
            center_point = self.rect_train_box_M.center
        elif self.size == "L":
            center_point = self.rect_train_box_L.center
        else:
            center_point = (0, 0)

        # draw state indicator bottom
        radius = 10

        if engine.state == "manual": color = BLUE
        elif engine.state == "stop": color = GREEN
        elif engine.state == "move": color = YELLOW
        elif engine.state == "wait": color = ORANGE
        else: color = RED

        if engine.state == "wait":
            temp_rect = pygame.Rect(center_point[0]-radius, center_point[1]-radius, 2*radius, 2*radius)
            pygame.draw.arc(win, color, temp_rect, math.pi/2, 2*math.pi * engine.wait_time / engine.full_wait_time + math.pi/2, radius)
        else: pygame.draw.circle(win, color, center_point, radius, 0)

        # draw engine indicator
        rotated_image = pygame.transform.rotate(engine.imgs, -math.degrees(engine.angle))
        new_rect = rotated_image.get_rect(center = center_point)
        win.blit(rotated_image, new_rect.topleft)

        # draw state indicator top
        pygame.draw.circle(win, color, center_point, 2, 0)

    def press(self, dict_with_carriages, click):
        engine = dict_with_carriages[self.id]

        if self.size == "M" and self.rect_bar_M.collidepoint(click):
            if self.rect_train_box_M.collidepoint(click) or self.rect_button_3.collidepoint(click):
                if engine.state == "manual": engine.state = "stop"
                elif engine.state == "stop" or engine.state == "move" or engine.state == "wait":
                    engine.state = "manual"
                    engine.v_target = 0
                    engine.wait_time = 0
            if self.rect_button_2.collidepoint(click):
                if engine.state == "manual":
                    engine.flip(dict_with_carriages)
            if self.rect_button_1.collidepoint(click):
                self.size = "L"
            if self.rect_bar_faster_M.collidepoint(click):
                if engine.state == "manual":
                    engine.v_target += 0.5
                    if engine.v_target >= 5: engine.v_target = engine.v_max_current # Vehicle.v_max # -----------------------------------------
            if self.rect_bar_slower_M.collidepoint(click):
                if engine.state == "manual":
                    engine.v_target -= 0.5
                    if engine.v_target <= -5: engine.v_target = -engine.v_max_current # Vehicle.v_max ----------------------------------

        elif self.size == "L" and self.rect_bar_L.collidepoint(click):
            if self.rect_train_box_L.collidepoint(click) or self.rect_button_3.collidepoint(click):
                if engine.state == "manual": engine.state = "stop"
                elif engine.state == "stop" or engine.state == "move" or engine.state == "wait":
                    engine.state = "manual"
                    engine.v_target = 0
                    engine.wait_time = 0
            if self.rect_button_2.collidepoint(click):
                if engine.state == "manual":
                    engine.flip(dict_with_carriages)
            if self.rect_button_1.collidepoint(click):
                self.size = "M"
            if self.rect_bar_faster_L.collidepoint(click):
                if engine.state == "manual":
                    engine.v_target += 0.5
                    if engine.v_target >= 5: engine.v_target = engine.v_max_current # Vehicle.v_max # -----------------------------------------
            if self.rect_bar_slower_L.collidepoint(click):
                if engine.state == "manual":
                    engine.v_target -= 0.5
                    if engine.v_target <= -5: engine.v_target = -engine.v_max_current # Vehicle.v_max ----------------------------------

    def draw(self, win, engine, mouse_pos): #, id_to_show = 0):

        show = False # center view on engine

        if self.size == "S" and self.rect_bar_S.collidepoint(mouse_pos):
            self.size = "M"
            show = True
        if self.size == "M":
            if self.rect_bar_M.collidepoint(mouse_pos): show = True
            else: self.size = "S"
        if self.size == "L" and self.rect_bar_L.collidepoint(mouse_pos): show = True

        if self.size == "S": self.draw_bar_S(win, engine)
        if self.size == "M": self.draw_bar_M(win, engine)
        if self.size == "L": self.draw_bar_L(win, engine)

        self.draw_engine(win, engine)

        if show: return engine.id
        else: return 0

    def draw_bar_S(self, win, engine):
        # width = self.rect_bar_S.width
        # height = self.rect_bar_S.height
        # lenght = width - height - 10
        # orgin = self.rect_bar_S.topleft

        pygame.draw.rect(win, BLACK, self.rect_bar_S, 0) # black background
        pygame.draw.rect(win, WHITE, self.rect_bar_S, 1) # white frame

        # pygame.draw.rect(win, YELLOW, self.bar_auto_button, 0)

        # draw velocity indicator
        # target velocity
        pygame.draw.line(win, GREEN, (self.rect_bar_slower_S.right, self.rect_bar_slower_S.centery - 3), (engine.v_target/5 * self.rect_bar_slower_S.width + self.rect_bar_slower_S.right, self.rect_bar_slower_S.centery - 3), 2)
        # current velocity
        pygame.draw.line(win, RED, (self.rect_bar_slower_S.right, self.rect_bar_slower_S.centery + 2), (engine.v_current/5 * self.rect_bar_slower_S.width + self.rect_bar_slower_S.right, self.rect_bar_slower_S.centery + 2), 2)
        # ruler
        pygame.draw.line(win, WHITE, (self.rect_bar_slower_S.left, self.rect_bar_slower_S.centery),(self.rect_bar_faster_S.right, self.rect_bar_slower_S.centery)) # ---
        pygame.draw.line(win, WHITE, (self.rect_bar_slower_S.right, self.rect_bar_slower_S.centery - 4), (self.rect_bar_slower_S.right, self.rect_bar_slower_S.centery + 4)) # -|-
        pygame.draw.line(win, WHITE, (self.rect_bar_slower_S.left, self.rect_bar_slower_S.centery - 4), (self.rect_bar_slower_S.left, self.rect_bar_slower_S.centery + 4)) # |--
        pygame.draw.line(win, WHITE, (self.rect_bar_faster_S.right, self.rect_bar_slower_S.centery - 4), (self.rect_bar_faster_S.right, self.rect_bar_slower_S.centery + 4)) # --|


    def draw_bar_M(self, win, engine):
        pygame.draw.rect(win, BLACK, self.rect_bar_M, 0) # black background
        pygame.draw.rect(win, WHITE, self.rect_bar_M, 1) # white frame

        # draw velocity indicator
        # target velocity
        pygame.draw.line(win, GREEN, (self.rect_bar_slower_M.right, self.rect_bar_slower_M.centery - 3), (engine.v_target/5 * self.rect_bar_slower_M.width + self.rect_bar_slower_M.right, self.rect_bar_slower_M.centery - 3), 2)
        # current velocity
        pygame.draw.line(win, RED, (self.rect_bar_slower_M.right, self.rect_bar_slower_M.centery + 2), (engine.v_current/5 * self.rect_bar_slower_M.width + self.rect_bar_slower_M.right, self.rect_bar_slower_M.centery + 2), 2)
        # ruler
        pygame.draw.line(win, WHITE, (self.rect_bar_slower_M.left, self.rect_bar_slower_M.centery),(self.rect_bar_faster_M.right, self.rect_bar_slower_M.centery)) # ---
        pygame.draw.line(win, WHITE, (self.rect_bar_slower_M.right, self.rect_bar_slower_M.centery - 4), (self.rect_bar_slower_M.right, self.rect_bar_slower_M.centery + 4)) # -|-
        pygame.draw.line(win, WHITE, (self.rect_bar_slower_M.left, self.rect_bar_slower_M.centery - 4), (self.rect_bar_slower_M.left, self.rect_bar_slower_M.centery + 4)) # |--
        pygame.draw.line(win, WHITE, (self.rect_bar_faster_M.right, self.rect_bar_slower_M.centery - 4), (self.rect_bar_faster_M.right, self.rect_bar_slower_M.centery + 4)) # --|

        # buttons
        # manual/auto
        if engine.state == "manual":
            win.blit(MANUAL_MODE, self.rect_button_3.topleft)
        elif engine.state == "stop" or engine.state == "move" or engine.state == "wait":
            win.blit(AUTO_MODE, self.rect_button_3.topleft)

        # flip engine
        win.blit(ARROW_FLIP, self.rect_button_2.topleft)

        # switch to size L
        win.blit(ARROW_LEFT, self.rect_button_1.topleft)


    def draw_bar_L(self, win, engine):
        pygame.draw.rect(win, BLACK, self.rect_bar_L, 0) # black background
        pygame.draw.rect(win, WHITE, self.rect_bar_L, 1) # white frame

        # draw velocity indicator
        # target velocity
        pygame.draw.line(win, GREEN, (self.rect_bar_slower_L.right, self.rect_bar_slower_L.centery - 3), (engine.v_target/5 * self.rect_bar_slower_L.width + self.rect_bar_slower_L.right, self.rect_bar_slower_L.centery - 3), 2)
        # current velocity
        pygame.draw.line(win, RED, (self.rect_bar_slower_L.right, self.rect_bar_slower_L.centery + 2), (engine.v_current/5 * self.rect_bar_slower_L.width + self.rect_bar_slower_L.right, self.rect_bar_slower_L.centery + 2), 2)
        # ruler
        pygame.draw.line(win, WHITE, (self.rect_bar_slower_L.left, self.rect_bar_slower_L.centery),(self.rect_bar_faster_L.right, self.rect_bar_slower_L.centery)) # ---
        pygame.draw.line(win, WHITE, (self.rect_bar_slower_L.right, self.rect_bar_slower_L.centery - 4), (self.rect_bar_slower_L.right, self.rect_bar_slower_L.centery + 4)) # -|-
        pygame.draw.line(win, WHITE, (self.rect_bar_slower_L.left, self.rect_bar_slower_L.centery - 4), (self.rect_bar_slower_L.left, self.rect_bar_slower_L.centery + 4)) # |--
        pygame.draw.line(win, WHITE, (self.rect_bar_faster_L.right, self.rect_bar_slower_L.centery - 4), (self.rect_bar_faster_L.right, self.rect_bar_slower_L.centery + 4)) # --|

        # buttons
        # manual/auto
        if engine.state == "manual":
            win.blit(MANUAL_MODE, self.rect_button_3.topleft)
        elif engine.state == "stop" or engine.state == "move" or engine.state == "wait":
            win.blit(AUTO_MODE, self.rect_button_3.topleft)

        # flip engine
        win.blit(ARROW_FLIP, self.rect_button_2.topleft)

        # switch to size 
        win.blit(ARROW_RIGHT, self.rect_button_1.topleft)

        # placeholders
        win.blit(PLACEHOLDER, self.rect_button_4.topleft)
        win.blit(PLACEHOLDER, self.rect_button_5.topleft)
