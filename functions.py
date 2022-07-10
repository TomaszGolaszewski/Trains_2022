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
        number_of_points, number_of_segments, number_of_track_switches = map_file.readline().split()
        number_of_points = int(number_of_points)
        number_of_segments = int(number_of_segments)
        number_of_track_switches = int(number_of_track_switches)

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

        # close file
        map_file.close()

        # return dictionaries with data
        return dict_with_segments, dict_with_track_switches

    # except:
    #     print("Map error")
    #     quit()

def make_test_trains(dict_with_segments):
    id = 0
    dict = {}
    list_with_engines = []

    for i in range(5):
        dict[id] = Engine(id, [230, 10+10*i], 0, which_segment(dict_with_segments, [230, 10+10*i], 2))
        list_with_engines.append(id)
        id += 1

    for i in range(5):
        for j in range(9):
            dict[id] = Carriage(id, [30+20*j, 10+10*i], 0, which_segment(dict_with_segments, [230, 10+10*i], 2))
            id += 1

    dict[1].v_target = 5
    dict[1].state = "move"
    return dict, list_with_engines

def which_segment(dict_with_segments, point, offset):
    for segment_id in dict_with_segments:
        if dist_to_segment(dict_with_segments[segment_id], point) < offset:
            return segment_id
