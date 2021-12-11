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
        The function should return a tuple of (x,y) coordinates to which the player moves.
        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Trap* actions, 
        taking into account the probabilities of them landing in the positions you believe they'd throw to.
        Note that you are not required to account for the probabilities of it landing in a different cell.
        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        getMax minimax tree : Max --> chance --> min --> max
        """
        playerPos = PlayerAI.getPosition(self)
        depth = 0
        print("player1 at " + str(playerPos))
        #get move from heuristic
        avaliable_cells = grid.get_neighbors(playerPos,True)
        print("avaliable cells: " + str(avaliable_cells))
        for child in avaliable_cells:
            print(str(child) + "'s utility: " +  str(PlayerAI.getMoveHeuristic(self, grid, child))) 
           
        

        # call and return outcome of moveExpectedMinimax for decision
        move = PlayerAI.moveExpectedMinimax(self, grid, avaliable_cells, playerPos, True, depth, -10000000000, 10000000000)
        print("move is" + str(move[0]))
        print("utility is" + str(move[1]))

  
        return PlayerAI.moveDecision(self, grid, move[1], avaliable_cells) #should be move[0] but keeping this for now for code to work 
   
    def moveDecision(self, grid, utility, potential_cells) -> tuple:
        for child in potential_cells:
            if PlayerAI.getMoveHeuristic(self, grid, child) == utility:
                return child

    def moveExpectedMinimax(self, grid: Grid, potential_cells, pos, maximizing, depth, a, b) -> tuple:
        """
        move strategically to avoid being trapped by the opponent
        pick the best course of action (i.e., maximize utility) based on where you predict that the Opponent might throw a trap.
        """
        if depth == 5 or potential_cells == 0 or len(grid.getAvailableCells()) == 0: #terminal state
            return (None, PlayerAI.getMoveHeuristic(self, grid, pos)) 

        if maximizing: 
            #print("maximizing")
            maxNode = (None, -10000000000) #(maxChild, maxUtility)
            for child in potential_cells:
                minNode = PlayerAI.moveExpectedMinimax(self, grid, potential_cells, child, False, depth+1, a, b)
                if minNode[1] > maxNode[1]: #utility comparison
                    maxNode = (child, minNode[1])
                a = max(a, minNode[1])
                if b <= a:
                    break
            return maxNode

        else:
            #print("minimizing")
            minNode = (None, 10000000000) #(minChild, minUtility)
            for child in potential_cells:    
                maxNode = PlayerAI.moveExpectedMinimax(self, grid,potential_cells, child, True, depth+1, a, b)
                if maxNode[1] < minNode[1]: #utility comparison
                    minNode = (child, maxNode[1])
                b = min(b, maxNode[1])
                if b <= a:
                    break
            return minNode


    def getMoveHeuristic(self, grid : Grid, cell : tuple) -> int:
        # the difference between the current number of moves Player (You) 
        #can make and the current number of moves the opponent can make.

        # if player1 has more free neighbors (score > 0), it is a good cell 
         
        #moves player1 can make at this cell
       
        player_neighbors = grid.get_neighbors(cell, only_available=True)


        #moves player2 can make 
        opponent_neighbors = grid.get_neighbors(grid.find(2), only_available=True)

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
        
        
            
        
        
        
    

        
    


    