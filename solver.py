# -*- coding: utf-8 -*-
"""
Author: Alexander Ulery

"""

import math
import time
import random
import sys
sys.setrecursionlimit(10000)

puzzlelog = open("8puzzlelog","a")

global u_turncount
u_turncount = 0

input_list = input("Please enter your INITIAL STATE with digits 0-8 separated by ' ': ")
pre_state = list(map(int, input_list.split()))
    
winput = input("Please enter your GOAL STATE with digits 0-8 separated by ' ': ")
winningState = list(map(int, winput.split()))

n = int(math.sqrt(len(winningState)))
print("n = ", n)




#print turnCount & time. To display turnCount and time in n_puzzle()
def readData(turns, time):
    print("Turn count: ", turns, " turns")
    print(f"Time expired: {time:0.4f}s")

#class for boardstate functions; hamming, equals, neighbors
class Board():
    def hamming(state, turnCount):
        ham = turnCount
        for i in state:
            if state[i] == winningState[i]:
                ham = ham + 1
        return(ham)

    def equals(state, Y):
        for i in state:
            if state[i] != Y[i]:
                return(False)   
        return(True)
    
    #return optimal neighbor for heuristic A* search via hamming distance
    def A_neighbors(nextState, prevState, turnCount):
        
        i = Board.findhole(nextState)
        
        rightDist = 0
        leftDist = 0
        upDist = 0
        downDist = 0
        
        #top row
        if i < n:           
            if i == 0:
                #top left position; only move right or down
                tempRight = Board.right(nextState)
                if not Board.equals(tempRight, prevState):
                    rightDist = Board.hamming(tempRight, turnCount)
                
                tempDown = Board.down(nextState)
                if not Board.equals(tempDown, prevState):
                    downDist = Board.hamming(tempDown, turnCount)
                
                if(rightDist > downDist):
                    return(tempRight)
                elif(downDist > rightDist):
                    return(tempDown)

            elif i == (n - 1):
                #top right position; only move left or down
                tempLeft = Board.left(nextState)
                if not Board.equals(tempLeft, prevState):
                    leftDist = Board.hamming(tempLeft, turnCount)
                
                tempDown = Board.down(nextState)
                if not Board.equals(tempDown, prevState):
                    downDist = Board.hamming(tempDown, turnCount)
                
                if(leftDist > downDist):
                    return(tempLeft)
                elif(downDist > leftDist):
                    return(tempDown)
                    
            else:
                #only move right, down or left
                tempRight = Board.right(nextState)
                if not Board.equals(tempRight, prevState):
                    rightDist = Board.hamming(tempRight, turnCount)
                
                tempDown = Board.down(nextState)
                if not Board.equals(tempDown, prevState):
                    downDist = Board.hamming(tempDown, turnCount)
                
                tempLeft = Board.left(nextState)
                if not Board.equals(tempLeft, prevState):
                    leftDist = Board.hamming(tempLeft, turnCount)
                
                if(rightDist > leftDist) and (rightDist > downDist):
                    return(tempRight)
                elif(leftDist > rightDist) and (leftDist > downDist):
                    return(tempLeft)
                elif(downDist > rightDist) and (downDist > leftDist):
                    return(tempDown)                  
        
        #bottom row
        elif i > ((n * n) - n):
            if i == ((n * n) - 1):
                #only move left or up
                tempLeft = Board.left(nextState)
                if not Board.equals(tempLeft, prevState):
                    leftDist = Board.hamming(tempLeft, turnCount)
                
                tempUp = Board.up(nextState)
                if not Board.equals(tempUp, prevState):
                    upDist = Board.hamming(tempUp, turnCount)
                
                if(upDist > leftDist):
                    return(tempUp)
                elif(leftDist > upDist):
                    return(tempLeft)
  
            elif i == ((n * n) - n):
                #bottom-left position; only move up or right
                tempRight = Board.right(nextState)
                if not Board.equals(tempRight, prevState):
                    rightDist = Board.hamming(tempRight, turnCount)
                
                tempUp = Board.up(nextState)
                if not Board.equals(tempUp, prevState):
                    upDist = Board.hamming(tempUp, turnCount)
                
                if(upDist > rightDist):
                    return(tempUp)
                elif(rightDist > upDist):
                    return(tempRight)
                    
            else:
                #only move left, up or right
                tempRight = Board.right(nextState)
                if not Board.equals(tempRight, prevState):
                    rightDist = Board.hamming(tempRight, turnCount)

                tempLeft = Board.left(nextState)
                if not Board.equals(tempLeft, prevState):
                    leftDist = Board.hamming(tempLeft, turnCount)
                
                tempUp = Board.up(nextState)
                if not Board.equals(tempUp, prevState):
                    upDist = Board.hamming(tempUp, turnCount)
                
                if(rightDist > leftDist) and (rightDist > upDist):
                    return(tempRight)
                elif(leftDist > rightDist) and (leftDist >upDist):
                    return(tempLeft)
                elif(upDist > rightDist) and (upDist > leftDist):
                    return(tempUp)
                
        #Not bottom or top row
        else:
            if (i % n == 0):
                #left wall; cannot move left
                tempRight = Board.right(nextState)
                if not Board.equals(tempRight, prevState):
                    rightDist = Board.hamming(tempRight, turnCount)
                
                tempUp = Board.up(nextState)
                if not Board.equals(tempUp, prevState):
                    upDist = Board.hamming(tempUp, turnCount)
                
                tempDown = Board.down(nextState)
                if not Board.equals(tempDown, prevState):
                    downDist = Board.hamming(tempDown, turnCount)
                
                if(rightDist > upDist) and (rightDist > downDist):
                    return(tempRight)
                elif(upDist > rightDist) and (upDist > downDist):
                    return(tempUp)
                elif(downDist > rightDist) and (downDist > upDist):
                    return(tempDown)
  
            elif (i + 1) % n == 0:
                #right wall; cannot move right
                tempLeft = Board.left(nextState)
                if not Board.equals(tempLeft, prevState):
                    leftDist = Board.hamming(tempLeft, turnCount)
                
                tempUp = Board.up(nextState)
                if not Board.equals(tempUp, prevState):
                    upDist = Board.hamming(tempUp, turnCount)
                
                tempDown = Board.down(nextState)
                if not Board.equals(tempDown, prevState):
                    downDist = Board.hamming(tempDown, turnCount)
                
                if(leftDist > upDist) and (leftDist > downDist):
                    return(tempLeft)
                elif(upDist > leftDist) and (upDist > downDist):
                    return(tempUp)
                elif(downDist > leftDist) and (downDist > upDist):
                    return(tempDown)
                
            else:
                #can move any direction
                tempRight = Board.right(nextState)
                if not Board.equals(tempRight, prevState):
                    rightDist = Board.hamming(tempRight, turnCount)
                
                tempLeft = Board.left(nextState)
                if not Board.equals(tempLeft, prevState):
                    leftDist = Board.hamming(tempLeft, turnCount)
                
                tempUp = Board.up(nextState)
                if not Board.equals(tempUp, prevState):
                    upDist = Board.hamming(tempUp, turnCount)
                
                tempDown = Board.down(nextState)
                if not Board.equals(tempDown, prevState):
                    downDist = Board.hamming(tempDown, turnCount)
                
                if(rightDist > leftDist) and (rightDist > upDist) and (rightDist > downDist):
                    return(tempRight)
                elif(leftDist > rightDist) and (leftDist > upDist) and (leftDist > downDist):
                    return(tempLeft)
                elif(upDist > rightDist) and (upDist > leftDist) and (upDist > downDist):
                    return(tempUp)
                elif(downDist > rightDist) and (downDist > leftDist) and (downDist > upDist):
                    return(tempDown)       
        
        #if two or more of the hamming distances are equal,
        #then return one of them at random.
        random.seed(turnCount)
        
        if(rightDist == leftDist == upDist == downDist != 0):
            choices = [tempRight, tempLeft, tempUp, tempDown]
            return(random.choice(choices))
        elif(rightDist == leftDist == upDist != 0):
            choices = [tempRight, tempLeft, tempUp]
            return(random.choice(choices))
        elif(rightDist == upDist == downDist != 0):
            choices = [tempRight, tempUp, tempDown]
            return(random.choice(choices))
        elif(rightDist ==  leftDist == downDist != 0):
            choices = [tempRight, tempLeft, tempDown]
            return(random.choice(choices))
        elif(leftDist == upDist == downDist != 0):
            choices = [tempLeft, tempUp, tempDown]
            return(random.choice(choices))
        elif(rightDist == leftDist != 0):
            choices = [tempRight, tempLeft]
            return(random.choice(choices))
        elif(rightDist == upDist != 0):
            choices = [tempRight, tempUp]
            return(random.choice(choices))
        elif(rightDist == downDist != 0):
            choices = [tempRight, tempDown]
            return(random.choice(choices))
        elif(leftDist == downDist != 0):
            choices = [tempLeft, tempDown]
            return(random.choice(choices))
        elif(upDist == downDist != 0):
            choices = [tempUp, tempDown]
            return(random.choice(choices))
        elif(upDist == leftDist != 0):
            choices = [tempUp, tempLeft]
            return(random.choice(choices))
        else:
            print("ERROR: NEXT DIRECTION NOT FOUND.")
            return
        
    def FindNeighbors(state):
        
            #new_choices = [0, 0, 0, 0]   for   [UP, DOWN, LEFT, RIGHT]
        i = Board.findhole(state)
        if i < n:   #top row         
            if i == 0:                  #top-left; only move down or right
                return([0, 1, 0, 1])
            elif i == (n - 1):          #top-right; only down or left
                return([0, 1, 1, 0])
            else:                       #down, left or right
                return([0, 1, 1, 1])
                
        elif i >= ((n * n) - n):         #bottom row
            if i == ((n * n) - 1):      #bottom-right; only up or left
                return([1, 0, 1, 0])
            elif i == ((n * n) - n):    #bottom-left; only up or right
                return([1, 0, 0, 1])
            else:                       #up, left or right
                return([1, 0, 1, 1])
        else:       #center row(s)
            if (i % n == 0):            #left wall; only up, down or right
                return([1, 1, 0, 1])
            elif (i + 1) % n == 0:      #right wall; only up, down or left
                return([1, 1, 1, 0])
            else:    #all neighbors applicable
                return([1, 1, 1, 1])
                
    def iterate(currentState, prev_state, neighbors):
                #check to see if match present in current node
                prev_neighbors = Board.FindNeighbors(prev_state)
                
                global u_turncount
                u_turncount += 1
                
                    #DEBUG
                #print("TURNCOUNT: ", u_turncount)
                #print(neighbors[0], neighbors[1], neighbors[2], neighbors[3])
                #Board.showState(currentState)
                
                if(Board.equals(currentState, winningState)):
                    return(True)
                if(Board.equals(Board.up(currentState),winningState)):
                    currentState = Board.up(currentState)
                    return(True)
                elif(Board.equals(Board.down(currentState),winningState)):
                    currentState = Board.down(currentState)
                    return(True)
                elif(Board.equals(Board.left(currentState),winningState)):
                    currentState = Board.left(currentState)
                    return(True)
                elif(Board.equals(Board.right(currentState),winningState)):
                    currentState = Board.right(currentState)
                    return(True)

                if(neighbors[0] == 1):      #[U, D, L, R]
                    newState = Board.up(currentState)
                    new_neighbors = Board.FindNeighbors(newState)
                    new_neighbors[1] -= 1
                    if(Board.iterate(newState,currentState,new_neighbors) == True):
                        return(True)
                    
                if(neighbors[1] == 1):
                    newState = Board.down(currentState)
                    new_neighbors = Board.FindNeighbors(newState)
                    new_neighbors[0] -= 1
                    if(Board.iterate(newState,currentState,new_neighbors) == True):
                        return(True)
                    
                if(neighbors[2] == 1):
                    newState = Board.left(currentState)
                    new_neighbors = Board.FindNeighbors(newState)
                    new_neighbors[3] -= 1
                    if(Board.iterate(newState,currentState,new_neighbors) == True):
                        return(True)
                    
                if(neighbors[3] == 1):
                    newState = Board.right(currentState)
                    new_neighbors = Board.FindNeighbors(newState)
                    new_neighbors[2] -= 1
                    if(Board.iterate(newState,currentState,new_neighbors) == True):
                        return(True)
                
    def findhole(state):
        hole = 0
        for i in state:
            if state[i] == 0:
                hole = i
        return(hole)
        
    def up(state):
        tempState = state.copy()
        i = Board.findhole(state)
        if i > (n - 1):
            tempState[i] = state[i - n]
            tempState[i - n] = 0
        return(tempState)
        
    def down(state):
        tempState = state.copy()
        i = Board.findhole(state)
        if i < ((n*n) - n):
            tempState[i] = state[i + n]
            tempState[i + n] = 0
        return(tempState)
        
    def left(state):
        tempState = state.copy()
        i = Board.findhole(state)
        if (i % n != 0):        #if i > 0
            tempState[i] = state[i - 1]
            tempState[i - 1] = 0
        return(tempState)
        
    def right(state):
        tempState = state.copy()
        i = Board.findhole(tempState)     
        if (i < ((n*n) - 1)):       #if i < 8
            tempState[i] = state[i + 1]
            tempState[i + 1] = 0
        return(tempState)

    def showState(state):
        print("----------")
        print(state[0], " ", state[1], " ", state[2])
        print(state[3], " ", state[4], " ", state[5])
        print(state[6], " ", state[7], " ", state[8])
        return
    
    def uploadState(state):
        tempString = "\n--------\n"
        for i in range(0,n):
            if state[i] == 0:
                tempString += "   "
            else:
                tempString += str(state[i]) + "  "
        puzzlelog.write(tempString)
        
        tempString = "\n"
        for i in range(n,(n*2)):
            if state[i] == 0:
                tempString += "   "
            else:
                tempString += str(state[i]) + "  "
        puzzlelog.write(tempString)
        
        tempString = "\n"
        for i in range((n*2),(n*n)):
            if state[i] == 0:
                tempString += "   "
            else:
                tempString += str(state[i]) + "  "
        puzzlelog.write(tempString)
        return
    
