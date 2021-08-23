# For testing only: Based on: https://cs50.harvard.edu/ai/2020/notes/0/, https://github.com/wbsth/cs50ai/blob/master/week0/tictactoe/tictactoe.py
"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

class TicTacToe:
    def __init__(self, 
                 width=5, 
                 height=5,
                 agents=["blue", "red"],
                 agents_colors={"blue":"blue", "red":"red"},
                 max_num_step=100,
                 node_size=5):
        


        self.X = "X"
        self.O = "O"
        self.player_dict = {"X":"blue", "O":"red"}
        self.EMPTY = None

        self.reset()

    def initial(self):
        """
        Returns starting state of the board.
        """
        return [[self.EMPTY, self.EMPTY, self.EMPTY],
                [self.EMPTY, self.EMPTY, self.EMPTY],
                [self.EMPTY, self.EMPTY, self.EMPTY]]

    def reset(self):
        self.board = self.initial()
        return {"world": self.board, "turn": self.player()}



    def player(self):
        """
        Returns player who has the next turn on a board.
        """
        Xcount = 0
        Ocount = 0

        for row in self.board:
            Xcount += row.count(self.X)
            Ocount += row.count(self.O)

        if Xcount <= Ocount:
            return self.X
        else:
            return self.O


    def actions(self):
        """
        Returns set of all possible actions (i, j) available on the board.
        """

        possible_moves = set()

        for row_index, row in enumerate(self.board):
            for column_index, item in enumerate(row):
                if item == None:
                    possible_moves.add((row_index, column_index))
        
        return possible_moves


    def result(self, action):
        """
        Returns the board that results from making move (i, j) on the board.
        """
        player_move = self.player()

        new_board = deepcopy(self.board)
        i, j = action

        if self.board[i][j] != None:
            raise Exception
        else:
            new_board[i][j] = player_move

        return new_board

    def get_done(self):
        return self.terminal()

    def get_turn(self):
        return self.player_dict[self.player()]

    def get_possible_actions(self):
        return self.actions()

    def get_scores(self):
        return {"blue":self.utility(), "red":0}

    def winner(self):
        """
        Returns the winner of the game, if there is one.
        """
        for player in (self.X, self.O):
            # check vertical
                for row in self.board:
                    if row == [player] * 3:
                        return player

            # check horizontal
                for i in range(3):
                    column = [self.board[x][i] for x in range(3)]
                    if column == [player] * 3:
                        return player
            
            # check diagonal
                if [self.board[i][i] for i in range(0, 3)] == [player] * 3:
                    return player

                elif [self.board[i][~i] for i in range(0, 3)] == [player] * 3:
                    return player
        return None
                               

    def terminal(self):
        """
        Returns True if game is over, False otherwise.
        """
        # game is won by one of the players
        if self.winner() != None:
            return True

        # moves still possible
        for row in self.board:
            if self.EMPTY in row:
                return False

        # no possible moves
        return True


    def utility(self):
        """
        Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
        """

        win_player = self.winner()

        if win_player == self.X:
            return 1
        elif win_player == self.O:
            return -1
        else:
            return 0

    def action_intrep(self, action):
        return action[list(action.keys())[0]][0]
    def step(self, action):
        self.board = self.result(self.action_intrep(action))
        return {"world": self.board, "turn": self.player()}, self.utility, self.terminal(), {"error": ''}

    def render(self, timeout=0):
        print(self.board)

    # def minimax(board):
    #     """
    #     Returns the optimal action for the current player on the board.
    #     """

    #     def max_value(board):
    #         optimal_move = ()
    #         if terminal(board):
    #             return utility(board), optimal_move
    #         else:
    #             v = -5
    #             for action in actions(board):
    #                 minval = min_value(result(board, action))[0]
    #                 if minval > v:
    #                     v = minval
    #                     optimal_move = action
    #             return v, optimal_move

    #     def min_value(board):
    #         optimal_move = ()
    #         if terminal(board):
    #             return utility(board), optimal_move
    #         else:
    #             v = 5
    #             for action in actions(board):
    #                 maxval = max_value(result(board, action))[0]
    #                 if maxval < v:
    #                     v = maxval
    #                     optimal_move = action
    #             return v, optimal_move

    #     curr_player = player(board)

    #     if terminal(board):
    #         return None

    #     if curr_player == X:
    #         return max_value(board)[1]

    #     else:
    #         return min_value(board)[1]
