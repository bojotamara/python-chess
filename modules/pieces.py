import pygame

def capture_check(your_color, y, x, board):
    """
    Checks if a square (y,x) can be captured by the color inputted
    """
    piece = board.array[y][x]
    if piece == None:
        return False
    else:
        if piece.color != your_color:
            return True
        else:
            return False


def move_check(your_color, y, x, board):
    """
    A very basic move check. The only rules that are checked are: (y,x) is
    empty or (y,x) contains an opposing player, move is within bounds of the board
    """
    if x < 0 or x > 7 or y < 0 or y > 7:
        return False
    piece = board.array[y][x]
    if piece == None:
        return True
    else:
        if piece.color != your_color:
            return True
        else:
            return False

class Piece(pygame.sprite.Sprite):
    """
    Piece in the chess game. Stores the color and the position in the board
    Each piece type inherits from this class, which inherits from pygame sprite class.
    """

    def __init__(self, color, y, x):
        super().__init__()
        self.color = color

        # position on board matrix
        self.x = x
        self.y = y

        # allows for transparency
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA, 32)
        self.image.convert_alpha()

        # position on screen surface
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x * 60, y * 60

        self.highlighed = False

    def line_attack_gen(self, board):
        """
        Generates legal moves for a piece that can move in 'lines'
        Args:
            A instance of the board class
        Returns:
            move_set - set containing tuples (y,x) of the legal moves.
        """
        # vertical lines
        move_set = set()
        newX = self.x

        for i in (-1, 1):
            newY = self.y
            while(True):
                newY += i
                if move_check(self.color, newY, newX, board):
                    move_set.add((newY, newX))
                    if capture_check(self.color, newY, newX, board):
                        break
                else:  # there is an obstruction
                    break

        # horizontal lines
        newY = self.y

        for i in (-1, 1):
            newX = self.x
            while(True):
                newX += i
                if move_check(self.color, newY, newX, board):
                    move_set.add((newY, newX))
                    if capture_check(self.color, newY, newX, board):
                        break
                else:  # there is an obstruction
                    break

        return move_set

    def diag_attack_gen(self, board):
        """
        Generates legal moves for a piece that can move in 'diagonals'
        Args:
            A instance of the board class
        Returns:
            move_set - set containing tuples (y,x) of the legal moves.
        """
        move_set = set()

        # loop through all the possible diagonal directions
        increments = [(-1, -1), (1, 1), (1, -1), (-1, 1)]
        for offset in increments:
            newX = self.x  # start search from the piece's location
            newY = self.y
            while (True):
                newX += offset[0]
                newY += offset[1]
                if move_check(self.color, newY, newX, board):
                    move_set.add((newY, newX))
                    # square can be captured, thus later moves are not valid
                    if capture_check(self.color, newY, newX, board):
                        break
                else:  # there is an obstruction, later moves aren't valid
                    break
        return move_set

    def highlight(self):
        '''
        Called when the user clicked on a sprite of their color.
        This draws a purple square around the selected piece
        '''
        pygame.draw.rect(self.image, (138, 43, 226), (0, 0, 60, 60),  5)
        self.highlighed = not self.highlighed

    def unhighlight(self):
        '''
        Redraws entire sprite to get rid of the purple square, since
        blitting a transparent portion over the square of course
        doesn't update that part.
        '''
        self.image = pygame.Surface((60, 60), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.blit(self.sprite, (0, 0))
        self.highlighed = not self.highlighed


class Pawn(Piece):

    def __init__(self, color, y, x):
        super().__init__(color, y, x)
        self.symbol = "P"

        # load the corresponding sprite image and draw on own surface.
        # similar process for the other pieces
        self.sprite = pygame.image.load("assets/{}pawn.png".format(self.color))
        self.image.blit(self.sprite, (0, 0))


    def gen_legal_moves(self, board):
        """
        Generates the pseudo-legal moves for the piece. Check is not taken into
        account, hence 'pseudo-legal'. Returns a set of the coords where the piece
        can move.
        """
        move_set = set()

        incr = {"w": -1, "b": 1}
        offsets = [-1, 1]
        c = self.color

        newY = self.y + incr[c]
        # normal move forward
        if newY >= 0 and newY < 8 and board.array[newY][self.x] == None:
            move_set.add((newY, self.x))

            if (self.y == 1 and c == "b") or (self.y == 6 and c == "w"):
                newY += incr[c]
                if newY >= 0 and newY < 8 and board.array[newY][self.x] == None:
                    move_set.add((newY, self.x))

        for diff in offsets:
            newX = self.x + diff
            newY = self.y + incr[c]

            if not move_check(c, newY, newX, board) or not capture_check(c, newY, newX, board):
                continue

            else:
                move_set.add((newY, newX))

        return move_set


class Rook(Piece):

    def __init__(self, color, y, x):
        super().__init__(color, y, x)
        self.sprite = pygame.image.load("assets/{}rook.png".format(self.color))
        self.symbol = "R"
        self.image.blit(self.sprite, (0, 0))
        self.moved = False

    def gen_legal_moves(self, board):

        return self.line_attack_gen(board)


class Bishop(Piece):

    def __init__(self, color, y, x):
        super().__init__(color, y, x)
        self.sprite = pygame.image.load(
            "assets/{}bishop.png".format(self.color))
        self.symbol = "B"
        self.image.blit(self.sprite, (0, 0))

    def gen_legal_moves(self, board):

        return self.diag_attack_gen(board)


class Knight(Piece):

    def __init__(self, color, y, x):
        super().__init__(color, y, x)
        self.sprite = pygame.image.load(
            "assets/{}knight.png".format(self.color))
        self.symbol = "N"
        self.image.blit(self.sprite, (0, 0))

    def gen_legal_moves(self, board):
        move_set = set()
        offsets = [(-1, -2), (-1, 2), (-2, -1), (-2, 1),
                   (1, -2), (1, 2), (2, -1), (2, 1)]

        for offset in offsets:
            newX = self.x + offset[0]
            newY = self.y + offset[1]

            if move_check(self.color, newY, newX, board):
                move_set.add((newY, newX))

        return move_set


class King(Piece):

    def __init__(self, color, y, x):
        super().__init__(color, y, x)
        self.sprite = pygame.image.load("assets/{}king.png".format(self.color))
        self.symbol = "K"
        self.image.blit(self.sprite, (0, 0))
        self.moved = False

    def gen_legal_moves(self, board):
        move_set = set()
        offsets = [(1, 1), (-1, -1), (1, -1), (-1, 1),
                   (0, 1), (1, 0), (-1, 0), (0, -1)]

        for offset in offsets:
            newX = self.x + offset[0]
            newY = self.y + offset[1]

            if move_check(self.color, newY, newX, board):
                move_set.add((newY, newX))

        return move_set


class Queen(Piece):

    def __init__(self, color, y, x):
        super().__init__(color, y, x)
        self.sprite = pygame.image.load(
            "assets/{}queen.png".format(self.color))
        self.symbol = "Q"
        self.image.blit(self.sprite, (0, 0))

    def gen_legal_moves(self, board):

        move_set1 = self.line_attack_gen(board)
        move_set2 = self.diag_attack_gen(board)

        return move_set1.union(move_set2)
