# -*- coding: utf-8 -*-
"""
Created on Mon May  6 09:12:09 2019

@author: md131
"""

def greedySum(L, s):
    """ input: s, positive integer, what the sum should add up to
               L, list of unique positive integers sorted in descending order
        Use the greedy approach where you find the largest multiplier for 
        the largest value in L then for the second largest, and so on to 
        solve the equation s = L[0]*m_0 + L[1]*m_1 + ... + L[n-1]*m_(n-1)
        return: the sum of the multipliers or "no solution" if greedy approach does 
                not yield a set of multipliers such that the equation sums to 's'
    """  
    Lcopy = L.copy()
    multList = []
    result = 0      
   
    for i in range(len(Lcopy)):
        num = Lcopy[i]
        multiplier = 0
        multList.append(multiplier)
        
        
        while result <= s:
            multiplier += 1
            resultNow = num + result
            
            if resultNow < s:
                result = resultNow
                
                try:
                    multList[i] = multiplier
                except:
                    multList.append(multiplier)
                
            elif resultNow == s:
                result = resultNow
                
                try:
                    multList[i] = multiplier
                except:
                    multList.append(multiplier)
                    
                return (sum(multList[:]))
            
            else:
                break
                       
    return ("no solution") #print('No', multList, sum(multList[:]))              

# Potential inputs to greedySum

L = [10, 9, 4, 2]
#(10, 9, 4, 2) should give [2, 0, 1, 1] for s = 27

s = 27 # optimal answer is 10*1 + 9*0 + 5*1 + 4*3
# real answer is 10*2 + 5*1
print(greedySum(L, s))