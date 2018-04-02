class Board:

    #None is empty
    #X is invalid

    def __init__(self):
        self.array = [[None for x in range(8)] for y in range(8)]


class Piece:

    def __init__(self, color, x, y):
        self.color = color
        self.coords = (x,y)

    def gen_legal_moves():
        # returns a move-list thats a tuple
        pass

    def check_bounds(x,y):
        if x >= 0 and x < 8 and y >= 0 and y < 0:
            return True
        else:
            return False

class Pawn(Piece):

    def __init__(self, color, x, y):
        super().__init__(color,x,y)

    def gen_legal_moves(board):
        move_list = []
        offsets = [-1, 1]

        if self.color == "white":
            # normal move forward
            if board.array[self.y - 1][self.x] == None:
                move_list.append( (self.x, self.y - 1) )

            #if board.array[self.y -1][]

        elif self.color == "black":
            # normal move forward
            if board.array[self.y + 1][self.x] == None:
                move_list.append( (self.x, self.y + 1) )



class Rook(Piece):

    def __init__(self, color, x, y):
        super().__init__(color,x,y)

class Bishop(Piece):

    def __init__(self, color, x, y):
        super().__init__(color,x,y)

class Knight(Piece):

    def __init__(self, color, x, y):
        super().__init__(color,x,y)

class King(Piece):

    def __init__(self, color, x, y):
        super().__init__(color,x,y)

class Queen(Piece):

    def __init__(self, color, x, y):
        super().__init__(color,x,y)


board = Board()
print(board.array[7][8])
board.array[0][0] = Pawn("white",0,0)
piece = board.array[0][0]
print(piece.coords)
