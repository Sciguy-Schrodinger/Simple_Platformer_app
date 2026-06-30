import pygame # Origin is top left
import random
import time
import sys
import datetime
from datetime import timedelta
from pygame import mixer
import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path('.')

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1700,1700))
pygame.display.flip()

width = 1700
height = 1700
ground_width = 50
Game_Over = False

score = 0
old_time = datetime.datetime.now()

collect_coin = pygame.mixer.Sound(base_path / 'Mario_coin_sound.mp3')
game_over = pygame.mixer.Sound(base_path / 'Mario_death_sound.mp3')
music = pygame.mixer.music.load(base_path / 'Mario_tune.mp3')
pygame.mixer.music.play(-1)

pygame.display.set_caption("Platformer")
Background = pygame.image.load(base_path / "Background.png")
platform_big = pygame.image.load(base_path / "Platform.png")
platform = pygame.transform.scale(platform_big,(350,75))
player_big_left = pygame.image.load(base_path / "Mario_Left.png")
player_left = pygame.transform.scale(player_big_left,(100,100))
player_big_right = pygame.image.load(base_path / "Mario_Right.png")
player_right = pygame.transform.scale(player_big_right,(100,100))
player_big_jump = pygame.image.load(base_path / "Mario_Jump.png")
player_jump = pygame.transform.scale(player_big_jump,(100,100))
player_big_still = pygame.image.load(base_path / "Mario.png")
player_still = pygame.transform.scale(player_big_still,(100,100))
player_big_death = pygame.image.load(base_path / "Mario_Death.png")
player_death = pygame.transform.scale(player_big_death,(100,100))
coin_big = pygame.image.load(base_path / "coin.png")
coin = pygame.transform.scale(coin_big,(50,50))
baddie_big = pygame.image.load(base_path / "Goomba.png")
baddie = pygame.transform.scale(baddie_big,(100,100))

baddie_width = 100
player_width = 100

move_left = False
move_right = False
jump = False
on_ground = False

x_p = 0.1*width
y_p = 0.1*height

x_c = random.randint(int(-width/25.0),int(width))
y_c = 0

def Baddie(x,y):
    screen.blit(baddie,(x,y))
    
def Player_left(x,y):
    screen.blit(player_left,(x,y))

def Player_right(x,y):
    screen.blit(player_right,(x,y))

def Player_jump(x,y):
    screen.blit(player_still,(x,y))

def Player_death(x,y):
    screen.blit(player_death,(x,y))
    
def Coin(x,y):
    screen.blit(coin,(x,y))
        
def Game_over():
    Game_Over = True
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(game_over)
    close = datetime.datetime.now() + timedelta(seconds=3)
    while datetime.datetime.now() < close:
        Player_death(x_p,y_p+10)
        font = pygame.font.Font(pygame.font.get_default_font(),75)
        Game_Over_text = font.render('Game Over! Your score is: '+str(score),True,pygame.Color(255,255,255),pygame.Color(0,0,0))
        screen.blit(Game_Over_text,(width/4.5,0))
        pygame.display.update()
    pygame.quit()
    sys.exit()
    
num_of_bad_guys = random.randint(1,6)

x_bs = []
y_bs = []
delta_x = []
delta_y = []

for i in range(num_of_bad_guys):
    x_b = random.randint(int(-width + ground_width),int(width - ground_width))
    y_b = random.randint(int(-width + ground_width),int(width - ground_width))
    while x_b == 0 or y_b == 0:
            x_b = random.randint(int(-width + ground_width),int(width - ground_width))
            y_b = random.randint(int(-width + ground_width),int(width - ground_width))
    x_bs.append(x_b)
    y_bs.append(y_b)
    
def background():
    screen.blit(Background,(0,0))
    ground_1 = screen.blit(platform,(0.1*width,0.5*height))
    ground_2 = screen.blit(platform,(0.4*width,0.3*height))
    ground_3 = screen.blit(platform,(0.7*width,0.5*height))
    
def Score():
    font = pygame.font.Font(pygame.font.get_default_font(),25)
    Score_text = font.render('Score: '+str(score),True,pygame.Color(255,255,255),pygame.Color(0,0,0))
    screen.blit(Score_text,(807*width/1700,0))

for i in range(num_of_bad_guys):
    delta_x.append(random.randint(-2,2))
    delta_y.append(random.randint(-2,2))
    
