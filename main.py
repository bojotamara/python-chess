#!/usr/bin/python3
import pygame
# from assets import *
from board import *

pygame.init()

screen = pygame.display.set_mode((800,60*8))
pygame.display.set_caption('Boss Ass Chess Game')

#load background image
bg = pygame.image.load("assets/chessboard.png")
#blit like puts the image on there
screen.blit(bg, [0, 0])

# wk = pygame.image.load("assets/wking.png")
# screen.blit(wk, [0,0])

#board matrix
board=Board()
def update_board():
    screen.blit(bg, [0, 0])
    for row in board.array:
        for piece in row:
            if piece: #if piece is not none
                print(piece)
                s=pygame.image.load(piece.sprite)
                pos = (piece.x*60,piece.y*60)
                screen.blit(s,pos)

update_board()

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
        # update_board()
        print(event)

    pygame.display.update()
    clock.tick(60)


# if __name__ == "__main__":
#     b = Board()
