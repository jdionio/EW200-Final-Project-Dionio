import pygame
import sys

# Import necessary files
from parameters import *
from player import Player, all_sprites
from bullet import Bullet
from enemy import Enemy, enemies

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Zombie Shooter')
background = pygame.image.load("assets/ground.png").convert()
# Make a clock
clock = pygame.time.Clock()

# Make camera that follows player around map
class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.floor_rect = background.get_rect(topleft = (0,0))

    def custom_draw(self):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH // 2 # Integer division
        self.offset.y = player.rect.centery - SCREEN_HEIGHT // 2

        # Shift the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        screen.blit(background, floor_offset_pos)

        # Account for offset for each sprite whilst moving
        for sprite in all_sprites:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)

player = Player()
camera = Camera()
zombie = Enemy(400,400, player)
# Add player and enemy instance to all sprites group
enemies.add(zombie)
all_sprites.add(player)
all_sprites.add(zombie)




# Main loop
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Draw background
    screen.blit(background, (0,0))
    # Draws all sprites on screen and updates

    all_sprites.update()
    # Draw all sprites on screen in accordance to the offset
    camera.custom_draw()
    # Make enemy hunt player
    # Update display
    pygame.display.flip()

    # Limit frames per second
    clock.tick(FPS)