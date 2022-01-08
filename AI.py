from Player import Player
from random import randint

class AI(Player):
    P1Man = "⚫ "
    P2Man = "⚪ "
    P1King = " ♔ "
    P2King = " ♚ "
    _EMPTY = "   "


    def __init__(self, difficulty):
        self._difficulty = difficulty
        self.__piece = [AI.P2Man,AI.P2King]
        self.__colour = "White"

    def get_move(self, movelist, takes):
        if self._difficulty == "Easy":
            r = randint(0,len(movelist)-1)
            return movelist[r]
        elif self._difficulty == "Hard":
            pass
        elif self._difficulty == "Extreme":
            pass

    def calculate_board_worth(self, board):
        man = AI.P2Man
        opp_man = AI.P1Man
        king = AI.P2King
        opp_king = AI.P1King
        result = 0
        mine = 0
        opp = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == man or board[i][j] == king:
                    mine += 1

                    if board[i][j] == man: #if piece is computers
                        result += 5
                    if board[i][j] == king: #if piece is computers
                        result += 10
                    if i == 0 or j == 0 or i == 7 or j == 7: #if the piece is on the edge of the board so cannot be taken
                        result += 7
                    if i + 1 > 7 or j - 1 < 0 or i - 1 < 0 or j + 1 > 7: #skip next checks if piece cannot take/be taken
                        continue
                    if (board[i + 1][j - 1] == opp_man or board[i + 1][j - 1] == opp_king) and board[i - 1][
                        j + 1] == AI._EMPTY: #if the piece can be taken
                        result -= 3
                    if (board[i + 1][j + 1] == opp_man or board[i + 1][j + 1] == opp_king) and board[i - 1][j - 1] == AI._EMPTY: #if the piece can be taken
                        result -= 3
                    if board[i - 1][j - 1] == opp_king and board[i + 1][j + 1] == AI._EMPTY: #if king can take piece
                        result -= 3

                    if board[i - 1][j + 1] == opp_king and board[i + 1][j - 1] == AI._EMPTY: #if king can take piece
                        result -= 3
                    if i + 2 > 7 or i - 2 < 0: # skip next steps if piece cannot take
                        continue
                    if (board[i + 1][j - 1] == opp_king or board[i + 1][j - 1] == opp_man) and board[i + 2][
                        j - 2] == AI._EMPTY: #if a piece can be taken by current piece
                        result += 6
                    if i + 2 > 7 or j + 2 > 7: #skip next steps if piece cannot take
                        continue
                    if (board[i + 1][j + 1] == opp_king or board[i + 1][j + 1] == opp_man) and board[i + 2][
                        j + 2] == AI._EMPTY: #if a piece can be taken by current piece
                        result += 6

                elif board[i][j] == opp_man or board[i][j] == opp_king:
                    opp += 1

        return result + (mine - opp) * 1000