import pygame
import os

# window
WIN_WIDTH = 1260
WIN_HEIGHT = 720
FRAMERATE = 30

# colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
ORANGE = (255, 95, 30)
WHITE = (255, 255, 255)
SILVER = (192, 192, 192)
GRAY = (128, 128, 128)
LIGHTSLATEGRAY = (119, 136, 153)
DARKSTEELGRAY = (67,70,75)

# sprites - trains
ENGINE_IMGS = pygame.image.load(os.path.join("imgs","trains","engine1.png")) # .convert()
HUSARZ_IMGS = pygame.image.load(os.path.join("imgs","trains","engine2.png"))
CARRIAGE_IMGS = [
    pygame.image.load(os.path.join("imgs","trains","carriage1.png")),
    pygame.image.load(os.path.join("imgs","trains","carriage1_container_green.png")),
    pygame.image.load(os.path.join("imgs","trains","carriage1_container_blue.png")),
    pygame.image.load(os.path.join("imgs","trains","carriage1_container_white.png"))]
CARRIAGE_PASSENGER_IMGS = pygame.image.load(os.path.join("imgs","trains","carriage_passenger.png"))
CARRIAGE_PASSENGER_OLDTIMER_IMGS = pygame.image.load(os.path.join("imgs","trains","carriage_passenger_oldtimer.png"))
MULTIPLE_UNIT_1_IMGS = [
    pygame.image.load(os.path.join("imgs","trains","multiple_unit1_engine.png")),
    pygame.image.load(os.path.join("imgs","trains","multiple_unit1_carriage.png")),
    pygame.image.load(os.path.join("imgs","trains","multiple_unit1_end.png"))]
MULTIPLE_UNIT_2_IMGS = [
    pygame.image.load(os.path.join("imgs","trains","multiple_unit2_engine.png")),
    pygame.image.load(os.path.join("imgs","trains","multiple_unit2_carriage.png")),
    pygame.image.load(os.path.join("imgs","trains","multiple_unit2_end.png"))]
EN57_IMGS = [
    pygame.image.load(os.path.join("imgs","trains","EN57_engine.png")),
    pygame.image.load(os.path.join("imgs","trains","EN57_carriage.png")),
    pygame.image.load(os.path.join("imgs","trains","EN57_end.png"))]
EN57_KM_IMGS = [
    pygame.image.load(os.path.join("imgs","trains","EN57_KM_engine.png")),
    pygame.image.load(os.path.join("imgs","trains","EN57_KM_carriage.png")),
    pygame.image.load(os.path.join("imgs","trains","EN57_KM_end.png"))]
STEAM_LOCOMOTIVE_1_IMGS = [
    pygame.image.load(os.path.join("imgs","trains","steam_locomotive.png")),
    pygame.image.load(os.path.join("imgs","trains","steam_tender.png"))]

# sprites - building
SHIP_PATH = ["imgs","buildings","container_ship.png"]
PORTAL_CRANE_PATH = ["imgs","buildings","portal_crane.png"]
BIG_PORTAL_CRANE_PATH = ["imgs","buildings","big_portal_crane.png"]
CONTAINERS_PATH = ["imgs","buildings","containers.png"]
CONTAINERS2_PATH = ["imgs","buildings","containers2.png"]
CONTAINERS3_PATH = ["imgs","buildings","containers3.png"]

# sprites - buttons
ARROW_LEFT = pygame.image.load(os.path.join("imgs","buttons","arrow_left.png"))
ARROW_RIGHT = pygame.image.load(os.path.join("imgs","buttons","arrow_right.png"))
ARROW_FLIP = pygame.image.load(os.path.join("imgs","buttons","arrow_flip.png"))
MANUAL_MODE = pygame.image.load(os.path.join("imgs","buttons","manual_mode.png"))
AUTO_MODE = pygame.image.load(os.path.join("imgs","buttons","auto_mode.png"))

# sprites - other
ICON = pygame.image.load(os.path.join("imgs","other","icon.png"))
