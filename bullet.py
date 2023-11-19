import pygame
from parameters import *
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load("assets/bullet.png").convert_alpha()
        # Resize bullet image
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SCALE)
        # Create hitbox for bullet
        self.rect = self.image.get_rect()
        # Set center of bullet to coordinates
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = BULLET_SPEED
        # Calculate speed of bullet using trig
        self.x_speed = math.cos(self.angle * (2 * math.pi / 360) * self.speed)
        self.y_speed = math.sin(self.angle * (2 * math.pi / 360) * self.speed)

    # Create function to move bullet when fired
    def bullet_movement(self):
        # Update bullet position
        self.x += self.x_speed
        self.y += self.y_speed
        # Convert x and y coodrinates to integers to use rect function
        # Update hitbox position of bullet
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def update(self):
        self.bullet_movement()


bullets = pygame.sprite.Group()
