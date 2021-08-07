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


    P1Man = "⚫"
    P2Man = "⚪"
    P1King = "♔"
    P2King = "♚"

    _DIM = 8
    _EMPTY = "   "
        
    def __init__(self, player1, player2):
        if player1 == Game.AI:
            self.__player1 = AI()
        elif player1 == Game.Human:
            self.__player1 = Human()
        elif player1 == Game.Network:
            self.__player1 = Client()
        if player2 == Game.AI:
            self.__player2 = AI()
        elif player2 == Game.Human:
            self.__player2 = Human()
        elif player2 == Game.Network:
            self.__player2 = Client()
        self._board = [[Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man],[Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY],[Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man,Game._EMPTY,Game.P2Man],[Game._EMPTY]*Game._DIM,[Game._EMPTY]*Game._DIM,[Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY],[Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man],[Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY,Game.P1Man,Game._EMPTY]]
        self._player = Game.P1
        
    def _do_move(self, row, col, row_to_move, col_to_move, take_used):
        #Validation of piece being theres
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
                    _, takes = self._get_legal_moves(row_to_move+1, col_to_move+1)

                else:
                    self._board[row_to_move][col_to_move] = Game.P1King if self._player is Game.P1 else Game.P2King
                    self._board[int((row_to_move + row)/2)][int((col_to_move + col)/2)] = Game._EMPTY
                    print(self._board)
                    _, takes = self._get_legal_moves(row_to_move+1,col_to_move+1)
        self.check_for_new_king()
        if takes != 0:
            return takes
        else:
            if self._player == Game.P1:
                self._player = Game.P2
            else:
                self._player = Game.P1
            return 0
        
    def check_for_new_king(self):
        for row in range(Game._DIM):
                for col in range(Game._DIM):
                    if self._player == Game.P1:
                        if col == 8:
                            if self._board[row][col] in [Game.P1Man]:
                                self._board[row][col] == Game.P1King
                    else:
                        if col == 1:
                            if self._board[row][col] in [Game.P2Man]:
                                self._board[row][col] == Game.P2King


    def _get_legal_moves(self, row_of_piece, col_of_piece):
        if self._player == Game.P1:
            possible = [Game.P1King,Game.P1Man] 
        else: 
            possible = [Game.P2King,Game.P2Man]
        if self._board[row_of_piece-1][col_of_piece-1] not in possible:
            raise GameError("Not your piece")
        take = 0
        result = []
        row_of_piece -= 1
        col_of_piece -= 1
        if self._player == Game.P1:
            row = row_of_piece - 1
            if col_of_piece == 0:
                col = col_of_piece + 1
                if self._board[row][col] in [Game.P1Man,Game.P1King]:
                    result = result
                elif self._board[row][col] == Game._EMPTY:
                    result.append([row,col])
                else:
                    if self._board[row-1][col+1] == Game._EMPTY:
                        result.append([row-1,col+1])
                        take += 1
                    else:
                        result = result
            elif col_of_piece == 7:
                col = col_of_piece - 1
                if self._board[row][col] in [Game.P1Man,Game.P1King]:
                    result = result
                elif self._board[row][col] == Game._EMPTY:
                    result.append([row,col])
                else:
                    if self._board[row-1][col-1] == Game._EMPTY:
                        result.append([row-1,col-1])
                        take += 1
                    else:
                        result = result
            elif col_of_piece in [1,2,3,4,5,6]:
                col = col_of_piece - 1
                if self._board[row][col] in [Game.P1Man,Game.P1King]:
                    result = result
                elif self._board[row][col] == Game._EMPTY:
                    result.append([row,col])
                else:
                    if self._board[row-1][col-1] == Game._EMPTY:
                        result.append([row-1,col-1])
                        take += 1
                    else:
                        result = result
                col = col_of_piece + 1
                if self._board[row][col] in [Game.P1Man,Game.P1King]:
                    result = result
                elif self._board[row][col] == Game._EMPTY:
                    result.append([row,col])
                else:
                    if self._board[row-1][col+1] == Game._EMPTY:
                        result.append([row-1,col+1])
                        take += 1
                    else:
                        result = result
            if self._board[row][col] == Game.P1King:
                row = row_of_piece + 1
                if col_of_piece == 0:
                    col = col_of_piece + 1
                    if self._board[row][col] in [Game.P2Man,Game.P2King]:
                        result = result
                    elif self._board[row][col] == Game._EMPTY:
                        result.append([row,col])
                    else:
                        if self._board[row-1][col+1] == Game._EMPTY:
                            result.append([row-1,col+1])
                            take += 1
                        else:
                            result = result
                elif col_of_piece == 7:
                    col = col_of_piece + 1
                    if self._board[row][col] in [Game.P2Man,Game.P2King]:
                        result = result
                    elif self._board[row][col] == Game._EMPTY:
                        result.append([row,col])
                    else:
                        if self._board[row-1][col-1] == Game._EMPTY:
                            result.append([row-1,col-1])
                            take += 1
                        else:
                            result = result
                elif col_of_piece in [1,2,3,4,5,6]:
                    col = col_of_piece - 1
                    if self._board[row][col] in [Game.P2Man,Game.P2King]:
                        result = result
                    elif self._board[row][col] == Game._EMPTY:
                        result.append([row,col])
                    else:
                        if self._board[row-1][col-1] == Game._EMPTY:
                            result.append([row-1,col-1])
                            take += 1
                        else:
                            result = result
                    col = col_of_piece + 1
                    if self._board[row][col] in [Game.P2Man,Game.P2King]:
                        result = result
                    elif self._board[row][col] == Game._EMPTY:
                        result.append([row,col])
                    else:
                        if self._board[row-1][col+1] == Game._EMPTY:
                            result.append([row-1,col+1])
                            take += 1
                        else:
                            result = result
        else:
            row = row_of_piece + 1
            if col_of_piece == 0:
                col = col_of_piece + 1
                if self._board[row][col] in [Game.P2Man,Game.P2King]:
                    result = result
                elif self._board[row][col] == Game._EMPTY:
                    result.append([row,col])
                else:
                    if self._board[row-1][col+1] == Game._EMPTY:
                        result.append([row-1,col+1])
                        take += 1
                    else:
                        result = result
            elif col_of_piece == 7:
                col = col_of_piece - 1
                if self._board[row][col] in [Game.P2Man,Game.P2King]:
                    result = result
                elif self._board[row][col] == Game._EMPTY:
                    result.append([row,col])
                else:
                    if self._board[row-1][col-1] == Game._EMPTY:
                        result.append([row-1,col-1])
                        take += 1
                    else:
                        result = result
            elif col_of_piece in [1,2,3,4,5,6]:
                col = col_of_piece - 1
                if self._board[row][col] in [Game.P2Man,Game.P2King]:
                    result = result
                elif self._board[row][col] == Game._EMPTY:
                    result.append([row,col])
                else:
                    if self._board[row-1][col-1] == Game._EMPTY:
                        result.append([row-1,col-1])
                        take += 1
                    else:
                        result = result
                col = col_of_piece + 1
                if self._board[row][col] in [Game.P2Man,Game.P2King]:
                    result = result
                elif self._board[row][col] == Game._EMPTY:
                    result.append([row,col])
                else:
                    if self._board[row-1][col+1] == Game._EMPTY:
                        result.append([row-1,col+1])
                        take += 1
                    else:
                        result = result
            if self._board[row_of_piece][col_of_piece] == Game.P2King:
                row = row_of_piece - 1
                if col_of_piece == 0:
                    col = col_of_piece + 1
                    if self._board[row][col] in [Game.P2Man,Game.P2King]:
                        result = result
                    elif self._board[row][col] == Game._EMPTY:
                        result.append([row,col])
                    else:
                        if self._board[row-1][col+1] == Game._EMPTY:
                            result.append([row-1,col+1])
                            take += 1
                        else:
                            result = result
                elif col_of_piece == 7:
                    col = col_of_piece - 1
                    if self._board[row][col] in [Game.P2Man,Game.P2King]:
                        result = result
                    elif self._board[row][col] == Game._EMPTY:
                        result.append([row,col])
                    else:
                        if self._board[row-1][col-1] == Game._EMPTY:
                            result.append([row-1,col-1])
                            take += 1
                        else:
                            result = result
                elif col_of_piece in [1,2,3,4,5,6]:
                    col = col_of_piece - 1
                    if self._board[row][col] in [Game.P2Man,Game.P2King]:
                        result = result
                    elif self._board[row][col] == Game._EMPTY:
                        result.append([row,col])
                    else:
                        if self._board[row-1][col-1] == Game._EMPTY:
                            result.append([row-1,col-1])
                            take += 1
                        else:
                            result = result
                    col = col_of_piece + 1
                    if self._board[row][col] in [Game.P2Man,Game.P2King]:
                        result = result
                    elif self._board[row][col] == Game._EMPTY:
                        result.append([row,col])
                    else:
                        if self._board[row-1][col+1] == Game._EMPTY:
                            result.append([row-1,col+1])
                            take += 1
                        else:
                            result = result
        return result, take

    def whos_move(self):
        return "Black to move" if self._player is Game.P1 else "White to move"

    def return_player(self):
        return self._player

    @property
    def finished(self):
        for p in [Game.P1Man, Game.P2Man, Game.P1King, Game.P2King]:
            finished = True
            for row in range(Game._DIM):
                for col in range(Game._DIM):
                    if self._board[row][col] == p:
                        finished = False
            if finished == False:
                return None
        if finished == True:
            return p
    
    def __repr__(self):
        result = "  " + " ".join(str(i+1)+"  " for i in range(Game._DIM))
        for row in range(Game._DIM):
            result += f"\n{row+1} " + "|".join(self._board[row])
            if row != Game._DIM - 1:
                dashes = "--" * (2 * Game._DIM - 1)
                result += f"\n  {dashes}"
        return result