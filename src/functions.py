import os
import random

from classes_world import *
from classes_vehicles import *
from classes_interface import *
from settings import *
from functions_math import *

def load_from_file():
# function that load data from file in Trains_2015 standard and convert to an object-oriented structure

    # open file
    # try:
    if 1:
        # try to open file
        map_file = open(os.path.join("maps","map.txt"), "r")

        # read numbers of world building elements
        number_of_points, number_of_segments, number_of_track_switches, number_of_semaphores = map_file.readline().split()
        number_of_points = int(number_of_points)
        number_of_segments = int(number_of_segments)
        number_of_track_switches = int(number_of_track_switches)
        number_of_semaphores = int(number_of_semaphores)

        # read empty line
        map_file.readline()

        # read points
        dict_with_points = {}
        for _ in range(number_of_points):
            id, x, y, segment1, segment2 = [int(i) for i in map_file.readline().split()]
            # (self, number, coord, segment1, segment2)
            dict_with_points[id] = Point(id, (x, y), segment1, segment2)

        # read empty line
        map_file.readline()

        # read segments
        dict_with_segments = {}
        for _ in range(number_of_segments):
            id, point1_id, point2_id = [int(i) for i in map_file.readline().split()]

            # check which segments are preceding and which are following
            if dict_with_points[point1_id].segment1 == id: segment1_id = dict_with_points[point1_id].segment2
            elif dict_with_points[point1_id].segment2 == id: segment1_id = dict_with_points[point1_id].segment1
            # else: print(str(id) + " segment1 error")
            #     raise Exception

            if dict_with_points[point2_id].segment1 == id: segment2_id = dict_with_points[point2_id].segment2
            elif dict_with_points[point2_id].segment2 == id: segment2_id = dict_with_points[point2_id].segment1
            # else:
            #     print(id + " segment2 error")
            #     raise Exception

            # (self, id, point1, point2, segment1, segment2)
            dict_with_segments[id] = Segment(id, dict_with_points[point1_id].coord, dict_with_points[point2_id].coord, segment1_id, segment2_id)

        # read empty line
        map_file.readline()

        # read track switches
        dict_with_track_switches = {}
        for _ in range(number_of_track_switches):
            number, x, y, first, active, passive, point = [int(i) for i in map_file.readline().split()]
            # (self, number, coord, first, active, passive)
            dict_with_track_switches[number] = Track_switch(number, (x, y), first, active, passive)
            dict_with_segments[passive].state = "passive"

        # check correctness of passive segments
        for switch_id in dict_with_track_switches:
            if dict_with_segments[dict_with_track_switches[switch_id].passive].segment1 != dict_with_track_switches[switch_id].first:
                if dict_with_segments[dict_with_track_switches[switch_id].passive].segment2 != dict_with_track_switches[switch_id].first:
                    if dist_two_points(dict_with_segments[dict_with_track_switches[switch_id].passive].point1, dict_with_segments[dict_with_track_switches[switch_id].first].point1) < 1:
                        dict_with_segments[dict_with_track_switches[switch_id].passive].segment1 = dict_with_track_switches[switch_id].first
                    if dist_two_points(dict_with_segments[dict_with_track_switches[switch_id].passive].point1, dict_with_segments[dict_with_track_switches[switch_id].first].point2) < 1:
                        dict_with_segments[dict_with_track_switches[switch_id].passive].segment1 = dict_with_track_switches[switch_id].first
                    if dist_two_points(dict_with_segments[dict_with_track_switches[switch_id].passive].point2, dict_with_segments[dict_with_track_switches[switch_id].first].point1) < 1:
                        dict_with_segments[dict_with_track_switches[switch_id].passive].segment2 = dict_with_track_switches[switch_id].first
                    if dist_two_points(dict_with_segments[dict_with_track_switches[switch_id].passive].point2, dict_with_segments[dict_with_track_switches[switch_id].first].point2) < 1:
                        dict_with_segments[dict_with_track_switches[switch_id].passive].segment2 = dict_with_track_switches[switch_id].first
                    # dict_with_segments[dict_with_track_switches[switch_id].passive].state = "wrong"
                    # print(str(switch_id)+" "+str(dict_with_track_switches[switch_id].passive))

        # read empty line
        map_file.readline()

        # read semaphores
        dict_with_semaphores = {}
        for _ in range(number_of_semaphores):
            id, x_light, y_light, x_sensor, y_sensor  = [int(i) for i in map_file.readline().split()]
            # (self, njumber, light_coord, sensor_coord)
            dict_with_semaphores[id] = Semaphore(id, (x_light, y_light), (x_sensor, y_sensor))

        # close file
        map_file.close()

        # return dictionaries with data
        return dict_with_segments, dict_with_track_switches, dict_with_semaphores

    # except:
    #     print("Map error")
    #     quit()

