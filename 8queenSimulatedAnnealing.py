#-----------------------------------------------------------------------
#Author: Christian Tran
#R number: R#11641653
#Assignment 2
#-----------------------------------------------------------------------
#Solve the 8 queen problem by using simulated annealing.
# 8 queen problem:
# there are 8 queens on a chess board (board is represented in a dimension of 8x8)
# objective:
# create a board that has 8 queens on it where all 8 queens do not attack each other.
# Queens:
# queens can move vertically, diagonally, and horizontal.
# Assumption: 
# since queens cannot attack each other, we need them to not be:
#   -on the same row
#   -on the same column
#   -diagonal to any other
# queens can only move in their individual column. Each row will be assigned a numerical value of 0 to 7 (8 in total)
#-----------------------------------------------------------------------
import random #For random number generation
import math #For calculations
import matplotlib.pyplot as plt

total_queens = 8 #Total number of queens on the chess board

#getRandChess() function
# - Used to generate a random starting board
def getRandChess():
    board_list = [] #initial empty chess board array
    
    #Fills up the empty list with random starting positions
    for i in range(0, total_queens):
        rand_pos = random.randint(1, total_queens) #random positions from 1 to 8 respectively
        board_list.append(rand_pos)

    return board_list

#detectQueenAttack
# - Checks if the starting_board has any queens that are attacking each other and returns the total number found
def detectQueenAttack(starting_board):
    row_queen_attack = 0
    diag_queen_attack = 0
    #Detect rows
    for row in range(0, len(starting_board) - 1):
        for next_row in range(row+1, len(starting_board)):
            if(starting_board[row] == starting_board[next_row]):
                row_queen_attack = row_queen_attack + 1  #Iterates through the chess board and sees if any of the queens are on the same row (if they equal the same number then add 1 to the counter)

    #print("row attacks = " + str(row_queen_attack)) #Test print for row counter

    #Detect diagonals 
    for row2 in range(0, len(starting_board) - 1):
        for next_row2 in range(row2+1, len(starting_board)):
            if(not(starting_board[row2] == starting_board[next_row2]) and (abs(starting_board[row2] - starting_board[next_row2]) == abs(row2 - next_row2))):
                diag_queen_attack = diag_queen_attack + 1 #Checks to see if they are on the same diag with diag detecting formula for queen

    #print("diag attacks = " + str(diag_queen_attack))

    queen_attack_total = row_queen_attack + diag_queen_attack #Total number of attacks detected

    return queen_attack_total


#Main() function
def Main():
    starting_board = getRandChess() #Generate starting chess board with random queen positions

    starting_queens_attacking = detectQueenAttack(starting_board) #Gets the number of queens attacking each other (cannot be in the same column, so check row and diagonals)
    
    print("Starting State: ")
    print(str(starting_board))
    print("Detected Queens that can attack: "+str(starting_queens_attacking))

    #Use simulated annealing to generate solution for 8 queen problem
    #Following the algorithm:
    #Note: The initial state we just generated (starting_board) is now considered our "current" state and cost
    x_axis = [] #For plotting
    y_axis = [] 

    current_state = starting_board #state itself
    current_cost = starting_queens_attacking #cost from the initial state
    Temperature = 18000 #Some large positive value
    boolean_solution_flag = False #This is used to flag if the program obtained the correct solution or not

    while Temperature > 0: #While the temperature is greater than (some low value)
        random_num = random.uniform(0,1) #Generate random number to compare if our probability_p WITH temperature is a good decision with this specific iteration

        next_neighbor_board = getRandChess() #Generate a random next neighbor state

        next_neighbor_queens_attacking = detectQueenAttack(next_neighbor_board) #Get the cost of the next random neighbor state

        delt_C = next_neighbor_queens_attacking - current_cost #calculate delta C (the cost of next_neighbor - current_cost)


        #Check if the solution has been found:
        if current_cost == 0:
            #Return current state
            print("Final State CORRECT: ")
            print(current_state)
            print("Detected Queens that can attack : "+str(current_cost))
            boolean_solution_flag = True #Turn true if the solution is found 
            break
        
        if delt_C < 0: #If the next_neighbor state is an improvement (when delt_C is compared to 0, meaning that the current state's cost was higher than the next_neighbor) switch the current state to the next neighbor
            current_state = next_neighbor_board 

            current_cost = next_neighbor_queens_attacking

            #print("IF ACTIVATED")

        else:
            #print("ELSE ACTIVATED")
            probability_p = math.exp(-delt_C / Temperature) #Use the probability formula provided from the algorithm of simulated annealing. Generates a floating number between 0 and 1
            #print("probability_p = "+str(probability_p))
            #print("rand = "+str(random_num))
            if(random_num < probability_p): #If the neighbor is not an improvement, then move to the neighbor probabilistically depending on the probability formula compared to current state
                current_state = next_neighbor_board

                current_cost = next_neighbor_queens_attacking

        x_axis.append(Temperature)
        y_axis.append(current_cost)


        Temperature = Temperature - 1 #Decrease T (Temperature)

        #print("Iteration "+ str(counter))
        #print(current_state)
        #counter = counter + 1

    if(boolean_solution_flag == False):
        #Return current state
        print("Final State WRONG: ")
        print(current_state)
        print("Detected Queens that can attack : "+str(current_cost))

    #Did the plotting for the graph
    plt.plot(x_axis, y_axis, label = "line 1")
    plt.xlabel("X - Axis: Temperature")
    plt.ylabel("Y - Axis: Current Cost")
    plt.title("Temperature over time vs. Cost over time")
    plt.legend()
    plt.show()


#Runs the Main() function
if __name__ == '__main__': 
    Main()