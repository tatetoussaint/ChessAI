"""
Date: 10/12/21
Author: Tate Toussaint
Description: Chess AI test program
"""

# pip3 install python-chess
import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from IterativeDeepeningAI import IterativeDeepeningAI
from ChessGame import ChessGame
import sys


player1 = HumanPlayer()
player2 = RandomAI()
player3 = MinimaxAI(3, True)                    # depth, if color == white
player4 = AlphaBetaAI(5, True, False)     # depth, if color == white, if simple heuristic used (instead of michniewski)
player5 = IterativeDeepeningAI(5, True, False)  # max depth, if color == white; note: uses Alpha Beta
player6 = AlphaBetaAI(5, False, True)           # depth, if color == white, if simple heuristic used

game = ChessGame(player5, player1)  # first is white, second is black

while not game.is_game_over():
    print(game)
    game.make_move()


#print(hash(str(game.board)))
