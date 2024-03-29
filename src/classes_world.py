import pygame
import math

from settings import *
from functions_math import *
from classes_vehicles import Engine

class Point:
    def __init__(self, number, coord, segment1, segment2):
        self.number = number
        self.coord = coord
        self.segment1 = segment1
        self.segment2 = segment2

class Segment:
    def __init__(self, id, point1, point2, segment1, segment2):
        self.id = id
        self.point1 = point1 # coordinates of point before
        self.point2 = point2 # coordinates of point after
        self.segment1 = segment1 # id of point before
        self.segment2 = segment2 # id of point after
        self.state = "active"

    def __str__(self):
        return str(self.segment1) + " " + str(self.point1) + " " + str(self.id) + " " + str(self.point2) + " " + str(self.segment2)

    def save(self):
        return str(self.id) + "\t" + str(self.point1[0]) + "\t" + str(self.point1[1]) + "\t" + str(self.point2[0]) + "\t" + str(self.point2[1]) + "\t" + str(self.segment1) + "\t" + str(self.segment2) + "\n"

    def draw(self, win, offset_x, offset_y, scale):
        if self.state == "active": color = WHITE
        elif self.state == "passive": color = BLUE
        else: color = RED
        pygame.draw.line(win, color, move_point(self.point1, offset_x, offset_y, scale), move_point(self.point2, offset_x, offset_y, scale), 1)

    def draw_ends(self, win, offset_x, offset_y, scale):
        if self.segment1 == 9999: color = RED
        else: color = WHITE
        pygame.draw.circle(win, color, move_point(self.point1, offset_x, offset_y, scale), 4*scale, 0)

        if self.segment2 == 9999: color = RED
        else: color = WHITE
        pygame.draw.circle(win, color, move_point(self.point2, offset_x, offset_y, scale), 4*scale, 0)

class Track_switch:
    def __init__(self, number, coord, first, active, passive):
        self.number = number
        self.coord = coord
        self.first = first
        self.active = active
        self.passive = passive

    def save(self):
        return str(self.number) + "\t" + str(self.coord[0]) + "\t" + str(self.coord[1]) + "\t" + str(self.first) + "\t" + str(self.active) + "\t" + str(self.passive) + "\n"

    def draw(self, win, offset_x, offset_y, scale):
        pygame.draw.circle(win, BLUE, move_point(self.coord, offset_x, offset_y, scale), 4*scale, 0)

    def is_switch_pressed(self, click):
    # check if the switch button is pressed
        return dist_two_points(self.coord, click) < 10

    def switch_switch(self, dict_with_segments):
    # switch the track switch
        if dict_with_segments[self.first].segment1 == self.active:
            dict_with_segments[self.first].segment1 = self.passive
        elif dict_with_segments[self.first].segment2 == self.active:
            dict_with_segments[self.first].segment2 = self.passive

        dict_with_segments[self.active].state = "passive"
        dict_with_segments[self.passive].state = "active"
        self.active, self.passive = self.passive, self.active

