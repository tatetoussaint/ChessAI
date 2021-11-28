"""
Date: 11/26/21
Author: Tate Toussaint
Description: Allows user to play chess at the commandline using 4 AIs; inputs described in README.md
"""

import sys
from ChessGame import ChessGame
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from HumanPlayer import HumanPlayer
from RandomAI import RandomAI

if __name__ == "__main__":
    # check length of arguments
    if len(sys.argv) != 5:
        print("expected 5 args; received " + str(len(sys.argv)) +
              "\nInput: python3 [player1] [depth1] [player2] [depth2]")
        sys.exit()

    # check if AI1 uses recursive depth limit
    isDepthAI1 = True
    if int(sys.argv[2]) == -1:
        isDepthAI1 = False
    elif int(sys.argv[2]) < 1:
        print("Usage: depth1 must be a valid integer greater than 0")
        sys.exit()

    # check if AI2 uses recursive depth limit
    isDepthAI2 = True
    if int(sys.argv[4]) == -1:
        isDepthAI2 = False
    elif int(sys.argv[4]) < 1:
        print("Usage: depth2 must be a valid integer greater than 0")
        sys.exit()

    # initialize player1
    if str(sys.argv[1]).lower() == "human" and not isDepthAI1:
        player1 = HumanPlayer()
    elif str(sys.argv[1]).lower() == "random" and not isDepthAI1:
        player1 = RandomAI()
    elif str(sys.argv[1]).lower() == "minimax" and isDepthAI1:
        player1 = MinimaxAI(int(sys.argv[2]), True)
    elif str(sys.argv[1]).lower() == "alphabeta" and isDepthAI1:
        player1 = AlphaBetaAI(int(sys.argv[2]), True)
    else:
        print("Usage: 'human' and 'random' with depth -1, 'minimax' and 'alphabeta' with depth > 0")
        sys.exit()

    # initialize player2
    if str(sys.argv[3]).lower() == "human" and not isDepthAI2:
        player2 = HumanPlayer()
    elif str(sys.argv[3]).lower() == "random" and not isDepthAI2:
        player2 = RandomAI()
    elif str(sys.argv[3]).lower() == "minimax" and isDepthAI2:
        player2 = MinimaxAI(int(sys.argv[4]), False)
    elif str(sys.argv[3]).lower() == "alphabeta" and isDepthAI2:
        player2 = AlphaBetaAI(int(sys.argv[4]), False, True)
    else:
        print("Usage: 'human' and 'random' with depth -1, 'minimax' and 'alphabeta' with depth > 0")
        sys.exit()

    # initialize game and run game loop
    game = ChessGame(player1, player2)
    while not game.is_game_over():
        print(game)
        game.make_move()
