"""
Date: 10/12/21
Author: Tate Toussaint
Description: Iterative Deepening AI using AlphaBeta AI
"""

import chess
import math
from AlphaBetaAI import AlphaBetaAI


class IterativeDeepeningAI:
    def __init__(self, max_depth, color, simple):
        self.max_depth = max_depth
        self.color = color  # color of the player
        self.AI = AlphaBetaAI(max_depth, self.color, simple)
        self.best_move = None

    def choose_move(self, board):
        best_move_list = []

        for depth in range(0, self.max_depth + 1):
            # AI = AlphaBetaAI(depth, self.color)
            self.AI.depth = depth
            move = self.AI.minimax_decision(board)
            self.best_move = move   # update move in case it needs to be returned by a time
            best_move_list.append(move)
            print("Depth: " + str(depth) + " | Move: " + str(move) + " | recommended by Iterative Deepening AI (using "
                                                                     "Alpha Beta)")

        print("\nIterative Deepening AI (using Alpha Beta) recommending move " + str(best_move_list[len(best_move_list) - 1]))
        return best_move_list[len(best_move_list) - 1]  # the last move recommended
