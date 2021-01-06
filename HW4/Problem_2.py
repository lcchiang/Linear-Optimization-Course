# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 10:00:30 2020

@author: Luke Chiang
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

arrivals = {}
for k in range(10**5):
    arrivals[k] = np.random.normal(50,10,5)


thresholds = {}
for num in range(len(arrivals[0])-1,0,-1):
    exp_score = 0
    count = 0
    if num == len(arrivals[0])-1:
        for trial in arrivals.values():
            for score in trial:
                exp_score += score
                count += 1
        exp_score = exp_score/count
        thresholds[num] = exp_score
    else:
        for trial in arrivals.values():
            for score in trial:
                if score > thresholds[num+1]:
                    exp_score += score
                    count += 1
        exp_score = exp_score/count
        prob = norm.cdf((thresholds[num+1]-50)/10)
        thresholds[num] = prob*exp_score + (1-prob)*thresholds[num+1]

for num in range(1,len(arrivals[0])):
        print('Round', num, 'threshold =', thresholds[num])

"""
For  Part A

prob = (100 - thresholds[num+1])/100

"""
