import random
import math
from GameObjects import *

pygame.init()

width = 800
height = 600

top_boundary = 300
left_boundary = 10
right_boundary = width - 42
bottom_boundary = height - 42

menu_height = 300
menu_width = 400
menu_x = 400 - menu_width / 2
menu_y = 300 - menu_height / 2

game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('CPA Project')

clock = pygame.time.Clock()
time = pygame.time
draw = pygame.draw
font = pygame.font.SysFont("monospace", 15, True)
font2 = pygame.font.SysFont("monospace", 25, True)

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
grey = (128, 128, 128)

game_display.fill(white)

fps = 60

enemy_spawm_millis = 2000
enemy_fire_millis = 2500

# instantiate objects
enemy_list = []
enemy_bullet_list = []
player_bullet_list = []
player_bullets = []

list_inputs = []


def new_game():
    list_inputs.clear()
    enemy_bullet_list.clear()
    player_bullet_list.clear()
    enemy_list.clear()


is_first_run = True

class MainWindow:


    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.spawn_time = 0
        self.points = 0
        self.is_running = True
        self.is_main_game = False
        self.player = Character(400, 520, 32, 32, 3)
        self.base_hitpoints = 10

    def main(self):

        # game loop
        while self.is_running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if self.is_main_game:

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            if list_inputs.__contains__('left'):
                                print('!')
                            else:
                                list_inputs.append('left')
                        elif event.key == pygame.K_RIGHT:
                            if list_inputs.__contains__('right'):
                                print('!')
                            else:
                                list_inputs.append('right')
                        elif event.key == pygame.K_UP:
                            if list_inputs.__contains__('up'):
                                print('!')
                            else:
                                list_inputs.append('up')
                        elif event.key == pygame.K_DOWN:
                            if list_inputs.__contains__('down'):
                                print('!')
                            else:
                                list_inputs.append('down')
                        if event.key == pygame.K_SPACE:
                            if list_inputs.__contains__('space'):
                                print('!')
                            else:
                                print('space down')
                                list_inputs.append('space')

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        if list_inputs.__contains__('left'):
                            list_inputs.remove('left')
                    elif event.key == pygame.K_RIGHT:
                        if list_inputs.__contains__('right'):
                            list_inputs.remove('right')
                    elif event.key == pygame.K_UP:
                        if list_inputs.__contains__('up'):
                            list_inputs.remove('up')
                    elif event.key == pygame.K_DOWN:
                        if list_inputs.__contains__('down'):
                            list_inputs.remove('down')

                    if event.key == pygame.K_SPACE:
                        if list_inputs.__contains__('space'):
                            list_inputs.remove('space')

            print(list_inputs)

            # check if list contains movement commands to move player character
            if list_inputs.__contains__('left') and self.player.rect.x > left_boundary:
                self.player.move(-5, 0)
            elif list_inputs.__contains__('right') and self.player.rect.x < right_boundary:
                self.player.move(5, 0)
            if list_inputs.__contains__('up') and self.player.rect.y > top_boundary:
                self.player.move(0, -5)
            elif list_inputs.__contains__('down') and self.player.rect.y < bottom_boundary:
                self.player.move(0, 5)

