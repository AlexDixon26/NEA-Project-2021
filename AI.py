from Player import Player
from Game import Game

class AI(Player):
    def __init__(self, difficulty, piece):
        self._difficulty = difficulty
        self.__game = Game
        self.__piece = [self.__game.P1Man,self.__game.P1King] if piece == "Black" else [self.__game.P2Man,self.__game.P2King]

    def get_possible_move(self):
        # no ideas waht this is even trying to do: for self.__piece in self.__game:
        pass