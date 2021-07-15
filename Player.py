from abc import ABC

class Player(ABC):
    def __init__(self):
        pass

    def get_move(self):
        raise NotImplementedError