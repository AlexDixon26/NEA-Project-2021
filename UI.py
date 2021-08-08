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
                    if len(legal_moves) == 0:
                        takes = 0
                        print("This piece cannot move")
                    take_used = False
                    result = ""
                    potential_rows = []
                    potential_columns = []
                    if takes != 0:
                        print("There is a take[s] available, which you must do")
                        take_used = True
                        current_player = self._game.return_player()
                        potential_rows, potential_columns = self.print_out_moves(legal_moves, current_player, row)
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
                    takes = self._game._do_move(row, col, row_to_move, col_to_move, take_used)
                    row = row_to_move
                    col = col_to_move
                    if takes != 0:
                        print(self._game)
                        print("Another Take[s] is available")
                        legal_moves, takes = self._game._get_legal_moves(row_to_move, col_to_move)
                        potential_rows, potential_columns = self.print_out_moves(legal_moves, current_player, row_to_move)
                        row_to_move = int(input("Enter row to move to:"))
                        col_to_move = int(input("Enter col to move to:"))
                        if row_to_move not in potential_rows:
                            print("You cannot move there!")
                            raise ValueError
                        if col_to_move not in potential_columns:
                            print("You cannot move there!")
                            raise ValueError
                        takes = self._game._do_move(row, col, row_to_move, col_to_move, take_used)
                        row = row_to_move
                        col = col_to_move
                        if takes != 0:
                            print(self._game)
                            print("Another Take[s] is available")
                            legal_moves, takes = self._game._get_legal_moves(row, col)
                            potential_rows, potential_columns = self.print_out_moves(legal_moves, current_player, row)
                            row_to_move = int(input("Enter row to move to:"))
                            col_to_move = int(input("Enter col to move to:"))
                            if row_to_move not in potential_rows:
                                print("You cannot move there!")
                                raise ValueError
                            if col_to_move not in potential_columns:
                                print("You cannot move there!")
                                raise ValueError
                            takes = self._game._do_move(row, col, row_to_move, col_to_move, take_used)

                except GameError:
                    print("not your piece to move!")
                except ValueError:
                    continue
            else:
                print("Row and column must be within 1 - 8")
        print(self._game)
        print("Game Finished!")
        w = self._game.finished
        print(f"The winner was {w}")
    
    def print_out_moves(self, legal_moves_list, current_player, row):
        potential_columns = []
        potential_rows = []
        for i in legal_moves_list:
            result = ""
            for num in i:
                result += str(num + 1)
            if current_player == "Black":
                if int(result[0]) == int(row - 2) or int(result[0]) == int(row + 2):
                    print(result[0] + "," + result[1])
                    potential_rows.append(int(result[0]))
                    potential_columns.append(int(result[1]))
            else:
                if int(result[0]) == int(row + 2) or int(result[0]) == int(row - 2):
                    print(result[0] + "," + result[1])
                    potential_rows.append(int(result[0]))
                    potential_columns.append(int(result[1]))
        return potential_rows, potential_columns

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
