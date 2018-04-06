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

class Piece:

    def __init__(self, color, y, x):
        self.color = color
        self.x = x
        self.y = y

    def line_attack_gen(self,board):
        #vertical lines
        move_set = set()
        newX = self.x

        for i in (-1,1):
            newY = self.y
            while(True):
                newY += i
                if move_check(self.color,newY,newX,board):
                    move_set.add((newY,newX))
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
                    move_set.add((newY,newX))
                    if eat_check(self.color,newY,newX,board):
                        break
                else: # there is an obstruction
                    break

        return move_set

    def diag_attack_gen(self,board):
        move_set = set()
        increments = [(-1,-1),(1,1),(1,-1),(-1,1)]

        for offset in increments:
            newX = self.x
            newY = self.y

            while (True):
                newX += offset[0]
                newY += offset[1]

                if move_check(self.color,newY,newX,board):
                    move_set.add((newY,newX))
                    if eat_check(self.color,newY,newX,board):
                        break
                else: # there is an obstruction
                    break
        return move_set

class Pawn(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)
        self.symbol = "P"
        self.sprite = "assets/{}pawn.png".format(self.color)

    # returns a list that contains tuples where the piece can move
    def gen_legal_moves(self, board):
        move_set = set()

        incr = {"w": -1, "b":1}
        offsets = [-1, 1]
        c = self.color

        newY = self.y + incr[c]
        # normal move forward
        if newY >=0 and newY <8 and board.array[newY][self.x] == None:
            move_set.add( (newY, self.x) )

            if (self.y == 1 and c == "b") or (self.y == 6 and c == "w"):
                newY += incr[c]
                if newY >=0 and newY <8 and board.array[newY][self.x] == None:
                    move_set.add( (newY, self.x) )


        for diff in offsets:
            newX = self.x + diff
            newY = self.y + incr[c]

            if not move_check(c,newY,newX,board) or not eat_check(c,newY,newX,board):
                continue

            else:
                move_set.add( (newY,newX))


        return move_set

class Rook(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)
        self.sprite = "assets/{}rook.png".format(self.color)
        self.symbol = "R"

    def gen_legal_moves(self, board):

        return self.line_attack_gen(board)

class Bishop(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)
        self.sprite = "assets/{}bishop.png".format(self.color)
        self.symbol = "B"

    def gen_legal_moves(self, board):

        return self.diag_attack_gen(board)

class Knight(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)
        self.sprite = "assets/{}knight.png".format(self.color)
        self.symbol = "N"

    def gen_legal_moves(self, board):
        move_set = set()
        offsets = [(-1,-2),(-1,2),(-2,-1),(-2,1),(1,-2),(1,2),(2,-1),(2,1)]

        for offset in offsets:
            newX = self.x + offset[0]
            newY = self.y + offset[1]

            if move_check(self.color,newY,newX,board):
                move_set.add((newY,newX))

        return move_set

class King(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)
        self.sprite = "assets/{}king.png".format(self.color)
        self.symbol = "K"

    def gen_legal_moves(self, board):
        move_set = set()
        offsets = [(1,1),(-1,-1),(1,-1),(-1,1),(0,1),(1,0),(-1,0),(0,-1)]

        for offset in offsets:
            newX = self.x + offset[0]
            newY = self.y + offset[1]

            if move_check(self.color,newY,newX,board):
                move_set.add((newY,newX))

        return move_set

class Queen(Piece):

    def __init__(self, color, y, x):
        super().__init__(color,y,x)
        self.sprite = "assets/{}queen.png".format(self.color)
        self.symbol = "Q"

    def gen_legal_moves(self, board):


        move_set1 = self.line_attack_gen(board)
        move_set2 = self.diag_attack_gen(board)

        return move_set1.union(move_set2)
