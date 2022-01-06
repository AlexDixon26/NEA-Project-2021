from Game import Game, GameError
from abc import ABC, abstractmethod
from tkinter import *
# END, Button, Tk, Toplevel, Frame, X, StringVar, Text,Scrollbar, LEFT, RIGHT, Y, Grid, N, S, W, E, Message, Label, Image, PhotoImage
from itertools import product
from Human import Human
from AI import AI
from random import randint as r

class UI(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError

class GUI(UI):
    def __init__(self):
        self.__started = False
        self.__finished = False
        root = Tk()
        root.title("Draughts")
        frame = Frame(root)
        frame.pack()
        self.__root = root
        self.login()
        self._WHITECOUNTER = PhotoImage(file="white counter.png")
        self._BLACKCOUNTER = PhotoImage(file="black counter.png")
        self._BLANKSQUARE = PhotoImage(file="blank square.png")
        self._WHITEKING = PhotoImage(file="white king.png")
        self._BLACKKING = PhotoImage(file="black king.png")
        self._POSSIBLEMOVE = PhotoImage(file="possible move.png")
        try:
            self._eventno = self._eventno
        except AttributeError:
            self._eventno = 1

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


        console = Text(frame,height=15,width=50)
        scroll = Scrollbar(frame)
        scroll.pack(side=RIGHT,fill=Y)
        console.pack(side=LEFT,fill=Y)
        
        scroll.config(command=console.yview)
        console.config(yscrollcommand=scroll.set)
        self.__console = console

    def _play_callback(self):
        if self.__started == False:
            return
        play_menu = Toplevel(self.__root)
        play_menu.title("Play Menu")
        frame = Frame(play_menu)
        frame.pack()

        Button(
            frame,
            text='Play Offline (Player vs Player)',
            command= self._play_offline).pack(fill=X)
        
        Button(
            frame,
            text='Play Offline (Player vs Computer)',
            command = self._play_computer).pack(fill=X)
        
        self._play_menu = play_menu

    def _play_computer(self):
        difficulty = ""
        self.play_computer = Toplevel(self.__root)
        self.play_computer.title("Choose Computer Difficulty")
        frame = Frame(self.play_computer)
        frame.pack()

        warning = StringVar()
        warning.set(f"Choose a Computer Difficulty")
        rulesLabel = Label(frame, textvariable=warning).pack()
    
        easy = lambda: [self.computer_versus("Easy")]
        hard = lambda: [self.computer_versus("Hard")]
        extreme = lambda: [self.computer_versus("Extreme")]
        
        Button(
            frame,
            text='Easy',
            command = easy).pack(fill=X)
        
        Button(
            frame,
            text='Hard',
            command = hard).pack(fill=X)
        
        Button(
            frame,
            text='Extreme',
            command = extreme).pack(fill=X)

    def computer_versus(self,difficulty):
        piece = r(1,2)
        piece = "Black" if piece == 1 else "White"
        #Create New Computer Opponent
        self._Computer = AI(difficulty,piece)
        self.play_computer.destroy()
        self._takes = []
        self.__console.delete("1.0", END)
        self.__playing_comp = True
        self.__game = Game()
        self.__finished = False
        self._computer_piece = "White" if piece == "Black" else "Black"
        self._print_board()
    
    def __make_ai_move(self):
        results = self.__game.check_all_legal_moves(self._computer_piece)
        movex, movey = self._Computer.get_move(results)

        if self.__game._player == Game.P1:
            self.__game._player = Game.P2
        else:
            self.__game._player = Game.P1


    def _join_game(self):
        pass

    def _create_game(self):
        pass

    def _help_callback(self):
        if self.__started == False:
            return
        help_instructions = Toplevel(self.__root)
        help_instructions.title("Rules")
        frame = Frame(help_instructions)
        frame.pack()

        rules = StringVar()
        rules.set(f"If you click on a peice and then change your mind, click on the same peice again to deselect it!")
        rulesLabel = Label(frame, textvariable=rules).pack()

    def _quit_callback(self):
        if self.__started:
            self.__root.quit()
        else:
            return

    def _play_offline(self):
        self._play_menu.destroy()
        self._takes = []
        self.__console.delete("1.0", END)
        self.__game = Game() #Game.Ai/Human/Client,Game.Ai/Human/Client in brackets CHANGE THIS LATER TO BE WHICHEVER IS DECIDED UPON
        self.__finished = False
        self._print_board()
    
    def _print_board(self):
        game_window = Toplevel(self.__root)
        game_window.title("Draughts Board")
        frame = Frame(game_window)
        frame.pack()
        self._frame = frame
        self.__buttons = [[None]*8 for _ in range(8)]  
        self._eventno = 1 
        self.__game_win = game_window                          
        for row, col in product(range(0,8), range(0,8)):
            img = self._text_to_image(row, col)
            cmd = lambda r=row, c=col: self.__event_handler(self._eventno, r, c)
        
            button = Button(frame,image=img,command=cmd)
            button.grid(row=row,column=col,sticky=N+S+W+E)
            self.__buttons[row][col] = button
        
        self._turn = StringVar()
        self._turn.set(f"Turn: {self.__game._player}")
        turnlabel = Label(frame, textvariable=self._turn).grid(row=9,column=1,columnspan=2,sticky=N+S+W+E)

        if self.__playing_comp == True and self.__game._player == self._computer_piece:
            self.__make_ai_move()

        #USE THIS FOR THE COMPUTER PLAYER
        
        #IF CUSTOM MAPS(UNLIKELY) THIS WILL BE NEEDED
        #takes = self.__game.check_for_takes()
        #if takes != []:
        #    self.__console.insert(END,"There are take[s] available", str(takes), "\n")


    def __event_handler(self, eventno, row, col):
        if self.__playing_comp == True and self.__game._player == self._computer_piece:
            return
        if self.__finished:
            return
        if eventno == 1:
            self._takes = []
            self._row_of_curr = row
            self._col_of_curr = col
            self._eventno = 2
            self.__check_poss_moves(row, col)
        elif eventno == 2:
            if self._row_of_curr == row and self._col_of_curr == col:
                self.__remove_poss()
                return
            self._eventno = 1
            self.__make_move(self._row_of_curr, self._col_of_curr, row, col)
            self._turn.set(f"Turn: {self.__game._player}")
            takes = self.__game.check_for_takes()
            if takes != []:
                self.__console.insert(END,"There are take[s] available", str(takes), "\n")
            self._takes = takes

    def __remove_poss(self):
        self.__game.remove_possible_moves()
        self._update_board()
        self._eventno = 1

    def __check_poss_moves(self, row, col):
        self.possiblerow = []
        self.possiblecol = []
        movelist = []
        succeed = False
        if self.__finished:
            return
        for move in self._takes:
            strmove = ""
            for num in move:
                strmove += str(num)
            movelist.append(strmove)
        for item in movelist:
            if row == int(item[0])-1 and col == int(item[1])-1:
                succeed = True
            
        if succeed == False and self._takes != []:
            self._eventno = 1
            self.__console.insert(END, "This peice cannot move, because there are takes available elsewhere\n")
            return

        try:
            moves, takes = self.__game._get_legal_moves(row+1, col+1, False)
        except GameError:
            self._eventno = 1
            self.__console.insert(END, "That's not your peice to move! Pick again\n")
            return
        for move in moves:
            if takes != 0:
                if int(move[0]) == int(row - 2) or int(move[0]) == int(row + 2):
                    self.__game.print_possible_moves(move[0]+1,move[1]+1)
            else:
                self.__game.print_possible_moves(move[0]+1,move[1]+1)
            self.possiblerow.append(move[0])
            self.possiblecol.append(move[1])
        #except:
            #pass

        self._update_board()

    def _text_to_image(self, row, col):
        b = self.__game.at(row,col)
        if b == "⚫ ":
            img = self._BLACKCOUNTER
        elif b == "⚪ ":
            img = self._WHITECOUNTER
        elif b == " ♔ ":
            img = self._BLACKKING
        elif b == " ♚ ":
            img = self._WHITEKING
        elif b == "🟢":
            img = self._POSSIBLEMOVE
        elif b == "   ":
            img = self._BLANKSQUARE
        else:
            GameError()
        return img

    def _update_board(self):
        for row, col in product(range(8),range(8)):
            img = self._text_to_image(row, col)
            self.__buttons[row][col].config(image=img)

    
    
    def __make_move(self, row, col, row_to_move, col_to_move):
        if row_to_move not in self.possiblerow:
            self._eventno = 2
            self.__console.insert(END, "Not able to move there\n")
            return
        if col_to_move not in self.possiblecol:
            self._eventno = 2
            self.__console.insert(END, "Not able to move there\n")
            return
        if row_to_move in [row-2,row+2]:
            take_used = True
        else:   
            take_used = False
        take = self.__game._do_move(row+1, col+1, row_to_move+1, col_to_move +1, take_used)


        if take != 0:
            if self.__game._player == Game.P1:
                self.__game._player = Game.P2
            else:
                self.__game._player = Game.P1
        
        self._update_board()
        if take != 0:
            self.__console.insert(END,"Another take is available\n")

        if self.__game._finished_game is not None:
            self.__finished = True
            self.__console.insert(END, f"The winner was {self.__game._finished_game}\n")
            self.__winner = self.__game._finished_game
            finished_game = Toplevel()
            finished_game.title("Game Finished")
            frame = Frame(finished_game)
            finished_text = f"Winner was: {self.__winner}"
            Message(finished_game,text=finished_text).pack(fill=X)
            Button(finished_game, text="Dismiss",command=finished_game.destroy).pack(fill=X)


    def run(self):
        self.__root.mainloop()

    def login(self):
        login = Toplevel(self.__root)
        login.title("Login/Signup")
        login.geometry("300x250")
        frame = Frame(login)
        frame.pack()
        Button(
            frame,
            text='Login',
            command= self._loginmenu).pack(fill=X)
        
        Button(
            frame,
            text='Sign up',
            command= self._signup).pack(fill=X)
        
        Button(
            frame,
            text='Continue as guest',
            command = self._continue_as_guest).pack(fill=X)

        self.__login = login
    
    def _loginmenu(self)    :
        login = Toplevel(self.__login)
        login.title("Login")
        login.geometry("300x250")

        #global username
        #global password
        #global username_entry
        #global password_entry
        username = StringVar()
        password = StringVar()

        Label(login, text="Please enter login details below").pack()
        Label(login, text="").pack()
        Label(login, text="Username:").pack()
        username_entry = Entry(login, textvariable = username)
        username_entry.pack()
        Label(login, text="Password:").pack()
        password_entry = Entry(login, textvariable = password, show = "*")
        password_entry.pack()
        Label(login, text="").pack()
        Button(login, text = "Login", width = 10, height = 1, command = self.login_user).pack()

    def login_user(self):
        
        pass

    def register_user(self):
        if self.__password_check != password.get():
            failure = Toplevel(self.__login)
            failure.title("Sign Up Failure")
            failure.geometry("300x300")
            Label(failure, text="Passwords do not match", fg = "red", font = ("Calibri")).pack()
            command = lambda: [failure.destroy(), self.__password_check == ""]
            Button(failure, command=command, text = "continue", width = 10, height = 1).pack()
            
        user_info = username.get()
        pass_info = password.get()
        file = open("C:/Users/alexa/Documents/NEA-Project-2021/userfiles/"+user_info, "w")
        file.write(str(user_info, pass_info))       
        file.close()    
        self._user = Human(user_info)
        self.__signup.destroy()
        success = Toplevel(self.__login)
        success.title("Sign Up Success")
        success.geometry("200x200")
        Label(success, text="Registration Success", fg = "green", font = ("Calibri")).pack()
        Button(success, command=self.__login.destroy, text = "continue", width = 10, height = 1).pack()
        self.__started = True

    def _signup(self):
        signup = Toplevel(self.__login)
        signup.title("Sign Up")
        signup.geometry("300x250")

        global username
        global password
        global username_entry
        global password_entry
        username = StringVar()
        password = StringVar()
        self.__password_check = ""
        Label(signup, text="Please enter sign up details below").pack()
        Label(signup, text="").pack()
        Label(signup, text="Username:").pack()
        username_entry = Entry(signup, textvariable = username)
        username_entry.pack()
        Label(signup, text="Password:").pack()
        password_entry = Entry(signup, textvariable = password)
        password_entry.pack()
        password_check = Entry(signup, textvariable = self.__password_check)
        password_check.pack()
        Label(signup, text="").pack()
        Button(signup, text = "Sign Up", width = 10, height = 1, command = self.register_user).pack()
            

        self.__signup = signup


    def _continue_as_guest(self):
        cont_guest = Toplevel(self.__login)
        cont_guest.title("Warning - Continuing as Guest")
        frame = Frame(cont_guest)
        frame.pack()

        warning = StringVar()
        warning.set(f"Are you sure you want to continue as a Guest? You can't save games as a Guest!")
        rulesLabel = Label(frame, textvariable=warning).pack()
        
        button_lambda = lambda: [cont_guest.destroy(),self.__login.destroy()]
        Button(
            frame,
            text='Continue as guest',
            command = button_lambda).pack(fill=X)

        self.__started = True


class Terminal(UI):
    def __init__(self):
        self._game = Game(Game.Human,Game.Human)


    def run(self):
        while not self._game._finished_game:
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
                    legal_moves, takes = self._game._get_legal_moves(row, col, False)
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
                        legal_moves, takes = self._game._get_legal_moves(row_to_move, col_to_move, False)
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
                            legal_moves, takes = self._game._get_legal_moves(row, col, False)
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