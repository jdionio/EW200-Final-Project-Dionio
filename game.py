import pygame
import sys
import random

# Import necessary files
from parameters import *
from player import Player, all_sprites
from bullet import Bullet, bullets
from enemy import Enemy, enemies
from button import Button

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Zombie Shooter')
background = pygame.image.load("assets/ground.png").convert()
# Make a clock
clock = pygame.time.Clock()

# Wave
wave_num = 0
wave_cooldown = WAVE_COOLDOWN
text_cooldown = TEXT_COOLDOWN
# Keep track of money
money_num = 0

# Import sound effects
zombie_growl = pygame.mixer.Sound('assets/sounds/zombiegrowl.mp3')
zombie_hurt = pygame.mixer.Sound('assets/sounds/zombiehurt.mp3')
player_oof = pygame.mixer.Sound('assets/sounds/playerhurt.mp3')
main_menu_music = pygame.mixer.Sound('assets/sounds/menu_background.mp3')
death_sound = pygame.mixer.Sound('assets/sounds/death.mp3')

# Keep trak of score
score = 0
game_font = pygame.font.Font('assets/fonts/font.ttf', 48)
dmg_cooldown = DAMAGE_COOLDOWN

# Conditions
running = True
mainmenu = True
is_playing = False
is_shopping = False

owns_pistol = True
owns_shotgun = False
owns_machinegun = False

pistol_equipped = True
shotgun_equipped = False
machinegun_equipped = False
# Make camera that follows player around map
class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.floor_rect = background.get_rect(topleft=(0, 0))

    def custom_draw(self):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH // 2  # Integer division
        self.offset.y = player.rect.centery - SCREEN_HEIGHT // 2

        # Shift the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        screen.blit(background, floor_offset_pos)

        # Account for offset for each sprite whilst moving
        for sprite in all_sprites:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)


# Create random coordinates for zombies to spawn

player = Player()
camera = Camera()


# Add player and enemy instance to all sprites group
def add_zombie():
    for x in range(wave_num * 5):
        random_x = random.randint(SCREEN_WIDTH, 4000)
        random_y = random.randint(SCREEN_HEIGHT, 2500)
        zombie = Enemy(random_x, random_y, player)
        enemies.add(zombie)
        all_sprites.add(zombie)
        pygame.mixer.Sound.play(zombie_growl)



all_sprites.add(player)


def main_menu():
    screen.blit(background, (-500,-100))
    title_font = pygame.font.Font('assets/fonts/font.ttf', 72)
    title = title_font.render('ZOMBIE SHOOTER', True, (181, 9, 9))
    screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width()/2, title.get_height()))

def display_shop():
    # Draw black outline for shop box
    pygame.draw.rect(screen, BLACK, ((SCREEN_WIDTH / 2) - (SHOP_WIDTH / 2) - 2, (SCREEN_HEIGHT / 2) - (SHOP_HEIGHT/2) - 2, SHOP_WIDTH + 4, SHOP_HEIGHT + 4), 0)
    # Draw rect for shop
    pygame.draw.rect(screen, SHOP_BACKGROUND, ((SCREEN_WIDTH / 2) - (SHOP_WIDTH / 2), (SCREEN_HEIGHT / 2) - (SHOP_HEIGHT / 2), SHOP_WIDTH, SHOP_HEIGHT),0)
    # Draw text for shop
    shop_title = game_font.render('SHOP', True, BLACK)
    screen.blit(shop_title, ((SCREEN_WIDTH / 2) - (shop_title.get_width() / 2), (SCREEN_HEIGHT / 2) - SHOP_HEIGHT / 2))
    # Buyable items text
    buy_pistol = game_font.render('PISTOL OWNED', True, BLACK)
    buy_shotgun = game_font.render('SHOTGUN  250', True, BLACK)
    buy_machinegun = game_font.render('MACHINEGUN  750', True, BLACK)
    screen.blit(buy_pistol,((SCREEN_WIDTH/ 2) - (buy_pistol.get_width() / 2), (SCREEN_HEIGHT / 2) - 8*(buy_pistol.get_height() / 2)))
    screen.blit(buy_shotgun, ((SCREEN_WIDTH/ 2) - (buy_shotgun.get_width() / 2), (SCREEN_HEIGHT / 2) - 2*(buy_shotgun.get_height() / 2)))
    screen.blit(buy_machinegun, ((SCREEN_WIDTH / 2) - (buy_machinegun.get_width() / 2), (SCREEN_HEIGHT / 2) + 4*(buy_machinegun.get_height() / 2)))

def can_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



