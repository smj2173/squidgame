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
        avaliable_cells = grid.getAvailableCells()
        return avaliable_cells[0]

     def getMoveHeuristic(self, grid : Grid) -> int:
         # the difference between the current number of moves Player (You) 
         #can make and the current number of moves the opponent can make.
         
         #moves player1 can make 
        player_neighbors = self.grid.get_neighbors(self.playerAI.getPosition(), only_available=True)

         #moves player2 can make 
        opponent_neighbors = self.grid.get_neighbors(self.computerAI.getPosition(), only_available=True)

        improved_score = len(player_neighbors) - len(opponent_neighbors)

        return improved_score
         

         
        

    