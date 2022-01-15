from Game import Game, GameError
from abc import ABC, abstractmethod
from tkinter import *
from itertools import product
from AI import AI
from random import randint as r
from database import PlayerDatabase,GamesDatabase


#Super Class to GUI
class UI(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError

class GUI(UI):
    def __init__(self):
        #Initialising the databases
        self.playersDB = PlayerDatabase()
        self.gamesDB = GamesDatabase()
        #Initialising the GUI
        self._inprogress = False
        self.__playing_comp = False
        self.__started = False
        self.__finished = False
        #Making the main window of my GUI
        root = Tk()
        root.title("Draughts")
        frame = Frame(root)
        frame.pack()
        self.__root = root
        self.login()
        #Importing the images for the pieces used in the game
        self._WHITECOUNTER = PhotoImage(file="images/white counter.png")
        self._BLACKCOUNTER = PhotoImage(file="images/black counter.png")
        self._BLANKSQUARE = PhotoImage(file="images/blank square.png")
        self._WHITEKING = PhotoImage(file="images/white king.png")
        self._BLACKKING = PhotoImage(file="images/black king.png")
        self._POSSIBLEMOVE = PhotoImage(file="images/possible move.png")
        #Try/Except to set the current Event Number to 1 unless it has already been defined
        try:
            self._eventno = self._eventno
        except AttributeError:
            self._eventno = 1

        #Buttons for the main window
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

        #Defining the console
        console = Text(frame,height=15,width=50)
        scroll = Scrollbar(frame)
        scroll.pack(side=RIGHT,fill=Y)
        console.pack(side=LEFT,fill=Y)
        
        scroll.config(command=console.yview)
        console.config(yscrollcommand=scroll.set)
        self.__console = console

    def load_saved_game(self):
        load_saved_game = True

    def _play_callback(self):
        #Window for user to input gamemode

        #if a game has already begun, do not open this window
        if self.__started == False:
            return
        
        if self.load_saved_game:
            game = self.gamesDB.load_game(self.__user)
            print(game)
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
        #Window for playing against the computer

        #if a game is in progress, do not open this window
        if self._inprogress:
            return
        self._inprogress = True
        difficulty = ""
        self.play_computer = Toplevel(self.__root)
        self.play_computer.title("Choose Computer Difficulty")
        frame = Frame(self.play_computer)
        frame.pack()

        #Choosing a computer difficulty
        warning = StringVar()
        warning.set(f"Choose a Computer Difficulty")
        rulesLabel = Label(frame, textvariable=warning).pack()
    

        #Using a lambda to set the difficulty
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
        #Function that prints the board to play against the computer
        self.play_computer.destroy()
        self._takes = []

        #Empties the console
        self.__console.delete("1.0", END)
        self.__playing_comp = True

        #Creates a new game
        self.__game = Game()

        #Creates a new computer opponent
        self._Computer = AI(difficulty, self.__game)
        self.__finished = False
        self._computer_piece = "White"
        self._print_board()
    
    def __make_ai_move(self):
        #function to make the computer player move
        results = 0
        takes = 0
        play = lambda: [results, takes == self.__game.find_white_player_available_moves(self.__game._board)]
        self.__game_win.after(500, play)
        move = self._Computer.get_move(results, self.__game._board)

        old_x = move[0]
        old_y = move[1]
        new_x = move[2]
        new_y = move[3]

        self.__make_move(old_x,old_y,new_x,new_y)

        #Updating the board
        self._update_board()
        self._turn.set(f"Turn: {self.__game._player}")

    def _help_callback(self):
        #Main window for the rules and help class
        help_instructions = Toplevel(self.__root)
        help_instructions.title("Rules")
        frame = Frame(help_instructions)
        frame.pack()

        rules = StringVar()
        rules.set(f"If you click on a peice and then change your mind, click on the same peice again to deselect it!")
        rulesLabel = Label(frame, textvariable=rules).pack()

    def _quit_callback(self):
        #Quits the main program
        if self.__started:
            self.__root.quit()
        else:
            return

    def _play_offline(self):
        #Function for printing the board when playing player versus player
        if self._inprogress:
            return
        self._inprogress = True
        self._play_menu.destroy()
        self._takes = []
        self.__console.delete("1.0", END)
        #creates a new game class
        self.__game = Game()
        self.__finished = False
        self._print_board()
    
    def _print_board(self):
        #Function to print the board
        game_window = Toplevel(self.__root)
        game_window.title("Draughts Board")
        frame = Frame(game_window)
        frame.pack()
        self._frame = frame
        self.__buttons = [[None]*8 for _ in range(8)]  
        self._eventno = 1 
        self.__game_win = game_window
        game_window.protocol("WM_DELETE_WINDOW", self._quit_from_game)

        #Menu 
        menubar = Menu(game_window)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self._quit_from_game)
        menubar.add_cascade(label="Menu", menu=filemenu)    
        game_window.config(menu=menubar)

        #printing the board
        for row, col in product(range(0,8), range(0,8)):
            img = self._text_to_image(row, col)
            cmd = lambda r=row, c=col: self.__event_handler(self._eventno, r, c)
        
            button = Button(frame,image=img,command=cmd)
            button.grid(row=row,column=col,sticky=N+S+W+E)
            self.__buttons[row][col] = button

        self._turn = StringVar()
        self._turn.set(f"Turn: {self.__game._player}")
        turnlabel = Label(frame, textvariable=self._turn).grid(row=9,column=1,columnspan=2,sticky=N+S+W+E)

        #If it is the AI's turn, then call the function to make the ai move
        if self.__playing_comp == True and self.__game._player == self._computer_piece:
                self.__make_ai_move()

    def _quit_from_game(self):
        #Quiting the game/Saving
        quit_instructions = Toplevel(self.__root)
        quit_instructions.title("Quit the game?")
        frame = Frame(quit_instructions)
        frame.pack()

        warning = StringVar()
        warning.set(f"Do you wish to quit the game?") #Save the game function here
        Label(frame, textvariable=warning).pack()

    def __event_handler(self, eventno, row, col):
        #Algorithm to determine whether the user has just clicked on a piece to check if it is to be moved or whether the user has clicked on a place to move to it
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
            takes = []
            takes = self.__game.check_for_takes()
            if takes != []:
                self.__console.insert(END,"There are take[s] available", str(takes), "\n")
            self._takes = takes

    def __remove_poss(self):
        #removes the possible moves from the board
        self.__game.remove_possible_moves()

        #updates the board
        self._update_board()
        self._eventno = 1

    def __check_poss_moves(self, row, col):
        #Checks whether the user has picked a piece that is theirs to move, using algorithms from game class
        self.possiblerow = []
        self.possiblecol = []
        movelist = []
        succeed = False
        if self.__finished:
            return
        # Creates a list of all possible moves
        for move in self._takes:
            strmove = ""
            for num in move:
                strmove += str(num)
            movelist.append(strmove)
        for item in movelist:
            if row == int(item[0])-1 and col == int(item[1])-1:
                succeed = True
            
        #checks if the piece is able to move
        if succeed == False and self._takes != []:
            self._eventno = 1
            self.__console.insert(END, "This peice cannot move, because there are takes available elsewhere\n")
            return

        #Uses game classes to calculate possible moves for the piece to make
        try:
            if self.__game._player == Game.P1:
                moves, takes = self.__game.find_black_piece_moves(row,col,self.__game._board)
            else:
                moves, takes = self.__game.find_white_piece_moves(row,col,self.__game._board)
        except GameError:
            self._eventno = 1
            self.__console.insert(END, "That's not your peice to move! Pick again\n")
            return

        #list of possible moves
        if len(self.__game.check_for_takes()) != 0:
            list = takes
        else:
            list = moves
        
        if list == []:
            self._eventno = 1

        #adds the move to a list of possible moves that the do move function uses
        for move in list:
            self.__game.print_possible_moves(move[2]+1,move[3]+1)
            self.possiblerow.append(move[2])
            self.possiblecol.append(move[3])
        self._update_board()

    def _text_to_image(self, row, col):
        #changes each character piece in the board to an image 
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
        #updates the board
        for row, col in product(range(8),range(8)):
            img = self._text_to_image(row, col)
            self.__buttons[row][col].config(image=img)

    
    
    def __make_move(self, row, col, row_to_move, col_to_move):
        #function to make a move
        if self.__playing_comp == True and self.__game._player == self._computer_piece:
            self._eventno = self._eventno
        else:
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
        try:
            take = self.__game.do_move(row+1, col+1, row_to_move+1, col_to_move +1, take_used, self.__game._board, self.__game._player)
        except GameError:
            self.play_computer = Toplevel(self.__root)
            self.play_computer.title("ERROR: Not a Viable move")
            frame = Frame(self.play_computer)
            frame.pack()
            warning = StringVar()
            warning.set(f"That's not a legal move/not a legal piece to move!")
            rulesLabel = Label(frame, textvariable=warning).pack()
            take = [1]
            self._eventno = 1
            self.__game.remove_possible_moves()
        if take in [[],0]:
            if self.__game._player == Game.P1:
                self.__game._player = Game.P2
            else:
                self.__game._player = Game.P1
        


        self._update_board()



        if take != 0:
            self.__console.insert(END,"Another take is available\n")

        #checks if game won
        if self.__game.finished_game is not None:
            self.__finished = True
            self.__console.insert(END, f"The winner was {self.__game.finished_game}\n")
            self.__winner = self.__game.finished_game
            finished_game = Toplevel()
            finished_game.title("Game Finished")
            frame = Frame(finished_game)
            finished_text = f"Winner was: {self.__winner}"
            Message(finished_game,text=finished_text).pack(fill=X)
            Button(finished_game, text="Dismiss",command=finished_game.destroy).pack(fill=X)
            self.__game_win.destroy()

        if self.__playing_comp == True and self.__game._player == self._computer_piece:
                self.__make_ai_move()


    def run(self):
        #Run the main game
        self.__root.mainloop()

    def login(self):
        #Login TopLevel
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
    
    def _loginmenu(self):
        #Menu to log in
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
        self.username_entry = Entry(login, textvariable = username)
        self.username_entry.pack()
        Label(login, text="Password:").pack()
        self.password_entry = Entry(login, textvariable = password, show = "*")
        self.password_entry.pack()
        Label(login, text="").pack()
        Button(login, text = "Login", width = 10, height = 1, command = self.login_user).pack()
        self._login = login

    def login_user(self):
        #Searches the login database for the users credentials, if found logs them in if not allows user to login again
        loginfail = Toplevel(self._login)
        loginfail.title("Login Failed")
        loginfail.geometry("100x50")
        found = self.playersDB.find_user(self.username_entry.get(),self.password_entry.get())
        if found == False:
            Label(loginfail, text="That username does not exist in our database!", fg = "red", font = ("Calibri")).pack()
            signup = lambda: [self._login.destroy(),loginfail.destroy(),self._signup()]
            Button(loginfail, command=signup, text = "signup", width = 10, height = 1).pack()
        self.__user = self.username_entry.get()
        self.__started = True
        self.__login.destroy()


        if self.gamesDB.check_for_saved_game():
            save = Toplevel(self.__root)
            save.title("Saved Game")
            frame = Frame(save)
            frame.pack()
            warning = StringVar()
            warning.set(f"Do you want to load your saved game? If not just close this window")
            Label(frame, textvariable=warning).pack()
            com = lambda: [self.load_saved_game,save.destroy()]
            Button(
                frame,
                text='Yes',
                command= com).pack(fill=X)


    def _signup(self):
        #Sign Up menu, where player inputs new username/password
        signup = Toplevel(self.__login)
        signup.title("Sign Up")
        signup.geometry("300x250")

        username = StringVar()
        password = StringVar()
        password_check = StringVar()
        Label(signup, text="Please enter sign up details below").pack()
        Label(signup, text="").pack()
        Label(signup, text="Username:").pack()
        self.username_entry = Entry(signup, textvariable = username)
        self.username_entry.pack()
        Label(signup, text="Password:").pack()
        self.password_entry = Entry(signup, textvariable = password, show = "*")
        self.password_entry.pack()
        Label(signup, text="Re-enter Password:").pack()
        self.password_check = Entry(signup, textvariable = password_check, show = "*")
        self.password_check.pack()
        Label(signup, text="").pack()
        Button(signup, text = "Sign Up", width = 10, height = 1, command = self.register_user).pack()
            
        self.__signup = signup

    def register_user(self):
        #Registers the user
        if self.password_check.get() != self.password_entry.get():
            failure = Toplevel(self.__login)
            failure.title("Sign Up Failure")
            failure.geometry("300x300")
            Label(failure, text="Passwords do not match", fg = "red", font = ("Calibri")).pack()
            command = lambda: [failure.destroy()]
            Button(failure, command=command, text = "continue", width = 10, height = 1).pack()
            return  
        user_info = self.username_entry.get()
        user_info = user_info.strip("(')")
        pass_info = self.password_entry.get()
        pass_info = pass_info.strip("(')")
        created = self.playersDB.create_user(user_info,pass_info)
        if not created:
            fail = Toplevel(self.__login)
            fail.title("Sign Up Failure")
            fail.geometry("200x200")
            Label(fail, text="That Username is already in use!", fg = "green", font = ("Calibri")).pack()
        self.__signup.destroy()
        if created:
            success = Toplevel(self.__login)
            success.title("Sign Up Success")
            success.geometry("200x200")
            Label(success, text="Registration Success", fg = "green", font = ("Calibri")).pack()
            Button(success, command=self.__login.destroy, text = "continue", width = 10, height = 1).pack()
            self.__user = self.username_entry.get()
            self.__started = True

    def _continue_as_guest(self):
        #If the player does not wish to log in, they can continue as a guest
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