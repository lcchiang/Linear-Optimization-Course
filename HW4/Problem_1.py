# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 20:06:35 2020

@author: Luke Chiang
"""


import numpy as np
import matplotlib.pyplot as plt

values = {('A', 1): 87, ('A', 2): 6, ('A', 3): 81, ('A', 4): 89, ('A', 5): 99, ('A', 6): 8, ('A', 7): 47,
 ('A', 8): 81, ('B', 1): 18, ('B', 2): 17, ('B', 3): 50, ('B', 4): 66, ('B', 5): 91, ('B', 6): 47, ('B', 7): 98,
 ('B', 8): 55, ('C', 1): 21, ('C', 2): 1, ('C', 3): 16, ('C', 4): 9, ('C', 5): 70, ('C', 6): 96, ('C', 7): 93,
 ('C', 8): 34, ('D', 1): 19, ('D', 2): 63, ('D', 3): 52, ('D', 4): 74, ('D', 5): 50, ('D', 6): 5, ('D', 7): 90,
 ('D', 8): 45, ('E', 1): 35, ('E', 2): 3, ('E', 3): 30, ('E', 4): 43, ('E', 5): 62, ('E', 6): 57, ('E', 7): 20,
 ('E', 8): 54, ('F', 1): 51, ('F', 2): 70, ('F', 3): 70, ('F', 4): 49, ('F', 5): 20, ('F', 6): 8, ('F', 7): 5,
 ('F', 8): 92, ('G', 1): 70, ('G', 2): 79, ('G', 3): 21, ('G', 4): 86, ('G', 5): 42, ('G', 6): 76, ('G', 7): 67,
 ('G', 8): 33, ('H', 1): 1, ('H', 2): 26, ('H', 3): 78, ('H', 4): 53, ('H', 5): 39, ('H', 6): 73, ('H', 7): 24,
 ('H', 8): 85}

# Gathering letter and number combo's
letters = []
numbers = []
for square in values:
    if square[0] not in letters:
        letters.append(square[0])
    if square[1] not in numbers:
        numbers.append(square[1])
letters.sort()
numbers.sort()


# Creating blank copy to map the optimal values
opt_val = {}
for char in letters:
    for num in numbers:
        opt_val[char,num] = 0

# filling right most column and bottom most row
previous_val = 0
for char in reversed(letters):
    opt_val[(char,numbers[-1])] = previous_val + values[(char,numbers[-1])]
    previous_val = opt_val[(char,numbers[-1])]
    
previous_val = 0
for num in reversed(numbers):
    opt_val[(letters[-1],num)] = previous_val + values[(letters[-1],num)]
    previous_val = opt_val[(letters[-1],num)]
    
# Filling rest of opt_val matrix
for char in range(len(letters)-1,-1,-1):
    for num in range(len(numbers)-1,-1,-1):
        if opt_val[(letters[char],numbers[num])] == 0:
            opt_val[(letters[char],numbers[num])] = values[(letters[char],numbers[num])] + max(opt_val[(letters[char+1],numbers[num])],opt_val[(letters[char],numbers[num+1])])
print('optimal answer =', opt_val[(letters[0],numbers[0])])


opt_path = []
# Find next optimal path
def next_optimal_pos(char,num):
    pos = (letters[char],numbers[num])
    opt_path.append(pos)
    if pos == (letters[-1],numbers[-1]):
        print('Optimal Path =',opt_path)
        return
    
    if char == (len(letters)-1):
        return next_optimal_pos(char,num+1)
    if num == (len(numbers)-1):
        return next_optimal_pos(char+1,num)
    
    opt_1 = (letters[char+1],numbers[num])
    opt_2 = (letters[char],numbers[num+1])
    if opt_val[opt_1] > opt_val[opt_2]:
        return next_optimal_pos(char+1,num)
    else:
        return next_optimal_pos(char,num+1)

# Finding optimal path
next_optimal_pos(0,0)


