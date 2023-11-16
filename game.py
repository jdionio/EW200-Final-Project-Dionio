import pygame
import sys

# Import necessary files
from parameters import *
from background import draw_background
from player import Player

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Zombie Shooter')

# Make a clock
clock = pygame.time.Clock()

player = Player()







# Main loop
running = True
background = screen.copy()
draw_background(background)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.update()

    # Draw background
    screen.blit(background, (0,0))

    # Draw player
    player.draw(screen)

    # Update display
    pygame.display.flip()

    # Limit frames per second
    clock.tick(FPS)