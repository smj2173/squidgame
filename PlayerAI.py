import numpy as np
import random
import time
import sys
import os 
from BaseAI import BaseAI
from Grid import Grid
#setting path to parent directory
sys.path.append(os.getcwd())

# TO BE IMPLEMENTED
# 
class PlayerAI(BaseAI):

    def __init__(self) -> None:
        # You may choose to add attributes to your player - up to you!
        super().__init__()
        self.pos = None
        self.player_num = None
    
    def getPosition(self):
        return self.pos

    def setPosition(self, new_position):
        self.pos = new_position 

    def getPlayerNum(self):
        return self.player_num

    def setPlayerNum(self, num):
        self.player_num = num

    def getMove(self, grid: Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player moves.

        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Trap* actions, 
        taking into account the probabilities of them landing in the positions you believe they'd throw to.

        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        
        """
        #get random move 
        avaliable_cells = grid.getAvailableCells()
        return avaliable_cells[0]

    def getTrap(self, grid : Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player *WANTS* to throw the trap.
        
        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Move* actions, 
        taking into account the probabilities of it landing in the positions you want. 
        
        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        
        """
        #heuristic to determine which cells to consider > slowly reduce which cells are available to throw trap

        available_cells = grid.getAvailableCells()
        pos_1 = grid.find(1) #position of player 1 (us)
        pos_2 = grid.find(2) #position of player 2 (opponent)
        #remove positions of players (don't want traps to go there)
        options = []

        neighbors = grid.get_neighbors(pos_2, True) #available neighbors of player 2
        for tup in neighbors: #add available neighboring cells of opponent to list of cells to consider
            options.append(tup) # add all neighbors of player 2
            
        
        
        
        

        
        
        

    