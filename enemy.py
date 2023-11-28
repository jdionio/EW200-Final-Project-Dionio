import pygame
from parameters import *
import math
from player import Player

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.player = player
        self.image = pygame.image.load("assets/zombies/skeleton-attack_0.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.35)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x,y)
        self.player.hitbox_rect.center = player.hitbox_rect.center

        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = ENEMY_SPEED
        self.velocity = pygame.math.Vector2()
        self.base_image = self.image

    def hunt(self):
        player_pos = pygame.math.Vector2(self.player.hitbox_rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)
        distance = self.get_distance(player_pos, enemy_pos)

        if distance > 0:
            self.direction = (player_pos - enemy_pos).normalize() # changes length of vector to 1 while keeping same direction
        else:
            self.direction = pygame.math.Vector2()

        self.velocity = self.direction * self.speed
        self.pos += self.velocity
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

    def get_distance(self, vector1, vector2):
        return (vector1-vector2).magnitude()

    def rotate(self):
        player_pos = pygame.math.Vector2(self.player.hitbox_rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)
        self.x_enemy_to_player = player_pos[0] - enemy_pos[0]
        self.y_enemy_to_player = player_pos[1] - enemy_pos[1]
        self.angle = math.degrees(math.atan2(self.y_enemy_to_player, self.x_enemy_to_player))
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rotate()
        self.hunt()






enemies = pygame.sprite.Group()