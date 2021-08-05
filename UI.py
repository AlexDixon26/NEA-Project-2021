from Game import Game, GameError
from sys import argv

class GUI:
    def __init__(self):
        self._game = Game() #Game.Ai/Human/Client,Game.Ai/Human/Client in brackets

    def run(self):
        pass

class Terminal:
    def __init__(self):
        self._game = Game(Game.Human,Game.Human)


    def run(self):
        while not self._game.finished:
            print(self._game)
            print(self._game.whos_move())
            try:
                print("Enter Row and Column of piece to move:")
                row = int(input("row: "))
                col = int(input("column: "))
            except:
                print("non numeric input")
                continue
            if 1 <= row <= 8 and 1 <= col <= 8:
                try:
                    legal_moves, takes = self._game._get_legal_moves(row, col)
                    print("Legal moves for this piece: ")
                    take_used = False
                    result = ""
                    potential_rows = []
                    potential_columns = []
                    if takes != 0:
                        print("There is a take[s] available, which you must do")
                        take_used = True
                        current_player = self._game.return_player()
                        for i in legal_moves:
                            result = ""
                            for num in i:
                                result += str(num + 1)
                            if current_player == "Black":
                                if int(result[0]) == int(row - 2):
                                    print(result[0] + "," + result[1])
                                    potential_rows.append(int(result[0]))
                                    potential_columns.append(int(result[1]))
                            else:
                                if int(result[0]) == int(row + 2):
                                    print(result[0] + "," + result[1])
                                    potential_rows.append(int(result[0]))
                                    potential_columns.append(int(result[1]))
                    else:
                        for i in legal_moves:
                            result = ""
                            for num in i:
                                result += str(num + 1)
                            print(result[0] + "," + result[1])
                            potential_rows.append(int(result[0]))
                            potential_columns.append(int(result[1]))
                    row_to_move = int(input("Enter row to move to:"))
                    col_to_move = int(input("Enter col to move to:"))
                    if row_to_move not in potential_rows:
                        print("You cannot move there!")
                        raise ValueError
                    if col_to_move not in potential_columns:
                        print("You cannot move there!")
                        raise ValueError
                    self._game._do_move(row, col, row_to_move, col_to_move, take_used)
                except GameError:
                    print("not your piece to move!")
                except ValueError:
                    continue
            else:
                print("Row and column must be within 1 - 8")
        print("Game Finished!")
        w = self._game.finished
        print(f"The winner was {w}")

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
