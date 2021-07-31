from Game import Game
from sys import argv

class GUI:
    def __init__(self):
        self.__game = Game() #Game.Ai/Human/Client,Game.Ai/Human/Client in brackets

    def run(self):
        pass

class Terminal:
    def __init__(self):
        self.__game = Game(Game.Human,Game.Human)


    def run(self):
        _ = input("PLAY (Press Any Button to continue, Ctrl + C to stop)")




def usage():   
    print(f"""
Usage: {argv[0]} [g | t]
g : play with the GUI
t : play with the Terminal""")
    quit()

if __name__ == "__main__":
    if len(argv) != 2:
        usage()
    elif argv[1] == "t":
        ui = Terminal()
    elif argv[1] == "g":
        ui = GUI()
    else:
        usage()
    
    ui.run()
