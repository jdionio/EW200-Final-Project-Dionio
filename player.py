import pygame
from parameters import *
import math


# Create a player class

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load player image
        self.image = pygame.transform.rotozoom(  # This function resizes the player image
            pygame.image.load("assets/Top_Down_Survivor/Top_Down_Survivor/handgun/idle/survivor"
                              "-idle_handgun_0.png").convert_alpha(), 0, 0.35) # Convert alpha smoothens edges
        # Note that set_color key wasn't included; not needed for sprite
        # Found a way to put player position into one variable rather than having 2
        self.pos = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Check if key is pressed and move player accordingly
    def user_input(self):
        self.x_speed = 0
        self.y_speed = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.y_speed = -PLAYER_SPEED
        if keys[pygame.K_s]:
            self.y_speed = PLAYER_SPEED
        if keys[pygame.K_a]:
            self.x_speed = -PLAYER_SPEED
        if keys[pygame.K_d]:
            self.x_speed = PLAYER_SPEED

        # Check if player moves diagonally and prevent player from moving too fast (trig)
        if self.x_speed != 0 and self.y_speed != 0:
            self.x_speed /= math.sqrt(2)
            self.y_speed /= math.sqrt(2)

    def move(self):
        # Creates a vector for speed and adds it to the player position
        self.pos += pygame.math.Vector2(self.x_speed, self.y_speed)

    def update(self):
        # Calls functions from before and puts them into action to move player
        self.user_input()
        self.move()

    def draw(self, screen):
        # Draws player on screen
        screen.blit(self.image, self.pos)
