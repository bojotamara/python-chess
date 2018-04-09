# ------------- INITIALIZATIONS-------------------
import pygame
import copy
# import textwrap

# from assets import **

pygame.init()
pygame.font.init()  # for text

screen = pygame.display.set_mode((800, 60 * 8))
pygame.display.set_caption('Boss Ass Chess Game')

from modules.board import *
from modules.computer import *


# blit like puts the image on there

bg = pygame.image.load("assets/chessboard.png").convert()
sidebg = pygame.image.load("assets/woodsidemenu.jpg").convert()
player = 1  # 'AI' otherwise
myfont = pygame.font.Font("assets/Roboto-Black.ttf", 30)
clippy = pygame.image.load("assets/Clippy.png").convert_alpha()
clippy = pygame.transform.scale(clippy, (320, 240))
playeravatar = None


# board matrix
board = Board()

all_sprites_list = pygame.sprite.Group()
sprites = [piece for row in board.array for piece in row if piece]
all_sprites_list.add(sprites)

all_sprites_list.draw(screen)
# all_sprites_list = pygame.sprite.LayeredDirty(
#     piece for row in b.array for piece in row if piece)

clock = pygame.time.Clock()

# ----------- FUNCTIONS---------------------------------


def select_piece(color):
    pos = pygame.mouse.get_pos()
    # get a list of all sprites that are under the mouse cursor
    clicked_sprites = [
        s for s in sprites if s.rect.collidepoint(pos)]

    # only highlight, and return if its the player's piece
    if len(clicked_sprites) == 1 and clicked_sprites[0].color == color:
        # clicked_sprites[0].highlight(screen)
        # print(clicked_sprites[0])
        clicked_sprites[0].highlight()
        return clicked_sprites[0]


def select_square():
    x, y = pygame.mouse.get_pos()
    x = x // 60
    y = y // 60
    return (y, x)


def run_game():
    # clippy avatar for computer player
    global player, playeravatar, clippy
    playeravatar = pygame.image.load("assets/avatar.png").convert_alpha()
    playeravatar = pygame.transform.scale(playeravatar, (320, 240))
    update_sidemenu('Your Turn!', (255, 255, 255))

    # screen.blit(playeravatar, (550, 20))

    gameover = False

    selected = False  # indicates whether a piece is selected yet
    trans_table = dict()

    while not gameover:

        # Human player's turn
        if player == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True

                # select a piece to move
                elif event.type == pygame.MOUSEBUTTONDOWN and not selected:
                    piece = select_piece("w")
                    # print(piece)
                    # a white piece was selected
                    if piece != None:
                        player_moves = piece.gen_legal_moves(board)
                        selected = True

                # piece is selected, now move it somewhere
                elif event.type == pygame.MOUSEBUTTONDOWN and selected:
                    square = select_square()
                    if square in player_moves:
                        oldx = piece.x  # preserve, in case we have to reverse the move
                        oldy = piece.y
                        dest = board.array[square[0]][square[1]]
                        board.move_piece(piece, square[0], square[1])
                        if dest:
                            all_sprites_list.remove(dest)
                            sprites.remove(dest)
                        # see if move puts you in check
                        attacked = move_gen(board, "b", sprites, True)
                        if (board.white_king.y, board.white_king.x) not in attacked:
                            # MOVE NOT IN CHECK WE GOOD
                            selected = False
                            player = "AI"
                            # update avatar
                            update_sidemenu('CPU Thinking...', (255, 255, 255))

                            # delete sprite
                            if dest:
                                board.score -= board.pvalue_dict[type(dest)]
                        else:  # THIS MOVE IS IN CHECK
                            board.move_piece(piece, oldy, oldx)
                            board.array[square[0]][square[1]] = dest
                            if dest:
                                all_sprites_list.add(dest)
                                sprites.append(dest)
                            piece.highlight()
                            # TODO: print a message player is in check
                            if checkWhite:
                                update_sidemenu(
                                    'You have to get out\nof check!', (255, 0, 0))
                                pygame.display.update()
                                pygame.time.wait(1000)
                                update_sidemenu(
                                    'Your Turn: Check!', (255, 0, 0))
                            else:
                                update_sidemenu(
                                    'This move would put\nyou in check!', (255, 0, 0))
                                pygame.display.update()
                                pygame.time.wait(1000)
                                update_sidemenu('Your turn!', (255, 255, 255))

                    elif (piece.y, piece.x) == square:  # CANCEL MOVE
                        piece.unhighlight()
                        selected = False

                    else:  # INVALID MOVE

                        # TODO: print a message
                        update_sidemenu('Invalid move!', (255, 0, 0))
                        pygame.display.update()
                        pygame.time.wait(1000)
                        if checkWhite:
                            update_sidemenu('Your Turn: Check!', (255, 0, 0))
                        else:
                            update_sidemenu('Your turn!', (255, 255, 255))

        # AI's turn
        else:
            value, move = minimax(board, 3, float(
                "-inf"), float("inf"), True, trans_table, sprites, screen)

            if value == float("-inf"):
                print(value)
                print(move)
                # AI IS IN CHECKMATE
                gameover = True
            else:
                start = move[0]
                end = move[1]
                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]
                board.move_piece(piece, end[0], end[1])
                if dest:
                    all_sprites_list.remove(dest)
                    sprites.remove(dest)
                    board.score += board.pvalue_dict[type(dest)]
                player = 1
                attacked = move_gen(board, "b", sprites, True)
                if (board.white_king.y, board.white_king.x) in attacked:
                    update_sidemenu('Your Turn: Check!', (255, 0, 0))
                    checkWhite = True
                else:
                    update_sidemenu('Your Turn!', (255, 255, 255))
                    checkWhite = False
                print(board.score)
                # print('SIDE MENU UPDATE')
            if value == float("inf"):
                print("Player checkmate")
                gameover = True
                # update_sidemenu('Your Turn!', (255, 255, 255))

        screen.blit(bg, (0, 0))
        all_sprites_list.draw(screen)
        pygame.display.update()
        clock.tick(60)


