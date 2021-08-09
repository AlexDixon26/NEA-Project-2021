from Game import Game, GameError
from abc import ABC, abstractmethod
from tkinter import END, Button, Tk, Toplevel, Frame, X, StringVar, Text,Scrollbar, LEFT, RIGHT, Y, Grid, N, S, W, E, Message
from itertools import product

class UI(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError

class GUI(UI):
    def __init__(self):
        root = Tk()
        root.title("Draughts")
        frame = Frame(root)
        frame.pack()

        Button(
            frame,
            text='Tutorials/Info',
            command= self._help_callback).pack(fill=X)
        
        Button(
            frame,
            text='Play Game',
            command= self._play_callback).pack(fill=X)
        
        Button(
            frame,
            text='Quit',
            command = self._quit_callback).pack(fill=X)

        self.__root = root

    def _help_callback(self):
        pass

    def _quit_callback(self):
        self.__root.quit()

    def _play_callback(self):
        self.__game = Game(Game.Human,Game.Human) #Game.Ai/Human/Client,Game.Ai/Human/Client in brackets CHANGE THIS LATER TO BE WHICHEVER IS DECIDED UPON
        self.__finished = False
        game_window = Toplevel(self.__root)
        game_window.title("Draughts Board")
        frame = Frame(game_window)
        frame.pack()
        self._frame = frame

        self.__buttons = [[None]*8 for _ in range(8)]
                                         
        for row,col in product(range(8),range(8)):
            b = StringVar()
            b.set(self.__game.at(row+1,col+1))
            
            cmd = lambda r=row, c=col: self.__check_poss_moves(r,c)
            
            Button(frame,textvariable=b,command=cmd).grid(row=row,column=col,sticky=N+S+W+E)
            self.__buttons[row][col] = b

    def __check_poss_moves(self, row, col):
        self.possiblerow = []
        self.possiblecol = []
        if self.__finished:
            return
        try:
            moves, takes = self.__game._get_legal_moves(row+1, col+1)
            for move in moves:
                if takes != 0:
                    if int(move[0]) == int(row - 2) or int(move[0]) == int(row + 2):
                        self.__game.print_possible_moves(move[0]+1,move[1]+1)
                else:
                    self.__game.print_possible_moves(move[0]+1,move[1]+1)
                self.possiblerow.append(move[0])
                self.possiblecol.append(move[1])
        except:
            pass

        for row, col in product(range(8),range(8)):
            text = self.__game.at(row+1,col+1)
            self.__buttons[row][col].set(text)

        
    
    def __make_move(self, row, col):
        if row not in self.possiblerow:
            return
        if col not in self.possiblecol:
            return
        self.__game._do_move(row+1, col+1)
        self.__game.remove_possible_moves()

        for row, col in product(range(8),range(8)):
            text = self.__game.at(row+1,col+1)
            self.__buttons[row][col].set(text)

    def run(self):
        self.__root.mainloop()


class Terminal(UI):
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