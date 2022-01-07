from Player import Player
from random import randint

class AI(Player):
    P1Man = "⚫ "
    P2Man = "⚪ "
    P1King = " ♔ "
    P2King = " ♚ "


    def __init__(self, difficulty, piece):
        self._difficulty = difficulty
        self.__piece = [AI.P1Man,AI.P1King] if piece == "Black" else [AI.P2Man,AI.P2King]

    def get_move(self, movelist, takes):
        

        # FIRST 2 numbers are current piece (col, row)
        # SECOND 2 numbers are available move (col, row)
        if self._difficulty == "Easy":
            r = randint(0,len(movelist)-1)
            if takes == False:
                return movelist[r]
            else:
                return movelist[r]
                #
                #       WRITE CODE TO CHECK IF THE PIECE CAN TAKE AGAIN (MAYBE NEW FUNCTION?)
                #