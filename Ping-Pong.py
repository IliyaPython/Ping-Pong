from pygame import *

# pygame.init()
# transform.init()
window = display.set_mode((700, 256))
display.set_caption('Ping-Pong')

background = transform.scale(image.load('ping-pong.jpg'), (700, 256))
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
procces = True
clock = time.Clock()

while procces:
    for e in event.get():
        if e.type == QUIT:
            procces = False
    window.blit(background, (0,0))

    clock.tick(60)
    display.update()
