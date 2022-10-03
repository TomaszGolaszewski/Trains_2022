# Trains 2022
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
from classes_vehicles import *
from classes_interface import *
from functions import *

def run():
# main function - runs the simulation

    # load data
    DICT_WITH_SEGMENTS, DICT_WITH_TRACK_SWITCHES, DICT_WITH_SEMAPHORES, DICT_WITH_CONTROL_BOXES = load_from_file_v2()

    # make test TRAINS
    DICT_WITH_CARRIAGES, DICT_WITH_PANELS, LIST_WITH_ENGINES = make_test_trains(DICT_WITH_SEGMENTS)

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

    center_mark = 100 # center mark radius counter
    last_engine_to_show = 0 # variables to check on which train to centre on

    # for tests only
    # box1 = Control_box((20,410), which_segment(DICT_WITH_SEGMENTS, (20,410), 2), 0)
    # box2 = Control_box((30,410), which_segment(DICT_WITH_SEGMENTS, (30,410), 2), 0)

    # main loop
    running = True
    while running:
        CLOCK.tick(FRAMERATE)
        CURRENT_FRAME += 1
        if CURRENT_FRAME == FRAMERATE:
            CURRENT_FRAME = 0
            print("FPS: %.2f" % CLOCK.get_fps(), end="\t")
            print("TIME: " + str(pygame.time.get_ticks() // 1000))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

            # mouse
            if event.type == pygame.MOUSEBUTTONUP:
                # 1 - left click
                if event.button == 1:
                    # click on carriage
                    for carriage_id in DICT_WITH_CARRIAGES:
                        engine_id = DICT_WITH_CARRIAGES[carriage_id].engine_id
                        if engine_id:
                            if dist_two_points(DICT_WITH_CARRIAGES[engine_id].coord, move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)) < 10:
                                DICT_WITH_PANELS[engine_id].size = "L"

                    # engines control
                    # for engine_id in LIST_WITH_ENGINES:
                    #     pass
                    for engine_id in DICT_WITH_PANELS:
                        DICT_WITH_PANELS[engine_id].press(DICT_WITH_CARRIAGES, pygame.mouse.get_pos())

                    # switches control
                    for switch_id in DICT_WITH_TRACK_SWITCHES:
                        if DICT_WITH_TRACK_SWITCHES[switch_id].is_switch_pressed(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)):
                            DICT_WITH_TRACK_SWITCHES[switch_id].switch_switch(DICT_WITH_SEGMENTS)

                    # semaphore manual control - red/green
                    for semaphore_id in DICT_WITH_SEMAPHORES:
                        if DICT_WITH_SEMAPHORES[semaphore_id].is_pressed(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)):
                            DICT_WITH_SEMAPHORES[semaphore_id].change_light()

                    # control boxes
                    for control_box_id in DICT_WITH_CONTROL_BOXES:
                        if DICT_WITH_CONTROL_BOXES[control_box_id].is_pressed(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)):
                            DICT_WITH_CONTROL_BOXES[control_box_id].change_mode()

                    segment = which_segment(DICT_WITH_SEGMENTS, move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), 2)
                    if segment and segment != 9999: print(DICT_WITH_SEGMENTS[segment])

                    # print(str(pygame.mouse.get_pos()))

                # 2 - middle click
                if event.button == 2:
                    # define new view center
                    mouse_pos = pygame.mouse.get_pos()
                    OFFSET_HORIZONTAL -= (mouse_pos[0] - WIN_WIDTH/2) / SCALE
                    OFFSET_VERTICAL -= (mouse_pos[1] - WIN_HEIGHT/2) / SCALE
                    # center_mark = 1

                # 3 - right click
                if event.button == 3:
                    # semaphore manual control - on/off
                    for semaphore_id in DICT_WITH_SEMAPHORES:
                        if DICT_WITH_SEMAPHORES[semaphore_id].is_pressed(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)):
                            DICT_WITH_SEMAPHORES[semaphore_id].change_auto()

                # 4 - scroll up
                if event.button == 4:

                    old_scale = SCALE
                    # mouse_pos = pygame.mouse.get_pos()

                    SCALE += 0.25
                    # if SCALE == 1.5: SCALE = 1
                    # elif SCALE == 1.25: SCALE = 0.5
                    if SCALE >= 3: SCALE = 3

                    if old_scale - SCALE:
                        # OFFSET_HORIZONTAL -= mouse_pos[0] / old_scale - WIN_WIDTH/2 / SCALE
                        # OFFSET_VERTICAL -= mouse_pos[1] / old_scale - WIN_HEIGHT/2 / SCALE
                        OFFSET_HORIZONTAL -= WIN_WIDTH/2 / old_scale - WIN_WIDTH/2 / SCALE
                        OFFSET_VERTICAL -= WIN_HEIGHT/2 / old_scale - WIN_HEIGHT/2 / SCALE

                # 5 - scroll down
                if event.button == 5:

                    old_scale = SCALE
                    mouse_pos = pygame.mouse.get_pos()

                    SCALE -= 0.25
                    # if SCALE == 0: SCALE = 0.5
                    # elif SCALE == -0.5: SCALE = 0.25
                    if SCALE <= 0: SCALE = 0.25

                    if old_scale - SCALE:
                        # OFFSET_HORIZONTAL -= mouse_pos[0] / old_scale - WIN_WIDTH/2 / SCALE
                        # OFFSET_VERTICAL -= mouse_pos[1] / old_scale - WIN_HEIGHT/2 / SCALE
                        OFFSET_HORIZONTAL -= WIN_WIDTH/2 / old_scale - WIN_WIDTH/2 / SCALE
                        OFFSET_VERTICAL -= WIN_HEIGHT/2 / old_scale - WIN_HEIGHT/2 / SCALE


            # keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # manual close
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    running = False
                    pygame.quit()
                    quit()

        # keys that can be pressed multiple times
        keys_pressed=pygame.key.get_pressed()
        # move
        move_speed = 10 / SCALE
        # move left
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            OFFSET_HORIZONTAL += move_speed
        # move right
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            OFFSET_HORIZONTAL -= move_speed
        # move up
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            OFFSET_VERTICAL += move_speed
        # move down
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            OFFSET_VERTICAL -= move_speed
        # center
        if keys_pressed[pygame.K_c]:
            OFFSET_HORIZONTAL = 0
            OFFSET_VERTICAL = 0
            SCALE = 1

        # clear screen
        WIN.fill(BLACK)

        # draw platforms
        draw_test_platforms(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw track layout
        for segment_id in DICT_WITH_SEGMENTS:
            DICT_WITH_SEGMENTS[segment_id].draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw track switches
        for switch_id in DICT_WITH_TRACK_SWITCHES:
            DICT_WITH_TRACK_SWITCHES[switch_id].draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # check route for auto engines
        for engine_id in LIST_WITH_ENGINES:
            DICT_WITH_CARRIAGES[engine_id].accelerate()
            if DICT_WITH_CARRIAGES[engine_id].state == "stop" or DICT_WITH_CARRIAGES[engine_id].state == "move":
                if not CURRENT_FRAME % 10: DICT_WITH_CARRIAGES[engine_id].fore_run(DICT_WITH_SEGMENTS, DICT_WITH_SEMAPHORES, DICT_WITH_CARRIAGES)
                pygame.draw.line(WIN, RED, move_point(DICT_WITH_CARRIAGES[engine_id].coord, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), move_point(DICT_WITH_CARRIAGES[engine_id].fore_run_end, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), 1)

        # move and draw trains
        for carriage in DICT_WITH_CARRIAGES:
            DICT_WITH_CARRIAGES[carriage].push_pull(DICT_WITH_CARRIAGES)
            DICT_WITH_CARRIAGES[carriage].move(DICT_WITH_SEGMENTS)
            DICT_WITH_CARRIAGES[carriage].collision(DICT_WITH_CARRIAGES)
            DICT_WITH_CARRIAGES[carriage].change_semaphore(DICT_WITH_SEMAPHORES)
            DICT_WITH_CARRIAGES[carriage].draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw semaphores
        for semaphore in DICT_WITH_SEMAPHORES:
            if not CURRENT_FRAME % 30: DICT_WITH_SEMAPHORES[semaphore].fore_run(DICT_WITH_SEGMENTS, DICT_WITH_SEMAPHORES, DICT_WITH_CARRIAGES)
            # pygame.draw.line(WIN, YELLOW, move_point(DICT_WITH_SEMAPHORES[semaphore].light_coord, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), move_point(DICT_WITH_SEMAPHORES[semaphore].fore_run_end, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), 1)
            DICT_WITH_SEMAPHORES[semaphore].draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw control boxes
        for control_box_id in DICT_WITH_CONTROL_BOXES:
            if not (CURRENT_FRAME+15) % 30: DICT_WITH_CONTROL_BOXES[control_box_id].run(DICT_WITH_CARRIAGES, DICT_WITH_SEMAPHORES, DICT_WITH_PANELS)
            DICT_WITH_CONTROL_BOXES[control_box_id].draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw interface
        show = 0 # variables to check on which train to centre on
        engine_to_show = 0
        for panel_id in DICT_WITH_PANELS:
            if not (CURRENT_FRAME+15) % 30: DICT_WITH_CARRIAGES[panel_id].countdown()
            show = DICT_WITH_PANELS[panel_id].draw(WIN, DICT_WITH_CARRIAGES[panel_id], pygame.mouse.get_pos())
            if show: engine_to_show = show

        # center view
        if engine_to_show:
            SCALE = 1.5
            OFFSET_HORIZONTAL = -DICT_WITH_CARRIAGES[engine_to_show].coord[0] + WIN_WIDTH/2 / SCALE
            OFFSET_VERTICAL = -DICT_WITH_CARRIAGES[engine_to_show].coord[1] + WIN_HEIGHT/2 / SCALE
            if engine_to_show != last_engine_to_show:
                center_mark = 1
                last_engine_to_show = engine_to_show

        # draw center mark
        if center_mark < 50:
            pygame.draw.circle(WIN, RED, [WIN_WIDTH/2, WIN_HEIGHT/2], center_mark, 1)
            center_mark += 4

        # draw (0, 0)
        # pygame.draw.circle(WIN, RED, move_point((0, 0), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), 10*SCALE, 1)
        # pygame.draw.circle(WIN, RED, move_point((0, 0), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), 5*SCALE, 1)

        # flip the screen
        pygame.display.update()

if __name__ == "__main__":
    run()

    # input("input any key")