def load_from_file_v2():
# function that load data from file in Trains_2022 standard

    # open file
    # try:
    if 1:
        # try to open file
        map_file = open(os.path.join("maps","new_map.txt"), "r")

        # read empty line
        map_file.readline()

        # read numbers of world building elements
        number_of_segments, number_of_track_switches, number_of_semaphores, number_of_control_boxes = map_file.readline().split()
        number_of_segments = int(number_of_segments)
        number_of_track_switches = int(number_of_track_switches)
        number_of_semaphores = int(number_of_semaphores)
        number_of_control_boxes = int(number_of_control_boxes)

        # read empty line
        map_file.readline()
        map_file.readline()
        map_file.readline()

        # read segments
        dict_with_segments = {}
        for _ in range(number_of_segments):
            id, point1_x, point1_y, point2_x, point2_y, segment1, segment2 = [int(i) for i in map_file.readline().split()]

            # (self, id, point1, point2, segment1, segment2)
            dict_with_segments[id] = Segment(id, [point1_x, point1_y], [point2_x, point2_y], segment1, segment2)

        # read empty line
        map_file.readline()
        map_file.readline()
        map_file.readline()

        # read track switches
        dict_with_track_switches = {}
        for _ in range(number_of_track_switches):
            number, x, y, first, active, passive = [int(i) for i in map_file.readline().split()]
            # (self, number, coord, first, active, passive)
            dict_with_track_switches[number] = Track_switch(number, [x, y], first, active, passive)
            dict_with_segments[passive].state = "passive"

        # read empty line
        map_file.readline()
        map_file.readline()
        map_file.readline()

        # read semaphores
        dict_with_semaphores = {}
        for _ in range(number_of_semaphores):
            id, x_light, y_light, x_sensor, y_sensor, angle, mode  = [int(i) for i in map_file.readline().split()]
            # (self, number, light_coord, sensor_coord, angle, segment, mode)
            dict_with_semaphores[id] = Semaphore(id, [x_light, y_light], [x_sensor, y_sensor], angle, which_segment(dict_with_segments, [x_light, y_light], 1), mode)

        # read empty line
        map_file.readline()
        map_file.readline()
        map_file.readline()

        # read control boxes
        dict_with_control_boxes = {}
        for _ in range(number_of_control_boxes):
            id, coord_x, coord_y, mode = [int(i) for i in map_file.readline().split()]

            segment = which_segment(dict_with_segments, [coord_x, coord_y], 2)
            semaphores = []
            for semaphore_id in dict_with_semaphores:
                if dict_with_semaphores[semaphore_id].segment == segment:
                    semaphores.append(semaphore_id)

            # (self, id, coord, segment, semaphores, mode)
            dict_with_control_boxes[id] = Control_box(id, [coord_x, coord_y], segment, semaphores, mode)

        # close file
        map_file.close()

        # return dictionaries with data
        return dict_with_segments, dict_with_track_switches, dict_with_semaphores, dict_with_control_boxes

    # except:
    #     print("Map error")
    #     quit()

