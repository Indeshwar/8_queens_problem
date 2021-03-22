#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Beyond search homework. hill climbing algorithm and simulating annealing used to solve 8 queens problem """
"""
Created on Mon Mar  1 00:07:19 2021

__author__ = "indeshwar chaudhary"
"""
import random
import math
import sys

def generator_board():
    #generate the random position of queen in the board
    board =[random.randint(1,8) for x in range(8)]
    
    return board

def heuristic_board(board):
    #store the number of heuristic
    count_heuristic = 0
    n = len(board)
    for i in range(n-1): 
        k = i+1
        while k < n:
            #b1 and b2 store the position of queens
            b1 = board[i] - 1    
            b2 = board[k] -1
            if b1 == b2:            #check whether two queens in same the row
                count_heuristic = count_heuristic + 1
                
            elif (b1-b2) == (i-k):    #check whether queen is threathend from left diagnol
                count_heuristic = count_heuristic + 1
                
            elif (b1-b2) == (k-i):     #check whether queen is threathend from right diagnol
                count_heuristic = count_heuristic + 1
                
            k = k+1

               
    return count_heuristic

def get_successors(board):
    #create an empty successor list
    successor_board = []
    #copy the element of board in successor_board
    for x in board:
        successor_board.append(x)
    
    #h_1 holds the heuristic of board
    h_1 = heuristic_board(board)  
    
    #temp holds the updated position of queen that can produce best heuristic  
    temp = 0
    #lenth of board
    n = len(board)
    count = 0
    for i in range(n):
        for j in range(n):
            successor_board[i] = j+1
            h_2 = heuristic_board(successor_board)   #h_2 holds the heuristic of successor_board
            count = count+1
            if h_1 == h_2: #if h_1 and h_2 have same heuristic, just update the temp 
                temp = j+1
            
            if h_2 < h_1:   #if h_2 has better heuristic than h_1, update the temp 
                temp = j+1
                h_1 = h_2   #assign h_2 in h_1
                
        successor_board[i] = temp   #update the successor with best position of queen in a column  
    return successor_board, count

def hill_climbing(board):
    #initialize the current with initial problem
    current = board
    count = 0
    while True:
        
        count = count + 1
        #generate the best neibour from current state
        neighbor, c = get_successors(current)
        if heuristic_board(current) <= heuristic_board(neighbor):
            #if current has better heuristic than neighbour, 
            #just return the heuristic of current board and total number of successor board
            return heuristic_board(current), count*c 
        
        #update the current
        current = neighbor

def rand_successor(board):
    suc_board = board[:] #copy the all the queens
    row = random.randint(1,8) #generate random row
    col = random.randint(0,7) #generate random col
    suc_board[col] = row
    return suc_board
    

def sigmoid(deltaE, T):
    exp = math.exp(deltaE/T)
    sig = 1/(1+exp)
    return sig

def simulated_annealling(board):
    #initialize the current with initial state problem
    current = board
    #initialize the T
    T = 4000
    factor = 0.99
    count = 0
    
    while  True:
        T *= factor                               # T is dcreased by 0.99
        count = count+1                           #count the number of successor board generated
        if T < 0.015:                               #termination condition
            return heuristic_board(current),count
        
        next =  rand_successor(current)           #generate random successor of current
        
        deltaE = heuristic_board(next) - heuristic_board(current)  #compute the difference of heurestic of next and current
        
        sig = sigmoid(deltaE, T) #compute the probality
        
        if deltaE < 0:
            current = next[:] #copy from the next
            
            if heuristic_board(current) == 0: # if solution found, return the heureistic of current and number of successor board generated
                return heuristic_board(current),count
        
        elif random.uniform(0, 1) < sig: #choose successor_board based on some probability
            current = next[:] #copy from the next
           
   
def main(num):
    count = 0          #it represent number of puzzle
    num_of_problem_slvd_in_hill_climb = 0  #it represent number of problem solved by hill climbing algorithm
    num_of_problem_slvd_in_sim_annealing = 0 #it represent number of problem solved by simulating annealling algorithm
    total_successor_1 = 0   #it represent total number of successor of hill climbing algorithm
    total_successor_2 = 0   #it represent total number of successor of simulating annealling
   
    while count < num:
        board = generator_board()
        h,c_1 = hill_climbing(board)
        s_A,c_2 = simulated_annealling(board)
        if h == 0:
            num_of_problem_slvd_in_hill_climb = num_of_problem_slvd_in_hill_climb + 1
            
        if s_A == 0:
            num_of_problem_slvd_in_sim_annealing = num_of_problem_slvd_in_sim_annealing + 1
        count = count + 1        
        total_successor_1 = total_successor_1 + c_1  #count the total successor of board hill climbing algorithm
        total_successor_2 = total_successor_2 + c_2  #count the total successor of simulating annealling algorithm
    
    print("Hill Climbing: ", (num_of_problem_slvd_in_hill_climb/count)*100, "% solved", ", average search cost: ", (total_successor_1/count))
    print("Simm. Annelling: ", (num_of_problem_slvd_in_sim_annealing/count)*100, "% solved", ", average search cost: ", (total_successor_2/count))
   


num = int(sys.argv[1])
main(num)



    