from board import *

def minimax(board, depth, maximizingPlayer):


    board.evaluate()

    if depth == 0: #or node is a terminal node

        return board.score, 0

    if maximizingPlayer:
        bestValue = float("-inf")
        board.move_gen("b")
        for start, move_set in board.blackmoves.items():
            for end in move_set:

                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]
                board.move_piece(piece,end[0],end[1])

                v, __ = minimax(board, depth - 1, False)
                piece = board.array[end[0]][end[1]]
                board.move_piece(piece,start[0],start[1])
                board.array[end[0]][end[1]] = dest

                board.evaluate()
                if v > bestValue:
                    bestValue = v
                    move = (start, (end[0],end[1]))
                bestValue = max(bestValue, v)
        return bestValue, move

    else:    #(* minimizing player *)
        bestValue = float("inf")
        board.move_gen("w")
        for start, move_set in board.whitemoves.items():

            for end in move_set:
                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]
                board.move_piece(piece,end[0],end[1])

                v, __ = minimax(board, depth - 1, True)
                piece = board.array[end[0]][end[1]]
                board.move_piece(piece,start[0],start[1])
                board.array[end[0]][end[1]] = dest
                board.evaluate()
                if v < bestValue:
                    bestValue = v
                    move = (start, (end[0],end[1]))
                bestValue = min(bestValue, v)
        return bestValue, move

b = Board()
b.array[2][1] = Pawn("w",2,0)

b.array[2][6] = Rook("w",2,7)

b.array[6][0] = None
b.array[7][7] = None


value, move = minimax(b,1,True)
print(value)
print(move)
