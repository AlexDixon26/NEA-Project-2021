from Player import Player


class Human(Player):
    Users = []
    def __init__(self, User):
        self.__username = User
        if self.__username not in Human.Users:
            Human.Users.append(self.__username)

