#!/usr/bin/python3
import pygame
from assets import *

pygame.init()

screen = pygame.display.set_mode((800,500))
pygame.display.set_caption('Boss Ass Chess Game')

#load background image
bg = pygame.image.load("chessboard.png")
#blit like puts the image on there
screen.blit(bg, [0, 0])

clock = pygame.time.Clock()
crashed = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        print(event)

    pygame.display.update()
    clock.tick(60)
