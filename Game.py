from Client import Client
from Human import Human
from AI import AI

class GameError(Exception):
    pass

class Game:
    AI = "AI"
    Human = "Human"
    Network = "Network"

    P1 = "Black"
    P2 = "White"


    P1Man = "⚫ "
    P2Man = "⚪ "
    P1King = " ♔ "
    P2King = " ♚ "
    POSSIBLEMOVE = "🟢"

    _DIM = 8
    _EMPTY = "   "
        
    def __init__(self):
        self._board = [[Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man],[Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY],[Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man],[Game._EMPTY]*Game._DIM,[Game._EMPTY]*Game._DIM,[Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY],[Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man],[Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY]]
        self._player = Game.P1
        
    def _do_move(self, row, col, row_to_move, col_to_move, take_used):
        #Validation of piece being there
        takes = 0
        if self._player == Game.P1:
            possible = [Game.P1King,Game.P1Man]
        else: 
            possible = [Game.P2King,Game.P2Man]
        row -= 1
        col -= 1
        if self._board[row][col] not in possible:
            raise GameError("Not your piece")
        row_to_move -= 1
        col_to_move -= 1
        if self._board[row][col] == Game.P1Man or self._board[row][col] == Game.P2Man:
            man_or_king = "S"
        else:
            man_or_king = "K"
        if take_used == False:
            if self._board[row][col] != Game._EMPTY:
                self._board[row][col] = Game._EMPTY
                if man_or_king == "S":
                    self._board[row_to_move][col_to_move] = Game.P1Man if self._player is Game.P1 else Game.P2Man
                else:
                    self._board[row_to_move][col_to_move] = Game.P1King if self._player is Game.P1 else Game.P2King
        else:
             if self._board[row][col] != Game._EMPTY:
                self._board[row][col] = Game._EMPTY
                if man_or_king == "S":
                    self._board[row_to_move][col_to_move] = Game.P1Man if self._player is Game.P1 else Game.P2Man
                    self._board[int((row_to_move + row)/2)][int((col_to_move + col)/2)] = Game._EMPTY
                    try:
                        _, takes = self._get_legal_moves(row_to_move+1, col_to_move+1, False)
                    except:
                        takes = 0
                    if self._player == Game.P1:
                        if row == 1:
                            takes = 0
                    else:
                        if row == 6:
                            takes = 0
                else:
                    self._board[row_to_move][col_to_move] = Game.P1King if self._player is Game.P1 else Game.P2King
                    self._board[int((row_to_move + row)/2)][int((col_to_move + col)/2)] = Game._EMPTY
                    try:
                        _, takes = self._get_legal_moves(row_to_move+1,col_to_move+1, False)
                    except:
                        takes = 0
                    if self._player == Game.P1:
                        if row_to_move == 0:
                            takes = 0
                    else:
                        if row_to_move == 8:
                            takes = 0
        self.check_for_new_king()
        self.remove_possible_moves()
        if takes != 0:
            return takes
        else:
            return 0
                            
        
    def check_for_new_king(self):
        for row in range(Game._DIM):
                for col in range(Game._DIM):
                    if self._player == Game.P1:
                        if row == 0:
                            if self._board[row][col] == Game.P1Man:
                                self._board[row][col] = Game.P1King
                    else:
                        if row == 7:
                            if self._board[row][col] == Game.P2Man:
                                self._board[row][col] = Game.P2King


    def _get_legal_moves(self, row_of_piece, col_of_piece, just_checking):
        if self._player == Game.P1:
            possible = [Game.P1King,Game.P1Man] 
        else: 
            possible = [Game.P2King,Game.P2Man]
        if self._board[row_of_piece-1][col_of_piece-1] not in possible and just_checking == False:
            raise GameError("Not your piece")
        take = 0
        result = []
        row_of_piece -= 1
        col_of_piece -= 1
        if self._player == Game.P1 or just_checking == True:
            row = row_of_piece - 1
            if row in [0,1,2,3,4,5,6,7]:  
                if col_of_piece in [0,1,2,3,4,5,6]:
                    col = col_of_piece + 1
                    if self._board[row][col] == Game._EMPTY:
                        result.append([row,col])
                    elif self._board[row][col] in [Game.P2Man,Game.P2King]:
                        try:
                            if self._board[row-1][col+1] == Game._EMPTY:
                                result.append([row-1,col+1])
                                take += 1
                        except:
                            result = result
                if col_of_piece in [1,2,3,4,5,6,7]:
                    col = col_of_piece - 1
                    if self._board[row][col] == Game._EMPTY:
                        result.append([row,col])
                    elif self._board[row][col] in [Game.P2Man,Game.P2King]:
                        try:
                            if self._board[row-1][col-1] == Game._EMPTY:
                                result.append([row-1,col-1])
                                take += 1
                        except:
                            result = result
            if self._board[row_of_piece][col_of_piece] == Game.P1King:
                row = row_of_piece + 1
                if row in [0,1,2,3,4,5,6,7]:
                    if col_of_piece in [0,1,2,3,4,5,6]:
                        col = col_of_piece + 1
                        if self._board[row][col] == Game._EMPTY:
                            result.append([row,col])
                        elif self._board[row][col] in [Game.P2Man,Game.P2King]:
                            try:
                                if self._board[row+1][col+1] == Game._EMPTY:
                                    result.append([row+1,col+1])
                                    take += 1
                            except:
                                result = result
                    if col_of_piece in [1,2,3,4,5,6,7]:
                        col = col_of_piece - 1
                        if self._board[row][col] == Game._EMPTY:
                            result.append([row,col])
                        elif self._board[row][col] in [Game.P2Man,Game.P2King]:
                            try:
                                if self._board[row+1][col-1] == Game._EMPTY:
                                    result.append([row+1,col-1])
                                    take += 1
                            except:
                                result = result
        if self._player == Game.P2 or just_checking == True:
            row = row_of_piece + 1
            if row in [0,1,2,3,4,5,6,7]:
                if col_of_piece in [0,1,2,3,4,5,6]:
                    col = col_of_piece + 1
                    if self._board[row][col] == Game._EMPTY:
                        result.append([row,col])
                    elif self._board[row][col] in [Game.P1Man,Game.P1King]:
                        try:
                            if self._board[row+1][col+1] == Game._EMPTY:
                                result.append([row+1,col+1])
                                take += 1
                        except:
                            result = result
                if col_of_piece in [1,2,3,4,5,6,7]:
                    col = col_of_piece - 1
                    if self._board[row][col] == Game._EMPTY:
                        result.append([row,col])
                    elif self._board[row][col] in [Game.P1Man,Game.P1King]:
                        try:
                            if self._board[row+1][col-1] == Game._EMPTY:
                                result.append([row+1,col-1])
                                take += 1
                        except:
                            result = result
            if self._board[row_of_piece][col_of_piece] == Game.P2King:
                row = row_of_piece - 1
                if row in [0,1,2,3,4,5,6,7]:
                    if col_of_piece in [0,1,2,3,4,5,6]:
                        col = col_of_piece + 1
                        if self._board[row][col] == Game._EMPTY:
                            result.append([row,col])
                        elif self._board[row][col] in [Game.P1Man,Game.P1King]:
                            try:
                                if self._board[row-1][col+1] == Game._EMPTY:
                                    result.append([row-1,col+1])
                                    take += 1 
                            except:
                                result = result
                    if col_of_piece in [1,2,3,4,5,6,7]:
                        col = col_of_piece - 1
                        if self._board[row][col] == Game._EMPTY:
                            result.append([row,col])
                        elif self._board[row][col] in [Game.P1Man,Game.P1King]:
                            try:
                                if self._board[row-1][col-1] == Game._EMPTY:
                                    result.append([row-1,col-1])
                                    take += 1
                            except:
                                result = result

        for _, move in enumerate(result):
            if move[0] not in [0,1,2,3,4,5,6,7]:
                result.remove(move)
            if move[1] not in [0,1,2,3,4,5,6,7]:
                result.remove(move)

        for item in result:
            if item[0] not in [0,1,2,3,4,5,6,7]:
                result.remove(item)
            if item[1] not in [0,1,2,3,4,5,6,7]:
                result.remove(item)

        return result, take

    def print_possible_moves(self, row, col):
        self._board[row-1][col-1] = Game.POSSIBLEMOVE

    def remove_possible_moves(self):
        for row in range(8):
            for col in range(8):
                if self._board[row][col] == Game.POSSIBLEMOVE:
                    self._board[row][col] = Game._EMPTY
                
    def check_all_legal_moves(self, piece):
        result = []
        if piece == "Black":
            for col in range(Game._DIM):
                for row in range(Game._DIM):
                    if self._board[col][row] in [Game.P1Man,Game.P1King]:
                        temp = self._get_legal_moves(col, row, True)
                        result.append(temp)
        else:
            for col in range(Game._DIM):
                for row in range(Game._DIM):
                    if self._board[col][row] in [Game.P2Man,Game.P2King]:
                        temp = self._get_legal_moves(col, row, True)
                        result.append(temp)

    def whos_move(self):
        return "Black to move" if self._player is Game.P1 else "White to move"

    def at(self, row, col):
        return self._board[row][col]

    def return_player(self):
        return self._player

    def check_for_takes(self):
        result = []
        if self._player == Game.P1:
            PossiblePieces = [Game.P1King,Game.P1Man]
        else:
            PossiblePieces = [Game.P2King,Game.P2Man]
        for col in range(Game._DIM):
            for row in range(Game._DIM):
                takes = 0
                if self._board[col][row] in PossiblePieces:
                    _, takes = self._get_legal_moves(col+1,row+1,True)
                if takes != 0:
                    result.append([row+1,col+1])
        return result

    @property
    def _finished_game(self):
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