class Semaphore:
    def __init__(self, number, light_coord, sensor_coord, angle, segment, mode):
        self.number = number
        self.light_coord = light_coord
        self.sensor_coord = sensor_coord
        self.light = "red"
        self.light_used = False
        self.sensor_used = False
        self.light_on = False
        self.sensor_on = False

        self.direction = math.radians(angle) # direction in radians, angle in degrees
        self.top_light_coord = move_point_by_angle(light_coord, 5, self.direction)
        self.bottom_light_coord = light_coord
        self.base_coord = move_point_by_angle(light_coord, -5, self.direction)
        self.top_light = "red"

        # set mode of semaphore
        if mode == 1:
            self.bottom_light = "red"
        elif mode == 2:
            self.bottom_light = "off"

        self.segment = segment
        self.fore_run_end = light_coord
        self.request = 0
        self.time_request = 0

    def save(self):
        if self.bottom_light == "off": mode = 2
        else: mode = 1

        return str(self.number) + "\t" + str(self.light_coord[0]) + "\t" + str(self.light_coord[1]) + "\t" + str(self.sensor_coord[0]) + "\t" + str(self.sensor_coord[1]) + "\t" + str(int(math.degrees(self.direction))) + "\t" + str(mode) + "\n"

    def is_pressed(self, click):
    # check if the light button is pressed
        return dist_two_points(self.light_coord, click) < 5

    def logic(self):
    # check state of all lights and decide if it is safe to let the train run
        if self.bottom_light == "off":
            if self.top_light == "blue":
                self.light = "red"
            else:
                self.light = self.top_light
        else:
            if self.top_light == "red" or self.top_light == "blue" or self.bottom_light == "red":
                self.light = "red"
            elif self.top_light == "green" and self.bottom_light == "green":
                self.light = "green"
            else:
                self.light = "yellow"

    def change_light(self):
    # change color of the light
        if self.bottom_light == "red": self.bottom_light = "green"
        elif self.bottom_light == "green": self.bottom_light = "red"

        self.logic()

    def change_auto(self):
    # change semaphore to auto mode
        if self.bottom_light == "off": self.bottom_light = "red"
        else: self.bottom_light = "off"

        self.logic()

    def draw(self, win, offset_x, offset_y, scale):
        # draw base
        radius = 1
        if self.request: radius = 0
        pygame.draw.circle(win, WHITE, move_point(self.base_coord, offset_x, offset_y, scale), 4*scale, radius)
        # if self.light == "green": color = GREEN
        # elif self.light == "yellow": color = YELLOW
        # else: color = RED
        # pygame.draw.circle(win, color, move_point(self.base_coord, offset_x, offset_y, scale), 4*scale, 1)

        # draw bottom light
        radius = 0
        if self.bottom_light == "green": color = GREEN
        elif self.bottom_light == "yellow": color = YELLOW
        elif self.bottom_light == "off":
            color = WHITE
            radius = 1
        else: color = RED
        pygame.draw.circle(win, color, move_point(self.bottom_light_coord, offset_x, offset_y, scale), 4*scale, radius)

        # draw top light
        if self.top_light == "green": color = GREEN
        elif self.top_light == "yellow": color = YELLOW
        elif self.top_light == "blue": color = BLUE
        else: color = RED
        pygame.draw.circle(win, color, move_point(self.top_light_coord, offset_x, offset_y, scale), 4*scale, 0)

    def fore_run(self, dict_with_segments, dict_with_semaphores, dict_with_carriages, reservation_list):
    # function that checkes if the track in front of the train is free

        # run fore-run only when engine ask for it
        if self.request:

            max_steps = 200
            stop_next_semaphore = False
            stop_track_occuped = False
            stop_track_reserved = False
            temp_reservation_list = [] # temporary list with reserved segments - one entry [segment, ghost_engine_pos, ghost_engine_id]

            # make test engine
            # ghost_engine = Engine(0, self.light_coord.copy(), self.direction, self.segment)
            ghost_engine = Engine(self.request, self.light_coord.copy(), self.direction, self.segment)
            # set speed of the test engine
            ghost_engine.v_current = 15

            # run fore-run
            for step in range(max_steps+1):

                # move ghost engine
                ghost_engine.move(dict_with_segments)

                # temp_reservation_list.append([ghost_engine.segment, ghost_engine.coord.copy(), self.request])

                # check colision with carriages
                # if ghost_engine.is_segment_occupied(dict_with_carriages):
                if ghost_engine.is_collision(dict_with_carriages):
                    self.top_light = "red"
                    stop_track_occuped = True
                    break
                # smart-check of segments' ends and segments' conections' errors
                if ghost_engine.state == "broken":
                    self.top_light = "yellow"
                    break
                # looking for next semaphore
                for semaphore_id in dict_with_semaphores:
                    if dict_with_semaphores[semaphore_id].segment == ghost_engine.segment \
                    and (dict_with_semaphores[semaphore_id].direction == ghost_engine.angle \
                    or dict_with_semaphores[semaphore_id].direction == ghost_engine.angle + 2*math.pi \
                    or dict_with_semaphores[semaphore_id].direction + 2*math.pi == ghost_engine.angle) \
                    and dist_two_points(dict_with_semaphores[semaphore_id].light_coord, ghost_engine.coord) < 10:
                        stop_next_semaphore = True
                        break
                # checking track reservation
                for entry in reservation_list:
                    if ghost_engine.segment == entry[0] and self.request != entry[2]:
                        stop_track_reserved = True
                        break

                # break main loop
                if stop_next_semaphore:
                    self.top_light = "green"
                    break # break main loop
                if stop_track_reserved:
                    self.top_light = "blue"
                    break # break main loop

            if step == max_steps:
                self.top_light = "yellow" # reached endo of track

            # if self.request and not stop_track_reserved:
            # if not stop_track_reserved:
                # reservation_list = reservation_list + temp_reservation_list # reserve track

            self.fore_run_end = ghost_engine.coord.copy()
            self.request = 0

        else:
            self.top_light = "red"

        self.logic()

        # return reservation_list

