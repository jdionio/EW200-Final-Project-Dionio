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
        # Create a variable for the base player image
        self.base_player_image = self.image
        # Create a hit box for the player by getting the rect of the image and centering it at the player position
        self.hitbox_rect = self.base_player_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()

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
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    # Function to rotate a player based on the location of the pointer
    def rotate_player(self):
        # Crate a variable that tracks mouse position
        self.mouse_pos = pygame.mouse.get_pos() # Returns a list of an x and y coordinate
        # Variables to find distance between mouse and player
        self.x_player_to_mouse = (self.mouse_pos[0] - self.hitbox_rect.centerx)
        self.y_player_to_mouse = (self.mouse_pos[1] - self.hitbox_rect.centery)
        # Finds the angle between mouse and player using the distances and making a triangle (more trig)
        self.angle = math.degrees(math.atan2(self.y_player_to_mouse, self.x_player_to_mouse))
        # Rotate the image to the angle (note that angle is negative)
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)


    def update(self):
        # Calls functions from before and puts them into action to move player
        self.user_input()
        self.move()
        self.rotate_player()

    def draw(self, screen):
        # Draws player on screen
        screen.blit(self.image, self.rect)
