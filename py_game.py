import pygame
import time

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Space invasion')
size = width, height = 1000 + 10, 730
screen = pygame.display.set_mode(size)
r_file = open('Scoreboard.txt', 'r', encoding='utf-8')
scoreboard = [i.strip() for i in r_file]
r_file.close()
name_input = False
end = 0
font_username = pygame.font.SysFont(None, 44)
end_screen_pause = False
inp_name = 'Введите имя: '
name = ''
scoreboard_show = False
save = True
bukv = {113: 'й', 119: 'ц', 101: 'у', 114: 'к', 116: 'е', 121: 'н', 117: 'г',
        105: 'ш', 111: 'щ', 112: 'з', 97: 'ф', 115: 'ы', 100: 'в', 102: 'а', 103: 'п',
        104: 'р', 106: 'о', 107: 'л', 108: 'д', 122: 'я', 120: 'ч', 99: 'с', 118: 'м',
        98: 'и', 110: 'т', 109: 'ь', 91: 'х', 93: 'ъ', 59: 'ж', 39: 'э', 44: 'б', 46: 'ю', 96: 'ё'}

motion = None
running = True
working = True
font = pygame.font.SysFont(None, 40)
font2 = pygame.font.SysFont(None, 20)
font_end_screen = pygame.font.SysFont(None, 30)
pause = True
Start_screen = True
logo_pic = pygame.image.load('Space_Invaders_logo.png')
logo_pos = x, y = 200, 220
logo_rect = logo_pic.get_rect(topleft=logo_pos)


class Game:
    def __init__(self):
        self.win = None
        self.scr = 0
        self.time_passed = 0
        self.win_pic = pygame.image.load('Winning_screen(for_Game).png')
        self.position = self.x, self.y = 270, 270
        self.win_rect = self.win_pic.get_rect(topleft=self.position)
        self.lose_pic = pygame.image.load('Loosing_screen(for_game).png')
        self.lose_rect = self.lose_pic.get_rect(topleft=self.position)

    def checker(self):
        if len(ship.aliens) == 0:
            self.win = True
            return True
        else:
            for i in ship.aliens:
                if i.alien_rect[1] + i.alien_rect[3] >= ship.ship_rect[1]:
                    self.win = False
                    return True
        return False

    def draw_win(self):
        screen.blit(self.win_pic, self.win_rect)

    def draw_lose(self):
        screen.blit(self.lose_pic, self.lose_rect)

    def score(self):
        text = font.render(str(self.scr), 0, (255, 255, 255))
        screen.blit(text, (5, 5))


class Spaceship:
    def __init__(self):
        self.position = self.x, self.y = (width - 10) // 2, height - 100
        self.speed = 10
        self.ship = pygame.image.load('Space_ship.png')
        self.ship_rect = self.ship.get_rect(topleft=self.position)
        self.direction = None
        self.projectiles = []
        self.overheat = 0
        self.aliens = []
        self.poz = True
        self.speed_boost = 0.003
        self.del_pr = []
        for j in range(20, 200, 60):
            if self.poz:
                for i in range(20, width - 75, 110):
                    self.aliens.append(Alien(i, j + 5))
                self.poz = False
            else:
                for i in range(80, width - 75, 110):
                    self.aliens.append(Alien(i, j + 5))
                    self.aliens[-1].reverse = True
                self.poz = True

    def kill(self):
        for i in self.aliens:
            if len(self.projectiles) > 0:
                for j in self.projectiles:
                    if i.alien_rect.colliderect(j.shot_rect):
                        del self.aliens[self.aliens.index(i)]
                        del self.projectiles[self.projectiles.index(j)]
                        game.scr += 50

    def move_left(self):
        if self.x - self.speed >= -10:
            self.x -= self.speed
            self.position = self.x, self.y
            self.ship_rect = self.ship.get_rect(topleft=self.position)

    def move_right(self):
        if self.x + self.speed <= width - 100:
            self.x += self.speed
            self.position = self.x, self.y
            self.ship_rect = self.ship.get_rect(topleft=self.position)

    def shoot(self):
        if self.overheat == 0:
            self.projectiles.append(Shooting(self.x + 56, self.y))
        self.overheat = 35

    def handle_projectiles(self):
        if self.overheat > 0:
            self.overheat -= 1
        if len(self.projectiles) > 0:
            for i in range(len(self.projectiles)):
                try:
                    self.projectiles[i].move()
                    self.projectiles[i].draw()
                    if self.projectiles[i].position[1] < 0:
                        del self.projectiles[i]
                except Exception:
                    pass

    def draw(self):
        screen.blit(self.ship, self.ship_rect)


class Shooting:
    def __init__(self, x, y):
        self.speed = 10
        self.shot = pygame.image.load('projectile.png')
        self.position = self.x, self.y = x, y
        self.shot_rect = self.shot.get_rect(topleft=self.position)

    def move(self):
        self.y -= self.speed
        self.position = self.x, self.y
        self.shot_rect = self.shot.get_rect(topleft=self.position)

    def draw(self):
        screen.blit(self.shot, self.shot_rect)


