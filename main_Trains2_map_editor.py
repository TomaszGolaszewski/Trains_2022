# Trains 2022 - map editor
# By Tomasz Golaszewski
# 07.2022

# Railway traffic control simulator written in an object-oriented way

import pygame
import time
import os

from sys import path
path.append('.\\src')

from settings import *
from classes_world import *
# from classes_vehicles import *
from classes_interface import *
from functions import *
from functions_editor import *

def run_editor():
# main function - runs the simulation

    # load data
    # DICT_WITH_SEGMENTS, DICT_WITH_TRACK_SWITCHES, DICT_WITH_SEMAPHORES = load_from_file()
    DICT_WITH_SEGMENTS, DICT_WITH_TRACK_SWITCHES, DICT_WITH_SEMAPHORES = load_from_file_v2()


    # initialize the pygame
    pygame.init()
    pygame.display.set_caption("Trains 2022")
    pygame.display.set_icon(ICON)
    WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    CLOCK = pygame.time.Clock()
    CURRENT_FRAME = 0

    # window variables
    OFFSET_VERTICAL = 0
    OFFSET_HORIZONTAL = 90
    SCALE = 1
    # WIN_MOD_PARAM = (OFFSET_VERTICAL, OFFSET_HORIZONTAL, SCALE)

    # resources for editor
    new_segment_on = False
    temp_segment = [0,0,0,0,0]
    del_segment_on = False
    new_switch_on = False
    temp_switch = [0,0,0,0,0]
    del_switch_on = False
    new_semaphore_on = False
    temp_semaphore = [0,0]

    move_segment_on = False
    temp_move_segment = [0,0]
    add_end_of_segment_on = False

    print_instructions()

    # main loop
    running = True
    while running:
        CLOCK.tick(FRAMERATE)
        CURRENT_FRAME += 1
        if CURRENT_FRAME == FRAMERATE:
            CURRENT_FRAME = 0
            # print("FPS: %.2f" % CLOCK.get_fps(), end="\t")
            # print("TIME: " + str(pygame.time.get_ticks() // 1000))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            # mouse
            if event.type == pygame.MOUSEBUTTONUP:
                # 1 - left click
                if event.button == 1:
                    if new_segment_on:
                        new_segment_on = add_segment(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), temp_segment, DICT_WITH_SEGMENTS)
                    if del_segment_on:
                        del_segment_on = del_segment(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), DICT_WITH_SEGMENTS)
                    if new_switch_on:
                        new_switch_on = add_switch(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), temp_switch, DICT_WITH_TRACK_SWITCHES, DICT_WITH_SEGMENTS)
                    if del_switch_on:
                        del_switch_on = del_switch(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), DICT_WITH_TRACK_SWITCHES)
                    if new_semaphore_on:
                        new_semaphore_on = add_semaphore(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), temp_semaphore, DICT_WITH_SEMAPHORES, DICT_WITH_SEGMENTS)

                    if move_segment_on:
                        move_segment_on = move_end_of_segment(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), temp_move_segment, DICT_WITH_SEGMENTS)
                    if add_end_of_segment_on:
                        add_end_of_segment_on = add_end_of_segment(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), DICT_WITH_SEGMENTS)


                    if not new_segment_on and not del_segment_on and not new_switch_on and not del_switch_on and not move_segment_on and not add_end_of_segment_on:
                        for switch_id in DICT_WITH_TRACK_SWITCHES:
                            if DICT_WITH_TRACK_SWITCHES[switch_id].is_switch_pressed(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)):
                                DICT_WITH_TRACK_SWITCHES[switch_id].switch_switch(DICT_WITH_SEGMENTS)
                    # for semaphore_id in DICT_WITH_SEMAPHORES:
                    #     if DICT_WITH_SEMAPHORES[semaphore_id].is_pressed(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)):
                    #         DICT_WITH_SEMAPHORES[semaphore_id].change_light()

                    # segment = which_segment(DICT_WITH_SEGMENTS, move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), 3)
                    # if segment: print(DICT_WITH_SEGMENTS[segment])

                    # print(str(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)))
                    print(str(myround_point(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE))))

                # 2 - middle click
                if event.button == 2:
                    # define new view center
                    mouse_pos = pygame.mouse.get_pos()
                    OFFSET_HORIZONTAL -= (mouse_pos[0] - WIN_WIDTH/2) / SCALE
                    OFFSET_VERTICAL -= (mouse_pos[1] - WIN_HEIGHT/2) / SCALE

                    OFFSET_HORIZONTAL = myround(OFFSET_HORIZONTAL)
                    OFFSET_VERTICAL = myround(OFFSET_VERTICAL)

                # 3 - right click
                if event.button == 3:
                    # semaphore manual control - on/off
                    if not new_segment_on and not del_segment_on and not new_switch_on and not del_switch_on and not move_segment_on and not add_end_of_segment_on:
                        for semaphore_id in DICT_WITH_SEMAPHORES:
                            if DICT_WITH_SEMAPHORES[semaphore_id].is_pressed(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)):
                                DICT_WITH_SEMAPHORES[semaphore_id].change_auto()

                # 4 - scroll up
                if event.button == 4:

                    old_scale = SCALE

                    SCALE += 1
                    if SCALE == 1.5: SCALE = 1

                    if old_scale - SCALE:
                        OFFSET_HORIZONTAL -= WIN_WIDTH/2 / old_scale - WIN_WIDTH/2 / SCALE
                        OFFSET_VERTICAL -= WIN_HEIGHT/2 / old_scale - WIN_HEIGHT/2 / SCALE

                        OFFSET_HORIZONTAL = myround(OFFSET_HORIZONTAL)
                        OFFSET_VERTICAL = myround(OFFSET_VERTICAL)

                # 5 - scroll down
                if event.button == 5:

                    old_scale = SCALE

                    SCALE -= 1
                    if SCALE <= 0: SCALE = 0.5

                    if old_scale - SCALE:
                        OFFSET_HORIZONTAL -= WIN_WIDTH/2 / old_scale - WIN_WIDTH/2 / SCALE
                        OFFSET_VERTICAL -= WIN_HEIGHT/2 / old_scale - WIN_HEIGHT/2 / SCALE

                        OFFSET_HORIZONTAL = myround(OFFSET_HORIZONTAL)
                        OFFSET_VERTICAL = myround(OFFSET_VERTICAL)


            # keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # manual close
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    # save the map
                    save_file_v2(DICT_WITH_SEGMENTS, DICT_WITH_TRACK_SWITCHES, DICT_WITH_SEMAPHORES)
                    running = False
                    pygame.quit()
                    quit()
                # add segment
                if event.key == pygame.K_1:
                    new_segment_on = True
                    temp_segment = [0,0,0,0,0]
                    print("Please select first point")
                # del segment
                if event.key == pygame.K_2:
                    del_segment_on = True
                    print("Please select segment to delete")
                # add track switch
                if event.key == pygame.K_3:
                    new_switch_on = True
                    temp_switch = [0,0,0,0,0]
                    print("Please select button")
                # del track switch
                if event.key == pygame.K_4:
                    del_switch_on = True
                    print("Please select button to delete")
                # add semaphore
                if event.key == pygame.K_5:
                    new_semaphore_on = True
                    temp_semaphore = [0,0]
                    print("Please select semaphore")

                # move end of segment
                if event.key == pygame.K_9:
                    move_segment_on = True
                    temp_move_segment = [0,0]
                    print("Please select point to move")
                # add end of segment
                if event.key == pygame.K_0:
                    add_end_of_segment_on = True
                    print("Please select segment to end")

        # keys that can be pressed multiple times
        keys_pressed=pygame.key.get_pressed()
        # move left
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            OFFSET_HORIZONTAL += 5
        # move right
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            OFFSET_HORIZONTAL -= 5
        # move up
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            OFFSET_VERTICAL += 5
        # move down
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            OFFSET_VERTICAL -= 5
        # center
        if keys_pressed[pygame.K_c]:
            OFFSET_HORIZONTAL = 0
            OFFSET_VERTICAL = 0
            SCALE = 1

        # clear screen
        WIN.fill(BLACK)

        # draw grid
        if SCALE >= 2: draw_grid(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw platforms
        draw_test_platforms(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw track layout
        for segment_id in DICT_WITH_SEGMENTS:
            DICT_WITH_SEGMENTS[segment_id].draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)
            DICT_WITH_SEGMENTS[segment_id].draw_ends(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw track switches
        for switch_id in DICT_WITH_TRACK_SWITCHES:
            DICT_WITH_TRACK_SWITCHES[switch_id].draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw semaphores
        for semaphore in DICT_WITH_SEMAPHORES:
            DICT_WITH_SEMAPHORES[semaphore].draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # flip the screen
        pygame.display.update()

if __name__ == "__main__":
    run_editor()

    # input("input any key")
