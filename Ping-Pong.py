from pygame import *
from random import choice
mixer.init()

# Create Constants
TOP = 0
BOTTOM = 650
LEFT = 0
RIGHT = 850
# Now create bot point selection
Y_select = None

# Load music
mixer.music.load('Flames of war.mp3')
mixer.music.play(-1)

# Also
window = display.set_mode((900, 700))
display.set_caption('Ping-Pong')

background = transform.scale(image.load('background.png'), (900, 700))
class GameSprite(sprite.Sprite):
    '''It is super class for all next classes'''
    def __init__(self, sprite_image, cor_x, cor_y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (w, h))
        self.width = w
        self.height = h
        self.rect = self.image.get_rect()
        self.rect.x = cor_x
        self.rect.y = cor_y
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class PlayerLeft(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_s] and self.rect.y < 620:
            self.rect.y += self.speed            
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
class Ball(sprite.Sprite):
    def __init__(self, picture, w, h, speed_x, speed_y): # We don't specify X and Y because the ball will always be in the center of the screen.
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = int(str(window)[9:str(window).find('x')]) / 2.1 # This probably weird scheme works like this: we get a window instance, 
                                                                    # and then we cut off a segment of the digit x (Start to x), and convert that string to a number, then divide by two
        self.rect.y = int(str(window)[str(window).find('x')+1:-8]) / 2.1 # A similar situation occurs here, but here we are looking for the segment after the letter x and until the end of the characters in the ordinate
        self.speed_x = speed_x
        self.speed_y = speed_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x <= LEFT:
            self.speed_x *= -1
        if self.rect.x >= RIGHT:
            self.speed_x *= -1
        if self.rect.y <= TOP:
            # if self.speed_y <= 0.2 and self.speed_y > 0:
            #     self.speed_y = -0.6
            self.speed_y *= -1
        if self.rect.y >= BOTTOM:
            self.speed_y *= -1
        if sprite.collide_rect(self, player_left):
            if self.rect.bottom == player_left.rect.top: # if Ball bottom collide Player Top
                self.speed_y *= -1
            if self.rect.top == player_left.rect.bottom: # if Ball top collide Player bottom
                self.speed_y *= -1
            print(self.speed_y)
            # self.speed_y *= choice([0.5, 0.75, 2])
            self.speed_y = round(self.speed_y, 2)
            self.speed_x *= -1
        if sprite.collide_rect(self, player_right):
            if self.rect.bottom == player_right.rect.top: # if Ball bottom collide Player Top
                self.speed_y *= -1
            if self.rect.top == player_right.rect.bottom: # if Ball top collide Player bottom
                self.speed_y *= -1
            print(self.speed_y)
            # self.speed_y *= choice([0.5, 0.75, 2])
            self.speed_y = round(self.speed_y, 2)
            self.speed_x *= -1
class Bot(GameSprite):
    def Think(self):
        if ball.speed_x > 0:
            if ball.speed_y > 0:
                select_x = ball.rect.x
                select_y = ball.rect.y
                while select_y < BOTTOM and select_x < RIGHT:
                    select_y += ball.speed_y
                    select_x += ball.speed_x
                
            elif ball.speed_y < 0:
                select_x = ball.rect.x
                select_y = ball.rect.y
                while select_y > TOP and select_x < RIGHT:
                    select_y += ball.speed_y
                    select_x += ball.speed_x
            global Y_select
            try:
                Y_select = select_y
            except:
                select_y = ball.rect.y
                Y_select = select_y
    def bot_move(self):
        if self.rect.y < BOTTOM - (self.height - 50) and Y_select > self.rect.y:
            self.rect.y += self.speed            
        if self.rect.y > 0 and Y_select < self.rect.y:
            self.rect.y -= self.speed

player_left = PlayerLeft('bot.png', 50, 250, 180, 180, 7)
ball = Ball('ball.png', 50, 50, 8, 8)
player_right = Bot('bot.png', 760, 250, 180, 180, 7)
procces = True
clock = time.Clock()

while procces:
    for e in event.get():
        if e.type == QUIT:
            procces = False
    window.blit(background, (0,0))
    player_left.reset()
    player_left.update()
    ball.reset()
    ball.update()
    player_right.Think()
    player_right.bot_move()
    player_right.reset()
    clock.tick(60)
    display.update()

# Important comment - Sorry, but I am can't speak English :(
# I know only some words in English and often use a translater.