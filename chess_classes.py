
# a basic move check, that only checks if the space is occupied, or if
# its a friendly piece
def move_check(your_color, y, x ,board):

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



class Board:

    #None is empty
    def __init__(self):
        # self.array = [[None for x in range(8)] for y in range(8)]
        self.array =[
        [Rook("b",0,0),Knight("b",0,1),Bishop("b",0,2),Queen("b",0,3),King("b",0,4),Bishop("b",0,5),Knight("b",0,6),Rook("b",0,7)],
        [Pawn("b",1,i) for i in range(8)],
        [None for x in range(8)],
        [None for x in range(8)],
        [None for x in range(8)],
        [None for x in range(8)],
        [Pawn("w",6,i) for i in range(8)],
        [Rook("w",7,0),Knight("w",7,1),Bishop("w",7,2),Queen("w",7,3),King("w",7,4),Bishop("w",7,5),Knight("w",7,6),Rook("w",7,7)]
        ]
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
        self.move_list = []

    def gen_legal_moves():
        # returns a move-list thats a tuple
        pass

class Pawn(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)

    # returns a list that contains tuples where the piece can move
    def gen_legal_moves(self, board):

        offsets = [-1, 1]

        if self.color == "w":
            # normal move forward
            if board.array[self.y - 1][self.x] == None and check_bounds(self.y - 1,self.x):
                self.move_list.append( (self.y - 1, self.x) )

            for diff in offsets:
                newX = self.x + diff
                newY = self.y - 1

                if not move_check(self.color,newY,newX,board):
                    continue

                else:
                    self.move_list.append( (newY,newX))



        elif self.color == "b":
            # normal move forward
            if board.array[self.y + 1][self.x] == None and check_bounds(self.y + 1,self.x):
                self.move_list.append( (self.y + 1, self.x) )

            for diff in offsets:
                newX = self.x + diff
                newY = self.y + 1

                if not move_check(self.color,newY,newX,board):
                    continue

                else:
                    self.move_list.append( (newY,newX))

        return self.move_list

class Rook(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)

class Bishop(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)

class Knight(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)

    def gen_legal_moves(self, board):
        offsets = [(-1,-2),(-1,2),(-2,-1),(-2,1),(1,-2),(1,2),(2,-1),(2,1)]

        for offset in offsets:
            newX = self.x + offset[0]
            newY = self.y + offset[1]

            if move_check(self.color,newY,newX,board):
                self.move_list.append((newY,newX))

        return self.move_list


class King(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)

    def gen_legal_moves(self, board):
        offsets = [(1,1),(-1,-1),(1,-1),(-1,1),(0,1),(1,0),(-1,0),(0,-1)]

        for offset in offsets:
            newX = self.x + offset[0]
            newY = self.y + offset[1]

            if move_check(self.color,newY,newX,board):
                self.move_list.append((newY,newX))

        return self.move_list


class Queen(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)


board = Board()


#board.array[7][7] = King("w",7,7)
#board.array[4][4] = King("w",4,4)

piece = board.array[7][4]
board.array[6][4] = None
list1 = piece.gen_legal_moves(board)
print(list1)
