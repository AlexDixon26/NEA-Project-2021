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

    def get_move(self, movelist):
        random = randint(0,len(movelist)-1)
        temp = movelist[random]
        numeric_filter = filter(str.isdigit, str(temp))
        temp = "".join(numeric_filter)
        temp = temp[:-1]
        moved_from = temp[0:2]
        temp = temp[2:]
        list = []
        for item in temp:
            list.append(item)
        list2 = []
        for val in range(0,len(list),2):
            item = str(list[val] + list[val+1])
            list2.append(item)
        #
        #       REMEMBER THAT THE MOVED_FROM IS (row,col) but each movable space is (col-1,row-1) 
        #
        if self._difficulty == "Easy":
            return 1