def make_test_trains(dict_with_segments):
    id = 1
    dict = {}
    dict_panels = {}
    list_with_engines = []
    number_of_cargo_trains = 5
    number_of_passenger_trains = 2
    number_of_multiple_units_tracks = 1
    number_of_multiple_units_one_track = 1

    # engines for cargo
    for i in range(number_of_cargo_trains):
        # dict[id] = Engine(id, [230, 10+10*i], 0, which_segment(dict_with_segments, [230, 10+10*i], 2))
        # dict[id] = Engine(id, [220 + random.randint(0,10), 10+10*i], 0, which_segment(dict_with_segments, [230, 10+10*i], 2))
        new_coord = [10 + 25*i + random.randint(0,15), -80+10*i]
        dict[id] = Engine(id, new_coord, 0, which_segment(dict_with_segments, new_coord, 2))
        dict_panels[id] = Control_panel(id, (WIN_WIDTH, 29*i))
        list_with_engines.append(id)
        id += 1

    # engines for passangers
    for i in range(number_of_passenger_trains):
        new_coord = [190 + random.randint(0,10), 10+10*i]
        dict[id] = Engine(id, new_coord, 0, which_segment(dict_with_segments, new_coord, 2))
        dict_panels[id] = Control_panel(id, (WIN_WIDTH, 29*(len(list_with_engines))))
        list_with_engines.append(id)
        id += 1

    # carriages for cargo
    for i in range(number_of_cargo_trains):
        offset = random.randint(0,10)
        for j in range(12 + random.randint(0,6)):
            # dict[id] = Carriage(id, [30+22*j, 10+10*i], 0, which_segment(dict_with_segments, [230, 10+10*i], 2))
            # dict[id] = Carriage(id, [-80 + 22*j + offset , 10+10*i], 0, which_segment(dict_with_segments, [230, 10+10*i], 2))
            new_coord = [-420 + 25*i + 22*j + offset, -80+10*i]
            dict[id] = Carriage_cargo_container(id, new_coord, 0, which_segment(dict_with_segments, new_coord, 2))
            id += 1

    # carriages for passengers
    for i in range(number_of_passenger_trains):
        offset = random.randint(0,10)
        for j in range(5 + random.randint(0,2)):
            new_coord = [-50 + 32*j + offset , 10+10*i]
            dict[id] = Carriage_passenger(id, new_coord, 0, which_segment(dict_with_segments, new_coord, 2))
            id += 1

    # oldtime carriages for passengers
    for i in range(5):
        new_coord = [-50 + 32*i, 40]
        dict[id] = Carriage_oldtimer(id, new_coord, 0, which_segment(dict_with_segments, new_coord, 2))
        id += 1

    # multiple units
    for i in range(number_of_multiple_units_tracks):
        for j in range(number_of_multiple_units_one_track):
            offset = random.randint(0,10)
            # engines
            new_coord = [200 - 25*i- 180*j + offset , -10-10*i]
            dict[id] = Multiple_unit1_engine(id, new_coord, 0, which_segment(dict_with_segments, new_coord, 2))
            dict_panels[id] = Control_panel(id, (WIN_WIDTH, 29*(len(list_with_engines))))
            list_with_engines.append(id)
            id += 1

            # carriages 1
            new_coord = [200 - 32 - 25*i - 180*j + offset , -10-10*i]
            dict[id] = Multiple_unit1_carriage(id, new_coord, 0, which_segment(dict_with_segments, new_coord, 2))
            id += 1

            # carriages 2
            new_coord = [200 - 32*2 - 25*i - 180*j + offset , -10-10*i]
            dict[id] = Multiple_unit1_carriage(id, new_coord, 0, which_segment(dict_with_segments, new_coord, 2))
            id += 1

            # end
            new_coord = [200 - 32*3 - 25*i - 180*j + offset , -10-10*i]
            dict[id] = Multiple_unit1_end(id, new_coord, 0, which_segment(dict_with_segments, new_coord, 2))
            id += 1


    # EN57
    # engine
    new_coord = [190, 50]
    dict[id] = EN57_engine(id, new_coord, 0, which_segment(dict_with_segments, new_coord, 2))
    dict_panels[id] = Control_panel(id, (WIN_WIDTH, 29*(len(list_with_engines))))
    list_with_engines.append(id)
    id += 1

    # carriage
    new_coord = [190 - 32, 50]
    dict[id] = EN57_carriage(id, new_coord, 0, which_segment(dict_with_segments, new_coord, 2))
    id += 1

    # end
    new_coord = [190 - 32*2, 50]
    dict[id] = EN57_end(id, new_coord, 0, which_segment(dict_with_segments, new_coord, 2))
    id += 1


    # steam locomotive
    # tender
    new_coord = [170 - 27, 40]
    dict[id] = Steam_tender(id, new_coord, 0, which_segment(dict_with_segments, new_coord, 2))
    id += 1

    # engine
    new_coord = [170, 40]
    dict[id] = Steam_locomotive(id, new_coord, 0, which_segment(dict_with_segments, new_coord, 2))
    dict_panels[id] = Control_panel(id, (WIN_WIDTH, 29*(len(list_with_engines))))
    list_with_engines.append(id)
    id += 1


    return dict, dict_panels #, list_with_engines

