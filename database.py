import os
import sqlite3

class PlayerDatabase:
    def __init__(self):

        #######################################################################
        #                                                                     #
        #                       (B2) Non - Parameterised SQL                  #
        #                                                                     #
        #######################################################################

        self._con = sqlite3.connect("players.db")
        self._cursor = self._con.cursor()
        self._cursor.execute("CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY, username text, userpass text)")   
        self._con.commit()

    def create_user(self, username, password):
        usernam = (username,)
        self._cursor.execute(f"SELECT username FROM users WHERE username = (?) ",usernam)
        names = self._cursor.fetchall()
        if names != []:
            return False
        user = (str(username),str(password),)
        self._cursor.execute("INSERT INTO users(username, userpass) VALUES(?,?)", user)
        self._con.commit()
        return True

    def read_Data(self):
        self._cursor.execute("SELECT username,userpass FROM users")
        results = self._cursor.fetchall()
        return results

    def find_user(self, username, password):
        found = False
        results = self.read_Data()
        for result in results:
            if result[0] == username and result[1] == password:
                found = True
                return found
        return found

class GamesDatabase:
    def __init__(self):
        self._con = sqlite3.connect("games.db")
        self._cursor = self._con.cursor()
        self._cursor.execute("CREATE TABLE IF NOT EXISTS games(id integer PRIMARY KEY, username text, board text, computer boolean, player text, difficulty text)")   
        self._con.commit()

    def read_Data(self):
        self._cursor.execute("SELECT * FROM games")
        results = self._cursor.fetchall()
        return results

    def save_game(self, username, board, comp, player, difficulty):
        self._cursor.execute("SELECT username FROM games WHERE username = (?) ",(username,))
        names = self._cursor.fetchall()
        if names != []:
            self._cursor.execute("DELETE FROM games WHERE username = (?)", (username,))
            self._con.commit()
        self._cursor.execute("INSERT INTO games(username, board, computer, player, difficulty) VALUES (?,?,?,?,?)",[username,board,comp,player,difficulty,])
        self._con.commit()

    def check_for_saved_game(self, username):
        self._cursor.execute("SELECT * FROM games WHERE username = (?) ",(username,))
        names = self._cursor.fetchall()
        if names != []:
            return True
        return False

    def load_game(self, username):
        self._cursor.execute("SELECT * FROM games WHERE username = (?) ",(username,))
        names = self._cursor.fetchall()
        return names
