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

        getMax minimax tree : Max --> chance --> min --> max
        
        """
        #get move from heuristic
        avaliable_cells = grid.getAvailableCells()
        potential_cells = getPotentialMoves(self, grid, avaliable_cells)
        # call and return outcome of moveExpectedMinimax for decision
        move = moveExpectedMinimax(grid, potential_cells)
        

        return avaliable_cells[0] #should be move[0] but keeping this for now for code to work 

    def moveExpectedMinimax(grid: Grid) -> tuple:
        """
        move strategically to avoid being trapped by the opponent
        pick the best course of action (i.e., maximize utility) based on where you predict that the Opponent might throw a trap.
        """
        avaliable_cells = grid.getAvailableCells()
        if len(potential_cells) == 0: #terminal state
            return None

        potential_cells = getPotentialMoves(self, grid, avaliable_cells)

        maxNode = (None, -10000000000) #(maxChild, maxUtility)
        #maximize 

        for child in potential_cells:
            #TO-DO: chance 

            #minimize 
            minNode = PlayerAI.minimize(grid, list1)
            if minNode[1] > maxNode[1]: #utility comparison
                maxNode = (child, minNode[1])

        return maxNode
       
    def moveMinimize(grid) -> tuple : 
        avaliable_cells = grid.getAvailableCells()
        if len(potential_cells) == 0: #terminal state
            return None

        potential_cells = getPotentialMoves(self, grid, avaliable_cells)

        minNode = (None, 10000000000) #(minChild, minUtility)
        #maximize 

        for child in potential_cells:    
            #maximize
            maxNode = moveExpectedMinimax(grid)
            if maxNode[1] < minNode[1]: #utility comparison
                minNode = (child, maxNode[1])

        return minNode



    def getPotentialMoves(self, grid: Grid, available_cells) -> list:
        #using heuristic to determine which cells to consider to move to 
        options = []

        for cell in available_cells:
            if getMoveHeuristic(self, grid, cell) > 0:
                options.append(cell)

        return options

    def getMoveHeuristic(self, grid : Grid, cell : tuple) -> int:
        # the difference between the current number of moves Player (You) 
        #can make and the current number of moves the opponent can make.

        # if player1 has more free neighbors (score > 0), it is a good cell 
         
        #moves player1 can make at this cell
        player_neighbors = self.grid.get_neighbors(cell, only_available=True)

        #moves player2 can make 
        opponent_neighbors = self.grid.get_neighbors(self.computerAI.getPosition(), only_available=True)

        improved_score = len(player_neighbors) - len(opponent_neighbors)

        return improved_score

    def utility_trap(p1, option):     
        #option is intended position (i.e. one of the values of options)
        p = 1 - 0.05*(Utils.manhattan_distance(p1, option) - 1)
        return p

    def maximize(grid: Grid, options, a, b)->tuple:
        if len(grid.getAvailableCells()) == 0: #terminal state
            return None
        ans = (None, -10000000000)
        for child in options:
            print(child)
            list1 = [child]
            output = PlayerAI.minimize(grid, list1, a, b)
            if output[1] > ans[1]: #utility
                ans = (child, output[1])
            if ans[1] >= b:
                break
            if ans[1] > a:
                a = ans[1]
        return ans

    def minimize(grid : Grid, options, a, b)->tuple:
        if len(grid.getAvailableCells()) == 0: #terminal state
            return None
        ans = (None, 10000000000) #100000000 is initial utility value
        for child in options:
            utility = PlayerAI.utility_trap(grid.find(1), child)
            if utility < ans[1]:
                ans = (child, utility)
            if ans[1] <= a:
                break
            if ans[1] < b:
                b = ans[1]
        return ans

    def decision(grid: Grid, options)->tuple:
        ans =  PlayerAI.maximize(grid, options, -10000000000, 10000000000)
        return ans[0]


    def getTrap(self, grid : Grid) -> tuple:
        """ 
        The function should return a tuple of (x,y) coordinates to which the player *WANTS* to throw the trap.
        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Move* actions, 
        taking into account the probabilities of it landing in the positions you want. 
        Note that you are not required to account for the probabilities of it landing in a different cell
        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        """
        available_cells = grid.getAvailableCells()
        options = PlayerAI.getTrapHeuristic(self, grid) #possible trap locations
        ans = PlayerAI.decision(grid, options)
        return ans

        
    def getTrapHeuristic(self, grid : Grid) -> list:    
        #heuristic to determine which cells to consider > slowly reduce which cells are available to throw trap

        pos_1 = grid.find(1) #position of player 1 (us)
        pos_2 = grid.find(2) #position of player 2 (opponent) 
        #opponent can also be player 3 (not computer)
        options = []


        neighbors = grid.get_neighbors(pos_2, True) #available neighbors of player 2
        for tup in neighbors: #add available neighboring cells of opponent to list of cells to consider
            options.append(tup) # add all neighbors of player 2
        return options
        
        
            
        
        
        
    

        
    


    