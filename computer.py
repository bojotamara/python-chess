from board import *

def minimax(board, depth, maximizingPlayer):
    board.evaluate()

    if depth == 0: #or node is a terminal node
        return board.score

    if maximizingPlayer:
        bestValue = float("-inf")
        board.move_gen("b")
        for start, move_set in board.blackmoves.items():
            for end in move_set:
                piece = board.array[start[0]][start[1]]
                board.move_piece(piece,end[0],end[1])
                v = minimax(board, depth - 1, False)
                piece = board.array[end[0]][end[1]]
                board.move_piece(piece,start[0],start[1])
                bestValue = max(bestValue, v)
        return bestValue

    else:    #(* minimizing player *)
        bestValue = float("inf")
        board.move_gen("w")
        for start, move_set in board.whitemoves.items():

            for end in move_set:
                piece = board.array[start[0]][start[1]]
                board.move_piece(piece,end[0],end[1])
                v = minimax(child, depth - 1, True)
                piece = board.array[end[0]][end[1]]
                board.move_piece(piece,start[0],start[1])
                bestValue = max(bestValue, v)
        return bestValue

b = Board()


print(minimax(b,1,True))
