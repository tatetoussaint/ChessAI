"""
Date: 10/10/21
Author: Tate Toussaint
Description: Minimax AI
"""

import chess
import math


class MinimaxAI:
    def __init__(self, depth, color):
        self.depth = depth   # decremented until reaches depth limit of 0
        self.color = color   # color of the player (true is white, false is black)
        self.opponent_color = not color
        self.min_max_calls = 0   # keeps track of calls to min and max each iteration

    # goes through options at given depth and returns best move
    def choose_move(self, board):
        self.min_max_calls = 0  # resetting min/max calls before move decision process
        move = self.minimax_decision(board)
        print("Minimax AI recommending move " + str(move) + " | depth = " + str(self.depth) +
              " | min/max calls = " + str(self.min_max_calls))
        return move

    # checks if the game is over or depth is over
    def cutoff_test(self, board):
        if self.depth == 0 or board.is_game_over():   # if at depth limit or no legal moves
            return True
        return False

    # take the min value of each move and return the highest scoring move
    def minimax_decision(self, board):
        max_move = None
        max_move_value = -math.inf

        for move in board.legal_moves:
            board.push(move)
            self.depth -= 1  # decrement depth
            min_move_value = self.min_value(board)
            # check if the min value of the current move is better than min value of the best (max) move so far
            if min_move_value > max_move_value:  # if so, update move and value
                max_move = move
                max_move_value = min_move_value
            self.depth += 1  # move explored, increment depth back and pop move
            board.pop()

        return max_move

    # try to maximize the value of a board
    def max_value(self, board):
        self.min_max_calls += 1  # increment min/max call tracking variable

        if self.cutoff_test(board):  # game over or depth limit reached
            return self.utility(board)

        v = -math.inf
        # loop through board moves and calculate value
        for move in board.legal_moves:
            board.push(move)
            self.depth -= 1
            v = max(v, self.min_value(board))   # max value is the max of current max and the min value of new board
            self.depth += 1
            board.pop()
        return v

    # try to minimize the value of a board
    def min_value(self, board):
        self.min_max_calls += 1  # increment min/max call tracking variable

        if self.cutoff_test(board):  # game over or depth limit reached
            return self.utility(board)

        v = math.inf
        # loop through board moves and calculate value
        for move in board.legal_moves:
            board.push(move)
            self.depth -= 1
            v = min(v, self.max_value(board))  # min value is the min of current min and the max value of new board
            self.depth += 1
            board.pop()
        return v

    def calculate_player_score(self, board, color):
        pawn_score = len(board.pieces(1, color))  # pawn worth 1
        knight_score = 3 * len(board.pieces(2, color))  # knight worth 3
        bishop_score = 3 * len(board.pieces(3, color))  # bishop worth 3
        rook_score = 5 * len(board.pieces(4, color))  # rook worth 5
        queen_score = 9 * len(board.pieces(5, color))  # queen worth 9
        king_score = 200 * len(board.pieces(6, color))  # king worth 200
        return pawn_score + knight_score + bishop_score + rook_score + queen_score + king_score

    # a simple heuristic function as explained in the textbook
    def utility(self, board):
        player_score = self.calculate_player_score(board, self.color)               # value of player's pieces
        opponent_score = self.calculate_player_score(board, self.opponent_color)    # value of opponent's pieces
        return player_score - opponent_score

