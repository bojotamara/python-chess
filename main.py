#!/usr/bin/python3
import pygame
from assets import *

pygame.init()

screen = pygame.display.set_mode((800,60*8))
pygame.display.set_caption('Boss Ass Chess Game')

#load background image
bg = pygame.image.load("assets/chessboard.png")
#blit like puts the image on there
screen.blit(bg, [0, 0])

wk = pygame.image.load("assets/wking.png")
screen.blit(wk, [0,0])
c=0
clock = pygame.time.Clock()
crashed = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                c+=60
                screen.blit(bg, [0,0])
                screen.blit(wk, [c,c])

        print(event)

    pygame.display.update()
    clock.tick(60)
