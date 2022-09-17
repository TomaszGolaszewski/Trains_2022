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
WHITE = (255, 255, 255)
SILVER = (192, 192, 192)
GRAY = (128, 128, 128)
LIGHTSLATEGRAY = (119, 136, 153)
DARKSTEELGRAY = (67,70,75)

# sprites - trains
ENGINE_IMGS = pygame.image.load(os.path.join("imgs","trains","engine1.png"))
CARRIAGE_IMGS = [
    pygame.image.load(os.path.join("imgs","trains","carriage1.png")),
    pygame.image.load(os.path.join("imgs","trains","carriage1_container_green.png")),
    pygame.image.load(os.path.join("imgs","trains","carriage1_container_blue.png"))]
CARRIAGE_PASSENGER_IMGS = pygame.image.load(os.path.join("imgs","trains","carriage_passenger.png"))
CARRIAGE_PASSENGER_OLDTIMER_IMGS = pygame.image.load(os.path.join("imgs","trains","carriage_passenger_oldtimer.png"))
MULTIPLE_UNIT_1_IMGS = [
    pygame.image.load(os.path.join("imgs","trains","multiple_unit1_engine.png")),
    pygame.image.load(os.path.join("imgs","trains","multiple_unit1_carriage.png")),
    pygame.image.load(os.path.join("imgs","trains","multiple_unit1_end.png"))]
EN57_IMGS = [
    pygame.image.load(os.path.join("imgs","trains","EN57_engine.png")),
    pygame.image.load(os.path.join("imgs","trains","EN57_carriage.png")),
    pygame.image.load(os.path.join("imgs","trains","EN57_end.png"))]
STEAM_LOCOMOTIVE_1_IMGS = [
    pygame.image.load(os.path.join("imgs","trains","steam_locomotive.png")),
    pygame.image.load(os.path.join("imgs","trains","steam_tender.png"))]

# sprites - buttons
ARROW_LEFT = pygame.image.load(os.path.join("imgs","buttons","arrow_left.png"))
ARROW_RIGHT = pygame.image.load(os.path.join("imgs","buttons","arrow_right.png"))
ARROW_FLIP = pygame.image.load(os.path.join("imgs","buttons","arrow_flip.png"))
MANUAL_MODE = pygame.image.load(os.path.join("imgs","buttons","manual_mode.png"))
AUTO_MODE = pygame.image.load(os.path.join("imgs","buttons","auto_mode.png"))

# sprites - other
ICON = pygame.image.load(os.path.join("imgs","other","icon.png"))
