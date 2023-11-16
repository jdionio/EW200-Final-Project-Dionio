import pygame
from parameters import *


# Draw background function
def draw_background(screen):
    # Load tiles from assets folder
    grass = pygame.image.load("assets/map/grass.png")
    road = pygame.image.load("assets/map/road.png")
    sidewalk = pygame.image.load("assets/map/sidewalk.png")
    sky = pygame.image.load("assets/map/sky.png")
    stars = pygame.image.load("assets/map/stars.png")

    # Fill screen with sky
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            screen.blit(sky, (x,y))

    # Put stars in sky
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        for y in range(0, 2*TILE_SIZE, TILE_SIZE):
            screen.blit(stars,(x,y))

    # Fill bottom with grass
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        for y in range(SCREEN_HEIGHT - TILE_SIZE, SCREEN_HEIGHT, TILE_SIZE):
            screen.blit(grass, (x,y))

    # Lower Sidewalk
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        for y in range(SCREEN_HEIGHT - (2*TILE_SIZE), SCREEN_HEIGHT- TILE_SIZE, TILE_SIZE):
            screen.blit(sidewalk, (x,y))

    # Road
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        for y in range(SCREEN_HEIGHT - (4* TILE_SIZE), SCREEN_HEIGHT- (2*TILE_SIZE), TILE_SIZE):
            screen.blit(road, (x,y))
