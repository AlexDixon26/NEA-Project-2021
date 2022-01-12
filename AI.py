from Player import Player
from random import randint
from copy import deepcopy
from Game import Game
import math

class AI(Player):
    P1Man = "⚫ "
    P2Man = "⚪ "
    P1King = " ♔ "
    P2King = " ♚ "
    _EMPTY = "   "
    inf = math.inf


    def __init__(self, difficulty, game):
        #initialising a new AI class
        self._difficulty = difficulty
        self.__piece = [AI.P2Man,AI.P2King]
        self.__colour = "White"
        self.__game = game

    def get_move(self, movelist, board):
        #Depending upon the difficulty, returns a move using either randomisation or evaluating it using minimax
        if self._difficulty == "Easy":
            r = randint(0,len(movelist)-1)
            return movelist[r]
        elif self._difficulty == "Hard":
            move = self.evaluate_states(3, board)
            return move
        elif self._difficulty == "Extreme":
            move = self.evaluate_states(5, board)
            return move

    def calculate_board_worth(self, board):
        #evaluates the cost of the board
        man = AI.P2Man
        opp_man = AI.P1Man
        king = AI.P2King
        opp_king = AI.P1King
        result = 0
        mine = 0
        opp = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == man or board[i][j] == king:
                    mine += 1

                    if board[i][j] == man: #if piece is computers
                        result += 5
                    if board[i][j] == king: #if piece is computers
                        result += 10
                    if i == 0 or j == 0 or i == 7 or j == 7: #if the piece is on the edge of the board so cannot be taken
                        result += 7
                    if i + 1 > 7 or j - 1 < 0 or i - 1 < 0 or j + 1 > 7: #skip next checks if piece cannot take/be taken
                        continue
                    if (board[i + 1][j - 1] == opp_man or board[i + 1][j - 1] == opp_king) and board[i - 1][
                        j + 1] == AI._EMPTY: #if the piece can be taken
                        result -= 3
                    if (board[i + 1][j + 1] == opp_man or board[i + 1][j + 1] == opp_king) and board[i - 1][j - 1] == AI._EMPTY: #if the piece can be taken
                        result -= 3
                    if board[i - 1][j - 1] == opp_king and board[i + 1][j + 1] == AI._EMPTY: #if king can take piece
                        result -= 3

                    if board[i - 1][j + 1] == opp_king and board[i + 1][j - 1] == AI._EMPTY: #if king can take piece
                        result -= 3
                    if i + 2 > 7 or i - 2 < 0: # skip next steps if piece cannot take
                        continue
                    if (board[i + 1][j - 1] == opp_king or board[i + 1][j - 1] == opp_man) and board[i + 2][
                        j - 2] == AI._EMPTY: #if a piece can be taken by current piece
                        result += 6
                    if i + 2 > 7 or j + 2 > 7: #skip next steps if piece cannot take
                        continue
                    if (board[i + 1][j + 1] == opp_king or board[i + 1][j + 1] == opp_man) and board[i + 2][
                        j + 2] == AI._EMPTY: #if a piece can be taken by current piece
                        result += 6

                elif board[i][j] == opp_man or board[i][j] == opp_king:
                    opp += 1

        return result + (mine - opp) * 1000

    def evaluate_states(self, complexity, board):
        # user-defined algorithm to calculate the best possible move
        
        #The current board is used as a starter for a new Node class (deepcopy is used due to bugs found during testing)
        current_state = Node(deepcopy(board))

        #finds all the possible computer moves for the current board
        first_computer_moves = current_state.get_children(True)
        dict = {}
        for i in range(len(first_computer_moves)):
            child = first_computer_moves[i]
            #each board is used and minimaxed to calculate the best possible outcome
            value = self.minimax(child.get_board(), complexity, -AI.inf, AI.inf, False)
            dict[value] = child 
        #The maximum score move is returned as the best possible move to make
        move = dict[max(dict)].move
        return move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        #minimax algorithm to calculate the best possible move for the player to make

        #if the minimax is to go no further, it returns the board worth for the current board
        if depth == 0:
            return self.calculate_board_worth(board)
        current_state = Node(deepcopy(board))

        #if the current player is the one the minimax should be maximising the score of
        if maximizing_player is True:
            max_eval = -AI.inf
            #iterates through the children in the current board state
            for child in current_state.get_children(True):
                #recursively calls itself on the child's board state, using a depth one less than the previous depth
                ev = self.minimax(child.get_board(), depth - 1, alpha, beta, False)
                #maximum evaluation is set to be max_eval
                max_eval = max(max_eval, ev)

                #if a board class gets too large, the algorithm cuts out of the for loop
                alpha = max(alpha, ev)
                if beta <= alpha:
                    break
            
            #sets the value of the current board as the highest score possible
            current_state.set_value(max_eval)
            return max_eval
        else:
            #otherwise, tries to minimise the score of the opponent
            min_eval = AI.inf
            for child in current_state.get_children(False):
                ev = self.minimax(child.get_board(), depth - 1, alpha, beta, True)
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha:
                    break
            current_state.set_value(min_eval)
            return min_eval



