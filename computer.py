from board import *

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

def minimax(board, depth, alpha, beta, maximizingPlayer):

    if depth == 0: # end of the search is reached

        return board.score, 0

    if maximizingPlayer:
        bestValue = float("-inf")
        black_moves = move_gen(board,"b")
        for start, move_set in black_moves.items():
            for end in move_set:

                #develop the 'child'
                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]
                board.move_piece(piece,end[0],end[1])
                #change the board score
                if dest != None:
                    board.score += board.pvalue_dict[type(dest)]

                v, __ = minimax(board, depth - 1,alpha,beta, False)
                bestValue = max(bestValue, v)
                alpha = max(alpha, bestValue)

                # revert the board
                piece = board.array[end[0]][end[1]]
                board.move_piece(piece,start[0],start[1])
                board.array[end[0]][end[1]] = dest
                move = (start, (end[0],end[1])) # preserve the move

                #revert the score
                if dest != None:
                    board.score -= board.pvalue_dict[type(dest)]

                if beta <= alpha:
                    return bestValue, move

        return bestValue, move

    else:    #(* minimizing player *)
        bestValue = float("inf")
        white_moves = move_gen(board,"w")
        for start, move_set in white_moves.items():
            for end in move_set:

                #DEVELOP the child
                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]
                board.move_piece(piece,end[0],end[1])

                #update the score
                if dest != None:
                    board.score -= board.pvalue_dict[type(dest)]

                v, __ = minimax(board, depth - 1,alpha,beta, True)
                bestValue = min(v, bestValue)
                beta = min(beta,bestValue)

                #preserve shit
                piece = board.array[end[0]][end[1]]
                board.move_piece(piece,start[0],start[1])
                board.array[end[0]][end[1]] = dest

                # revert the score
                if dest != None:
                    board.score += board.pvalue_dict[type(dest)]

                if beta <= alpha:
                    return bestValue, 0

        return bestValue, 0


b = Board()
""
b.array[2][1] = Pawn("w",2,0)

b.array[2][6] = Rook("w",2,7)

b.array[6][0] = None
b.array[7][7] = None


value, move = minimax(b,5,float("-inf"),float("inf"),True)
print(" ")
b.print_to_terminal()
print(value)
print(move)