while not Game_Over:
    background()
    Score()
    for i in range(num_of_bad_guys):
        delta_x.append(random.randint(-2,2))
        delta_y.append(random.randint(-2,2))
        Baddie(x_bs[i],y_bs[i])
        x_bs.append(delta_x[i])
        y_bs.append(delta_y[i])
        x_bs[i] += delta_x[i]
        y_bs[i] += delta_y[i]
    Coin(x_c,y_c)
    y_c += 2
    y_p += 3
    if move_left:
        Player_left(x_p,y_p)
    if move_right:
        Player_right(x_p,y_p)
    if not move_left and not move_right:
        Player_jump(x_p,y_p)
    if (y_p >= 0.445*height and x_p >= 0.1*width and x_p <= 0.275*width): # ground 1
        y_p = 0.445*height
        on_ground = True
    if (y_p >= 0.445*height and x_p >= 0.7*width and x_p <= 0.875*width): # ground 2
        y_p = 0.445*height
        on_ground = True
    if (y_p >= 0.25*height and y_p <= 0.235*height + ground_width and x_p >= 0.4*width and x_p <= 0.575*width): # ground 3 above
        y_p = 0.25*height
        on_ground = True
    if (y_p >= 0.4*height + ground_width and x_p >= 0.4*width and x_p <= 0.575*width): # ground 3 below
        y_p += 3

    if (y_c >= 0.465*height and x_c >= 0.1*width and x_c <= 0.275*width): # ground 1
        y_c = 0.465*height
    if (y_c >= 0.465*height and x_c >= 0.7*width and x_c <= 0.875*width): # ground 2
        y_c = 0.455*height
    if (y_c >= 0.4*height + ground_width and y_c <= 0.275*height + ground_width and x_c >= 0.4*width and x_c <= 0.575*width): # ground 3 above
        y_c = 0.4*height + ground_width
    if (y_c >= 0.25*height + ground_width and x_c >= 0.4*width and x_c <= 0.575*width): # ground 3 below
        y_c = 0.25*height + ground_width

    player_rect = pygame.Rect(x_p,y_p,player_width,player_width)
    
    for i in range(num_of_bad_guys):
        if (y_bs[i] >= 0.445*height and x_bs[i] >= 0.1*width and x_bs[i] <= 0.275*width): # ground 1
            y_bs[i] = 0.445*height
        if (y_bs[i] >= 0.445*height and x_bs[i] >= 0.7*width and x_bs[i] <= 0.875*width): # ground 2
            y_bs[i] = 0.445*height
        if (y_bs[i] >= 0.25*height and y_bs[i] <= 0.235*height + ground_width and x_bs[i] >= 0.4*width and x_bs[i] <= 0.575*width): # ground 3 above
            y_bs[i] = 0.25*height
        if (y_bs[i] >= 0.25*height + ground_width and x_bs[i] >= 0.4*width and x_bs[i] <= 0.575*width): # ground 3 below
            y_bs[i] += 3
        baddie_rect = pygame.Rect(x_bs[i],y_bs[i],baddie_width,baddie_width)
        if player_rect.colliderect(baddie_rect): # collision
            Game_over()
    
        if x_bs[i] < -width/25.0:
            x_bs[i] = width
            x_bs[i] -= 1
            Baddie(x_bs[i],y_bs[i])

        if x_bs[i] > width:
            x_bs[i] = -width/25.0
            x_bs[i] += 1
            Baddie(x_bs[i],y_bs[i])

        if y_bs[i] > 0.57*height:
            y_bs[i] = 0
            y_bs[i] += 1
            Baddie(x_bs[i],y_bs[i])
        
        if y_bs[i] < 0:
            y_bs[i] = 0.57*height
            x_bs[i] += 1
            Baddie(x_bs[i],y_bs[i])
        
    if y_p > 0.57*height:
        Game_over()
    
    if y_c > 0.57*height:
        x_c = random.randint(int(-width/25.0),int(width))
        y_c = 0
        Coin(x_c,y_c)

    if x_p < 1.1*x_c and y_p < 1.1*y_c and x_p > 0.9*x_c and y_p > 0.9*y_c:
        score += 1
        num_of_bad_guys = random.randint(1,6)
        x_bs = []
        y_bs = []
        for i in range(num_of_bad_guys):
            x_b = random.randint(int(-width/25.0),int(width))
            y_b = random.randint(int(-width/25.0),int(width))
            x_bs.append(x_b)
            y_bs.append(y_b)
            Baddie(x_bs[i],y_bs[i])

        pygame.mixer.Sound.play(collect_coin)
        x_c = random.randint(-int(width/25.0),int(width))
        y_c = 0
        Coin(x_c,y_c)
    pygame.display.update()
    for event in pygame.event.get():
        pygame.key.set_repeat(1,1)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
                move_right = False
                jump = False
            elif event.key == pygame.K_RIGHT:
                move_left = False
                move_right = True
                jump = False
            elif event.key == pygame.K_UP:
                move_left = False
                move_right = False
                jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
                move_right = False
                jump = False
            elif event.key == pygame.K_RIGHT:
                move_left = False
                move_right = False
                jump = False
            elif event.key == pygame.K_UP:
                move_left = False
                move_right = False
                jump = False
                on_ground = False
        if move_left:
            x_p -= 1
            Player_left(x_p,y_p)
            if x_p < -width/25.0:
                x_p = width
                x_p -= 1
                Player_left(x_p,y_p)
        if move_right:
            x_p += 1
            Player_right(x_p,y_p)
            if x_p > width:
                x_p = -width/25.0
                x_p += 1
                Player_right(x_p,y_p)
        if jump and on_ground:
            y_p -= 600*random.random()
            if y_p <= 0:
                y_p = 0
            jump = False
            on_ground = False
            Player_jump(x_p,y_p)
