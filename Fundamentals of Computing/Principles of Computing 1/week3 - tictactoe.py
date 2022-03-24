"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import math
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1000    # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player


PLAYER_LIST = [provided.PLAYERX,provided.PLAYERO]





# Variable Definition
# board: n x n size grid coded as a list of lists that keeps track of 'X'
# 	and 'O'
# player: which player the machine player is. Will either be 'X' or 'O'
# scores: n x n grid coded as a list of lists, that keeps track of the 
# 	of each space
# trails: the number of trials to run the Monte Carlo simulation


    
# Main Functions
def mc_trial(board, player):
    '''
    Takes a current board and the next player
    to move, plays a random game, and returns a modified 
    board variable.
    '''
    
    empty_squares = board.get_empty_squares()

    
    while len(empty_squares) > 0:
        player_choice = random.choice(empty_squares)
        board.move(player_choice[0], player_choice[1], player)
        
        player = provided.switch_player(player)
        
        empty_squares = board.get_empty_squares()
        
        if board.check_win() != None:
            break
        
def mc_update_scores(scores, board, player):
    '''
    Takes a grid of scores, a board of a completed game, and
    the machine player (X or O), scores the completed board, and
    updates the score grid. Does not return anything.
    '''
   
    if board.check_win() != provided.DRAW:
        for row in range(len(scores)):
            for col in range(len(scores)): 
                if board.check_win() == player:
                    if board.square(row, col) == player:
                        scores[row][col] += SCORE_CURRENT
                    elif board.square(row, col) != provided.EMPTY:
                        scores[row][col] += -1*SCORE_OTHER
                else:
                    if board.square(row, col) == player:
                        scores[row][col] += -1*SCORE_CURRENT
                    elif board.square(row, col) != provided.EMPTY:
                        scores[row][col] += SCORE_OTHER


    

def get_best_move(board, scores):
    '''
    Takes the current board and grid of scores, finds all
    the empty squares with the maximum score and return 
    one of them as a (row, col) tuple.
    '''

    empty_squares = board.get_empty_squares()
    temp_scores = [scores[score[0]][score[1]] for score in empty_squares] 
    
    max_score = max(temp_scores)
    temp_max_scores = [score for score in empty_squares
                       if scores[score[0]][score[1]] == max_score]
    
    best_move = random.choice(temp_max_scores)

        
    return best_move

def mc_move(board, player, trials):
    '''
    Takes the current board, the machine player (X or O),
    and the number of trials to run, runs the Monte Carlo
    simulation, and returns the next move for the machine
    player in the form of a (row, col) tuple.
    '''
    
    scores = [[0* row * col for col in range(board.get_dim())]
              for row in range(board.get_dim())]
    
    
    for dummy in range(trials):
        board_clone = board.clone()
        mc_trial(board_clone, player)
        mc_update_scores(scores, board_clone, player)
        
    for row in range(len(scores)):
        for col in range(len(scores)):
            if board.square(row, col) != provided.EMPTY:
                scores[row][col] = 0

    if len(board.get_empty_squares()) > 0:
        move = get_best_move(board, scores)
        scores[move[0]][move[1]] = 0
    else:
        move = None
    
    return move

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.


#provided.play_game(mc_move, NTRIALS, False) 
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
