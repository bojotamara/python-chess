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

global all_sprites_list, sprites
all_sprites_list = pygame.sprite.Group()
sprites = [piece for row in board.array for piece in row if piece]

all_sprites_list.add(sprites)

all_sprites_list.draw(screen)
# all_sprites_list = pygame.sprite.LayeredDirty(
#     piece for row in b.array for piece in row if piece)

clock = pygame.time.Clock()

# ----------- FUNCTIONS---------------------------------


def select_piece(color):
    '''
    Select a piece on the chessboard
    '''
    pos = pygame.mouse.get_pos()
    # get a list of all sprites that are under the mouse cursor
    clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]

    # only highlight, and return if its the player's piece
    if len(clicked_sprites) == 1 and clicked_sprites[0].color == color:
        clicked_sprites[0].highlight()
        return clicked_sprites[0]


def select_square():
    '''
    Returns the chess board coordinates of where the mouse selected
    '''
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
    trans_table = dict() # holds previously computed minimax values

    while not gameover:

        # Human player's turn
        if player == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # select a piece to move
                elif event.type == pygame.MOUSEBUTTONDOWN and not selected:
                    piece = select_piece("w")

                    # a white piece was selected, generate pseudo-legal moves
                    if piece != None:
                        player_moves = piece.gen_legal_moves(board)
                        selected = True

                # piece is selected, now move it somewhere
                elif event.type == pygame.MOUSEBUTTONDOWN and selected:
                    square = select_square()
                    special_moves = special_move_gen(board, "w")

                    # square selected is a pseudo-legal move
                    if square in player_moves:
                        oldx = piece.x  # preserve, in case we have to reverse the move
                        oldy = piece.y
                        # preserve the piece we're potentially eating
                        dest = board.array[square[0]][square[1]]

                        # attempt to move the piece
                        # if a pawn promotion occurs, return the sprites that
                        # we need to update
                        pawn_promotion = board.move_piece(piece, square[0], square[1])

                        if pawn_promotion: # remove the pawn sprite, add the queen sprite
                            all_sprites_list.add(pawn_promotion[0])
                            sprites.append(pawn_promotion[0])
                            all_sprites_list.remove(pawn_promotion[1])
                            sprites.remove(pawn_promotion[1])
                        if type(piece) == King or type(piece) == Rook: # this is needed for proper castling
                            piece.moved = True
                        if dest: # remove the sprite of the piece that was eaten
                            all_sprites_list.remove(dest)
                            sprites.remove(dest)

                        # Now we have to see if move puts you in check
                        # generate a set of the attacked squared
                        attacked = move_gen(board, "b", True)
                        if (board.white_king.y, board.white_king.x) not in attacked:
                            # move not in check, we're good
                            selected = False
                            player = "AI"
                            update_sidemenu('CPU Thinking...', (255, 255, 255))

                            # update the 'score' of the board
                            if dest:
                                board.score -= board.pvalue_dict[type(dest)]
                        else:  # THIS MOVE IS IN CHECK, we have to reverse it
                            board.move_piece(piece, oldy, oldx)
                            if type(piece) == King or type(piece) == Rook:
                                piece.moved = False
                            board.array[square[0]][square[1]] = dest
                            if dest:
                                all_sprites_list.add(dest)
                                sprites.append(dest)
                            if pawn_promotion:
                                all_sprites_list.add(pawn_promotion[1])
                                sprites.append(pawn_promotion[1])
                            piece.highlight()

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

                    # cancel the move
                    elif (piece.y, piece.x) == square:
                        piece.unhighlight()
                        selected = False

                    # square selected is a potential special move
                    elif special_moves and square in special_moves:
                        special = special_moves[square]
                        if (special == "CR" or special == "CL") and type(piece) == King:
                            board.move_piece(
                                piece, square[0], square[1], special)
                            selected = False
                            player = "AI"

                        else:
                            update_sidemenu('Invalid move!', (255, 0, 0))
                            pygame.display.update()
                            pygame.time.wait(1000)
                            if checkWhite:
                                update_sidemenu(
                                    'Your Turn: Check!', (255, 0, 0))
                            else:
                                update_sidemenu('Your turn!', (255, 255, 255))

                    # move is invalid
                    else:

                        update_sidemenu('Invalid move!', (255, 0, 0))
                        pygame.display.update()
                        pygame.time.wait(1000)
                        if checkWhite:
                            update_sidemenu('Your Turn: Check!', (255, 0, 0))
                        else:
                            update_sidemenu('Your turn!', (255, 255, 255))

        # AI's turn
        elif player == "AI":
            value, move = minimax(board, 3, float(
                "-inf"), float("inf"), True, trans_table)

            if value == float("-inf") and move == 0:
                print(value)
                print(move)
                # AI IS IN CHECKMATE
                gameover = True
                player = 1
                update_sidemenu(
                    'Checkmate!\nYou Win!\nPress any key to quit.', (255, 255, 0))

            else:
                start = move[0]
                end = move[1]
                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]
                pawn_promotion = board.move_piece(piece, end[0], end[1])
                if pawn_promotion:
                    all_sprites_list.add(pawn_promotion[0])
                    sprites.append(pawn_promotion[0])
                    all_sprites_list.remove(pawn_promotion[1])
                    sprites.remove(pawn_promotion[1])

                if dest:
                    all_sprites_list.remove(dest)
                    sprites.remove(dest)
                    board.score += board.pvalue_dict[type(dest)]
                player = 1
                attacked = move_gen(board, "b", True)
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
                update_sidemenu(
                    'Checkmate!\nCPU Wins!\nPress any key to quit.', (255, 255, 0))

        screen.blit(bg, (0, 0))
        all_sprites_list.draw(screen)
        pygame.display.update()
        clock.tick(60)


def game_over():
    board.print_to_terminal()
    crown = pygame.image.load("assets/crown.png").convert_alpha()
    crown = pygame.transform.scale(crown, (80, 60))
    screen.blit(crown, (520, 20))
    pygame.event.clear()
    pygame.time.wait(1000)
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

    menuking = pygame.image.load("assets/menuking.png").convert_alpha()
    menuqueen = pygame.image.load("assets/menuqueen.png").convert_alpha()
    menuking = pygame.transform.scale(menuking, (200, 200))
    menuqueen = pygame.transform.scale(menuqueen, (200, 200))
    screen.blit(menuking, (100, 230))
    screen.blit(menuqueen, (500, 230))

    textsurface = myfont.render(
        'Arun Woosaree', False, (255, 255, 255))
    screen.blit(textsurface, (100, 420))

    textsurface = myfont.render(
        'Tamara Bojovic', False, (255, 255, 255))
    screen.blit(textsurface, (500, 420))
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
