import pygame
import random
import math

from settings import *
from functions_math import *

class Vehicle:
    acceleration = 0.02
    v_max = 5
    lenght = 18
    width = 8
    body_radius = 2 * 10 + 1

    def __init__(self, id, coord, angle, segment):
        self.id = id
        self.coord = coord
        self.angle = angle # in radians
        self.state = "stop"
        self.v_target = 0
        self.v_current = 0
        self.segment = segment
        self.engine_id = 0
        self.next_carriage = 0
        # self.type

    def draw(self, win, offset_x, offset_y, scale):
        if self.state == "manual": color = BLUE
        elif self.state == "stop": color = GREEN
        elif self.state == "move": color = YELLOW
        else: color = RED

        # draw body
        # body = pygame.Rect(self.coord, (scale*Vehicle.lenght, scale*Vehicle.width))
        # body.center = move_point(self.coord, offset_x, offset_y, scale)
        # pygame.draw.rect(win, LIGHTSLATEGRAY, body)

        # draw body
        if scale >= 0.75:
            body = self.imgs.get_rect()
            scaled_image = pygame.transform.scale(self.imgs, (scale*body.width, scale*body.height))
            rotated_image = pygame.transform.rotate(scaled_image, -math.degrees(self.angle))
            new_rect = rotated_image.get_rect(center = move_point(self.coord, offset_x, offset_y, scale))
            win.blit(rotated_image, new_rect.topleft)

        # draw state indicator
        if scale < 1: indicator_size = 3
        else: indicator_size = 2*scale
        pygame.draw.circle(win, color, move_point(self.coord, offset_x, offset_y, scale), indicator_size , int(self.engine_id == 0))

        # draw angle indicator
        # if not self.r: pygame.draw.line(win, BLACK, move_point(self.coord, offset_x, offset_y, scale), move_point(self.coord, offset_x + 8*math.cos(self.angle), offset_y + 8*math.sin(self.angle), scale), 1)

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

    def push_pull(self, dict_with_carriages = {}):
        if self.engine_id and self.engine_id != self.id:
            self.v_current = dict_with_carriages[self.engine_id].v_current
            self.state = dict_with_carriages[self.engine_id].state

    def move(self, dict_with_segments):
        if self.state != "broken" and self.v_current:
            last_coord = self.coord
            last_point = self.coord
            last_segment = self.segment
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

                # check end of the track
                if self.segment == 9999:
                    self.state = "broken"
                    self.segment = last_segment

                # calculate new angle
                new_angle = math.atan2(dict_with_segments[self.segment].point2[1]-dict_with_segments[self.segment].point1[1], dict_with_segments[self.segment].point2[0]-dict_with_segments[self.segment].point1[0])
                if abs(new_angle - self.angle) < math.pi/2 or abs(new_angle - self.angle) > 3*math.pi/2 and abs(new_angle - self.angle) < 5*math.pi/2: self.angle = new_angle
                else: self.angle = new_angle + math.pi

                # calculate new postion after turn
                self.coord[0] = last_point[0] + dist*math.cos(self.angle)
                self.coord[1] = last_point[1] + dist*math.sin(self.angle)

    def collision(self, dict_with_carriages):
    # check whether a collision occurs and...
        for carriage_id in dict_with_carriages:
            if self.id != carriage_id and self.segment == dict_with_carriages[carriage_id].segment and self.engine_id != dict_with_carriages[carriage_id].engine_id and dist_two_points(self.coord, dict_with_carriages[carriage_id].coord) <= self.body_radius + dict_with_carriages[carriage_id].body_radius + 1:
                # ...break carriages
                if abs(self.v_current) > 0.75:
                    self.state = "broken"
                    if self.engine_id: dict_with_carriages[self.engine_id].state = "broken"
                    dict_with_carriages[carriage_id].state = "broken"
                    if dict_with_carriages[carriage_id].engine_id: dict_with_carriages[dict_with_carriages[carriage_id].engine_id].state = "broken"
                # ...connect carriages
                else:
                    dict_with_carriages[carriage_id].engine_id = self.engine_id
                    self.next_carriage = dict_with_carriages[carriage_id].next_carriage
                    dict_with_carriages[carriage_id].v_target = self.v_target
                    dict_with_carriages[carriage_id].v_current = self.v_current
                    dict_with_carriages[carriage_id].state = self.state
                    dict_with_carriages[carriage_id].angle = self.angle

    def is_collision(self, dict_with_carriages):
    # check whether a collision occurs
        for carriage_id in dict_with_carriages:
            if self.id != carriage_id and self.segment == dict_with_carriages[carriage_id].segment and self.engine_id != dict_with_carriages[carriage_id].engine_id and dist_two_points(self.coord, dict_with_carriages[carriage_id].coord) <= Vehicle.body_radius:
                return True
        return False

    def change_semaphore(self, dict_with_semaphores):
    # change light of the semaphore to red
        for semaphore_id in dict_with_semaphores:
            if dict_with_semaphores[semaphore_id].bottom_light == "green" and dict_with_semaphores[semaphore_id].is_pressed(self.coord):
                dict_with_semaphores[semaphore_id].bottom_light = "red"
                dict_with_semaphores[semaphore_id].logic()


