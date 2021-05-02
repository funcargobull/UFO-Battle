#Создай собственный Шутер!

from pygame import *
import random, sys
from time import sleep

stop_game = False

count_score = 0
count_lose = 0
highscore = 0

init()

W = 700
H = 500
FPS = 60

window = display.set_mode((W, H))
display.set_caption("UFO Battle")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
clock = time.Clock()
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

class Player(sprite.Sprite):
    def __init__(self, x, y, file):
        super().__init__()
        self.x = x
        self.y = y
        self.image = transform.scale(image.load(file), (80, 118))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    
    def update(self):
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= 5
        if keys_pressed[K_RIGHT] and self.rect.x < W - 87:
            self.rect.x += 5
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(sprite.Sprite):
    def __init__(self, x, y, file):
        super().__init__()
        self.x = x
        self.y = y
        self.speed = random.randint(1, 3)
        self.image = transform.scale(image.load(file), (85, 43))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        global count_lose
        if self.rect.y <= 550:
            self.rect.y += self.speed
        else:
            count_lose += 1
            self.kill()

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(sprite.Sprite):
    def __init__(self, x, y, file):
        super().__init__()
        self.x = x
        self.y = y
        self.image = transform.scale(image.load(file), (18, 36))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        if self.rect.y >= -10:
            self.rect.y -= 6
        else:
            self.kill()

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

player = Player(W/2, H - 118, "rocket.png")
font1 = font.SysFont("Arial", 25)
score = font1.render(f"Счет: {count_score}", True, (255, 255, 255))
lose = font1.render(f"Пропущено: {count_lose}", True, (255, 255, 255))
record = font1.render(f"Рекорд: {highscore}", True, (255, 255, 255))
score_place = score.get_rect(center=(50, 30))
lose_place = lose.get_rect(center=(80, 60))
record_place = record.get_rect(center=(60, 90))

font2 = font.SysFont("Arial", 72)
youwin = font2.render("YOU WIN!", True, (0, 255, 0))
youlose = font2.render("YOU LOSE!", True, (255, 0, 0))
youwin_place = youwin.get_rect(center=(W/2, H/2))
youlose_place = youlose.get_rect(center=(W/2, H/2))

bullets = sprite.Group()
ufos = sprite.Group()

for i in range(5):
    x_coord = random.randint(100, 600)
    y_coord = random.randint(-500, -20)
    ufos.add(Enemy(x_coord, y_coord, "ufo.png"))

running = True
while running:
    clock.tick(FPS)
    window.blit(background, (0, 0))
    window.blit(score, score_place)
    window.blit(lose, lose_place)
    window.blit(record, record_place)
    # print(player.vulnerability)

    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                mixer.music.load("fire.ogg")
                bullet = Bullet(player.rect.centerx - 9, player.rect.top, "bullet.png")
                bullets.add(bullet)
                mixer.music.play()
    
    if len(ufos.sprites()) < 5:
        x_coord = random.randint(100, 600)
        y_coord = random.randint(-500, -20)
        ufos.add(Enemy(x_coord, y_coord, "ufo.png"))

    keys_pressed = key.get_pressed()

    ufo_with_bullet = sprite.groupcollide(
        ufos, bullets, True, True
    )
    player_with_ufo = sprite.spritecollide(
        player, ufos, False
    )
    if ufo_with_bullet:
        count_score += 1
    if player_with_ufo:
        # stop_game = True
        # window.blit(youlose, youlose_place)
        if count_score > highscore:
            highscore = count_score
        count_lose = 0
        count_score = 0
        player.rect.x = W / 2 - 40
        player.rect.y = H - 118
        ufos.empty()

    if stop_game == False:
        ufos.draw(window)
        player.draw()
        bullets.draw(window)
        player.update()
        ufos.update()
        score = font1.render(f"Счет: {count_score}", True, (255, 255, 255))
        lose = font1.render(f"Пропущено: {count_lose}", True, (255, 255, 255))
        record = font1.render(f"Рекорд: {highscore}", True, (255, 255, 255))
        bullets.update()

    if count_lose == 5:
        stop_game = True
        keys_pressed = None
        window.blit(youlose, youlose_place)

    # if count_score == 50:
    #     stop_game = True
    #     keys_pressed = None
    #     window.blit(youwin, youwin_place)

    display.update()