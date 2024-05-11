from pygame import *
from random import choice
from time import time as timer
mixer.init()
font.init()

# Now create bot point selection
Y_select = None
# Load music
mixer.music.load('back_music.ogg')
mixer.music.play(-1)
new_round = mixer.Sound('new_round.ogg')
start_game = mixer.Sound('start_game.ogg')
# Also
window = display.set_mode((900, 700))
display.set_caption('Ping-Pong')
# Create Constants
TOP = 0
BOTTOM = 650
LEFT = 0
RIGHT = 850
CENTERX = int(str(window)[9:str(window).find('x')]) / 2.1
CENTERY = int(str(window)[str(window).find('x')+1:-8]) / 2.1
# Create Base and Special font
base_font = font.SysFont('Arial', 80)
special_font = font.SysFont('Arial', 30)
small_font = font.SysFont('Arial', 15)
# Select background for menu and game
menu_fon = transform.scale(image.load('background'+choice(['1','2','3'])+'.jpg'), (900, 700))
background = transform.scale(image.load('background.jpg'), (900, 700))
# Create classes and functions
def return_to_start(p_left, p_right, ball):
    start_timer = timer()
    end_timer = timer()
    new_round.play()
    while end_timer - start_timer < 3:
        end_timer = timer()
    p_left.rect.y = int(str(window)[str(window).find('x')+1:-8]) / 2.5
    p_right.rect.y = int(str(window)[str(window).find('x')+1:-8]) / 2.5
    ball.rect.x = int(str(window)[9:str(window).find('x')]) / 2.1
    ball.rect.y = int(str(window)[str(window).find('x')+1:-8]) / 2.1
    
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
        if keys_pressed[K_s] and self.rect.y < BOTTOM - (self.height - 50):
            self.rect.y += self.speed            
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
class PlayerRight(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_DOWN] and self.rect.y < BOTTOM - (self.height - 50):
            self.rect.y += self.speed            
        if keys_pressed[K_UP] and self.rect.y > 0:
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
            player_right.counter += 1
            return_to_start(player_left, player_right, self)
            self.speed_x *= -1
        if self.rect.x >= RIGHT:
            player_left.counter += 1
            return_to_start(player_left, player_right, self)
            self.speed_x *= -1
        if self.rect.y <= TOP:
            # if self.speed_y <= 0.2 and self.speed_y > 0:
            #     self.speed_y = -0.6
            self.speed_y *= -1
        if self.rect.y >= BOTTOM:
            self.speed_y *= -1
        if sprite.collide_rect(self, player_left):
            if abs(self.rect.bottom - player_left.rect.top) <= 10: # if Ball bottom collide Player Top
                self.speed_y *= -1
            if abs(self.rect.top - player_left.rect.bottom) <= 10: # if Ball top collide Player bottom
                self.speed_y *= -1
            self.speed_y = round(self.speed_y, 2)
            self.speed_x *= -1
        if sprite.collide_rect(self, player_right):
            if abs(self.rect.bottom - player_left.rect.top) <= 20: # if Ball bottom collide Player Top
                self.speed_y *= -1
            if abs(self.rect.top - player_left.rect.bottom) <= 20: # if Ball top collide Player bottom
                self.speed_y *= -1
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
        random = choice([10,1,1,1,1,1,1,1,10,10]) # So, this can be explained this way: the chances of our bot being WRONG are 3/10 = 0.3 = 30 %
        if self.rect.y < BOTTOM - (self.height - 50) and Y_select > self.rect.centery *(random): # We make sure that the bot makes mistakes in calculations from time to time, and gives the player a chance
            self.rect.y += self.speed            
        if self.rect.y > 0 and Y_select < self.rect.centery *(random):
            self.rect.y -= self.speed
class Button(GameSprite):
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x,y)
# Create a buttons for menu
player_player = Button('PLAYER_PLAYER.png', 250, 140, 400, 205, 0)
player_bot = Button('PLAYER_BOT.png', 250, 390, 400, 205, 0)
license = GameSprite('CC_LICENSE.png', 20, 650, 40, 40, 0)
# Create values-flags
menu = True
procces = True

clock = time.Clock()
player_left = PlayerLeft('player_left.png', 0, 250, 100, 180, 7)
ball = Ball('ball.png', 50, 50, 6, 5) # For ball movement to work correctly, 
                                        # do not make the speed arguments the same! Otherwise it will get stuck
while procces:
    # Procces menu, when human can choise type of game
    while menu:
        window.blit(menu_fon, (0,0))
        window.blit(base_font.render(f'Ping-Pong', True, (0, 0, 0)), (300, 30))
        for e in event.get():
            if e.type == QUIT:
                menu = False
                procces = False
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if player_player.collidepoint(x, y):
                    menu = False
                    player_right = PlayerRight('player_right.png', 800, 250, 100, 180, 7)
                    player_right_won = mixer.Sound('win_right.ogg')
                    win_sound = mixer.Sound('left_win.ogg') # for the left player
                if player_bot.collidepoint(x, y):
                    menu = False
                    player_right = Bot('player_right.png', 800, 250, 100, 180, 7)
                    player_right_won = mixer.Sound('win_bot.ogg')
                    win_sound = mixer.Sound('bot_angry.ogg') # for the left player
                # Now create counters for points and timer before the game
                try:
                    player_right.counter = 0 # Reset counters
                    player_left.counter = 0  # Reset counters
                    # Same timer
                    start_timer = timer()
                    end_timer = timer()
                    start_game.play()
                    while end_timer - start_timer < 3:
                        end_timer = timer()
                except NameError:
                    pass
        license.reset()
        player_player.reset()
        player_bot.reset()
        clock.tick(60)
        display.update()
    if procces == False:
        break # This is so that after exiting the game will immediately stop
    for e in event.get():
        if e.type == QUIT:
            procces = False
    window.blit(background, (0,0))
    # Show counters for every player
    window.blit(special_font.render(f'Player: {player_left.counter}', True, (0, 0, 0)), (20, 20))
    window.blit(special_font.render(f'Player: {player_right.counter}', True, (0, 0, 0)), (790, 20))
    player_left.reset()
    player_left.update()
    ball.reset()
    ball.update()
    try: # Trying to go if it's a bot
        player_right.Think()
        player_right.bot_move()
    except AttributeError: # We move differently if the player
        player_right.update()
    player_right.reset()
    if player_left.counter >= 6:
        start_timer = timer()
        end_timer = timer()
        win_sound.play()
        window.blit(base_font.render(f'Player Left Win!', True, (255, 0, 0)), (200, CENTERY))
        display.update() # To display the text above
        while end_timer - start_timer < 3:
            end_timer = timer()
        menu = True # return to menu
    if player_right.counter >= 6:
        start_timer = timer()
        end_timer = timer()
        player_right_won.play()
        window.blit(base_font.render(f'Player Right Win!', True, (0, 0, 255)), (200, CENTERY))
        display.update() # To display the text above
        while end_timer - start_timer < 3:
            end_timer = timer()
        menu = True # return to menu
    clock.tick(60)
    display.update()
# Important comment - Sorry, but I am can't speak English :(
# I know only some words in English and often use a translater.