class Engine(Vehicle):
    def __init__(self, id, coord, angle, segment):
        Vehicle.__init__(self, id, coord, angle, segment)
        self.r = 0
        self.imgs = ENGINE_IMGS
        temp_rect = ENGINE_IMGS.get_rect()
        self.body_radius = temp_rect.width / 2

        self.state = "manual"
        self.fore_run_end = coord.copy()
        self.engine_id = id

        # control bar
        self.orgin = [0, 0] # bar orgin
        self.set_new_bar_orgin(self.orgin)

    def set_new_bar_orgin(self, orgin):
        width = 110
        height = 30
        lenght = width - height - 10
        self.bar = pygame.Rect([*orgin, width, height])
        self.bar_auto_button = pygame.Rect([*move_point(orgin, 5, 5), 20, 20])
        self.bar_slower = pygame.Rect([self.bar_auto_button.right+10, self.bar_auto_button.top, lenght/2, 20])
        self.bar_faster = pygame.Rect([*self.bar_slower.topright, lenght/2, 20])

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

        # draw state indicator bottom
        if self.state == "manual": color = BLUE
        elif self.state == "stop": color = GREEN
        elif self.state == "move": color = YELLOW
        else: color = RED
        pygame.draw.circle(win, color, self.bar_auto_button.center, 10, 0)

        # draw engine indicator
        rotated_image = pygame.transform.rotate(self.imgs, -math.degrees(self.angle))
        new_rect = rotated_image.get_rect(center = self.bar_auto_button.center)
        win.blit(rotated_image, new_rect.topleft)

        # draw state indicator top
        pygame.draw.circle(win, color, self.bar_auto_button.center, 2, 0)

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
            elif self.state == "stop" or self.state == "move":
                self.state = "manual"
                self.v_target = 0
        if self.bar_faster.collidepoint(click):
            if self.state == "manual":
                self.v_target += 0.5
                if self.v_target >= Vehicle.v_max: self.v_target = Vehicle.v_max
        if self.bar_slower.collidepoint(click):
            if self.state == "manual":
                self.v_target -= 0.5
                if self.v_target <= -Vehicle.v_max: self.v_target = -Vehicle.v_max

    def fore_run(self, dict_with_segments, dict_with_semaphores, dict_with_carriages):
    # function that checkes if the track in front of the train is free
        max_steps = 70 # 150
        min_v_fore_run = 0.5 # 0.3
        # max_v = 10
        stop = False

        # make test engine
        ghost_engine = Engine(self.id, self.coord.copy(), self.angle, self.segment)
        # set speed of the test engine
        if self.v_current > min_v_fore_run: ghost_engine.v_current = 2 * self.v_current
        else: ghost_engine.v_current = min_v_fore_run
        # run fore-run
        for step in range(max_steps+1):
            ghost_engine.move(dict_with_segments)
            if ghost_engine.is_collision(dict_with_carriages): break
            # if dict_with_segments[ghost_engine.segment].state == "passive": break
            if ghost_engine.state == "broken": break
            for semaphore_id in dict_with_semaphores:
                # if dict_with_semaphores[semaphore_id].stop_train(ghost_engine.coord):
                if dict_with_semaphores[semaphore_id].segment == ghost_engine.segment \
                and dict_with_semaphores[semaphore_id].light == "red" \
                and (dict_with_semaphores[semaphore_id].direction == ghost_engine.angle \
                or dict_with_semaphores[semaphore_id].direction == ghost_engine.angle + 2*math.pi \
                or dict_with_semaphores[semaphore_id].direction + 2*math.pi == ghost_engine.angle) \
                and dist_two_points(dict_with_semaphores[semaphore_id].light_coord, ghost_engine.coord) < 10:
                    stop = True
                    break
            if stop: break

        # for semaphore_id in dict_with_semaphores: dict_with_semaphores[semaphore_id].reset()

        # if the track is free - accelerate
        if step == max_steps:
            self.v_target += 1
            if self.v_target >= Vehicle.v_max: self.v_target = Vehicle.v_max
        # if fore-run encounters a problem - slow down
        else:
            self.v_target -= 1
            if self.v_target <= 0: self.v_target = 0
        self.fore_run_end = ghost_engine.coord.copy()