def make_test_commuter_rail_trains(dict_with_carriages, dict_with_panels, dict_with_segments, orgin, angle, number_of_multiple_units_tracks, number_of_multiple_units_one_track, shift = 0):
    # make multiple units for commuter rail

    for i in range(number_of_multiple_units_tracks):
        for j in range(number_of_multiple_units_one_track):

            offset = random.randint(0,10)

            # engines
            id = empty_slot(dict_with_carriages.keys())
            # new_coord = [200 - 25*i- 180*j + offset , -10-10*i]
            new_coord = [orgin[0] + (offset - 180*j + shift*i) * math.cos(angle) + 10 * i * math.sin(angle), orgin[1] + (offset - 180*j + shift*i) * math.sin(angle) - 10 * i * math.cos(angle)]
            dict_with_carriages[id] = Multiple_unit1_engine(id, new_coord, angle, which_segment(dict_with_segments, new_coord, 2))
            dict_with_panels[id] = Control_panel(id, (WIN_WIDTH, 29*(len(dict_with_panels))))
            # list_with_engines.append(id)
            # id += 1

            # carriages 1
            id = empty_slot(dict_with_carriages.keys())
            # new_coord = [200 - 32 - 25*i - 180*j + offset , -10-10*i]
            new_coord = [orgin[0] + (offset - 180*j - 32 + shift*i) * math.cos(angle) + 10 * i * math.sin(angle), orgin[1] + (offset - 180*j  - 32 + shift*i) * math.sin(angle) - 10 * i * math.cos(angle)]
            dict_with_carriages[id] = Multiple_unit1_carriage(id, new_coord, angle, which_segment(dict_with_segments, new_coord, 2))
            # id += 1

            # carriages 2
            id = empty_slot(dict_with_carriages.keys())
            # new_coord = [200 - 32*2 - 25*i - 180*j + offset , -10-10*i]
            new_coord = [orgin[0] + (offset - 180*j  - 32*2 + shift*i) * math.cos(angle) + 10 * i * math.sin(angle), orgin[1] + (offset - 180*j  - 32*2 + shift*i) * math.sin(angle) - 10 * i * math.cos(angle)]
            dict_with_carriages[id] = Multiple_unit1_carriage(id, new_coord, angle, which_segment(dict_with_segments, new_coord, 2))
            # id += 1

            # end
            id = empty_slot(dict_with_carriages.keys())
            # new_coord = [200 - 32*3 - 25*i - 180*j + offset , -10-10*i]
            new_coord = [orgin[0] + (offset - 180*j  - 32*3 + shift*i) * math.cos(angle) + 10 * i * math.sin(angle), orgin[1] + (offset - 180*j  - 32*3 + shift*i) * math.sin(angle) - 10 * i * math.cos(angle)]
            dict_with_carriages[id] = Multiple_unit1_end(id, new_coord, angle, which_segment(dict_with_segments, new_coord, 2))
            # id += 1


def draw_test_platforms(win, offset_x, offset_y, scale):

    # //TomaszLand Zachodni
	# bar(24,270,27,550);
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((24,270), offset_x, offset_y, scale), 3*scale, 280*scale))

	# //TomaszLand MAIN STATION
	# bar(450,644,730,647);
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((450,644), offset_x, offset_y, scale), 280*scale,3*scale))
	# bar(450,664,730,667);
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((450,664), offset_x, offset_y, scale), 280*scale, 3*scale))
	# bar(450,684,730,687);
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((450,684), offset_x, offset_y, scale), 280*scale, 3*scale))
    # platform no. 4
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((450,704), offset_x, offset_y, scale), 280*scale, 3*scale))

	# //TomaszLand OLD WEST
	# //bar(1124,140,1127,420);
	# bar(1114,140,1117,420);
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((1114,140), offset_x, offset_y, scale), 3*scale, 280*scale))
	# bar(1134,140,1137,420);
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((1134,140), offset_x, offset_y, scale), 3*scale, 280*scale))

    # TomaszLand Polnoc
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((1314,-730), offset_x, offset_y, scale), 3*scale, 280*scale))
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((1334,-730), offset_x, offset_y, scale), 3*scale, 280*scale))

    # TomaszLand Powisle
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((1390,704), offset_x, offset_y, scale), 280*scale, 3*scale))

    # TomaszLand WEST STATION
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((2380,654), offset_x, offset_y, scale), 280*scale, 3*scale))
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((2380,674), offset_x, offset_y, scale), 280*scale, 3*scale))
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((2380,694), offset_x, offset_y, scale), 280*scale, 3*scale))
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((2380,714), offset_x, offset_y, scale), 280*scale, 3*scale))

    # TomaszLand NORTH DEPOT
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((1324,-1655), offset_x, offset_y, scale), 3*scale, 280*scale))

    # TomaszLand SOUTH 1
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((-321,1030), offset_x, offset_y, scale), 3*scale, 280*scale))

    # TomaszLand SOUTH 2
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((-321,1860), offset_x, offset_y, scale), 3*scale, 280*scale))


def draw_test_buildings(win, harbor, offset_x, offset_y, scale):
    pass

def which_segment(dict_with_segments, point, offset):
    for segment_id in dict_with_segments:
        if dist_to_segment(dict_with_segments[segment_id], point) < offset:
            return segment_id
    return 9999

def empty_slot(list):
    lenght = len(list)
    for i in range(1,lenght):
        if i not in list: return i
    return lenght+1
