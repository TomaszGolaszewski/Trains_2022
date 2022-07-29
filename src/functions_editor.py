from classes_world import *

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
