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
        self._board = [[Game._EMPTY,Game.P2,Game._EMPTY,Game.P2,Game._EMPTY,Game.P2,Game._EMPTY,Game.P2],[Game.P2,Game._EMPTY,Game.P2,Game._EMPTY,Game.P2,Game._EMPTY,Game.P2,Game._EMPTY],[Game._EMPTY,Game.P2,Game._EMPTY,Game.P2,Game._EMPTY,Game.P2,Game._EMPTY,Game.P2],[Game._EMPTY]*Game._DIM,[Game._EMPTY]*Game._DIM,[Game.P1,Game._EMPTY,Game.P1,Game._EMPTY,Game.P1,Game._EMPTY,Game.P1,Game._EMPTY],[Game._EMPTY,Game.P1,Game._EMPTY,Game.P1,Game._EMPTY,Game.P1,Game._EMPTY,Game.P1],[Game.P1,Game._EMPTY,Game.P1,Game._EMPTY,Game.P1,Game._EMPTY,Game.P1,Game._EMPTY]]
        self._player = Game.P1
        
    def _do_move(self, row, col, row_to_move, col_to_move):
        row -= 1
        col -= 1
        row_to_move -= 1
        col_to_move -= 1
        if self._board[row][col] == Game.P1Man or self._board[row][col] == Game.P2Man:
            man_or_king = "S"
        else:
            man_or_king = "K"
        if self._board[row][col] != Game._EMPTY:
            self._board[row][col] = Game._EMPTY
            if man_or_king == "S":
                self._board[row_to_move][col_to_move] = Game.P2Man if self._player is Game.P1 else Game.P1Man
            else:
                self._board[row_to_move][col_to_move] = Game.P2King if self._player is Game.P1 else Game.P1King
        
    def check_for_new_king(self):
           

    def _get_legal_moves(self, row_of_piece, col_of_piece):
        moves = []
        not_player = Game.P1 if self._player is Game.P1 else Game.P2
        if self._board[row_of_piece-1][col_of_piece-1] == Game._EMPTY or  self._board[row_of_piece-1][col_of_piece-1] == not_player:
            return -1
        if self._board[row][col] == Game.P1Man or self._board[row][col] == Game.P2Man:
            man_or_king = "S"
        else:
            man_or_king = "K"
        if row_of_piece not in [1,8]:
            if self._player == Game.P1:
                moves.append((row_of_piece + 1, col_of_piece - 1))
                moves.append((row_of_piece - 1, col_of_piece - 1))
            else:
                moves.append((row_of_piece + 1, col_of_piece + 1))
                moves.append((row_of_piece - 1, col_of_piece + 1))
        else:
            if self._player == Game.P1:
                if row_of_piece == "1":
                    moves.append((row_of_piece - 1, col_of_piece - 1))
                else:
                    moves.append((row_of_piece + 1, col_of_piece - 1))
            else:
                if row_of_piece == "1":
                    moves.append((row_of_piece - 1, col_of_piece + 1))
                else:
                    moves.append((row_of_piece + 1, col_of_piece + 1))
        if man_or_king == "K":
            if row_of_piece not in [1,8]:
                if self._player == Game.P1:
                moves.append((row_of_piece + 1, col_of_piece + 1))
                moves.append((row_of_piece - 1, col_of_piece + 1))
            else:
                moves.append((row_of_piece + 1, col_of_piece - 1))
                moves.append((row_of_piece - 1, col_of_piece - 1))
        else:
            if self._player == Game.P1:
                if row_of_piece == "1":
                    moves.append((row_of_piece - 1, col_of_piece + 1))
                else:
                    moves.append((row_of_piece + 1, col_of_piece + 1))
            else:
                if row_of_piece == "1":
                    moves.append((row_of_piece - 1, col_of_piece - 1))
                else:
                    moves.append((row_of_piece + 1, col_of_piece - 1))
        return moves

    def _finished(self):
        for p in [Game.P1, Game.P2]:
            finished = True
            for row in range(Game._DIM):
                for col in range(Game._DIM):
                    if self._board[row][col] == p:
                        finished = False
            if finished == True:
                return True
        return None
        #Do Draw Mechanics later
    
    def __repr__(self):
        result = "  " + " ".join(str(i+1) for i in range(Game._DIM))
        for row in range(Game._DIM):
            result += f"\n{row+1} " + "|".join(self._board[row])
            if row != Game._DIM - 1:
                dashes = "--" * (2 * Game._DIM - 1)
                result += f"\n  {dashes}"
        return result