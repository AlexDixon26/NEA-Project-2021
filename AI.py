from Player import Player

class AI(Player):
    P1Man = "⚫ "
    P2Man = "⚪ "
    P1King = " ♔ "
    P2King = " ♚ "


    def __init__(self, difficulty, piece):
        self._difficulty = difficulty
        self.__piece = [AI.P1Man,AI.P1King] if piece == "Black" else [AI.P2Man,AI.P2King]

    def play(self):
        if self._difficulty == "Easy":
            print("Easy")
        elif self._difficulty == "Hard":
            print("Hard")
        else:
            print("Extreme")
        
        #place function in each if