import pygame
from parameters import *
import math
from bullet import Bullet, bullets


# Create a player class

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load player image
        self.bullet = None
        self.image = pygame.transform.rotozoom(  # This function resizes the player image
            pygame.image.load("assets/Top_Down_Survivor/Top_Down_Survivor/handgun/idle/survivor"
                              "-idle_handgun_0.png").convert_alpha(), 0, 0.35)  # Convert alpha smoothens edges
        # Note that set_color key wasn't included; not needed for sprite
        # Found a way to put player position into one variable rather than having 2
        self.pos = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        # Create a variable for the base player image
        self.base_player_image = self.image
        # Create a hit box for the player by getting the rect of the image and centering it at the player position
        self.hitbox_rect = self.base_player_image.get_rect(center=self.pos)
        self.rect = self.hitbox_rect.copy()
        self.shoot = False
        self.shoot_cooldown = 0
        # We want to create the bullet at the end of the gun barrel, so there will be some offset
        self.gun_barrel_offset = pygame.math.Vector2(GUN_OFFSET_X, GUN_OFFSET_Y)

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

        # Check if player clicks mouse to shoot weapon
        if pygame.mouse.get_pressed() == (1, 0, 0):  # Checks if left mouse is clicked
            self.shoot == True
            self.shooting()
        else:
            self.shoot == False

    # Make a function to check if player is shooting
    def shooting(self):
        # Check if player has already shot
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            # Make bullet equal to player position and account for gun barrel offset
            bullet_pos = self.pos + self.gun_barrel_offset.rotate(self.angle)
            self.bullet = Bullet(bullet_pos[0], bullet_pos[1], self.angle)
            bullets.add(self.bullet)
            all_sprites.add(self.bullet)

    def move(self):
        # Creates a vector for speed and adds it to the player position
        self.pos += pygame.math.Vector2(self.x_speed, self.y_speed)
        self.hitbox_rect.center = self.pos
        self.rect.center = self.hitbox_rect.center

    # Function to rotate a player based on the location of the pointer
    def rotate_player(self):
        # Crate a variable that tracks mouse position
        self.mouse_pos = pygame.mouse.get_pos()  # Returns a list of an x and y coordinate
        # Variables to find distance between mouse and player (note that player position is in middle of screen as
        # the player isn't moving, the screen is!
        self.x_player_to_mouse = (self.mouse_pos[0] - SCREEN_WIDTH // 2)
        self.y_player_to_mouse = (self.mouse_pos[1] - SCREEN_HEIGHT // 2)
        # Finds the angle between mouse and player using the distances and making a triangle (more trig)
        self.angle = math.degrees(math.atan2(self.y_player_to_mouse, self.x_player_to_mouse))
        # Rotate the image to the angle (note that angle is negative)
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)

    def update(self):
        # Calls functions from before and puts them into action to move and rotate player
        self.user_input()
        self.move()
        self.rotate_player()

        # Check if player has shot and activate cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self, screen):
        # Draws player on screen
        screen.blit(self.image, self.rect)


# Create a sprite group for all sprites
all_sprites = pygame.sprite.Group()
