
# a basic move check, that only checks if the space is occupied, or if
# its a friendly piece
def eat_check(your_color, y, x ,board):
    piece = board.array[y][x]

    if piece == None:
        return False
    else:

        if piece.color != your_color:
            return True
        else:
            return False


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

    def line_attack_gen(self,board):
        #vertical lines
        newX = self.x

        for i in (-1,1):
            newY = self.y
            while(True):
                newY += i
                if move_check(self.color,newY,newX,board):
                    self.move_list.append((newY,newX))
                    if eat_check(self.color,newY,newX,board):
                        break
                else: # there is an obstruction
                    break

        #horizontal lines
        newY = self.y

        for i in (-1,1):
            newX = self.x
            while(True):
                newX += i
                if move_check(self.color,newY,newX,board):
                    self.move_list.append((newY,newX))
                    if eat_check(self.color,newY,newX,board):
                        break
                else: # there is an obstruction
                    break

    def diag_attack_gen(self,board):
        increments = [(-1,-1),(1,1),(1,-1),(-1,1)]

        for offset in increments:
            newX = self.x
            newY = self.y

            while (True):
                newX += offset[0]
                newY += offset[1]

                if move_check(self.color,newY,newX,board):
                    self.move_list.append((newY,newX))
                    if eat_check(self.color,newY,newX,board):
                        break
                else: # there is an obstruction
                    break


class Pawn(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)
        self.sprite = "assets/{}pawn.png".format(self.color)

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
        self.sprite = "assets/{}rook.png".format(self.color)

    def gen_legal_moves(self, board):

        self.line_attack_gen(board)

        return self.move_list


class Bishop(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)
        self.sprite = "assets/{}bishop.png".format(self.color)

    def gen_legal_moves(self, board):

        self.diag_attack_gen(board)

        return self.move_list


class Knight(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)
        self.sprite = "assets/{}knight.png".format(self.color)

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
        self.sprite = "assets/{}king.png".format(self.color)

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
        self.sprite = "assets/{}queen.png".format(self.color)

    def gen_legal_moves(self, board):

        self.line_attack_gen(board)
        self.diag_attack_gen(board)

        return self.move_list


board = Board()


#board.array[7][7] = King("w",7,7)
board.array[3][3] = Queen("w",3,3)

piece = board.array[3][3]
#board.array[6][4] = None
list1 = piece.gen_legal_moves(board)
print(list1)
