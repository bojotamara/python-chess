#!/usr/bin/python3
import pygame

# from assets import *
from modules.board import *
from modules.computer import *

# pygame.init()

screen = pygame.display.set_mode((800, 60 * 8))
pygame.display.set_caption('Boss Ass Chess Game')

# load background image
bg = pygame.image.load("assets/chessboard.png")
# blit like puts the image on there
screen.blit(bg, (0, 0))

# wk = pygame.image.load("assets/wking.png")
# screen.blit(wk, [0,0])

# board matrix
b = Board()

# updates the pieces displayed based on the board matrix


# def update_board():
#     global b
#     screen.blit(bg, [0, 0])
#     for row in b.array:
#         for piece in row:
#             if piece:  # if piece is not none
#                 # print(piece)
#                 s = pygame.image.load(piece.sprite)
#                 pos = (piece.x * 60, piece.y * 60)
#                 screen.blit(s, pos)


# update_board()
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(
    (piece for row in b.array for piece in row if piece))

b.array = [[None for x in range(8)] for y in range(8)]

b.black_king = King("b",0,1)
b.white_king = King("w",5,5)
b.array[0][1] = b.black_king
b.array[1][1] = Bishop("b",1,1)
b.array[6][1] = Rook("w",6,1)
b.array[5][5] = b.white_king

b.print_to_terminal()
print("")

trans_table = dict()
value, move = minimax(b,5,float("-inf"),float("inf"), True, trans_table)
print(len(trans_table))
b.print_to_terminal()
print(value)
print(move)


"""
# all_sprites_list.draw(screen)
clock = pygame.time.Clock()
crashed = False

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        # update_board()
        print(event)

    screen.blit(bg, (0, 0))
    all_sprites_list.draw(screen)
    pygame.display.update()
    clock.tick(60)

#
# if __name__ == "__main__":
#     b = Board()
"""
