import pygame
import sys

# Import necessary files
from parameters import *
from background import draw_background

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bim bim bam bam')

# Make a clock
clock = pygame.time.Clock()









# Main loop
running = True
background = screen.copy()
draw_background(background)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    screen.blit(background, (0,0))

    # Update display
    pygame.display.flip()