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

# sprites
ICON = pygame.image.load(os.path.join("imgs","icon.png"))
ENGINE_IMGS = pygame.image.load(os.path.join("imgs","engine1.png"))
CARRIAGE_IMGS = [
    pygame.image.load(os.path.join("imgs","carriage1.png")),
    pygame.image.load(os.path.join("imgs","carriage1_container_green.png")),
    pygame.image.load(os.path.join("imgs","carriage1_container_blue.png"))]
CARRIAGE_PASSENGER_IMGS = pygame.image.load(os.path.join("imgs","carriage_passenger.png"))
MULTIPLE_UNIT_1_IMGS = [
    pygame.image.load(os.path.join("imgs","multiple_unit1_engine.png")),
    pygame.image.load(os.path.join("imgs","multiple_unit1_carriage.png")),
    pygame.image.load(os.path.join("imgs","multiple_unit1_end.png"))]
EN57_IMGS = [
    pygame.image.load(os.path.join("imgs","EN57_engine.png")),
    pygame.image.load(os.path.join("imgs","EN57_carriage.png")),
    pygame.image.load(os.path.join("imgs","EN57_end.png"))]
STEAM_LOCOMOTIVE_1_IMGS = [
    pygame.image.load(os.path.join("imgs","steam_locomotive.png")),
    pygame.image.load(os.path.join("imgs","steam_tender.png"))]
