import os

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

def load_from_file_2():
    pass

def make_test_trains(dict_with_segments):
    id = 0
    dict = {}
    list_with_engines = []

    for i in range(5):
        dict[id] = Engine(id, [230, 10+10*i], 0, which_segment(dict_with_segments, [230, 10+10*i], 2))
        dict[id].set_new_bar_orgin((1150,29*i))
        list_with_engines.append(id)
        id += 1

    for i in range(5):
        for j in range(8):
            dict[id] = Carriage(id, [30+22*j, 10+10*i], 0, which_segment(dict_with_segments, [230, 10+10*i], 2))
            id += 1

    return dict, list_with_engines

def draw_test_platforms(win, offset_x, offset_y, scale):

    # //TomaszLand Zachodni
	# bar(24,270,27,550);
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((24,270), offset_x, offset_y, scale), 3*scale, 280*scale))

	# //TomaszLand Centralny
	# bar(450,644,730,647);
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((450,644), offset_x, offset_y, scale), 280*scale,3*scale))
	# bar(450,664,730,667);
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((450,664), offset_x, offset_y, scale), 280*scale, 3*scale))
	# bar(450,684,730,687);
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((450,684), offset_x, offset_y, scale), 280*scale, 3*scale))

	# //TomaszLand Wschodni
	# //bar(1124,140,1127,420);
	# bar(1114,140,1117,420);
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((1114,140), offset_x, offset_y, scale), 3*scale, 280*scale))
	# bar(1134,140,1137,420);
    pygame.draw.rect(win, LIGHTSLATEGRAY, (*move_point((1134,140), offset_x, offset_y, scale), 3*scale, 280*scale))

def which_segment(dict_with_segments, point, offset):
    for segment_id in dict_with_segments:
        if dist_to_segment(dict_with_segments[segment_id], point) < offset:
            return segment_id
