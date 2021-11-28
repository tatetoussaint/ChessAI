"""
Date: 10/11/21
Author: Tate Toussaint
Description: AlphaBeta AI
"""

import random

import chess
import math
import PieceSquareTables as pst


class AlphaBetaAI:
    def __init__(self, depth, color, simple):
        self.depth = depth  # decremented until reaches depth limit of 0
        self.color = color  # true is white, false is black
        self.opponent_color = not color
        self.board_before_reorder = None
        self.min_max_calls = 0  # keeps track of calls to min and max each iteration
        self.heuristic_calls = 0
        self.simple = simple

    def choose_move(self, board):
        self.min_max_calls = 0  # resetting min/max calls before move decision process
        self.heuristic_calls = 0
        move = self.minimax_decision(board)
        print("Alpha Beta AI recommending move " + str(move) + " | depth = " + str(self.depth) +
              " | min/max calls = " + str(self.min_max_calls))
        print("heuristic calls: " + str(self.heuristic_calls))
        return move

    # checks if the game is over or depth is over
    def cutoff_test(self, board):
        if self.depth == 0 or board.is_game_over():  # if at depth limit or no legal moves
            return True
        return False

    # goes through options at given depth and returns best move
    def minimax_decision(self, board):
        max_move_value, max_move = self.max_value(board, -math.inf, math.inf)
        return max_move  # don't need the value

    # try to maximize the value of a board
    def max_value(self, board, alpha, beta):
        self.min_max_calls += 1  # increment min/max call tracking variable

        if self.cutoff_test(board):  # game over or depth limit reached
            if self.simple:
                return self.simple_heuristic(board), None
            else:
                return self.michniewski_heuristic(board), None  # no need to keep track of best move

        v = -math.inf
        max_move = None

        self.board_before_reorder = board  # keeps track of current board
        sorted_moves = sorted(board.legal_moves, key=self.move_reorderer, reverse=True)  # sort moves by board value
        # sorted_moves = sorted(board.legal_moves, key=lambda k: random.random())

        # loop through moves and update alpha/beta
        for move in sorted_moves:
            board.push(move)
            self.depth -= 1
            min_value, min_move = self.min_value(board, alpha, beta)
            self.depth += 1
            board.pop()

            # check if the min value of the current move is better than min value of the best (max) move so far
            if min_value > v:
                v = min_value
                max_move = move

            if v >= beta:
                return v, move  # move value greater than beta, return immediately
            alpha = max(alpha, v)

        return v, max_move

    # try to minimize the value of a board
    def min_value(self, board, alpha, beta):
        self.min_max_calls += 1  # increment min/max call tracking variable

        if self.cutoff_test(board):  # game over or depth limit reached
            if self.simple:
                return self.simple_heuristic(board), None
            else:
                return self.michniewski_heuristic(board), None

        v = math.inf
        min_move = None

        self.board_before_reorder = board  # keeps track of current board
        sorted_moves = sorted(board.legal_moves, key=self.move_reorderer, reverse=False)  # sort moves by board value
        # sorted_moves = sorted(board.legal_moves, key=lambda k: random.random())

        # loop through moves and update alpha/beta
        for move in sorted_moves:
            board.push(move)
            self.depth -= 1
            max_value, max_move = self.max_value(board, alpha, beta)
            self.depth += 1
            board.pop()

            # check if the max value of the current move is better than max value of the best (min) move so far
            if max_value < v:
                v = max_value
                min_move = move

            if v <= alpha:  # move value less than alpha, return immediately
                return v, move
            beta = min(beta, v)

        return v, min_move

    # calculate value of move using a simple heuristic
    def move_reorderer(self, move):
        self.board_before_reorder.push(move)
        move_utility = self.simple_heuristic(self.board_before_reorder)  # a simple material heuristic
        # move_utility = self.michniewski_heuristic(self.board_before_reorder)  # a simple material heuristic
        self.board_before_reorder.pop()
        return move_utility

    # calculate player material score according to Tomasz Michniewski's Simplified Evaluation Function
    def michniewski_player_material_score(self, board, color):
        pawn_score = 100 * len(board.pieces(1, color))  # pawn worth 100
        knight_score = 320 * len(board.pieces(2, color))  # knight worth 320
        bishop_score = 330 * len(board.pieces(3, color))  # bishop worth 330
        rook_score = 500 * len(board.pieces(4, color))  # rook worth 500
        queen_score = 900 * len(board.pieces(5, color))  # queen worth 900
        king_score = 20000 * len(board.pieces(6, color))  # king worth 20000
        return pawn_score + knight_score + bishop_score + rook_score + queen_score + king_score

    # calculate player position score according to Tomasz Michniewski's Simplified Evaluation Function
    def michniewski_player_position_score(self, board, color):
        white_position_score = 0
        black_position_score = 0

        # test for king middle-game or end-game
        white_queen = False
        black_queen = False
        num_minor_white_pieces = 0
        num_minor_black_pieces = 0
        for i in range(0, 64):
            piece = board.piece_at(i)  # get piece at index
            if piece is not None:
                if piece.piece_type == 5:
                    if piece.color == 1:
                        white_queen = True
                    else:
                        black_queen = True
                elif piece.piece_type != 6:  # not queen or king (must be minor piece)
                    if piece.color == 1:
                        num_minor_white_pieces += 1
                    else:
                        num_minor_black_pieces += 1

        # set king_endgame variable
        king_endgame = False
        if white_queen == False and black_queen == False:
            king_endgame = True
        elif white_queen == True and black_queen == False and num_minor_white_pieces <= 1:
            king_endgame = True
        elif white_queen == False and black_queen == True and num_minor_black_pieces <= 1:
            king_endgame = True
        elif num_minor_white_pieces <= 1 and num_minor_black_pieces <= 1:
            king_endgame = True

        # dictionary mapping piece ID to piece square table for white player
        white_switch = {
            1: pst.pawn_values_white,
            2: pst.knight_values_white,
            3: pst.bishop_values_white,
            4: pst.rook_values_white,
            5: pst.queen_values_white
        }

        # dictionary mapping piece ID to piece square table for black player
        black_switch = {
            1: pst.pawn_values_black,
            2: pst.knight_values_black,
            3: pst.bishop_values_black,
            4: pst.rook_values_black,
            5: pst.queen_values_black
        }

        # loop through chess board
        for i in range(0, 64):
            piece = board.piece_at(i)  # get piece at index
            if piece is not None:

                if piece.piece_type != 6:  # piece is not a king
                    if piece.color == True:  # piece is white, use white switch
                        table = white_switch.get(piece.piece_type)
                        white_position_score += table[i]
                    else:  # piece is black, use black switch
                        table = black_switch.get(piece.piece_type)
                        black_position_score += table[i]

                else:  # piece is a king
                    if king_endgame == True:  # board in end-game
                        if piece.color == True:  # white king
                            white_position_score += pst.king_values_white_endgame[i]
                        else:  # black king
                            black_position_score += pst.king_values_black_endgame[i]
                    else:  # board in middle-game
                        if piece.color == True:  # white king
                            white_position_score += pst.king_values_white_middlegame[i]
                        else:  # black king
                            black_position_score += pst.king_values_black_middlegame[i]

        if self.color == True:  # player is white
            return white_position_score - black_position_score
        else:
            return black_position_score - white_position_score

    # calculate player score according to Tomasz Michniewski's Simplified Evaluation Function
    # https://www.chessprogramming.org/Simplified_Evaluation_Function
    def michniewski_heuristic(self, board):
        board_score = 0
        color = not board.turn  # player that just moved

        # if board.is_game_over(): print(str(board.outcome()))

        if not board.has_insufficient_material(color):  # color can still win
            if board.is_repetition(3) or board.is_stalemate():
                board_score -= 200   # repetition and stalemate bad

        if board.is_checkmate():
            board_score += math.inf if color == self.color else -math.inf   # checkmate is infinite value

        board_score += self.michniewski_player_material_score(board, self.color) - \
                         self.michniewski_player_material_score(board, self.opponent_color)

        board_score += self.michniewski_player_position_score(board, self.color)

        return board_score

    # calculate material score according to textbook heuristic
    def simple_player_material_score(self, board, color):
        pawn_score = 1 * len(board.pieces(1, color))  # pawn worth 1
        knight_score = 3 * len(board.pieces(2, color))  # knight worth 3
        bishop_score = 3 * len(board.pieces(3, color))  # bishop worth 3
        rook_score = 5 * len(board.pieces(4, color))  # rook worth 5
        queen_score = 9 * len(board.pieces(5, color))  # queen worth 9
        king_score = 200 * len(board.pieces(6, color))  # king worth 200
        return pawn_score + knight_score + bishop_score + rook_score + queen_score + king_score

    # a simple heuristic function as explained in the textbook (uses just material values)
    def simple_heuristic(self, board):
        self.heuristic_calls += 1
        player_score = self.simple_player_material_score(board, self.color)  # value of player's pieces
        opponent_score = self.simple_player_material_score(board, self.opponent_color)  # value of opponent's pieces
        return player_score - opponent_score
