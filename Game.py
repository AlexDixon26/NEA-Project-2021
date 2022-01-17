from abc import abstractmethod


class GameError(Exception):
    pass

class Game:
    AI = "AI"
    Human = "Human"
    Network = "Network"

    P1 = "Black"
    P2 = "White"


    P1Man = "⚫"
    P2Man = "⚪"
    P1King = "♔"
    P2King = "♚"
    POSSIBLEMOVE = "🟢"

    _DIM = 8
    _EMPTY = "   "

       
    def __init__(self, board=None, player=None):
        default_board = [[Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man],[Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY],[Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man],[Game._EMPTY]*Game._DIM,[Game._EMPTY]*Game._DIM,[Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY],[Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man],[Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY]]
        if board == None:
            board = default_board
        self._board = board
        self._player = player if player != None else Game.P1
        
    def do_move(self, row, col, row_to_move, col_to_move, take_used, board, player):
        #Complex user defined algorithm to make a move
        takes = 0
        if player == Game.P1:
            possible = [Game.P1King,Game.P1Man]
        else: 
            possible = [Game.P2King,Game.P2Man]
        row -= 1
        col -= 1
        if board[row][col] not in possible:
            raise GameError("Not your piece")
        row_to_move -= 1
        col_to_move -= 1
        if board[row][col] == Game.P1Man or board[row][col] == Game.P2Man:
            man_or_king = "S"
        else:
            man_or_king = "K"
        if board[row_to_move][col_to_move] not in [Game.POSSIBLEMOVE,Game._EMPTY]:
            raise GameError("Not a move")
        #if the move is not a take, just change the original square to blank and the new square to the piece
        if take_used == False:
            if board[row][col] != Game._EMPTY:
                board[row][col] = Game._EMPTY
                if man_or_king == "S":
                    board[row_to_move][col_to_move] = Game.P1Man if player is Game.P1 else Game.P2Man
                else:
                    board[row_to_move][col_to_move] = Game.P1King if player is Game.P1 else Game.P2King
        else:
            #otherwise, the algorithm needs to check if there are more takes available, and if there are then it needs to allow the user to make that second take
            if board[row][col] != Game._EMPTY:
                board[row][col] = Game._EMPTY
                if man_or_king == "S":
                    board[row_to_move][col_to_move] = Game.P1Man if player is Game.P1 else Game.P2Man
                    board[int((row_to_move + row)/2)][int((col_to_move + col)/2)] = Game._EMPTY
                    try:
                        # this code statement checks for extra takes
                        if player == Game.P1:
                            _, takes = self.find_black_piece_moves(row_to_move,col_to_move, board)
                        else:
                            _, takes = self.find_white_piece_moves(row_to_move,col_to_move, board)
                    except:
                        takes = []
                    if player == Game.P1:
                        if row == 1:
                            takes = []
                    else:
                        if row == 6:
                            takes = []
                else:
                    board[row_to_move][col_to_move] = Game.P1King if player is Game.P1 else Game.P2King
                    board[int((row_to_move + row)/2)][int((col_to_move + col)/2)] = Game._EMPTY
                    try:
                        if player == Game.P1:
                            _, takes = self.find_black_piece_moves(row_to_move,col_to_move, board)
                        else:
                            _, takes = self.find_white_piece_moves(row_to_move,col_to_move, board)
                    except:
                        takes = []
                if player == Game.P1:
                    if row_to_move == 0:
                        takes = []
                else:
                    if row_to_move == 7:
                        takes = []
        #check for new king and then remove all posible moves from the board
        self.check_for_new_king(player)
        self.remove_possible_moves()
        return takes


    def check_for_new_king(self, player):
        #When a counter reaches the final row of the board, then this algorithm changes it to a king
        for row in range(Game._DIM):
                for col in range(Game._DIM):
                    if player == Game.P1:
                        if row == 0:
                            if self._board[row][col] == Game.P1Man:
                                self._board[row][col] = Game.P1King
                    else:
                        if row == 7:
                            if self._board[row][col] == Game.P2Man:
                                self._board[row][col] = Game.P2King

                            
    def find_white_piece_moves(self, m, n, board):
        #Finds all the moves possible for a white piece
        available_moves = []
        available_takes = []
        if board[m][n] == Game.P2Man:
                    if self._check_white_player_moves(m, n, m + 1, n + 1, board):
                        available_moves.append([m, n, m + 1, n + 1])
                    if self._check_white_player_moves(m, n, m + 1, n - 1, board):
                        available_moves.append([m, n, m + 1, n - 1])
                    if self._check_white_player_takes(m, n, m + 1, n - 1, m + 2, n - 2, board):
                        available_takes.append([m, n, m + 2, n - 2])
                    if self._check_white_player_takes(m, n, m + 1, n + 1, m + 2, n + 2, board):
                        available_takes.append([m, n, m + 2, n + 2])
        elif board[m][n] == Game.P2King:
                    if self._check_white_player_moves(m, n, m + 1, n + 1, board):
                        available_moves.append([m, n, m + 1, n + 1])
                    if self._check_white_player_moves(m, n, m + 1, n - 1, board):
                        available_moves.append([m, n, m + 1, n - 1])
                    if self._check_white_player_moves(m, n, m - 1, n - 1, board):
                        available_moves.append([m, n, m - 1, n - 1])
                    if self._check_white_player_moves(m, n, m - 1, n + 1, board):
                        available_moves.append([m, n, m - 1, n + 1])
                    if self._check_white_player_takes(m, n, m + 1, n - 1, m + 2, n - 2, board):
                        available_takes.append([m, n, m + 2, n - 2])
                    if self._check_white_player_takes(m, n, m - 1, n - 1, m - 2, n - 2, board):
                        available_takes.append([m, n, m - 2, n - 2])
                    if self._check_white_player_takes(m, n, m - 1, n + 1, m - 2, n + 2, board):
                        available_takes.append([m, n, m - 2, n + 2])
                    if self._check_white_player_takes(m, n, m + 1, n + 1, m + 2, n + 2, board):
                        available_takes.append([m, n, m + 2, n + 2])

        return available_moves, available_takes

    def find_black_piece_moves(self, m, n, board):
        #Finds all the moves possible for a black piece
        available_moves = []
        available_takes = []
        if board[m][n] == Game.P1Man:
                    if self._check_black_player_moves(m, n, m - 1, n - 1, board):
                        available_moves.append([m, n, m - 1, n - 1])
                    if self._check_black_player_moves(m, n, m - 1, n + 1, board):
                        available_moves.append([m, n, m - 1, n + 1])
                    if self._check_black_player_takes(m, n, m - 1, n - 1, m - 2, n - 2, board):
                        available_takes.append([m, n, m - 2, n - 2])
                    if self._check_black_player_takes(m, n, m - 1, n + 1, m - 2, n + 2, board):
                        available_takes.append([m, n, m - 2, n + 2])
        elif board[m][n] == Game.P1King:
                    if self._check_black_player_moves(m, n, m - 1, n - 1, board):
                        available_moves.append([m, n, m - 1, n - 1])
                    if self._check_black_player_moves(m, n, m - 1, n + 1, board):
                        available_moves.append([m, n, m - 1, n + 1])
                    if self._check_black_player_takes(m, n, m - 1, n - 1, m - 2, n - 2, board):
                        available_takes.append([m, n, m - 2, n - 2])
                    if self._check_black_player_takes(m, n, m - 1, n + 1, m - 2, n + 2, board):
                        available_takes.append([m, n, m - 2, n + 2])
                    if self._check_black_player_moves(m, n, m + 1, n - 1, board):
                        available_moves.append([m, n, m + 1, n - 1])
                    if self._check_black_player_takes(m, n, m + 1, n - 1, m + 2, n - 2, board):
                        available_takes.append([m, n, m + 2, n - 2])
                    if self._check_black_player_moves(m, n, m + 1, n + 1, board):
                        available_moves.append([m, n, m + 1, n + 1])
                    if self._check_black_player_takes(m, n, m + 1, n + 1, m + 2, n + 2, board):
                        available_takes.append([m, n, m + 2, n + 2])

        return available_moves, available_takes
        
    def find_white_player_available_moves(self, board):
        #finds ALL available white moves
        available_moves = []
        available_takes = []
        for m in range(8):
            for n in range(8):
                moves, takes = self.find_white_piece_moves(m,n,board)
                for item in moves:
                    available_moves.append(item)
                for item in takes:
                    available_takes.append(item)


        #returns the valid moves and whether there is a take available 
        if len(available_takes) != 0:
            return available_takes, True
        else:
            return available_moves, False

        
    def find_black_player_available_moves(self, board):
        #finds ALL available black moves
        available_moves = []
        available_takes = []
        for m in range(8):
            for n in range(8):
                moves, takes = self.find_black_piece_moves(m,n,board)
                for item in moves:
                    available_moves.append(item)
                for item in takes:
                    available_takes.append(item)

        #returns the valid moves in a list and whether there is a take available
        if len(available_takes) != 0:
            return available_takes, True
        else:
            return available_moves, False

    def _check_black_player_moves(self, old_x, old_y, new_x, new_y, board):
        #checks the pieces move to see if it is valid
        possible = [Game.P1King,Game.P1Man] 
        if new_x > 7 or new_x < 0: #if the move brings the piece outside the board, its not valid
            return False
        if new_y > 7 or new_y < 0: #same again
            return False
        if board[old_x][old_y] == Game._EMPTY: #if the piece is not actually a piece, move is not valid
            return False
        if board[new_x][new_y] != Game._EMPTY: #if the piece is trying to move to somewhere that is not available to move to, move is not valid
            return False
        if board[old_x][old_y] not in possible: #if the piece trying to be moved is not the current players piece, it is not valid
            return False
        if board[new_x][new_y] == Game._EMPTY: # if the piece is moving to an empty square, return True because move is valid
            return True

    def _check_white_player_moves(self, old_x, old_y, new_x, new_y, board):
        #checks the pieces move to see if it is valid, see above for info on each if statement
        possible = [Game.P2King,Game.P2Man] 
        if new_x > 7 or new_x < 0: 
            return False
        if new_y > 7 or new_y < 0:
            return False
        if board[old_x][old_y] == Game._EMPTY:
            return False
        if board[new_x][new_y] != Game._EMPTY:
            return False
        if board[old_x][old_y] not in possible:
            return False
        if board[new_x][new_y] == Game._EMPTY:
            return True

    def _check_black_player_takes(self, old_x, old_y, via_x, via_y, new_x, new_y, board):
        #checks the take to see if it is valid
        possible = [Game.P1King,Game.P1Man] 
        if new_x > 7 or new_x < 0: #validation of take being on board
            return False
        if new_y > 7 or new_y < 0:
            return False
        if board[via_x][via_y] == Game._EMPTY: #if the piece begin taken is not a piece, take is not valid
            return False
        if board[via_x][via_y] in possible: #if the piece being taken is of the same colour as the piece taking it, take is not valid
            return False
        if board[new_x][new_y] != Game._EMPTY: #if the square being moved to is not empty, take is not valid
            return False
        if board[old_x][old_y] == Game._EMPTY: #if the piece being moved is not a piece, take is not valid
            return False
        if board[old_x][old_y] not in possible: #if the piece being moved is not the current players piece, take is not valid
            return False
        return True #return true if it makes it past all of these

    def _check_white_player_takes(self, old_x, old_y, via_x, via_y, new_x, new_y, board):
        #checks the take to see if it is valid, see above for info on each if
        possible = [Game.P2King,Game.P2Man] 
        if new_x > 7 or new_x < 0: 
            return False
        if new_y > 7 or new_y < 0:
            return False
        if board[via_x][via_y] == Game._EMPTY:
            return False
        if board[via_x][via_y] in possible:
            return False
        if board[new_x][new_y] != Game._EMPTY:
            return False
        if board[old_x][old_y] == Game._EMPTY:
            return False
        if board[old_x][old_y] not in possible:
            return False
        return True

    def print_possible_moves(self, row, col):
        #places a green possible move counter on the square given
        self._board[row-1][col-1] = Game.POSSIBLEMOVE

    def remove_possible_moves(self):
        #removes all green possible move counters on the board
        for row in range(8):
            for col in range(8):
                if self._board[row][col] == Game.POSSIBLEMOVE:
                    self._board[row][col] = Game._EMPTY

    #four functions that each return their designated variable
    def whos_move(self):
        return "Black to move" if self._player is Game.P1 else "White to move"

    def at(self, row, col):
        return self._board[row][col]

    def return_player(self):
        return self._player
    
    def return_board(self):
        return self._board

    def check_for_takes(self):
        #function that checks the entire board to see if there is a take available
        result = []
        if self._player == Game.P1:
            PossiblePieces = [Game.P1King,Game.P1Man]
        else:
            PossiblePieces = [Game.P2King,Game.P2Man]
        for col in range(Game._DIM):
            for row in range(Game._DIM):
                takes = []
                if self._board[row][col] in PossiblePieces:
                    if self._player == Game.P1:
                        _, takes = self.find_black_piece_moves(row,col, self._board)
                    else:
                        _, takes = self.find_white_piece_moves(row,col, self._board)
                    #_get_legal_moves(col+1,row+1,True)
                if takes != []:
                    result.append([row+1,col+1])
        return result

    @property
    def finished_game(self):
        #property that checks if the game is finished
        for p in [Game.P1Man,Game.P2Man]:
            fin = True
            for row in range(Game._DIM):
                    for col in range(Game._DIM):
                        if self._board[row][col] == p:
                            fin = False
                            break
                    if fin == False:
                        break
            if fin == True:
                king = Game.P1King if p is Game.P1Man else Game.P2King
                for row in range(Game._DIM):
                    for col in range(Game._DIM):
                        if self._board[row][col] == king:
                            fin = False
                            break
                    if fin == False:
                        break
                
                if fin == True:
                    return Game.P2 if p is Game.P1Man else Game.P1
                return None
    
    def __repr__(self):
        result = "  " + " ".join(str(i+1)+"  " for i in range(Game._DIM))
        for row in range(Game._DIM):
            result += f"\n{row+1} " + "|".join(self._board[row])
            if row != Game._DIM - 1:
                dashes = "--" * (2 * Game._DIM - 1)
                result += f"\n  {dashes}"
        return result