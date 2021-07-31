from Client import Client
from Human import Human
from AI import AI

class GameError(Exception):
    pass

class Game:
    AI = "AI"
    Human = "Human"
    Network = "Network"

    P2 = "⚫"
    P1 = "⚪"

    _DIM = 8
    _EMPTY = " "
        
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
        self.board = [[Game._EMPTY for _ in range(Game._DIM)] for _ in range(Game._DIM)]
        self.__player = Game.P1
        
    def do_move(self, row, col):
        row, col -= 1, 1 #row & column entered will be 1-based, code will use 0-based
        if self._board[row][col] != Game._EMPTY:
            raise GameError("Invalid Move")
        self._board[row][col] = self._player
        self._player = Game.P2 if self._player is Game.P1 else Game.P1

        pass

    def finished(self):
        for p in [Game.P1, Game.P2]:
            finished = True
            for row in range(Game._DIM):
                for col in range(Game._DIM):
                    if self.board[row][col] == p:
                        finished = False
            if finished == True:
                return True
        return None
        #Do Draw Mechanics later