class Solver():
    def heuristicSolve(state):
        nextState = state.copy()
        newState = nextState.copy()
        prevState = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        turnCount = 0
        
        while True:
            
            if Board.equals(nextState, winningState):
                print("Boardstate matched with goal state. Uploading sequence...")
                break
            elif (Solver.isSolvable(turnCount) == False):
                print("Boardstate not solveable!")
                break
            
            nextState = Board.A_neighbors(newState, prevState, turnCount)
            
            Board.showState(nextState)
            Board.uploadState(nextState)
            
            prevState = newState.copy()
            newState = nextState.copy()
            turnCount += 1
            
        return(turnCount)
        
    def uninformedSolve(state):     #Breadth-first search
        currentState = state.copy()
        prev_state = []
        neighbors = Board.FindNeighbors(currentState)
        
        global u_turncount
        u_turncount = 0
        
        while True:
            if(Board.iterate(currentState, prev_state, neighbors) == True):
                break                       
        
        turnCount = u_turncount
        return(turnCount)
        
    def isSolvable(turnCount):
        if turnCount == 10000:
            return False
        else:
            return True    

#Main driver function
class n_puzzle():
    state = pre_state.copy()
    
    print("INITIAL STATE: ")
    Board.showState(state)
    
    #heuristic search solver
    heuristicSolver = Solver
    
    #uninformed search solver
    uninformedSolver = Solver
    
    #Begin timer to solve heuristic search
    H_time_start = time.perf_counter()
    
    #run heuristic solver
    H_turns = heuristicSolver.heuristicSolve(state)
    
    H_time_end = time.perf_counter()
    H_time = H_time_end - H_time_start
    
    #output heuristic search results
    print("\nHEURISTIC SEARCH SOLVE: ")
    readData(H_turns, H_time)
    
    print("\nHEURISTIC SEARCH STEPS UPLOADED TO 8PUZZLELOG.TXT")
    print("\n\nRUNNING UNINFORMED SEARCH. PLEASE WAIT.")
    
    #if H_turns >= 10000, then problem.isSolved returned false.
    if(H_turns >= 10000):
        print("UNINFORMED SEARCH UNAVAILABLE; PROBLEM CANNOT BE SOLVED")
    else:
        #Begin timer to solve uninformed search
        U_time_start = time.perf_counter()
         
        #run uninformed solver
        U_turns = heuristicSolver.uninformedSolve(state)
        
        U_time_end = time.perf_counter()
        U_time = U_time_end - U_time_start
    
        #compare data between heuristic search and uninformed search
        print("UNINFORMED SEARCH SOLVE: ")
        readData(U_turns, U_time)
        
        timeDiff = U_time - H_time
        if(timeDiff > 0):
            print(f"\nThe heuristic search was {timeDiff:0.4f}s faster than the uninformed search.")
        elif(timeDiff < 0):
            timeDiff *= -1
            print(f"\nThe heuristic search was {timeDiff:0.4f}s slower than the uninformed search.")


n_puzzle()
