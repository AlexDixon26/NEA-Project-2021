from Client import Client
from Human import Human
from AI import AI

class Game:
    AI = "AI"
    Human = "Human"
    Network = "Network"

    BLACK = "⚫"
    WHITE = "⚪"
        
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
        
    def next_move(self):
        #tell game to play next move
        pass

    def finished(self):
        #return true if finished
        pass