# Main Loop
while running:
    while mainmenu == True and is_playing == False:
        can_quit()
        main_menu()
        play_button = Button(WHITE, SCREEN_WIDTH/2 - 250, SCREEN_HEIGHT/2 - 63, 500, 125, 'PLAY', BLACK, 1)
        quit_button_main = Button(WHITE, (SCREEN_WIDTH / 2 - 250), SCREEN_HEIGHT / 2 + 88, 500, 125, 'QUIT', BLACK, 1)
        play_button.update(GREY)
        play_button.draw(screen, BLACK)
        quit_button_main.update(GREY)
        quit_button_main.draw(screen, BLACK)
        if play_button.button_clicked == True:
            mainmenu = False
            is_playing = True
            play_button.button_clicked = False
        if quit_button_main.button_clicked == True:
            pygame.quit()
            sys.exit()
        pygame.mixer.music.load('assets/sounds/menu_background.mp3')
        pygame.mixer.music.play(-1, 0, 10)
        pygame.mixer.music.set_volume(0.5)
        pygame.display.flip()
        clock.tick(FPS)

    # Actual game is playing
    while mainmenu == False and is_playing == True:
        can_quit()

        # Draw background
        # screen.blit(background, (0,0))
        # Draws all sprites on screen and updates

        all_sprites.update()
        # Draw all sprites on screen in accordance to the offset
        camera.custom_draw()

        # Check for bullet collisions
        # if player.bullet:
        for zombie in enemies:
            collide = pygame.sprite.spritecollide(zombie, bullets, True)
            if collide:
                zombie.health -= 1
                collide = {}
                pygame.mixer.Sound.play(zombie_hurt)
            if zombie.health < 1:
                zombie.kill()
                score += 1
                money_num += 5

        # Load text and draw score, health, wave number, etc. on screen
        text = game_font.render(f'SCORE {score}', True, RED)
        if player.health >= 40:
            health = game_font.render(f'HEALTH {player.health}', True, GREEN)
        else:
            health = game_font.render(f'HEALTH {player.health}', True, RED)
        wave = game_font.render(f'WAVE {wave_num}', True, WHITE)
        money = game_font.render(f'CASH {money_num}', True, GREEN)
        time_until_next_wave = game_font.render(f'TIME UNTIL NEXT WAVE {int(wave_cooldown / 50)}', True, WHITE)
        wave_complete = game_font.render(f'WAVE COMPLETE', True, WHITE)
        pistol_button = game_font.render('PISTOL Z', True, WHITE)
        shotgun_button = game_font.render('SHOTGUN X', True, WHITE)
        machinegun_button = game_font.render('MACHINEGUN C', True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - text.get_width(), 0))
        screen.blit(health, (0, SCREEN_HEIGHT - health.get_height()))
        screen.blit(money, (SCREEN_WIDTH - money.get_width(), SCREEN_HEIGHT - money.get_height()))
        screen.blit(pistol_button, (0, 100))
        screen.blit(shotgun_button, (0, 100 + pistol_button.get_height()))
        screen.blit(machinegun_button, (0, 100+ pistol_button.get_height() + machinegun_button.get_height()))
        if text_cooldown < TEXT_COOLDOWN and wave_cooldown == WAVE_COOLDOWN:
            screen.blit(wave_complete, (SCREEN_WIDTH / 2 - wave_complete.get_width() / 2, 0))
        elif wave_cooldown < WAVE_COOLDOWN:
            screen.blit(time_until_next_wave, (SCREEN_WIDTH / 2 - time_until_next_wave.get_width() / 2, 0))
        elif text_cooldown == TEXT_COOLDOWN and wave_cooldown == WAVE_COOLDOWN:
            screen.blit(wave, (SCREEN_WIDTH / 2 - wave.get_width() / 2, 0))

        # Check if zombies collide with player and take off health
        player_hurt = pygame.sprite.spritecollide(player, enemies, False)

        if player_hurt:
            player_hurt = {}
            player.is_hurt = False
            dmg_cooldown -= 1
        if dmg_cooldown < 0:
            dmg_cooldown = DAMAGE_COOLDOWN
            player.health -= 10
            pygame.mixer.Sound.play(player_oof)
            player.is_hurt = True
        if player.health <= 0:
            pygame.mixer.Sound.play(death_sound)
        if player.health <= 0:
            for zombie in enemies:
                zombie.kill()
            is_playing = False

        if len(enemies) < 1:
            text_cooldown -= 1
            if text_cooldown < 0:
                wave_cooldown -= 1
            if wave_cooldown < 0:
                wave_num += 1
                add_zombie()
                wave_cooldown = WAVE_COOLDOWN
        else:
            text_cooldown = TEXT_COOLDOWN

        # Shop
        shop_button = Button(GREEN, 0, 0, 200,75, 'SHOP', BLACK, 1)

        shop_button.update(GREY)
        shop_button.draw(screen, BLACK)
        if shop_button.button_clicked == True:
            is_shopping = True
            is_playing = False
            shop_button.button_clicked = False
        # Update display
        pygame.display.flip()

        # Limit frames per second
        clock.tick(FPS)

    # Shop loop
    while is_shopping == True and is_playing == False:
        can_quit()
        display_shop()
        exit_shop = Button(RED, (SCREEN_WIDTH / 2) - (SHOP_WIDTH / 2), (SCREEN_HEIGHT / 2) - (SHOP_HEIGHT / 2), 50,
                           50, 'X', WHITE, 1)
        exit_shop.update(GREY)
        exit_shop.draw(screen, BLACK)
        buy_shotgun_button = Button(GREEN, (SCREEN_WIDTH / 2) + 250, (SCREEN_HEIGHT / 2) - 50, 150, 50, 'BUY', BLACK, 1)
        buy_shotgun_button.update(GREY)
        buy_shotgun_button.draw(screen, BLACK)
        buy_machinegun_button = Button(GREEN, (SCREEN_WIDTH / 2) + 250, (SCREEN_HEIGHT / 2) + 85, 150, 50, 'BUY', BLACK, 1)
        buy_machinegun_button.update(GREY)
        buy_machinegun_button.draw(screen, BLACK)
        equip_shotgun_button = Button(GREEN, (SCREEN_WIDTH / 2) + 250, (SCREEN_HEIGHT / 2) - 50, 150, 50, 'EQUIP', BLACK, 1)
        insufficient_funds = game_font.render('INSUFFICIENT FUNDS', True, RED)
        already_equipped = game_font.render('ALREADY OWNED', True, RED)

        if exit_shop.button_clicked == True:
            exit_shop.button_clicked = False
            is_shopping = False
            is_playing = True
        if buy_shotgun_button.button_clicked == True:
            if player.equip_shotgun == True:
                screen.blit(already_equipped, ((SCREEN_WIDTH /2) - already_equipped. get_width()/ 2, SCREEN_HEIGHT / 2))
                buy_shotgun_button.button_clicked = False
            elif money_num >= 250:
                player.equip_shotgun = True
                is_shopping = False
                is_playing = True
                money_num -= 250
                buy_shotgun_button.button_clicked = False
            else:
                screen.blit(insufficient_funds, ((SCREEN_WIDTH /2) - insufficient_funds. get_width()/ 2, SCREEN_HEIGHT / 2))
                buy_shotgun_button.button_clicked = False

        if buy_machinegun_button.button_clicked == True:
            if player.equip_machinegun == True:
                screen.blit(already_equipped, ((SCREEN_WIDTH /2) - already_equipped. get_width()/ 2, SCREEN_HEIGHT / 2 + 135))
                buy_machinegun_button.button_clicked = False
            elif money_num >= 750:
                player.equip_machinegun = True
                is_shopping = False
                is_playing = True
                money_num -= 750
                buy_machinegun_button.button_clicked = False
            else:
                screen.blit(insufficient_funds, ((SCREEN_WIDTH / 2) - insufficient_funds.get_width() / 2, (SCREEN_HEIGHT / 2) + 135))
                buy_machinegun_button.button_clicked = False
        pygame.display.flip()
        clock.tick(FPS)

    # Create game over loop
    while player.health <= 0 and is_playing == False:
        can_quit()
        screen.blit(background, (0, 0))
        # Create game over screen
        game_over_message = game_font.render("GAME OVER", True, RED)
        screen.blit(game_over_message, (SCREEN_WIDTH / 2 - game_over_message.get_width() / 2, SCREEN_HEIGHT / 2))

        high_score_num = 0
        with open('assets/highscore.txt', 'r') as highscore:
            x = highscore.readlines()
            high_score_num = int(x[0])

            if score > high_score_num:
                with open('assets/highscore.txt', 'w') as new_highscore:
                    new_highscore.write(f'{score}')
                    high_score_num = score
                new_highscore_text = game_font.render(f'NEW HIGH SCORE {high_score_num}', True, RED)
                screen.blit(new_highscore_text, (0,0))
            else:
                highscore_text = game_font.render(f'HIGH SCORE {high_score_num}', True, RED)
                screen.blit(highscore_text, (0,0))

        # Show final score
        final_score = game_font.render(f'FINAL SCORE  {score}', True, RED)
        screen.blit(final_score,
                    (SCREEN_WIDTH / 2 - final_score.get_width() / 2, SCREEN_HEIGHT / 2 + final_score.get_height()))

        retry_button = Button(WHITE, SCREEN_WIDTH/2 - 250, SCREEN_HEIGHT/2 + 163, 500, 125, 'RETRY', BLACK, 1)
        quit_button = Button(WHITE, SCREEN_WIDTH/2 - 250, SCREEN_HEIGHT/2 + 313, 500, 125, 'QUIT', BLACK, 1)

        retry_button.update(GREY)
        quit_button.update(GREY)

        retry_button.draw(screen, BLACK)
        quit_button.draw(screen, BLACK)

        if retry_button.button_clicked == True:
            player.health = PLAYER_HEALTH
            player.pos = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            wave_num = 0
            money_num = 0
            score = 0
            player.equip_shotgun = False
            player.equip_machinegun = False
            player.has_machinegun = False
            player.has_shotgun = False
            player.has_pistol = True
            is_playing = True
            player.is_hurt = False
            mainmenu = False
            retry_button.button_clicked = False

        if quit_button.button_clicked == True:
            running = False
            pygame.quit()
            sys.exit()
        pygame.display.flip()
        clock.tick(FPS)