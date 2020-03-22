# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:32:03 2020

@author: MehmetSanisoglu
"""
import random
import numpy as np

currentState = np.array([[1,2,3],[4,5,6],[7,8,-1]])
generatedList = []

def compareStates(state1, state2):
    i=0 #Row
    j=0 #Column

    while( i<=2 and j<=2):
        if( state1[i][j] != state2[i][j] ):
            return False
        else:
            if(j==2):
                j = 0
                i += 1
            else:
                j += 1
    return True


def up(state, row, col):
    newRow = row - 1        #NEW INDECES
    newCol = col

    if(newRow < 0):          #CANNOT PERFORM SUCH AN OPERATION
        return False

    temp = state[newRow][newCol]
    state[newRow][newCol] = state[row][col]
    state[row][col] = temp

    return True

def down(state, row, col):
    newRow = row + 1
    newCol = col

    if(newRow > 2):
        return False

    temp = state[newRow][newCol]
    state[newRow][newCol] = state[row][col]
    state[row][col] = temp

    return True

def right(state, row, col):
    newRow = row
    newCol = col + 1

    if(newCol > 2):
        return False

    temp = state[newRow][newCol]
    state[newRow][newCol] = state[row][col]
    state[row][col] = temp

    return True

def left(state, row, col):
    newRow = row
    newCol = col - 1

    if(newCol < 0):
        return False

    temp = state[newRow][newCol]
    state[newRow][newCol] = state[row][col]
    state[row][col] = temp

    return True

def generatePuzzle(generatedList, state):

    while(len(generatedList)<30 ):  #CREATE 30 PUZZLES

        for i in range(10): #PERFORM 10 VALID OPERATIONS
            randomIndex = random.randrange(0,9,1)   #CHOSE RANDOM INDEX HAVE AN OPERATION ON
            row = int(randomIndex / 3)
            col = randomIndex % 3

            noProb = False
            while( not noProb ):        #IF IT'S OK TO PERFORM
                randomOperation = random.randrange (0,4,1)  #RANDOMIZE THE OPERATION

                if(randomOperation == 0):   #UP
                    result = up(state, row, col)
                elif(randomOperation == 1): #DOWN
                    result = down(state, row, col)
                elif(randomOperation == 2): #RIGHT
                    result = right(state, row, col)
                else:                       #LEFT
                    result = left(state, row, col)

                if(result == True):     #IF WE HAVE PERFORMED A VALID OPERATION
                    noProb = True       #NO NEED TO MAKE ANOTHER OPERATION AGAIN
        alreadyPresent = False

        for each in generatedList:
            if(compareStates(each, state)): #IF WE HAVE ALREADY CREATED THE SAME ONE
                state = np.array([[1,2,3],[4,5,6],[7,8,-1]]) #NEED TO RESET IT
                alreadyPresent = True
                break

        if (not alreadyPresent):
            generatedList.append(state)
            state = np.array([[1,2,3],[4,5,6],[7,8,-1]])     #NEED TO RESET IT


    return generatedList
