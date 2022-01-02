from Player import Player

class AI(Player):
    P1Man = "⚫ "
    P2Man = "⚪ "
    P1King = " ♔ "
    P2King = " ♚ "


    def __init__(self, difficulty, piece):
        self._difficulty = difficulty
        #self.__game = Game
        self.__piece = [AI.P1Man,AI.P1King] if piece == "Black" else [AI.P2Man,AI.P2King]

    def get_possible_move(self):
        # no ideas waht this is even trying to do: for self.__piece in self.__game:
        pass