class Alien:
    def __init__(self, x, y):
        self.alien = pygame.image.load('S_I_alien2.png')
        self.speed = 3
        self.position = self.x, self.y = x, y
        # 20, 20
        self.alien_rect = self.alien.get_rect(topleft=self.position)
        self.reverse = False

    def move(self):
        if self.reverse is False:
            if self.x + self.speed <= width - 75:
                self.x += round(self.speed)
                self.position = self.x, self.y
                self.alien_rect = self.alien.get_rect(topleft=self.position)
            else:
                self.y += 60
                self.position = self.x, self.y
                self.alien_rect = self.alien.get_rect(topleft=self.position)
                self.reverse = True
        else:
            if self.x - self.speed >= 0:
                self.x -= round(self.speed)
                self.position = self.x, self.y
                self.alien_rect = self.alien.get_rect(topleft=self.position)
            else:
                self.y += 60
                self.position = self.x, self.y
                self.alien_rect = self.alien.get_rect(topleft=self.position)
                self.reverse = False

    def draw(self):
        screen.blit(self.alien, self.alien_rect)


def winning_screen(pic):
    global end_screen_pause, name_input, end, start_time
    position = 0
    while position != 280:
        screen.fill('black')
        screen.blit(pic, (position, 150))
        position += 4
        pygame.display.flip()
    end = end_time = pygame.time.get_ticks()
    text3 = font_end_screen.render(str((game.scr * 2) + (end_time - start_time)) + ' points', 0,
                                   (255, 255, 255))
    screen.blit(text3, (440, 589))
    pygame.display.update()
    end_screen_pause = True
    name_input = True
    time.sleep(4)
    screen.fill((0, 0, 0))


def losing_screen(pic):
    global end_screen_pause, name_input
    position = 0
    while position != 260:
        screen.fill('black')
        screen.blit(pic, (position, 150))
        position += 4
        pygame.display.flip()
    text3 = font_end_screen.render(str(game.scr) + ' points', 0, (255, 255, 255))
    screen.blit(text3, (440, 589))
    pygame.display.update()
    end_screen_pause = True
    name_input = True
    time.sleep(4)
    screen.fill((0, 0, 0))


def upd():
    global working, end_screen_pause, name_input, end
    screen.fill((0, 0, 0))
    if game.checker():
        working = False
    if working:
        game.score()
        ship.handle_projectiles()
        ship.draw()
        ship.kill()
        for i in range(len(ship.aliens)):
            ship.aliens[i].draw()
            ship.aliens[i].move()
            ship.aliens[i].speed += ship.speed_boost
    else:
        screen.fill((0, 0, 0))
        if end_screen_pause is False:
            if game.win is True:
                winning_screen(game.win_pic)
            else:
                losing_screen(game.lose_pic)
        else:
            username_text = font_username.render(inp_name + name, 0, (255, 255, 255))
            screen.blit(username_text, (350, 360))
    pygame.display.update()  # 30240


def scoreboard_screen():
    global scoreboard_show, scoreboard
    screen.fill((0, 0, 0))
    font_scoreboard = pygame.font.SysFont(None, 30)
    font_scoreboard_title = pygame.font.SysFont(None, 38)
    ranging = 30
    height_scoreboard = 250
    text_scoreboard_name = font_scoreboard_title.render('Таблица очков:', 0, (255, 255, 255))
    screen.blit(text_scoreboard_name, (355, height_scoreboard - 40))
    for i in range(len(scoreboard)):
        text_scoreboard = font_scoreboard.render(scoreboard[i], 0, (255, 255, 255))
        screen.blit(text_scoreboard, (395, height_scoreboard))
        pygame.display.update()
        height_scoreboard += ranging
    scoreboard_show = True


def sort_scoreboard():
    global scoreboard
    scoreboard_score = sorted([int(i.split()[1]) for i in scoreboard], reverse=True)
    scoreboard_2 = []
    for i in scoreboard_score:
        for j in scoreboard:
            if str(i) in j:
                scoreboard_2.append(j)
    return scoreboard_2


game = Game()
ship = Spaceship()
while running is True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if pause:
                start_time = pygame.time.get_ticks()
            pause = False
            if working:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
            else:
                if name_input is True:
                    k = event.key  # 303, 304 shift
                    if k != 13:
                        if k in bukv or k == 8:
                            if k == 8 and len(name) > 0:
                                name = name[:-1]
                            elif len(name) > 0:
                                name += bukv[k]
                            else:
                                if k in bukv:
                                    name += bukv[k].upper()
                            pygame.display.update()
                    else:
                        if save:
                            if game.win is True:
                                scoreboard.append(name + ' ' + str((game.scr * 2) + (end - start_time)))
                            else:
                                scoreboard.append(name + ' ' + str(game.scr))
                            save = False
                            counter = 0
                            scoreboard = sort_scoreboard()
                            scoreboard = scoreboard[0:6]
                            r_file = open('Scoreboard.txt', 'w', encoding='utf-8')
                            for i in scoreboard:
                                r_file.write(i + '\n')
                            r_file.close()
                            name_input = False
                        scoreboard_screen()

    if pause is False:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            ship.move_left()
        elif keys[pygame.K_RIGHT]:
            ship.move_right()
        if scoreboard_show is False:
            upd()
        else:
            time.sleep(7)
            running = False
        clock.tick(60)
        pygame.display.flip()
    else:
        if Start_screen is True:
            screen.fill((0, 0, 0))
            screen.blit(logo_pic, (logo_rect[0], logo_rect[1] - 40))
            font_start_screen = pygame.font.SysFont(None, 40)
            start_screen_text = font_start_screen.render('Нажмите любую клавишу для начала игры', 0, (255, 255, 0))
            screen.blit(start_screen_text, (220, 600))
            pygame.display.update()
pygame.quit()
