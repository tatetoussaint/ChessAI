### Chess Engine
### Tate Toussaint

Table of Contents
---------------------

 * Project Overview
 * Parts of the Chess Engine
   * Random AI
   * Minimax AI
   * Alpha-Beta AI
   * Material Evaluation Heuristic
   * Michniewski Evaluation Heuristic
 * Running the Chess Engine

Project Overview
---------------------

In this project, I create a python chess engine in python that allows the user to play a game of chess on the commandline using AI or human generated moves.

Parts of the Chess Engine
---------------------

The chess engine consists of three different AIs and an infrastructure to run a chess game on. Furthermore, the game engine is implemented using the Python-Chess package found here: https://pypi.org/project/chess/

### Random AI

`RandomAI` receives a list of possible moves at every turn and simply carries out a move at random.

### Minimax AI

`MinimaxAI` uses the minimax algorithm to perform the maximal score move at each state assuming the opposing player chooses the move that minimizes players utility; it does this by recursively making moves until reaching a user-inputted maximum depth, where it returns the score calculated with an evaluation function. It then recursively backtracks at each step, minimizing the score during opponent turns and maximizing score during AI moves. The algorithm is described in depth here: https://en.m.wikipedia.org/wiki/Minimax.

### Alpha-Beta AI

`AlphaBetaAI` uses the alpha-beta algorithm similar to the minimax algorithm described above, but it utilizes alpha-beta pruning to reduce the number of max-depth states evaluated and increase the speed of the AIs decision process. The algorithm is described in depth here: https://en.m.wikipedia.org/wiki/Alpha–beta_pruning.

### Material Evaluation Heuristic

The material evaluation heuristic simply assigns a value to each piece on the table and sums up the piece value of each side; it returns high scores when the player being evaluated has a higher total value of pieces than the opposing player/

### Michniewski Evaluation Heuristic

The Michniewski evaluation heuristic implements the evaluation function described here: https://www.chessprogramming.org/Simplified_Evaluation_Function. It uses a combination of material values similar to the material heuristic above and also adds position scores for each type of piece and its corresponding location. The corresponding positional scores for each type of piece are contained in `PieceSquareTables.py`. Additionally, this heuristic evaluates end of game states (checkmate, stalemate, repetition of turns) and assigns scores to account for these. The total score at each position is a sum of the material, positional, and end-of-game scores.

Running the Chess Engine
---------------------

In order to run the chess engine, first navigate to the directory where this project is stored using the commandline. You can play by executing the command line sequence: `python3 play_chess.py [player1] [depth1] [player2] [depth2]`, where players 1 and 2 can be one of 'human', 'random', 'minimax', 'alphabeta'. player1 corresponds to the white player and player2 corresponds to the black player. When playing a human or random AI, the corresponding depth needs to be -1. When playing minimax or alphabeta, the corresponding depth can be any integer greater than 0. ex: `python3 play_chess.py human -1 alphabeta 3`

To test the chess engine, navigate to `test_chess.py` and change the players in game to the desired players. For each player, ensure the parameters for player color, depth, and heuristic are the valid parameters desired. The user can initialize additional AI bots to play by adding lines following players 1-6 already initialized. 
Note: Running the chess engines at depths greater than 5 can significantly slow down the AIs decision-making.

Example Output:
```
Moves can be entered using four characters. For example, d2d4 moves the piece at d2 to d4.
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R
----------------
a b c d e f g h

White to move

Please enter your move: 
b1c3
True
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . N . . . . .
P P P P P P P P
R . B Q K B N R
----------------
a b c d e f g h

Black to move

Alpha Beta AI recommending move g8h6 | depth = 3 | min/max calls = 613
heuristic calls: 1970
r n b q k b . r
p p p p p p p p
. . . . . . . n
. . . . . . . .
. . . . . . . .
. . N . . . . .
P P P P P P P P
R . B Q K B N R
----------------
a b c d e f g h

White to move

Please enter your move: 
```
