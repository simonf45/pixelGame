import pygame
import random
import os
import time
from os import path
list_of_cars = ['bil 1.png','bil 2.png','bil 3.']
img_dir = path.join(path.dirname(__file__), 'graphics')

WIDTH = 700
HEIGHT = 700
FPS = 60

border_right = 550
border_left = 150

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")
clock = pygame.time.Clock()

class Mob(pygame.sprite.Sprite):
     score = 0
     def __init__(self):
          pygame.sprite.Sprite.__init__(self)
          self.image = car_img
          self.image.set_colorkey(BLACK)
          #self.image = pygame.Surface((30,40)) #Rectangle, width and eight
          #self.image.fill(RED) #Define the rectangle
          self.rect = self.image.get_rect()
          self.score = 0
          
          self.radius = int(self.rect.height - 55)
          #pygame.draw.circle(self.image, RED, self.rect.center, self.radius) #Draw circle in car, hit reg

          self.rect.x = random.randrange(border_left,border_right - 30)
          #self.rect.x = random.randrange(WIDTH - self.rect.width)
          self.rect.y = random.randrange(-200, -40)

          self.speedy = random.randrange(1, 8)
          self.speedx = random.randrange(-3,3)

     def update(self):
          #self.rect.x +=self.speedx # Make mobs drive in different directions, rather than straight
          self.rect.y += self.speedy
          if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20: #If mob is out of edge, respawn.
               self.rect.x = random.randrange(border_left + 10,border_right - 60)#width of spawning
               self.rect.y = random.randrange(-200, -100) #Height of spawning
               self.speedy = random.randrange(2, 8) #Speed of mob from 2-8


class Player(pygame.sprite.Sprite):
     def __init__(self):
          pygame.sprite.Sprite.__init__(self)

          #self.image = player_img.transform.scale(player_img, (50,30)) #Resize image
          self.image = player_img
          self.image.set_colorkey(BLACK) #remove black background from image
          self.rect = self.image.get_rect()
          
          self.radius = int(self.rect.height - 57)
          #pygame.draw.circle(self.image, RED, self.rect.center,self.radius) #Draw circle in car, hit reg
          
          self.rect.centerx = WIDTH / 2 #Placement of X axis
          self.rect.bottom = HEIGHT - 10 #Placement of Y axis
          self.speedx = 0 #Speed of player

     def update(self):
          self.speedx = 0
          keystate = pygame.key.get_pressed()
          if keystate[pygame.K_LEFT]:
               self.speedx = -5
          if keystate[pygame.K_RIGHT]:
               self.speedx =5
               
          #Border control for player
          if self.rect.right > border_right:
               self.rect.right = border_right
          if self.rect.left < border_left:
               self.rect.left = border_left
               
          self.rect.x += self.speedx


#Load all game graphics
background = pygame.image.load(path.join(img_dir, "Map.png")).convert()
background_rect = background.get_rect()

player_img = pygame.image.load(path.join(img_dir,"bil 2.png")).convert()
car_img = pygame.image.load(path.join(img_dir,"bil 3.png")).convert()


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


#Spawn mobs, amount.
for i in range(4):
     m = Mob()
     all_sprites.add(m)
     mobs.add(m)


#Game config
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
             running = False
             
    all_sprites.update()

    #Check to see if mob hit player
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle) #False or True
    if hits:
         running = False
         print("GAME OVER!")

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    
    # *after* drawing everything, flip the display
    pygame.display.flip()
pygame.quit()
