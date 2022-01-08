from Player import Player
from random import randint
from copy import deepcopy
from Game import Game

class AI(Player):
    P1Man = "⚫ "
    P2Man = "⚪ "
    P1King = " ♔ "
    P2King = " ♚ "
    _EMPTY = "   "


    def __init__(self, difficulty):
        self._difficulty = difficulty
        self.__piece = [AI.P2Man,AI.P2King]
        self.__colour = "White"

    def get_move(self, movelist, takes):
        if self._difficulty == "Easy":
            r = randint(0,len(movelist)-1)
            return movelist[r]
        elif self._difficulty == "Hard":
            pass
        elif self._difficulty == "Extreme":
            pass

    def calculate_board_worth(self, board):
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

    def evaluate_states(self):
        current_state = Node(deepcopy(Game._board))

        first_computer_moves = current_state.get_children(True)
        dict = {}
        for i in range(len(first_computer_moves)):
            child = first_computer_moves[i]
            # minimax algorithm here
            dict[value] = child
        new_board = dict[max(dict)].get_board()
        move = dict[max(dict)].get_move()
        return move



class Node:
    def __init__(self, board, move, parent, value):
        self.board = board
        self.value = value
        self.move = move
        self.parent = parent

    def get_children(self, min_player):
        current_state = deepcopy(self.board)
        available_moves = []
        children_states = []
        if min_player == True:
            available_moves, takes = Game.find_white_player_available_moves(current_state)
            player = "White"
        else:
            available_moves, takes = Game.find_black_player_available_moves(current_state)
            player = "Black"
        for i in range(len(available_moves)):
            old_i = available_moves[i][0]
            old_j = available_moves[i][1]
            new_i = available_moves[i][2]
            new_j = available_moves[i][3]
            board_state = deepcopy(current_state)
            Game._do_move(old_i+1,old_j+1,new_i+1,new_j+1,takes,board_state,player)
            children_states.append(Node(board_state, [old_i, old_j, new_i, new_j]))
        return children_states
    
    def get_board(self):
        return self.board

    def get_move(self):
        return self.move