#           player shoot
            if list_inputs.__contains__('space'):
                if time.get_ticks() - self.player.last_time_shoot > 800:
                    player_bullet_list.append(Bullet(self.player.rect.x + 8, self.player.rect.y - 32, 16, 16, -4))
                    self.player.last_time_shoot = time.get_ticks()

            if self.is_main_game:
                # spawn enemies
                if time.get_ticks() - self.spawn_time > enemy_spawm_millis - (self.points * 20):
                    x_ = random.randint(left_boundary, right_boundary)
                    enemy_list.append(Character(x_, 0, 32, 32, 1))
                    self.spawn_time = time.get_ticks()

                # update all existing enemies
                for e in enemy_list:
                    if time.get_ticks() - e.last_time_shoot > enemy_fire_millis:
                        enemy_bullet_list.append(Bullet(e.rect.x, e.rect.y + 33, 16, 16, 2))
                        e.last_time_shoot = time.get_ticks()
                    e.move(0, 1)
                    if e.rect.y + e.rect. width == 600:
                        enemy_list.remove(e)
                        self.base_hitpoints -= e.hit_points
                        continue
                    if e.rect.colliderect(self.player.rect):
                        enemy_list.remove(e)
                        self.player.hit_points -= 1
                        if self.player.hit_points < 1:
                            # pygame.quit()
                            # quit()
                            # self.is_running = False
                            self.is_main_game = False

                    for b in player_bullet_list:
                        if b.rect.colliderect(e.rect):
                            player_bullet_list.remove(b)
                            enemy_list.remove(e)
                            self.points += 1
                            break

                # update all existing bullets
                for b in enemy_bullet_list:
                    b.update()
                    if b.rect.y + b.rect.width == 600:
                        enemy_bullet_list.remove(b)
                    if self.player.rect.colliderect(b.rect):
                        self.player.hit_points -= 1
                        enemy_bullet_list.remove(b)
                        if self.player.hit_points < 1:
                            # pygame.quit()
                            # quit()
                            # self.is_running = False
                            self.is_main_game = False

                for b in player_bullet_list:
                    b.update()
                    if b.rect.y + b.rect.width == 600:
                        player_bullet_list.remove(b)

                # draw game objects in the canvas
                # screen reset to white
                draw.rect(game_display, white, (0, 0, width, height))

                # draw bullets
                for b in enemy_bullet_list:
                    draw.rect(game_display, grey, (b.rect.x, b.rect.y, b.rect.width, b.rect.height))

                for b in player_bullet_list:
                    draw.rect(game_display, yellow, (b.rect.x, b.rect.y, b.rect.width, b.rect.height))

                # draw enemies
                for e in enemy_list:
                    draw.rect(game_display, black, (e.rect.x, e.rect.y, e.rect.width, e.rect.height))

                # draw player
                draw.rect(game_display, green, (self.player.rect.x, self.player.rect.y, self.player.rect.width, self.player.rect.height))

                score_text = "Score: " + str(self.points)
                hit_text = "Hitpoints: " + str(self.player.hit_points)
                base_text = "Base hit points: " + str(self.base_hitpoints)

                score_label = font.render(score_text, 1, blue)
                hit_label = font.render(hit_text, 1, blue)
                base_label = font.render(base_text, 1, blue)
                game_display.blit(score_label, (700, 40))
                game_display.blit(hit_label, (40, 40))
                game_display.blit(base_label, (40, 60))

            # if the game is not playing or menu is on is off
            # draw menu screens for 'start' and 'game over'
            else:

                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            print('New Game!')
                            new_game()
                            self.__init__(width, height)
                            self.is_main_game = True

                            global is_first_run
                            is_first_run = False

                # screen reset to white
                draw.rect(game_display, white, (0, 0, width, height))

                # draw menu screen
                draw.rect(game_display, black, (menu_x, menu_y, menu_width, menu_height))

                menu_text = "Blck Bx Shtr"

                menu_label = font2.render(menu_text, 1, white)

                if is_first_run:
                    menu_text_2 = "Press 'ENTER' key to start a new game."
                else:
                    menu_text_3 = "You got owned by bck bxs."
                    menu_text_2 = "Press 'ENTER' key to try again."
                    menu_label_3 = font.render(menu_text_3, 1, red)
                    game_display.blit(menu_label_3, (menu_x + 20, menu_y + 40))


                menu_label_2 = font.render(menu_text_2, 1, white)

                # draw menus
                game_display.blit(menu_label, (menu_x + 20, menu_y + 80))
                game_display.blit(menu_label_2, (menu_x + 20, menu_width - 20))

            pygame.display.update()
            clock.tick(fps)


window = MainWindow(width, height)
window.main()
