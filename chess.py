# ------------- INITIALIZATIONS-------------------
import pygame

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
myfont = pygame.font.SysFont(None, 30)
clippy = pygame.image.load("assets/cpu.jpg").convert()
clippy = pygame.transform.scale(clippy, (160, 120))
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
    playeravatar = pygame.image.load("assets/avatar.jpg").convert()
    playeravatar = pygame.transform.scale(playeravatar, (160, 120))
    update_sidemenu()

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
                    print(piece)
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
                        # see if move puts you in check
                        attacked = move_gen(board, "b", True)
                        if (board.white_king.y, board.white_king.x) not in attacked:
                            # MOVE NOT IN CHECK WE GOOD
                            selected = False
                            player = "AI"
                            # update avatar
                            update_sidemenu()
                            # delete sprite
                            if dest:
                                all_sprites_list.remove(dest)
                                sprites.remove(dest)
                        else:  # THIS MOVE IS IN CHECK
                            board.move_piece(piece, oldy, oldx)
                            board.array[square[0]][square[1]] = dest
                            # TODO: print a message

                    elif (piece.y, piece.x) == square:  # CANCEL MOVE
                        piece.unhighlight()
                        selected = False

                    else:  # INVALID MOVE
                        pass
                        # TODO: print a message

        # AI's turn
        else:
            """
            value, move = minimax(board,5,float("-inf"),float("inf"), True, trans_table)
            if value == float("-inf"):
                #AI IS IN CHECKMATE
                gameover = True
            """
            # just go back to player one for now lol
            player = 1
            pygame.time.wait(1000)
            # switch to player player avatar
            # screen.blit(playeravatar, (550, 20))
            update_sidemenu()
        screen.blit(bg, (0, 0))
        all_sprites_list.draw(screen)
        pygame.display.update()
        clock.tick(60)


def update_sidemenu():
    screen.blit(sidebg, (480, 0))
    global playeravatar, clippy
    if player == 1:
        screen.blit(playeravatar, (550, 20))
        textsurface = myfont.render('Your Turn!', False, (255, 255, 255))
    elif player == 'AI':
        screen.blit(clippy, (550, 20))
        textsurface = myfont.render('CPU Thinking...', False, (255, 255, 255))
    screen.blit(textsurface, (550, 150))


def camstream():
    # bulk of the camera code was no written by us, since it's just here for fun
    # and does not contribute to the actual game in any meaningful way
    # modified from https://gist.github.com/snim2/255151
    DEVICE = '/dev/video0'
    SIZE = (640, 480)
    FILENAME = 'assets/avatar.jpg'
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


if __name__ == "__main__":
    camstream()
    run_game()

    # delete picture taken
    # from os import remove
    # remove('assets/avatar.jpg')
