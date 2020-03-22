# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 17:25:42 2020

@author: MehmetSanisoglu
"""
import numpy as np
import generate

currentState = np.array([[1,2,3],[4,5,6],[7,8,-1]])
goalState = np.array([[1,2,3],[4,5,6],[7,8,-1]])

generatedPuzzles = []   #LIST TO STORE THE GENERATED PUZZLES
generate.generatePuzzle(generatedPuzzles,currentState)    #GENERATE THE PUZZLES AND STORE THEM
solutions = []

def copy( mat ):    #MAKES A COPY OF THE INPUTTED STATE MATRIX
    copyMat = np.array([[0,0,0],[0,0,0],[0,0,0]])
    i=0 #Row
    j=0 #Column

    while( i<=2 and j<=2):  #COPY CONTENTS
        copyMat[i][j] = mat[i][j]

        if(j==2):
            j = 0
            i += 1
        else:
            j += 1

    return copyMat

def copyPath( path ):   #MAKE A COPY OF THE INPUTTED PATH
    copyPath = []
    size = len(path)
    for i in range(size):
        copyState = [ path[i][0], copy(path[i][1]) ]
        copyPath.append(copyState )

    return copyPath

def calculateMisplaced(state1): #HEURISTIC METHOD, CALCULATES THE NUMBER OF MISPLACEMENTS

    goal = np.array([[1,2,3],[4,5,6],[7,8,-1]])
    i=0 #Row
    j=0 #Column

    count = 0
    while( i<=2 and j<=2):
        if( state1[i][j] != goal[i][j] ):
            count += 1

        if(j==2):
            j = 0
            i += 1
        else:
            j += 1

    return count

def comparePaths(path1, path2): #COMPARE TWO PATHS, RETURN TRUE IF THEY ARE SAME

    len1 = len(path1)
    len2 = len(path2)

    if(len1 != len2):
        return False    #PATHS OF UNEQUAL SIZES CANNOT BE SAME

    for i in range(len1):   #CHECK EVERY STATE IN BOTH PATHS

        if(generate.compareStates( path1[i][1], path2[i][1]) ):    #IF THEY ARE SAME KEEP LOOKING
            pass
        else:           #IF AT LEAST ONE DIFFERENT, THEY ARE DIFFERENT
            return False

    return True         #ITERATED OVER THE WHOLE PATH AND THEY ARE THE SAME

def checkPath( path ):  #CHECKS WHETHER THE INPUTTED PATH RESULTS IN TARGET STATE
    endState = path[-1][1]
    return generate.compareStates( endState, goalState )


def findPossibilities( path ):  #FINDS ALL THE POSSIBLE STATES THAT CAN BE REACHED
                                #FROM THE TERMINAL STATE OF THE INPUTTED PATH
    possibilities = []
    soFar = copyPath( path )        #MAKE A COPY
    terminal = copy(soFar[-1][1])   #THE LAST STATE OF THE PATH

    for i in range(9):  #ITERATE THE BOXES 1 TO 9
        x = int(i/3)
        y = i % 3

        temp = copy(terminal)   #COPY THE TERMINAL TO CALCULATE OTHER POSSIBILITIES
        tempSoFar = copyPath(soFar) #COPY THE SOFAR TO CALCULATE OTHER POSSIBILITIES

        if( generate.up(temp, x, y) ):    #TRY UP
            score = calculateMisplaced(temp)    #CALCULATE THE MISPLACEMENT OF NEW STATE
            new = [score,temp]                  #COMBINE SCORE WITH THE NEW STATE ITSELF
            tempSoFar.append(new)               #ADD THIS TO THE PATH SOFAR
            possibilities.append(tempSoFar)     #ADD THIS POSSIBLE PATH TO POSSIBILITIES
            temp = copy(terminal)               #RESET TEMP
            tempSoFar = copyPath(soFar)         #RESET SOFAR

        if( generate.down(temp, x, y) ):
            score = calculateMisplaced(temp)
            new = [score,temp]
            tempSoFar.append(new)
            possibilities.append(tempSoFar)
            temp = copy(terminal)
            tempSoFar = copyPath(soFar)

        if( generate.right(temp, x, y) ):
            score = calculateMisplaced(temp)
            new = [score,temp]
            tempSoFar.append(new)
            possibilities.append(tempSoFar)
            temp = copy(terminal)
            tempSoFar = copyPath(soFar)

        if( generate.left(temp, x, y) ):
            score = calculateMisplaced(temp)
            new = [score,temp]
            tempSoFar.append(new)
            possibilities.append(tempSoFar)

    return possibilities

def checkLoop ( path ):    #CHECKS WHETHER THERE IS A LOOP OR NOT IN THE INPUT PATH
    size = len(path)

    for i in range(size):
        j= i+1
        while( j < size):
            if(generate.compareStates (path[i][1] , path[j][1]) ): #IF WE ENCOUNTER ANY LOOPS
                    return True
            else:    #CHECK THE NEXT ONE
                j += 1
    return False

def removeLoops( possiblePaths ):   #REMOVES THE PATHS WITH LOOPS
    removedVersion = []
    for each in possiblePaths:
        check = checkLoop(each)     #IS THERE A LOOP IN THIS PATH?
        if(check == False):         #IF NO LOOPS
            removedVersion.append(each)

    return removedVersion

def removeLongers( possiblePaths ): #REMOVES THE PATHS THAT REACH THE SAME STATE
                                    #BUT HAVE LONGER PATH LENGTH
    removedVersion = []
    size = len(possiblePaths)

    for i in range(size):       #FOR EVERY INSPECTED PATH
        noMatch = True
        removedSize = len(removedVersion)

        for j in range(removedSize):    #ITERATE OVER THE SHORTENED LIST
            if( generate.compareStates( possiblePaths[i][-1][1] , removedVersion[j][-1][1]) ): #CHECK IF WE HAVE ADDED A PATH WITH SAME TERMINAL
                noMatch = False #WE HAVE ENCOUNTERED A MATCH
                len1 = len(removedVersion[j])   #THE LENGTH OF THE ALREADY ADDED ONE
                len2 = len(possiblePaths[i])    #THE LENGTH OF CANDIDATE PATH

                if(len2 < len1):    #IF THE CANDIDATE ONE IS SHORTER THAN THE ONE IN THE REMOVED LIST
                    removedVersion[j] = possiblePaths[i]    #CHANGE THE ONE IN THE SHORTENED LIST WITH THE "SHORTER PATH"

                else:    #IF THIS PATH HAS THE SAME TERMINAL STATE, BUT IT ISN'T THE SHORTEST ONE, NO NEED TO CHECK MORE
                    break
        if(noMatch):
            removedVersion.append(possiblePaths[i])

    return removedVersion

def getCost(path):     #CALCULATE THE COST SCORES ( TO ORDER IN THE QUEUE )
    return len(path) + path[-1][0]

def orderPaths( paths ):    #ORDER THE GIVEN PATHS BASED ON THEIR COST
    ordered = []

    for each in paths:          #ITERATE OVER EACH PATH
        score = getCost(each)   #GET THE COST OF CURRENT PATH
        size = len(ordered)

        correctIndex = 0        #NEED TO FIND THE CORRECT INDEX TO PLACE THIS PATH

        for i in range(size):   #ITERATE THE ALREADY ORDERED LIST

            if( score <= getCost(ordered[i]) ):  #IF WE HAVE A BETTER SCORE THAN THE INDEX AT ORDERED
                correctIndex = i
                ordered.insert(correctIndex, each)
                break

            else:
                correctIndex += 1

        if(correctIndex == size):
            ordered.insert(correctIndex, each)

    return ordered

def addToFront( queue, paths):
    pathsList = paths
    pathsList.reverse()
    size = len(paths)

    for i in range(size):
        queue.insert(0,pathsList[i])

    return

def solve(r, goalState):

    path  = copyPath(r)
    queue = [ path ]

    count = 0
    while( not checkPath(queue[0]) and len(queue)!=0 ):

        frontPath = queue.pop(0)                        #GET THE PATH IN FRONT OF THE QUEUE (ALSO THE SHORTEST ONE)
        possibilities = findPossibilities(frontPath)    #EXPAND IT TO THE POSSIBLE PATHS
        loopsRemoved = removeLoops(possibilities)       #REMOVE THE LOOPS FROM THEM
        addToFront( queue, loopsRemoved )               #ADD THESE NEW PATHS TO THE QUEUE
        longersRemoved = removeLongers(queue)           #REMOVE UNNECESSAIRLY LONGER ONES FROM THEM
        queue = orderPaths(longersRemoved)              #ORDER THE QUEUE WITH LOWER COST ONES IN FRONT

        count += 1
    print(count, "Tur sürdü")
    return queue[0]


#SOLVE EACH PUZZLE
index = 0
for each in generatedPuzzles:
    print("Puzzle No",index)
    testInput = [[calculateMisplaced(each), each]]
    solutionSteps = solve( testInput, goalState )
    solutions.append(solutionSteps)
    index += 1
