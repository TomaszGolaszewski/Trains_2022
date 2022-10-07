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
        elif self.state == "wait": color = ORANGE
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

    def flip(self, dick_with_carriages):
        self.angle += math.pi

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
                    if abs(self.v_current) > 0.05: # master is the one which is in motion
                        dict_with_carriages[carriage_id].engine_id = self.engine_id
                        self.next_carriage = carriage_id #dict_with_carriages[carriage_id].next_carriage
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
            if (dict_with_semaphores[semaphore_id].bottom_light == "green" or dict_with_semaphores[semaphore_id].bottom_light == "yellow") and dict_with_semaphores[semaphore_id].is_pressed(self.coord):
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
        self.wait_time = 0
        self.full_wait_time = 0
        self.fore_run_end = coord.copy()
        self.engine_id = id


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
                    dict_with_semaphores[semaphore_id].request = ghost_engine.id
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

    def wait(self, wait_time):
    # set wait time to engine
        self.wait_time = wait_time
        self.full_wait_time = wait_time
        self.state = "wait"

    def countdown(self):
    # decrease wait time of engine by 1 second
        if self.wait_time:
            self.wait_time -= 1
            if not self.wait_time: self.state = "stop"


class Steam_locomotive(Engine):
    def __init__(self, id, coord, angle, segment):
        Engine.__init__(self, id, coord, angle, segment)
        self.imgs = STEAM_LOCOMOTIVE_1_IMGS[0]
        temp_rect = self.imgs.get_rect()
        self.body_radius = temp_rect.width / 2

        self.chimney = 10
        self.smoke = []

    def draw(self, win, offset_x, offset_y, scale):
        Engine.draw(self, win, offset_x, offset_y, scale)

        # make new cloud in the smoke
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

    def flip(self, dick_with_carriages):
        pass

class Multiple_unit1_engine(Engine):
    def __init__(self, id, coord, angle, segment):
        Engine.__init__(self, id, coord, angle, segment)
        self.imgs = MULTIPLE_UNIT_1_IMGS[0]
        temp_rect = self.imgs.get_rect()
        self.body_radius = temp_rect.width / 2

    def flip(self, dick_with_carriages):
        coord_old_engine = self.coord

        next_carriage = self.next_carriage
        last_carriage = 0
        while next_carriage:
            dick_with_carriages[next_carriage].angle += math.pi
            if dick_with_carriages[next_carriage].angle > 2*math.pi:
                dick_with_carriages[next_carriage].angle -= 2*math.pi
            last_carriage = next_carriage
            next_carriage = dick_with_carriages[next_carriage].next_carriage

        if last_carriage:
            self.coord = dick_with_carriages[last_carriage].coord
            dick_with_carriages[last_carriage].coord = coord_old_engine
            self.angle += math.pi
            if self.angle > 2*math.pi:
                self.angle -= 2*math.pi


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

class Carriage_oldtimer(Carriage):
    def __init__(self, id, coord, angle, segment):
        Carriage.__init__(self, id, coord, angle, segment)
        self.imgs = CARRIAGE_PASSENGER_OLDTIMER_IMGS
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