class Steam_locomotive(Engine):
    def __init__(self, id, coord, angle, segment):
        Engine.__init__(self, id, coord, angle, segment)
        self.imgs = STEAM_LOCOMOTIVE_1_IMGS[0]
        temp_rect = self.imgs.get_rect()
        self.body_radius = temp_rect.width / 2

        self.chimney = 10
        self.smoke = []
        # self.smoke = [[[*self.chimney], 50, 5]]

    def draw(self, win, offset_x, offset_y, scale):
        Engine.draw(self, win, offset_x, offset_y, scale)

        # make new cloud in the smoke
        # if self.smoke[0][1] > 6*(5 - int(math.fabs(self.v_current))):
        if len(self.smoke) < 6 * math.fabs(self.v_current) + 1:
            self.smoke.append([[self.coord[0] + self.chimney * math.cos(self.angle), self.coord[1] + self.chimney * math.sin(self.angle)], 0, random.randint(0,1)]) # ..., frame, color)
            # 0 - coord
            # 1 - frame
            # 2 - color

        for cloud in self.smoke:
            # wind
            cloud[0][0] += 1
            cloud[0][1] += 1

            # draw smoke
            if scale >= 0.75:
                if cloud[2] == 0: color = DARKSTEELGRAY
                elif cloud[2] == 1: color = LIGHTSLATEGRAY
                elif cloud[2] == 2: color = GRAY
                elif cloud[2] == 3: color = SILVER
                else: color = RED
                pygame.draw.circle(win, color, move_point(cloud[0], offset_x, offset_y, scale), 5*scale , 0)
            cloud[1] += 1

        # delete last cloud from the smoke
        if len(self.smoke):
            if self.smoke[0][1] > 35:
                self.smoke.pop(0)



class Multiple_unit1_engine(Engine):
    def __init__(self, id, coord, angle, segment):
        Engine.__init__(self, id, coord, angle, segment)
        self.imgs = MULTIPLE_UNIT_1_IMGS[0]
        temp_rect = self.imgs.get_rect()
        self.body_radius = temp_rect.width / 2

class EN57_engine(Multiple_unit1_engine):
    def __init__(self, id, coord, angle, segment):
        Multiple_unit1_engine.__init__(self, id, coord, angle, segment)
        self.imgs = EN57_IMGS[0]
        temp_rect = self.imgs.get_rect()
        self.body_radius = temp_rect.width / 2


class Carriage(Vehicle):
    def __init__(self, id, coord, angle, segment):
        Vehicle.__init__(self, id, coord, angle, segment)
        self.r = 1
        self.imgs = CARRIAGE_IMGS[random.randint(0,2)]
        temp_rect = self.imgs.get_rect()
        self.body_radius = temp_rect.width / 2

    def accelerate(self):
        pass

class Carriage_passenger(Carriage):
    def __init__(self, id, coord, angle, segment):
        Carriage.__init__(self, id, coord, angle, segment)
        self.imgs = CARRIAGE_PASSENGER_IMGS
        temp_rect = self.imgs.get_rect()
        self.body_radius = temp_rect.width / 2

class Multiple_unit1_carriage(Carriage):
    def __init__(self, id, coord, angle, segment):
        Carriage.__init__(self, id, coord, angle, segment)
        self.imgs = MULTIPLE_UNIT_1_IMGS[1]
        temp_rect = self.imgs.get_rect()
        self.body_radius = temp_rect.width / 2

class Multiple_unit1_end(Carriage):
    def __init__(self, id, coord, angle, segment):
        Carriage.__init__(self, id, coord, angle, segment)
        self.imgs = MULTIPLE_UNIT_1_IMGS[2]
        temp_rect = self.imgs.get_rect()
        self.body_radius = temp_rect.width / 2

class EN57_carriage(Multiple_unit1_carriage):
    def __init__(self, id, coord, angle, segment):
        Multiple_unit1_carriage.__init__(self, id, coord, angle, segment)
        self.imgs = EN57_IMGS[1]
        temp_rect = self.imgs.get_rect()
        self.body_radius = temp_rect.width / 2

class EN57_end(Multiple_unit1_end):
    def __init__(self, id, coord, angle, segment):
        Multiple_unit1_end.__init__(self, id, coord, angle, segment)
        self.imgs = EN57_IMGS[2]
        temp_rect = self.imgs.get_rect()
        self.body_radius = temp_rect.width / 2

class Steam_tender(Carriage):
    def __init__(self, id, coord, angle, segment):
        Carriage.__init__(self, id, coord, angle, segment)
        self.imgs = STEAM_LOCOMOTIVE_1_IMGS[1]
        temp_rect = self.imgs.get_rect()
        self.body_radius = temp_rect.width / 2
