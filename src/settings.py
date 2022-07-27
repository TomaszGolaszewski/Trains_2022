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

# sprites
ICON = pygame.image.load(os.path.join("imgs","icon.png"))
ENGINE_IMGS = pygame.image.load(os.path.join("imgs","engine1.png"))
CARRIAGE_IMGS = [
    pygame.image.load(os.path.join("imgs","carriage1.png")),
    pygame.image.load(os.path.join("imgs","carriage1_container_green.png")),
    pygame.image.load(os.path.join("imgs","carriage1_container_blue.png"))]
