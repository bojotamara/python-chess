from pieces import *

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
        # Maps (y,x) of a piece to a set containing all the legal moves
        self.whitemoves = dict()
        self.blackmoves = dict()

    def move_piece(self, piece, y, x):
        oldx = piece.x
        oldy = piece.y
        piece.x = x
        piece.y = y
        self.array[oldy][oldx] = None
        self.array[y][x] = piece

    def move_gen(self):
        # Generates all the legal moves and stores them in whitemoves, blackmoves

        for j in range(8):
            for i in range(8):
                piece = self.array[i][j]
                if piece != None and piece.color == "w":
                    self.whitemoves[(i,j)] = piece.gen_legal_moves(board)
                elif piece != None and piece.color == "b":
                    self.blackmoves[(i,j)] = piece.gen_legal_moves(board)
    def test_speed(self):
    # literally ignore this

        for start, move_set in self.whitemoves.items():
            for end in move_set:
                piece = self.array[start[0]][start[1]]
                self.move_piece(piece,end[0],end[1]) # move piece
                #self.evaluate_board()
                piece = self.array[end[0]][end[1]]
                self.move_piece(piece,start[0],start[1]) # move it back

    # this is not a good place for this function, testing stuff out
    def check4checkOnW(self,kingy,kingx):
        flag = False
        for __, attacked in self.blackmoves.items():
            if (kingy,kingx) in attacked:
                flag = True
        return flag
