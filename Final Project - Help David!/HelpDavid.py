import pygame
from pygame.locals import *
from sys import exit

pygame.init()

# map size
width = 700
heigth = 480

# main character position
character = pygame.image.load('sprites\spritesheet32px.png')
b = 0
x_sprite = 0
y_sprite = 0
x = 555
y = 150

# objects
cs50david = pygame.image.load('sprites\cs50davidmalan.png')
xd = 515
yd = 140
stressball = pygame.image.load('sprites\stressball.png')
xb = 630
yb = 470
stressballpickup = 0
computer = pygame.image.load('sprites\computer.png')
xc = 135
yc = 295
computerpickup = 0
cs50duck = pygame.image.load('sprites\cs50duck.png')
xcd = 140
ycd = 510
cs50duckpickup = 0

# all objects picked up
sum = (cs50duckpickup + computerpickup + stressballpickup)

# songs
song = pygame.mixer.music.load('songs\Traverse_town_song_8bit.mp3')
pygame.mixer.music.play(-1)
picked_object = pygame.mixer.Sound('songs\picked_object.wav')

# screen datas
time = pygame.time.Clock()
screen = pygame.display.set_mode((width, heigth))
background = pygame.image.load('sprites\map.png')
tree = pygame.image.load('sprites\Tree.png')
flag = pygame.image.load('sprites\Flag.png')
help = pygame.image.load('sprites\TextbarHelp.png')
win = pygame.image.load('sprites\TextbarWin.png')
pygame.display.set_caption("CS50 Final Project - Help David!")

# camera
map_surface = pygame.Surface((background.get_width(), background.get_height()))

while True:
    time.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    map_surface.blit(background, (0,0))

    # objects
    d = map_surface.blit(cs50david,(xd, yd))
    s = map_surface.blit(stressball, (xb,yb))
    c = map_surface.blit(computer, (xc,yc))
    cd = map_surface.blit(cs50duck, (xcd, ycd))

    thiago = map_surface.blit(character, (x, y), ((x_sprite)*32, y_sprite*32, 32, 32))
    
    # thiago = pygame.draw.rect(map_surface, (255,255,255), (x, y, 16, 16))
    map_surface.blit(tree, (321,299))
    map_surface.blit(tree, (174,477))
    map_surface.blit(tree, (147,380))
    map_surface.blit(tree, (405,382))
    map_surface.blit(tree, (159,260))
    map_surface.blit(flag, (191, 406))
    map_surface.blit(flag, (584, 401))
    map_surface.blit(flag, (278, 280))

    # main character movement
    b += 1
    if b > 29:
        b = 0
    elif b == 0:
        x_sprite += 1
    elif b == 9:
        x_sprite += 1
    elif b == 19:
        x_sprite += 1
    elif b == 29:
        x_sprite += 1
    
    if x_sprite > 3:
        x_sprite = 0
    if pygame.key.get_pressed()[K_a]:
        y_sprite = 4
        x = x - 1
    elif pygame.key.get_pressed()[K_d]:
        y_sprite = 3
        x = x + 1
    elif pygame.key.get_pressed()[K_s]:
        y_sprite = 1
        y = y + 1
    elif pygame.key.get_pressed()[K_w]:
        y_sprite = 2
        y = y - 1
    else:
        if y_sprite == 1:
            y_sprite = 0    
        elif y_sprite == 2:
            y_sprite = 8
        elif y_sprite == 3:
            y_sprite = 6
        elif y_sprite == 4:
            y_sprite = 7

    # picking up objects
    if thiago.colliderect(s):
        if pygame.key.get_pressed()[K_p]:
            y_sprite = 5
            xb = 0
            yb = 0
            stressballpickup = 1
            picked_object.play()
            print("A lecture object was picked up.")
        
    if thiago.colliderect(c):
        if pygame.key.get_pressed()[K_p]:
            y_sprite = 5
            xc = 32
            yc = 0
            computerpickup = 1
            picked_object.play()
            print("The computer was picked up.")
        
    if thiago.colliderect(cd):
        if pygame.key.get_pressed()[K_p]:
            y_sprite = 5
            xcd = 64
            ycd = 0 
            cs50duckpickup = 1
            picked_object.play()
            print("A lecture object was picked up.")

    # talking to david
    if thiago.colliderect(d):
        if sum < 3:
            map_surface.blit(help, (460, 100))

        if pygame.key.get_pressed()[K_g]:
            if sum < 3:
                print("You gotta pick the other lecture objects.")
            if sum == 3:
                y_sprite = 5
                xc, yc = 500, 155
                xb, yb = 565, 128
                xcd, ycd = 545, 139    

    if xc == 500:
        sum = sum + 1
    if sum == 4:
            map_surface.blit(win, (460, 100))

    # top wall
    if y <= 133:
        y = 133
    # top-left tree wall   
    if  x <= 470 and y < 271:
        x = 470
    # left side tree wall
    elif y < 280 and x < 470:
        y = 280
    elif x < 90:
        x = 90
    elif x < 134 and y < 350:
        x = 134
    elif x <= 133 and y < 351:
        y = 352
    
    # right side tree wall
    if x >= 600 and y < 388:
        x = 600
    elif x >= 632 and y < 600:
        x = 632
    
    # bottom wall
    if x <= 500 and y >=543:
        y = 543
    elif x <= 185 and y >= 520:
        y = 520
    elif y >= 487 and x > 500:
        y = 487
    elif x > 512 and y > 549:
        x = 512
    
    sum = (cs50duckpickup + computerpickup + stressballpickup)

    # camera move
    xcam = x + 8 - (width / (6))
    ycam = y + 8 - (heigth / (6))
    camrect = pygame.Rect(xcam, ycam, width/3, heigth/3)
    camrect.clamp_ip(map_surface.get_rect())

    camera_surface = map_surface.subsurface(camrect)
    scaled_surface = pygame.transform.scale(camera_surface, (width, heigth))
    
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()
