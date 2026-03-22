from learntools.core import binder
binder.bind(globals())
from learntools.game_ai.ex1 import *
import numpy as np
import random
# Config.inarow means no.of pieces a player needs to get in a row inorder to win(4 for ConnectFour)
# Gives boards next step after agent drops a piece

def drop_piece(grid, col,piece,config):
    next_grid = grid.copy()
    for row in range(config.rows-1,-1,-1):
        if next_grid[row][col] == 0:
            break
    next_grid[row][col] = piece
    return next_grid
#Returns True if dropping piece in column results in game win
#Piece is either opponent or ur move

def check_winning_move(obs,config,col,piece):
    #Convert the board to a 2D Grid
    grid = np.asarray(obs.board).reshape(config.rows,config.columns)
    next_grid = drop_piece(grid,col,piece,config)
    # Horizontal
    for row in range(config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[row,col:col+config.inarow])
            if window.count(piece) == config.inarow:
                return True
    # Vertical
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns):
            window = list(next_grid[row:row+config.inarow,col])
            if window.count(piece) == config.inarow:
                return True
    # Positive diagonal
    for row in range(config.rows-(config.inarow-1)):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[range(row,row+config.inarow),range(col,col+config.inarow)])
            if window.count(piece) == config.inarow:
                return True
    #Negative Diagonal
    for row in range(config.inarow-1,config.rows):
        for col in range(config.columns-(config.inarow-1)):
            window = list(next_grid[range(row,row-config.inarow,-1),range(col,col+config.inarow)])
            if window.count(piece) == config.inarow:
                return True
    return False

#To check if agent can win in next move,you should set piece = obs.mark

def agent_q1(obs,config):
    valid_moves = [col for col in range(config.columns) if obs.board[col]==0]
    for col in valid_moves:
        if check_winning_move(obs,config,col,obs.mark):
            return col
        return random.choice(valid_moves)
    
def agent_q2(obs, config):

    valid_moves = [col for col in range(config.columns) if obs.board[col]==0]
    for col in valid_moves:
        if check_winning_move(obs,config,col,obs.mark):
            return col
        elif check_winning_move(obs,config,col,obs.mark%2+1):
            return col
    return random.choice(valid_moves)
    return 0
def my_agent(obs, config):
    
    import random
    valid_moves = [col for col in range(config.columns) if obs.board[col] == 0]
    return random.choice(valid_moves)
            
from kaggle_environments import evaluate, make

env = make("connectx", debug=True)
env.run([my_agent, "random"])
env.render(mode="ipython")

