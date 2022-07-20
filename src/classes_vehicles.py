import pygame

from settings import *
from functions_math import *

class Vehicle:
    acceleration = 0.02
    v_max = 5

    def __init__(self, id, coord, angle, segment):
        self.id = id
        self.coord = coord
        self.angle = angle # in radians
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
        pygame.draw.line(win, RED, move_point(self.coord, offset_x, offset_y, scale), move_point(self.coord, offset_x + 8*math.cos(self.angle), offset_y + 8*math.sin(self.angle), scale), 1)

    def accelerate(self):
        if self.state != "broken":
            if self.v_target > self.v_current:
                self.v_current += Vehicle.acceleration
                if self.v_target < self.v_current: self.v_current = self.v_target
            if self.v_target < self.v_current:
                self.v_current -= Vehicle.acceleration
                if self.v_target > self.v_current: self.v_current = self.v_target

            if self.state == "stop" and self.v_current != 0: self.state = "move"
            elif self.state == "move" and self.v_target == 0 and self.v_current == 0: self.state = "stop"

    def move(self, dict_with_segments):
        if self.state != "broken" and self.v_current:
            last_coord = self.coord
            last_point = self.coord
            self.coord[0] += self.v_current*math.cos(self.angle)
            self.coord[1] += self.v_current*math.sin(self.angle)

            # check if vehicle is still on segment
            dist = dist_to_segment(dict_with_segments[self.segment], self.coord)
            if dist > 0.02: # if vehicle is not on segment - turn
                # vehicle turns on point1
                if dist_two_points(self.coord, dict_with_segments[self.segment].point1) <= abs(self.v_current)+1:
                    last_point = dict_with_segments[self.segment].point1
                    self.segment = dict_with_segments[self.segment].segment1

                # vehicle turns on point2
                elif dist_two_points(self.coord, dict_with_segments[self.segment].point2) <= abs(self.v_current)+1:
                    last_point = dict_with_segments[self.segment].point2
                    self.segment = dict_with_segments[self.segment].segment2

                else: self.state = "broken"

                # calculate new angle
                new_angle = math.atan2(dict_with_segments[self.segment].point2[1]-dict_with_segments[self.segment].point1[1], dict_with_segments[self.segment].point2[0]-dict_with_segments[self.segment].point1[0])
                if abs(new_angle - self.angle) < math.pi/2 or abs(new_angle - self.angle) > 3*math.pi/2: self.angle = new_angle
                else: self.angle = new_angle + math.pi

                # calculate new postion after turn
                self.coord[0] = last_point[0] + (self.v_current-dist)*math.cos(self.angle)
                self.coord[1] = last_point[1] + (self.v_current-dist)*math.sin(self.angle)



    def collision(self, dict_with_carriages):
        for carriage_id in dict_with_carriages:
            if self.id != carriage_id and dist_two_points(self.coord, dict_with_carriages[carriage_id].coord) <= 5:
                self.state = "broken"
                dict_with_carriages[carriage_id].state = "broken"

class Engine(Vehicle):
    def __init__(self, id, coord, angle, segment):
        Vehicle.__init__(self, id, coord, angle, segment)
        self.r = 0
        self.state = "manual"
        self.fore_run_end = coord.copy()

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
                if self.v_target >= Vehicle.v_max: self.v_target = Vehicle.v_max
        if self.bar_slower.collidepoint(click):
            if self.state == "manual":
                self.v_target -= 0.5
                if self.v_target <= -Vehicle.v_max: self.v_target = -Vehicle.v_max

    def fore_run(self, dict_with_segments, dict_with_carriages):
        ghost_engine = Engine(self.id, self.coord.copy(), self.angle, self.segment)
        ghost_engine.v_current = self.v_current
        for _ in range(200):
            ghost_engine.move(dict_with_segments)
        self.v_target = Vehicle.v_max
        self.fore_run_end = ghost_engine.coord.copy()

class Carriage(Vehicle):
    def __init__(self, id, coord, angle, segment):
        Vehicle.__init__(self, id, coord, angle, segment)
        self.r = 1
