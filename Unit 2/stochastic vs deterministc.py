# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 16:23:52 2019

@author: md131
"""
import random

mylist = []

# this is stochastic: it will return a list of 7's, but
# the lenth of the list is determined by a stochastic variable (the first call to
# (random.randint()). Usually, the run of the program will return a list of 7's
# and every run after that will return a single 7. Restart the kernal to reset this.
for i in range(random.randint(1, 10)):
    random.seed(0)
    if random.randint(1, 10) > 3:
        number = random.randint(1, 10)
        mylist.append(number)
print(mylist)

mylist2 = []
# this is deterministic, it will always return [7] because of the second if statement
for i in range(random.randint(1, 10)):
    random.seed(0)
    if random.randint(1, 10) > 3:
        number = random.randint(1, 10)
        if number not in mylist2:
            mylist2.append(number)
print(mylist2)