class Control_box:
    def __init__(self, id, coord, segment, semaphores, mode):
        self.id = id
        self.coord = coord
        self.segment = segment
        self.semaphores = semaphores

        self.last_engine = 0

        # set mode of control box
        if mode == 0:
            self.mode = "off"
        elif mode == 1:
            self.mode = "reverse"
        elif mode == 2:
            self.mode = "wait_10"
        elif mode == 3:
            self.mode = "wait_30"
        elif mode == 100:
            self.mode = "cargo_off"
        elif mode == 101:
            self.mode = "cargo_empty"
        elif mode == 102:
            self.mode = "cargo_full"
        elif mode == 103:
            self.mode = "cargo_random"

    def save(self):
        if self.mode == "off": mode = 0
        elif self.mode == "reverse": mode = 1
        elif self.mode == "wait_10": mode = 2
        elif self.mode == "wait_30": mode = 3
        elif self.mode == "cargo_off": mode = 100
        elif self.mode == "cargo_empty": mode = 101
        elif self.mode == "cargo_full": mode = 102
        elif self.mode == "cargo_random": mode = 103
        else: mode = 0

        return str(self.id) + "\t" + str(self.coord[0]) + "\t" + str(self.coord[1]) + "\t" + str(mode) + "\n"

    def draw(self, win, offset_x, offset_y, scale):
        radius = 4
        border = 0
        if self.mode == "off" or self.mode == "cargo_off":
            color = WHITE
            border = 1
        elif self.mode == "reverse": color = YELLOW
        elif self.mode == "wait_10": color = ORANGE
        elif self.mode == "wait_30": color = RED
        elif self.mode == "cargo_empty": color = SILVER
        elif self.mode == "cargo_full": color = DARKSTEELGRAY
        elif self.mode == "cargo_random": color = DEEPPINK
        else: color = RED

        pygame.draw.rect(win, color, [*move_point(self.coord, offset_x-radius, offset_y-radius, scale), 2*radius*scale, 2*radius*scale], border)

    def is_pressed(self, click):
    # check if the control box is pressed
        return dist_two_points(self.coord, click) < 5

    def change_mode(self):
    # change mode of the box
        if self.mode == "off": self.mode = "reverse"
        elif self.mode == "reverse": self.mode = "wait_10"
        elif self.mode == "wait_10": self.mode = "wait_30"
        elif self.mode == "wait_30":
            self.mode = "off"
            self.current_engine = 0
            self.last_engine = 0

        if self.mode == "cargo_off": self.mode = "cargo_empty"
        elif self.mode == "cargo_empty": self.mode = "cargo_full"
        elif self.mode == "cargo_full": self.mode = "cargo_random"
        elif self.mode == "cargo_random":
            self.mode = "cargo_off"
            self.current_engine = 0
            self.last_engine = 0

    def run(self, dict_with_carriages, dict_with_semaphores, dict_with_panels):
    # control the engine
        if self.mode != "off":
            self.current_engine = 0
            # find engine on the same track ac control box
            for engine_id in dict_with_panels:
                if dict_with_carriages[engine_id].segment == self.segment:
                    self.current_engine = engine_id
                    if self.mode == "reverse": self.reverse_and_wait(dict_with_carriages, dict_with_semaphores, 10)
                    elif self.mode == "wait_10": self.wait(dict_with_carriages, dict_with_semaphores, 10)
                    elif self.mode == "wait_30": self.wait(dict_with_carriages, dict_with_semaphores, 30)
                    elif self.mode == "cargo_empty": self.unload(dict_with_carriages)
                    elif self.mode == "cargo_full": self.load(dict_with_carriages)
                    elif self.mode == "cargo_random": self.load_random(dict_with_carriages)

            if not self.current_engine: self.last_engine = 0

    def reverse(self, dict_with_carriages):
        engine = dict_with_carriages[self.current_engine]
        if engine.state == "stop" and engine.engine_id != self.last_engine:
            engine.flip(dict_with_carriages)
            self.last_engine = self.current_engine

    def reverse_and_wait(self, dict_with_carriages, dict_with_semaphores, wait_time):
        engine = dict_with_carriages[self.current_engine]
        if engine.state == "stop" and engine.engine_id != self.last_engine:
            engine.flip(dict_with_carriages)
            engine.wait(wait_time)
            self.change_semaphore(dict_with_semaphores, engine)
            self.last_engine = self.current_engine

    def wait(self, dict_with_carriages, dict_with_semaphores, wait_time):
        engine = dict_with_carriages[self.current_engine]
        if engine.state == "stop" and engine.engine_id != self.last_engine:
            engine.wait(wait_time)
            self.change_semaphore(dict_with_semaphores, engine)
            self.last_engine = self.current_engine

    def load(self, dict_with_carriages):
        for carriage_id in dict_with_carriages:
            if dict_with_carriages[carriage_id].segment == self.segment and dict_with_carriages[carriage_id].state == "stop":
                dict_with_carriages[carriage_id].load()

    def unload(self, dict_with_carriages):
        for carriage_id in dict_with_carriages:
            if dict_with_carriages[carriage_id].segment == self.segment and dict_with_carriages[carriage_id].state == "stop":
                dict_with_carriages[carriage_id].unload()

    def load_random(self, dict_with_carriages):
        for carriage_id in dict_with_carriages:
            if dict_with_carriages[carriage_id].segment == self.segment and dict_with_carriages[carriage_id].state == "stop":
                dict_with_carriages[carriage_id].load_random()

    def change_semaphore(self, dict_with_semaphores, engine):
        for semaphore_id in self.semaphores:
            if (dict_with_semaphores[semaphore_id].direction == engine.angle \
            or dict_with_semaphores[semaphore_id].direction == engine.angle + 2*math.pi \
            or dict_with_semaphores[semaphore_id].direction + 2*math.pi == engine.angle):
                dict_with_semaphores[semaphore_id].bottom_light = "yellow"
                dict_with_semaphores[semaphore_id].logic()
