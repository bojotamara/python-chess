from modules.board import *

def matrix_to_tuple(array, empty_array):
    """
    Given a 2D list, converts it to 2D tuple. This is useful for using a
    matrix as a key in a dictionary
    (an empty 8x8 should be given, just for efficiency)
    """
    for i in range(8):
        empty_array[i] = tuple(array[i])
    return tuple(empty_array)

# possible improvement: Make a list of all the pieces, so you don't have
# to iterate through the whole board for move gen

def check_castling(board,c,side):

    castleLeft = False
    castleRight = False

    if c == "w":
        king = board.white_king
        leftRook = board.white_rook_left
        rightRook =  board.white_rook_right
        attacked = move_gen(board, "b", True)
        i = 7
    elif c == "b":
        king = board.black_king
        leftRook = board.black_rook_left
        rightRook =  board.black_rook_right
        attacked = move_gen(board, "w", True)
        i = 0

    squares = set()

    if king.moved == False:
    # left castle, check the rook
        if board.array[i][0] == leftRook and leftRook.moved == False:
            squares = {(i,1),(i,2),(i,3),(i,1),(i,2),(i,3)}
            if not board.array[i][1] and not board.array[i][2] and not board.array[i][3]:
                if not attacked.intersection(squares):
                    castleLeft = True
    #right castle
        if board.array[i][7] == rightRook and rightRook.moved == False:
            squares = {(i,6),(i,5)}
            if not board.array[i][6] and not board.array[i][5]:
                if not attacked.intersection(squares):
                    castleRight = True

    if side == "r":
        return castleRight
    elif side == "l":
        return castleLeft

def special_move_gen(board,color,moves = None):
    if moves == None:
        moves = dict()
    if color == "w":
        x = 7
    elif color == "b":
        x = 0
    rightCastle = check_castling(board,color,"r")
    leftCastle = check_castling(board,color,"l")

    if rightCastle:
        moves[(x,6)] = "CR"
    if leftCastle:
        moves[(x,2)] = "CL"

    return moves


def move_gen(board, color, attc = False):
    """
    Generates the legal moves from a board state, for a specific color.
    Return:
    attc = False: moves (dict) - maps coord (y,x) to a set containing the coords of
                                where is can legally move
    attc = True: moves (set) - the set of attacked squares for that color.
    """
    if attc:
        moves = set()
    else:
        moves = dict()
        #moves = special_move_gen(board,color,moves)
    # Generates all the legal moves and stores them in whitemoves, blackmoves

    for j in range(8):
        for i in range(8):
            piece = board.array[i][j]
            if piece != None and piece.color == color:
                legal_moves = piece.gen_legal_moves(board)
                if legal_moves and not attc:
                    moves[(i,j)] = legal_moves
                elif legal_moves and attc:
                    #print('hey')
                    #print(legal_moves)
                    moves = moves.union(legal_moves)

    '''
    for piece in sprites:
            if piece.color == color:
                legal_moves = piece.gen_legal_moves(board)
                if legal_moves and not attc:
                    moves[(piece.y,piece.x)] = legal_moves
                elif legal_moves and attc:
                    #print('hey')
                    #print(legal_moves)
                    moves = moves.union(legal_moves)
    '''
    return moves

# IF FUNCTION RETURNS value= -INF, AI IS IN CHECKMATE
# OR move = 0
# (returning +inf for value MIGHT indicate player checkmate. not sure)
def minimax(board, depth, alpha, beta, maximizing, memo):
    """
    Minimax algorithm with alpha-beta pruning determines the best move for
    black from the current board state.
    Return: bestValue - score of the board resulting from the best move
            move - tuple containing the start coord and the end coord of the best move
            ex. ((y1,x1),(y2,x2)) -> the piece at (y1,x1) should move to (y2,x2)
    """

    tuple_mat = matrix_to_tuple(board.array, board.empty)
    if tuple_mat in memo and depth != 3: # set this to the depth of the initial call
        return memo[tuple_mat], 0

    if depth == 0: # end of the search is reached
        memo[tuple_mat] = board.score
        return board.score, 0

    if maximizing:
        bestValue = float("-inf")
        black_moves = move_gen(board,"b")
        for start, move_set in black_moves.items():
            #if start = SPECIAL MOVE
            for end in move_set:


                #develop the 'child'
                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]
                board.move_piece(piece,end[0],end[1],False,True)
                #if dest:
                    #sprites.remove(dest)

                # see if the move puts you in check
                attacked = move_gen(board,"w",True) #return spaces attacked by white

                if (board.black_king.y,board.black_king.x) in attacked:
                    piece = board.array[end[0]][end[1]]
                    board.move_piece(piece,start[0],start[1],False, True)
                    board.array[end[0]][end[1]] = dest
                    #if dest:
                        #sprites.append(dest)
                    continue


                #change the board score
                if dest != None:
                    board.score += board.pvalue_dict[type(dest)]

                v, __ = minimax(board, depth - 1,alpha,beta, False, memo)


                # revert the board
                piece = board.array[end[0]][end[1]]
                board.move_piece(piece,start[0],start[1],False, True)
                board.array[end[0]][end[1]] = dest
                #if dest:
                    #sprites.append(dest)
                if v >= bestValue:

                    move = (start, (end[0],end[1])) # preserve the move

                bestValue = max(bestValue, v)
                alpha = max(alpha, bestValue)

                #revert the score
                if dest != None:
                    board.score -= board.pvalue_dict[type(dest)]

                if beta <= alpha:
                    return bestValue, move
        try:
            return bestValue, move
        except:
            return bestValue, 0
            #pygame.image.save(screen,"screen.jpg")
            #print(bestValue)
            #board.print_to_terminal()
            #raise ValueError("Hey somethings wrong")



    else:    #(* minimizing player *)
        bestValue = float("inf")
        white_moves = move_gen(board,"w")
        for start, move_set in white_moves.items():
            for end in move_set:

                #DEVELOP the child
                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]
                board.move_piece(piece,end[0],end[1],False,True)
                #if dest:
                    #sprites.remove(dest)

                # see if the move puts your in check
                attacked = move_gen(board,"b",True) #return spaces attacked by white

                if (board.white_king.y,board.white_king.x) in attacked:
                    piece = board.array[end[0]][end[1]]
                    board.move_piece(piece,start[0],start[1],False,True)
                    board.array[end[0]][end[1]] = dest
                    #if dest:
                    #    sprites.append(dest)
                    continue


                #update the score
                if dest != None:
                    board.score -= board.pvalue_dict[type(dest)]

                v, __ = minimax(board, depth - 1,alpha,beta, True, memo)
                bestValue = min(v, bestValue)
                beta = min(beta,bestValue)

                #preserve shit
                piece = board.array[end[0]][end[1]]
                board.move_piece(piece,start[0],start[1],False,True)
                board.array[end[0]][end[1]] = dest
                #if dest:
                #    sprites.append(dest)

                # revert the score
                if dest != None:
                    board.score += board.pvalue_dict[type(dest)]

                if beta <= alpha:
                    return bestValue, 0

        return bestValue, 0

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((800, 60 * 8))
    b = Board()
    sprites = []

    trans_table = dict()
    value, move = minimax(b,3,float("-inf"),float("inf"), True, trans_table)
    print(len(trans_table))
    print(" ")
    b.print_to_terminal()
    print(value)
    print(move)
