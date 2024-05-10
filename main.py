#Создай собственный Шутер!
from pygame import *
from random import choice, randint
from time import time as timer
mixer.init()
font.init()

window = display.set_mode((700, 500))
missed = 0
shotdown = 0
num_fire = 0
rel_time = False
display.set_caption('Space Shooter')
base_font = font.SysFont(None, 35)
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
lose_back = transform.scale(image.load('failed.png'), (700, 500))
win_back = transform.scale(image.load('winn.png'), (700, 500))
reload_label = base_font.render('Wait, reload..', True, (255, 0,0))
shot = mixer.Sound('fire.ogg')
mixer.music.load('space.ogg')
mixer.music.play(-1)
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, cor_x, cor_y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = cor_x
        self.rect.y = cor_y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if (keys_pressed[K_d] or keys_pressed[K_RIGHT]) and self.rect.x < 635:
            self.rect.x += self.speed            
        if (keys_pressed[K_a] or keys_pressed[K_LEFT]) and self.rect.x > 5:
            self.rect.x -= self.speed
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.rect.y = 10
        if self.rect.y >= 555:
            self.rect.y = 10
            self.rect.x = randint(30, 650)
            self.speed = randint(1, 5)
            global missed
            missed += 1
class SpaceObjects(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= -20:
            self.rect.y = 10
        if self.rect.y >= 555:
            self.rect.y = 10
            self.rect.x = randint(30, 650)
            global missed
            missed += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -30:
            self.remove(bullets)
Spaceship = Player('rocket.png', 450, 420, 65, 75, 5)
Alien1 = Enemy('ufo.png', randint(30, 650), 10, 65, 45, randint(1, 5))
Alien2 = Enemy('ufo.png', randint(30, 650), 10, 65, 45, randint(1, 5))
Alien3 = Enemy('ufo.png', randint(30, 650), 10, 65, 45, randint(1, 5))
Alien4 = Enemy('ufo.png', randint(30, 650), 10, 65, 45, randint(1, 5))
Alien5 = Enemy('ufo.png', randint(30, 650), 10, 65, 45, randint(1, 5))
Aliens = sprite.Group()
Aliens.add(Alien1, Alien2, Alien3, Alien4, Alien5)
black_hole = SpaceObjects('black_fall.png', randint(30, 650), 0, 80, 80, 1)
bullets = sprite.Group()
clock = time.Clock()

procces = True
finish = False
while procces:
    for e in event.get():
        if e.type == QUIT:
            procces = False
        if finish != True:
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if num_fire < 10 and rel_time == False:
                        shot.play()
                        bullet = Bullet('bullet.png', Spaceship.rect.centerx, Spaceship.rect.top,
                            15, 35, 7)
                        bullets.add(bullet)
                        num_fire += 1
                    if num_fire >= 10 and rel_time == False:
                        start_rel = timer()
                        rel_time = True
    if finish == False:
        window.blit(background, (0, 0))
        window.blit(base_font.render(f'Счёт: {shotdown}', True, (255, 255, 255)), (10, 10))
        window.blit(base_font.render(f'Пропущено: {missed}', True, (255, 255, 255)), (10, 40))
        Spaceship.reset()
        Spaceship.update()
        bullets.update()
        bullets.draw(window)
        Aliens.update()
        Aliens.draw(window)
        black_hole.update()
        black_hole.reset()
        if rel_time == True:
            end_rel = timer()
            if end_rel - start_rel < 3:
                window.blit(reload_label, (360, 460))
            else:
                num_fire = 0
                rel_time = False
        if sprite.groupcollide(bullets, Aliens, True, True):
            Alien = Enemy(choice(['ufo', 'asteroid'])+'.png', randint(30, 650), 10, 65, 45, randint(1, 5))
            Aliens.add(Alien)
            shotdown += 1
        if sprite.spritecollide(black_hole, Aliens, True):
            Alien = Enemy(choice(['ufo', 'asteroid'])+'.png', randint(30, 650), 10, 65, 45, randint(1, 5))
            Aliens.add(Alien)
        if sprite.spritecollide(black_hole, bullets, True):
            pass
        if shotdown >= 12:
            mixer.music.load('win_music.mp3'); mixer.music.play(-1)
            finish = True
            window.blit(win_back, (0,0))
        elif missed >= 4 or sprite.spritecollide(Spaceship, Aliens, False) or sprite.collide_rect(Spaceship, black_hole):
            mixer.music.load('lose_music.mp3'); mixer.music.play(-1)
            finish = True
            window.blit(lose_back, (0,0))
    display.update()
    clock.tick(60)