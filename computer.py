from board import *
from copy import *

def move_gen(board, color):
    moves = dict()
    # Generates all the legal moves and stores them in whitemoves, blackmoves
    for j in range(8):
        for i in range(8):
            piece = board.array[i][j]
            if piece != None and piece.color == color:
                legal_moves = piece.gen_legal_moves(board)
                if legal_moves:
                    moves[(i,j)] = legal_moves

    return moves

def minimax(board, depth, maximizingPlayer):

    board.evaluate()

    if depth == 0: #or node is a terminal node

        return board.score, 0

    if maximizingPlayer:
        bestValue = float("-inf")
        black_moves = move_gen(board,"b")
        for start, move_set in black_moves.items():
            for end in move_set:

                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]
                board.move_piece(piece,end[0],end[1])

                v, __ = minimax(board, depth - 1, False)
                piece = board.array[end[0]][end[1]]
                board.move_piece(piece,start[0],start[1])
                board.array[end[0]][end[1]] = dest

                if v > bestValue:
                    bestValue = v
                    move = (start, (end[0],end[1]))
                bestValue = max(bestValue, v)
        return bestValue, move

    else:    #(* minimizing player *)
        bestValue = float("inf")
        white_moves = move_gen(board,"w")
        for start, move_set in white_moves.items():
            for end in move_set:
                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]
                board.move_piece(piece,end[0],end[1])

                v, __ = minimax(board, depth - 1, True)
                piece = board.array[end[0]][end[1]]
                board.move_piece(piece,start[0],start[1])
                board.array[end[0]][end[1]] = dest

                bestValue = min(bestValue, v)
        return bestValue, 0


b = Board()
""
b.array[2][1] = Pawn("w",2,0)

b.array[2][6] = Rook("w",2,7)

b.array[6][0] = None
b.array[7][7] = None
"""
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


b.print_to_terminal()
"""

value, move = minimax(b,3,True)
print(" ")
b.print_to_terminal()
print(value)
print(move)
