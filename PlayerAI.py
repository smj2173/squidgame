import numpy as np
import random
import time
import sys
import os 
from BaseAI import BaseAI
from Grid import Grid
import Utils
#setting path to parent directory
sys.path.append(os.getcwd())
sys.setrecursionlimit(10000)

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


    def utility(self, grid: Grid):
        #returns some numerical value that estimates the goodness of this state for you
        #improved score
        pos_1 = grid.find(1) #position of player 1 (us)
        pos_2 = grid.find(2) #position of player 2 (opponent) 
        possible_moves_1 = len(grid.get_neighbors(pos_1, True)) # num available neighbors to move to
        possible_moves_2 = len(grid.get_neighbors(pos_2, True)) #
        improved_score = possible_moves_1 - possible_moves_2
        #bigger number for IS means better chances for player 1
        return improved_score

    def maximize(grid: Grid, options)->tuple:
        if len(grid.getAvailableCells()) == 0: #terminal state
            return None
        ans = (None, -10000000000)
        for child in options:
            utility = PlayerAI.utility_trap(grid.find(1), child)
            list1 = [child]
            output = PlayerAI.minimize(grid, list1)
            if output[1] > ans[1]:
                ans = (child, output[1])
        return ans

    def utility_trap(p1, option):     
        #option is intended position (i.e. one of the values of options)
        p = 1 - 0.05*(Utils.manhattan_distance(p1, option) - 1)
        return p

    def minimize(grid : Grid, options)->tuple:
        if len(grid.getAvailableCells()) == 0: #terminal state
            return None
        ans = (None, 10000000000) #100000000 is initial utility value
        for child in options:
            utility = PlayerAI.utility_trap(grid.find(1), child)
            if utility < ans[1]:
                ans = (child, utility)
            list1 = [child]
            output = PlayerAI.maximize(grid, list1)
            if output[1] < ans[1]:
                ans = (child, output[1])
        return ans

    def decision(grid: Grid, options)->tuple:
        ans =  PlayerAI.maximize(grid, options)
        return ans
        #need to incorporate probability of success p into minimax
        #utility related to p somehow?


    def getTrap(self, grid : Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player *WANTS* to throw the trap.
        
        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Move* actions, 
        taking into account the probabilities of it landing in the positions you want. 
        
        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        
        """
        available_cells = grid.getAvailableCells()
        options = PlayerAI.getTrapHeuristic(self, grid) #possible trap locations
        #ans = PlayerAI.decision(grid, options)
        return available_cells[0]

    def getMoveHeuristic(self, grid : Grid) -> int:
        # the difference between the current number of moves Player (You) 
        #can make and the current number of moves the opponent can make.
         
        #moves player1 can make 
        player_neighbors = self.grid.get_neighbors(self.playerAI.getPosition(), only_available=True)

        #moves player2 can make 
        opponent_neighbors = self.grid.get_neighbors(self.computerAI.getPosition(), only_available=True)

        improved_score = len(player_neighbors) - len(opponent_neighbors)

        return improved_score
        
    def getTrapHeuristic(self, grid : Grid) -> list:    
        #heuristic to determine which cells to consider > slowly reduce which cells are available to throw trap

        pos_1 = grid.find(1) #position of player 1 (us)
        pos_2 = grid.find(2) #position of player 2 (opponent) 
        #opponent can also be player 3 (not computer)
        options = []


        neighbors = grid.get_neighbors(pos_2, True) #available neighbors of player 2
        for tup in neighbors: #add available neighboring cells of opponent to list of cells to consider
            options.append(tup) # add all neighbors of player 2

        print(options)
        return options
        
        
            
        
        
        
    

        
    


    