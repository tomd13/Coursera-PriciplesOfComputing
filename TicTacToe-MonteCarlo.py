"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 500  # Number of trials to run
SCORE_CURRENT = 1.0  # Score for squares played by the current player
SCORE_OTHER = 1.0  # Score for squares played by the other player


def mc_trial(board, player):
    """
    Runs one monte-carlo trial, taking the current board state
    and the next player to move
    """
    next_move = random.choice(board.get_empty_squares())
    board.move(next_move[0], next_move[1], player)
    if board.check_win() is None:
        mc_trial(board, provided.switch_player(player))


def mc_update_scores(scores, board, player):
    """
    Updates grid of scores from completed game
    """
    if not board.check_win() == provided.DRAW:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.square(row, col) == player:
                    scores[row][col] += SCORE_CURRENT
                elif board.square(row, col) == provided.switch_player(player):
                    scores[row][col] -= SCORE_OTHER


def get_best_move(board, scores):
    """
    Returns the best move given a current board and trained scores
    """
    max_score = 0
    max_score_squares = []
    for square in board.get_empty_squares():
        if scores[square[0]][square[1]] > max_score:
            max_score = scores[square[0]][square[1]]
            max_score_squares = [square]
        elif scores[square[0]][square[1]] == max_score:
            max_score_squares.append(square)
    return random.choice(max_score_squares)


def mc_move(board, player, trials):
    scores = [[0 for dummy_i in range(board.get_dim())] for dummy_j in range(board.get_dim())]
    for dummy_count in range(trials):
        mc_board = board.clone()
        mc_trial(mc_board, player)
        mc_update_scores(scores, mc_board, player)
    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