class Node:
    #Node class for graph of best possible moves
    def __init__(self, board, move=None, parent=None, value=None):
        self.board = board
        self.value = value
        self.move = move
        self.parent = parent

    def get_children(self, min_player):
        #uses game functions to calculate all possible moves that a player can make on the current board
        current_state = deepcopy(self.board)
        available_moves = []
        children_states = []
        #calculate the moves
        if min_player == True:
            available_moves, takes = find_white_player_available_moves(current_state)
            king = Game.P2King
            king_row = 7
        else:
            available_moves, takes = find_black_player_available_moves(current_state)
            king = Game.P1King
            king_row = 0
        #for each move, performs the move on a copy of the current board and creates a new Node which is set as a child state for the current state
        for i in range(len(available_moves)):
            old_x = available_moves[i][0]
            old_y = available_moves[i][1]
            new_x = available_moves[i][2]
            new_y = available_moves[i][3]
            board_state = deepcopy(current_state)
            make_a_move(board_state, old_x, old_y, new_x, new_y, king, king_row)
            children_states.append(Node(board_state, [old_x, old_y, new_x, new_y]))
        return children_states
    

    #3 functions to return certain variables/set certain variables
    def get_board(self):
        return self.board

    def get_move(self):
        return self.move

    def set_value(self, value):
        self.value = value


#######################################################################
#                                                                     #
#    Re-paste of game code (necessary due to circular import issues)  #
#                                                                     #
#######################################################################

def find_white_piece_moves(m, n, board):
        available_moves = []
        available_takes = []
        if board[m][n] == Game.P2Man:
                    if _check_white_player_moves(m, n, m + 1, n + 1, board):
                        available_moves.append([m, n, m + 1, n + 1])
                    if _check_white_player_moves(m, n, m + 1, n - 1, board):
                        available_moves.append([m, n, m + 1, n - 1])
                    if _check_white_player_takes(m, n, m + 1, n - 1, m + 2, n - 2, board):
                        available_takes.append([m, n, m + 2, n - 2])
                    if _check_white_player_takes(m, n, m + 1, n + 1, m + 2, n + 2, board):
                        available_takes.append([m, n, m + 2, n + 2])
        elif board[m][n] == Game.P2King:
                    if _check_white_player_moves(m, n, m + 1, n + 1, board):
                        available_moves.append([m, n, m + 1, n + 1])
                    if _check_white_player_moves(m, n, m + 1, n - 1, board):
                        available_moves.append([m, n, m + 1, n - 1])
                    if _check_white_player_moves(m, n, m - 1, n - 1, board):
                        available_moves.append([m, n, m - 1, n - 1])
                    if _check_white_player_moves(m, n, m - 1, n + 1, board):
                        available_moves.append([m, n, m - 1, n + 1])
                    if _check_white_player_takes(m, n, m + 1, n - 1, m + 2, n - 2, board):
                        available_takes.append([m, n, m + 2, n - 2])
                    if _check_white_player_takes(m, n, m - 1, n - 1, m - 2, n - 2, board):
                        available_takes.append([m, n, m - 2, n - 2])
                    if _check_white_player_takes(m, n, m - 1, n + 1, m - 2, n + 2, board):
                        available_takes.append([m, n, m - 2, n + 2])
                    if _check_white_player_takes(m, n, m + 1, n + 1, m + 2, n + 2, board):
                        available_takes.append([m, n, m + 2, n + 2])

        return available_moves, available_takes

