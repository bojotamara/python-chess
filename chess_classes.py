def check_bounds(x,y):
    if x >= 0 and x < 8 and y >= 0 and y < 8:
        return True
    else:
        return False



class Board:

    #None is empty
    def __init__(self):
        self.array = [[None for x in range(8)] for y in range(8)]

    def move_piece(self, piece, y, x):
        oldx = piece.x
        oldy = piece.y
        self.array[oldy][oldx] = None
        self.array[y][x] = piece


class Piece:

    def __init__(self, color, y, x):
        self.color = color
        self.x = x
        self.y = y

    def gen_legal_moves():
        # returns a move-list thats a tuple
        pass

class Pawn(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)

    def gen_legal_moves(board):
        move_list = []
        offsets = [-1, 1]

        if self.color == "white":
            # normal move forward
            if board.array[self.y - 1][self.x] == None and check_bounds(self.y - 1,self.x):
                move_list.append( (self.x, self.y - 1) )

            for diff in offsets:
                newX = self.x + diff
                newY = self.y + 1
                space = board.array[newY][newX]

                if space.color == "black" and check_bounds(newX,newY):
                    move.list.append( (newX,newY))



        elif self.color == "black":
            # normal move forward
            if board.array[self.y + 1][self.x] == None and check_bounds(self.y + 1,self.x):
                move_list.append( (self.x, self.y + 1) )

            for diff in offsets:
                newX = self.x + diff
                newY = self.y + 1
                space = board.array[newY][newX]

                if space.color == "white" and check_bounds(newX,newY):
                    move.list.append( (newX,newY))


class Rook(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)

class Bishop(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)

class Knight(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)

class King(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)

class Queen(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)


board = Board()

board.array[6][7] = Pawn("white",6,7)
piece = board.array[6][7]
board.move_piece(piece,1,1)
print(board.array[1][1])
print(board.array[6][7])
