from board import *

def matrix_to_tuple(array, empty_array):
    for i in range(8):
        empty_array[i] = tuple(array[i])
    return tuple(empty_array)

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

def minimax(board, depth, alpha, beta, maximizing, trans_table = None):
    if trans_table == None:
        trans_table = dict()

    tuple_mat = matrix_to_tuple(board.array,board.empty)
    if tuple_mat in trans_table:
        return trans_table[tuple_mat], 0

    if depth == 0: # end of the search is reached
        trans_table[tuple_mat] = board.score
        return board.score, 0

    if maximizing:
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

                v, __ = minimax(board, depth - 1,alpha,beta, False,trans_table)
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

                v, __ = minimax(board, depth - 1,alpha,beta, True, trans_table)
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



"""
diction = dict()
board = Board()
array = matrix_to_tuple(board.array,board.empty)



diction[array] = 0
""
b = board
b.array[0][0] = None

print("")


array1 = matrix_to_tuple(b.array,b.empty)

print(array1 in diction)

"""
b = Board()
b.array[2][1] = Pawn("w",2,0)

b.array[2][6] = Rook("w",2,7)

b.array[6][0] = None
b.array[7][7] = None
value, move = minimax(b,5,float("-inf"),float("inf"),True)
print(" ")
b.print_to_terminal()
print(value)
print(move)