def find_black_piece_moves(m, n, board):
        available_moves = []
        available_takes = []
        if board[m][n] == Game.P1Man:
                    if _check_black_player_moves(m, n, m - 1, n - 1, board):
                        available_moves.append([m, n, m - 1, n - 1])
                    if _check_black_player_moves(m, n, m - 1, n + 1, board):
                        available_moves.append([m, n, m - 1, n + 1])
                    if _check_black_player_takes(m, n, m - 1, n - 1, m - 2, n - 2, board):
                        available_takes.append([m, n, m - 2, n - 2])
                    if _check_black_player_takes(m, n, m - 1, n + 1, m - 2, n + 2, board):
                        available_takes.append([m, n, m - 2, n + 2])
        elif board[m][n] == Game.P1King:
                    if _check_black_player_moves(m, n, m - 1, n - 1, board):
                        available_moves.append([m, n, m - 1, n - 1])
                    if _check_black_player_moves(m, n, m - 1, n + 1, board):
                        available_moves.append([m, n, m - 1, n + 1])
                    if _check_black_player_takes(m, n, m - 1, n - 1, m - 2, n - 2, board):
                        available_takes.append([m, n, m - 2, n - 2])
                    if _check_black_player_takes(m, n, m - 1, n + 1, m - 2, n + 2, board):
                        available_takes.append([m, n, m - 2, n + 2])
                    if _check_black_player_moves(m, n, m + 1, n - 1, board):
                        available_moves.append([m, n, m + 1, n - 1])
                    if _check_black_player_takes(m, n, m + 1, n - 1, m + 2, n - 2, board):
                        available_takes.append([m, n, m + 2, n - 2])
                    if _check_black_player_moves(m, n, m + 1, n + 1, board):
                        available_moves.append([m, n, m + 1, n + 1])
                    if _check_black_player_takes(m, n, m + 1, n + 1, m + 2, n + 2, board):
                        available_takes.append([m, n, m + 2, n + 2])

        return available_moves, available_takes
        
def find_white_player_available_moves(board):
        available_moves = []
        available_takes = []
        for m in range(8):
            for n in range(8):
                moves, takes = find_white_piece_moves(m,n,board)
                for item in moves:
                    available_moves.append(item)
                for item in takes:
                    available_takes.append(item)

        if len(available_takes) != 0:
            return available_takes, True
        else:
            return available_moves, False

        
def find_black_player_available_moves(board):
        available_moves = []
        available_takes = []
        for m in range(8):
            for n in range(8):
                moves, takes = find_black_piece_moves(m,n,board)
                for item in moves:
                    available_moves.append(item)
                for item in takes:
                    available_takes.append(item)
        if len(available_takes) != 0:
            return available_takes, True
        else:
            return available_moves, False

def _check_black_player_moves(old_x, old_y, new_x, new_y, board):
        possible = [Game.P1King,Game.P1Man] 
        if new_x > 7 or new_x < 0:
            return False
        if new_y > 7 or new_y < 0:
            return False
        if board[old_x][old_y] == Game._EMPTY:
            return False
        if board[new_x][new_y] != Game._EMPTY:
            return False
        if board[old_x][old_y] not in possible:
            return False
        if board[new_x][new_y] == Game._EMPTY:
            return True

def _check_white_player_moves(old_x, old_y, new_x, new_y, board):
        possible = [Game.P2King,Game.P2Man] 
        if new_x > 7 or new_x < 0:
            return False
        if new_y > 7 or new_y < 0:
            return False
        if board[old_x][old_y] == Game._EMPTY:
            return False
        if board[new_x][new_y] != Game._EMPTY:
            return False
        if board[old_x][old_y] not in possible:
            return False
        if board[new_x][new_y] == Game._EMPTY:
            return True

def _check_black_player_takes(old_x, old_y, via_x, via_y, new_x, new_y, board):
        possible = [Game.P1King,Game.P1Man] 
        if new_x > 7 or new_x < 0:
            return False
        if new_y > 7 or new_y < 0:
            return False
        if board[via_x][via_y] == Game._EMPTY:
            return False
        if board[via_x][via_y] in possible:
            return False
        if board[new_x][new_y] != Game._EMPTY:
            return False
        if board[old_x][old_y] == Game._EMPTY:
            return False
        if board[old_x][old_y] not in possible:
            return False
        return True

def _check_white_player_takes(old_x, old_y, via_x, via_y, new_x, new_y, board):
        possible = [Game.P2King,Game.P2Man] 
        if new_x > 7 or new_x < 0:
            return False
        if new_y > 7 or new_y < 0:
            return False
        if board[via_x][via_y] == Game._EMPTY:
            return False
        if board[via_x][via_y] in possible:
            return False
        if board[new_x][new_y] != Game._EMPTY:
            return False
        if board[old_x][old_y] == Game._EMPTY:
            return False
        if board[old_x][old_y] not in possible:
            return False
        return True

def make_a_move(board, old_x, old_y, new_x, new_y, king, king_row):
        letter = board[old_x][old_y]
        x_diff = old_x - new_x
        y_diff = old_y - new_y
        if x_diff == -2 and y_diff == 2:
            board[old_x + 1][old_y - 1] = Game._EMPTY

        elif x_diff == 2 and y_diff == 2:
            board[old_x - 1][old_y - 1] = Game._EMPTY

        elif x_diff == 2 and y_diff == -2:
            board[old_x - 1][old_y + 1] = Game._EMPTY

        elif x_diff == -2 and y_diff == -2:
            board[old_x + 1][old_y + 1] = Game._EMPTY

        if new_x == king_row:
            letter = king
        board[old_x][old_y] = Game._EMPTY
        board[new_x][new_y] = letter