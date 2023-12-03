import pygame
from parameters import *
from player import all_sprites

class Button():
    def __init__(self, color, x, y, width, height, text = '', text_color = BLACK, action = None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.action = action
        self.button_clicked = False

    def draw(self, screen, outline = 'None'):
        # Give option to give button outline
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        # Put text on button if given
        if self.text != '':
            font = pygame.font.Font('assets/fonts/font.ttf', 60)
            text = font.render(self.text, 1, self.text_color)
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def button_action(self):
        if self.action == 1:
            self.button_clicked = True

    def update(self, hover_color = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        click_sound = pygame.mixer.Sound('assets/sounds/click.mp3')
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:

            if hover_color:
                self.color = hover_color

            if click[0] == 1 and self.action != None:
                self.button_action()
                pygame.mixer.Sound.play((click_sound))