def game_over():
    board.print_to_terminal()


def update_sidemenu(message, colour):

    screen.blit(sidebg, (480, 0))
    global playeravatar, clippy
    if player == 1:
        screen.blit(playeravatar, (480, 0))

    elif player == 'AI':
        screen.blit(clippy, (480, 0))

    # textsurface = myfont.render(textwrap.fill(message, 19), False, colour)
    # screen.blit(textsurface, (500, 250))
    message = message.splitlines()
    c = 0
    for m in message:
        textsurface = myfont.render(m, False, colour)
        screen.blit(textsurface, (500, 250 + c))
        c += 40


def camstream():
    # bulk of the camera code was no written by us, since it's just here for fun
    # and does not contribute to the actual game in any meaningful way
    # modified from https://gist.github.com/snim2/255151
    DEVICE = '/dev/video0'
    SIZE = (640, 480)
    FILENAME = 'assets/avatar.png'
    import pygame.camera
    pygame.camera.init()
    display = pygame.display.set_mode((800, 60 * 8), 0)
    camera = pygame.camera.Camera(DEVICE, SIZE)
    camera.start()
    screen = pygame.surface.Surface(SIZE, 0, display)
    screen = camera.get_image(screen)
    # display.blit(screen, (0, 0))
    # pygame.display.flip()
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         capture = False
    #     elif event.type == pygame.KEYDOWN and event.key == K_s:
    pygame.image.save(screen, FILENAME)
    camera.stop()
    return


def welcome():
    menubg = pygame.image.load("assets/menubg.jpg").convert()
    screen.blit(menubg, (0, 0))
    bigfont = pygame.font.Font("assets/Roboto-Black.ttf", 80)
    textsurface = bigfont.render('Python Chess Game', False, (255, 255, 255))
    screen.blit(textsurface, (30, 10))

    medfont = pygame.font.Font("assets/Roboto-Black.ttf", 50)
    textsurface = medfont.render(
        'CMPUT 275 Final Project', False, (255, 255, 255))
    screen.blit(textsurface, (100, 100))
    textsurface = myfont.render(
        'Press any key to begin!', False, (255, 255, 255))
    screen.blit(textsurface, (250, 170))

    arun = pygame.image.load("assets/arun.jpg").convert()
    tamara = pygame.image.load("assets/tamara.jpg").convert()
    arun = pygame.transform.scale(arun, (200, 200))
    tamara = pygame.transform.scale(tamara, (200, 200))
    screen.blit(arun, (100, 230))
    screen.blit(tamara, (500, 230))

    textsurface = myfont.render(
        'Arun Woosaree', False, (255, 255, 255))
    screen.blit(textsurface, (100, 440))

    textsurface = myfont.render(
        'Tamara Bojovic', False, (255, 255, 255))
    screen.blit(textsurface, (500, 440))
    while True:
        for event in pygame.event.get():
            # print(event.type)
            # print(event)
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                return
            elif event.type == pygame.QUIT:
                import sys
                sys.exit()
        pygame.display.update()


if __name__ == "__main__":
    welcome()
    try:
        camstream()
    except:
        pass
    run_game()
    game_over()
