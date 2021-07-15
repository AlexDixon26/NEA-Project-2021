from Game import Game


class GUI:
    def __init__(self):
        self.__game = Game(Game.Human,Game.Human)

    def run(self):
        pass

if __name__ == "__main__":
    g = GUI()
    g.run()
