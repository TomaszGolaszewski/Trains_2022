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
    # DICT_WITH_SEGMENTS, DICT_WITH_TRACK_SWITCHES, DICT_WITH_SEMAPHORES = load_from_file()
    DICT_WITH_SEGMENTS, DICT_WITH_TRACK_SWITCHES, DICT_WITH_SEMAPHORES = load_from_file_v2()

    # make test TRAINS
    DICT_WITH_CARRIAGES, LIST_WITH_ENGINES = make_test_trains(DICT_WITH_SEGMENTS)

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
                    for engine_id in LIST_WITH_ENGINES:
                        if DICT_WITH_CARRIAGES[engine_id].is_bar_pressed(pygame.mouse.get_pos()):
                            DICT_WITH_CARRIAGES[engine_id].press_bar(pygame.mouse.get_pos())
                    for switch_id in DICT_WITH_TRACK_SWITCHES:
                        if DICT_WITH_TRACK_SWITCHES[switch_id].is_switch_pressed(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)):
                            DICT_WITH_TRACK_SWITCHES[switch_id].switch_switch(DICT_WITH_SEGMENTS)
                    for semaphore_id in DICT_WITH_SEMAPHORES:
                        if DICT_WITH_SEMAPHORES[semaphore_id].is_pressed(move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)):
                            DICT_WITH_SEMAPHORES[semaphore_id].change_light()

                    segment = which_segment(DICT_WITH_SEGMENTS, move_point_back(pygame.mouse.get_pos(), OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE), 2)
                    if segment and segment != 9999: print(DICT_WITH_SEGMENTS[segment])

                    # print(str(pygame.mouse.get_pos()))
                # 2 - middle click
                # 3 - right click
                # 4 - scroll up
                if event.button == 4:
                    SCALE += 1
                    if SCALE == 1.5: SCALE = 1
                # 5 - scroll down
                if event.button == 5:
                    SCALE -= 1
                    if SCALE <= 0: SCALE = 0.5
                  # pos = pygame.mouse.get_pos()


            # keys that can be pressed only ones
            if event.type == pygame.KEYDOWN:
                # manual close
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    running = False
                    pygame.quit()
                    quit()

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
            DICT_WITH_SEMAPHORES[semaphore].draw(WIN, OFFSET_HORIZONTAL, OFFSET_VERTICAL, SCALE)

        # draw interface
        for bar in LIST_WITH_ENGINES:
            DICT_WITH_CARRIAGES[bar].draw_bar(WIN)

        # flip the screen
        pygame.display.update()

if __name__ == "__main__":
    run()

    # input("input any key")
