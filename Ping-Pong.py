from pygame import *

# pygame.init()
# transform.init()
window = display.set_mode((700, 256))
display.set_caption('Ping-Pong')

background = transform.scale(image.load('ping-pong.jpg'), (700, 256))

procces = True
clock = time.Clock()

while procces:
    for e in event.get():
        if e.type == QUIT:
            procces = False
    window.blit(background, (0,0))
    
    clock.tick(60)
    display.update()