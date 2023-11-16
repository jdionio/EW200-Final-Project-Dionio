import pygame
from parameters import *


# Draw background function
def draw_background(screen):
    # Load tiles from assets folder
    # Load ground image and scale it to screen dimensions
    ground = pygame.transform.scale(pygame.image.load("assets/map/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(ground, (0,0))
