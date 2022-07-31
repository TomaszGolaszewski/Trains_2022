from classes_world import *
from functions import *

def save_file_v2(dict_with_segments, dict_with_track_switches, dict_with_semaphores):
# function that save data into file in Trains_2022 standard

    # open file
    # try:
    if 1:
        # try to open file
        map_file = open(os.path.join("maps","new_map.txt"), "w")

        # count numbers of world building elements
        number_of_segments = len(dict_with_segments)
        number_of_track_switches = len(dict_with_track_switches)
        number_of_semaphores = len(dict_with_semaphores)

        # write numbers of world building elements
        map_file.write("number_of_segments\tnumber_of_track_switches\tnumber_of_semaphores\n")
        map_file.write(str(number_of_segments) + "\t" + str(number_of_track_switches) + "\t" + str(number_of_semaphores) + "\n")

        # write empty line
        map_file.write("\n")

        # write segments
        map_file.write("segments\n")
        map_file.write("id\tpoint1_x\tpoint1_y\tpoint2_x\tpoint2_y\tsegment1\tsegment2\n")
        for segment_id in dict_with_segments:
            map_file.write(dict_with_segments[segment_id].save())

        # write empty line
        map_file.write("\n")

        # write track switches
        map_file.write("track switches\n")
        map_file.write("id\tbutton_x\tbutton_y\tsegment_first\tsegment_active\tsegment_passive\n")
        for switch_id in dict_with_track_switches:
            map_file.write(dict_with_track_switches[switch_id].save())

        # write empty line
        map_file.write("\n")

        # write semaphores
        map_file.write("semaphores\n")
        map_file.write("id\tlight_coord_x\tlight_coord_y\tsensor_coord_x\tsensor_coord_y\n")
        for semaphore_id in dict_with_semaphores:
            map_file.write(dict_with_semaphores[semaphore_id].save())

        # close file
        map_file.close()

def draw_grid(win, offset_x, offset_y, scale):
    for x in range(WIN_WIDTH//10):
        # pygame.draw.line(win, DARKSTEELGRAY, move_point((x*10, 0), offset_x, offset_y, scale), move_point((x*10, WIN_HEIGHT), offset_x, offset_y, scale), 1)
        pygame.draw.line(win, DARKSTEELGRAY, (x*10*scale, 0), (x*10*scale, WIN_HEIGHT*scale), 1)
    for y in range(WIN_HEIGHT//10):
        pygame.draw.line(win, DARKSTEELGRAY, (0, y*10*scale), (WIN_WIDTH*scale, y*10*scale), 1)

def add_segment(coord, temp_list, dict_with_segments):
    if temp_list[0] == 0:
        temp_list[1] = myround_point(coord)
        print("Please select second point")
    elif temp_list[0] == 1:
        temp_list[2] = myround_point(coord)
        print("Please select first segment")
    elif temp_list[0] == 2:
        segment1 = which_segment(dict_with_segments, coord, 5)
        if not segment1: segment1 = 9999
        temp_list[3] = segment1
        print("Please select second segment")
    elif temp_list[0] == 3:
        segment2 = which_segment(dict_with_segments, coord, 5)
        if not segment2: segment2 = 9999
        temp_list[4] = segment2
        new_id = empty_slot(dict_with_segments.keys())
        dict_with_segments[new_id] = Segment(new_id, *temp_list[1:])

        if temp_list[3] != 9999:
            if dict_with_segments[temp_list[3]].segment1 == 9999 and dist_two_points(dict_with_segments[temp_list[3]].point1, temp_list[1]) < 1:
                dict_with_segments[temp_list[3]].segment1 = new_id
            if dict_with_segments[temp_list[3]].segment2 == 9999 and dist_two_points(dict_with_segments[temp_list[3]].point2, temp_list[1]) < 1:
                dict_with_segments[temp_list[3]].segment2 = new_id
        if temp_list[4] != 9999:
            if dict_with_segments[temp_list[4]].segment1 == 9999 and dist_two_points(dict_with_segments[temp_list[4]].point1, temp_list[2]) < 1:
                dict_with_segments[temp_list[3]].segment1 = new_id
            if dict_with_segments[temp_list[4]].segment2 == 9999 and dist_two_points(dict_with_segments[temp_list[4]].point2, temp_list[2]) < 1:
                dict_with_segments[temp_list[3]].segment2 = new_id
        print("New segment " + str(new_id) + " has been added")

    temp_list[0] += 1
    if temp_list[0] >= 4:
        temp_list[0] = 0
        return False
    else: return True

def add_switch(coord, temp_list, dict_with_track_switches, dict_with_segments):
    if temp_list[0] == 0:
        temp_list[1] = myround_point(coord)
        print("Please select first segment")
    elif temp_list[0] == 1:
        segment_first = which_segment(dict_with_segments, coord, 5)
        if not segment_first: segment_first = 9999
        temp_list[2] = segment_first
        print("Please select active segment")
    elif temp_list[0] == 2:
        segment_active = which_segment(dict_with_segments, coord, 5)
        if not segment_active: segment_active = 9999
        temp_list[3] = segment_active
        print("Please select passive segment")
    elif temp_list[0] == 3:
        segment_passive = which_segment(dict_with_segments, coord, 5)
        if not segment_passive: segment_passive = 9999
        temp_list[4] = segment_passive
        new_id = empty_slot(dict_with_track_switches.keys())
        dict_with_track_switches[new_id] = Track_switch(new_id, *temp_list[1:])
        print("New track switch " + str(new_id) + " has been added")

    temp_list[0] += 1
    if temp_list[0] >= 4:
        temp_list[0] = 0
        return False
    else: return True
