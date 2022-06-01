# -*- coding: utf-8 -*-
"""
Created on Wed May 11 20:34:49 2022

@author: NatBr
"""

from Ranges import Rangeselection

player_range = {
    }

possible_hands = {
    }

positions = { #Button is 0 and each iterator up is one right of the button, therefore sb = 1, bb = 2, etc. 
    }

def hands(player,opp):
        HandRange = Rangeselection(opp, player_range[player])
        return HandRange
    
def PreFlopAO(n):
    IndexOrder = []
    if(n == 2):
        order = [0,1]
    if(n == 3):
        order = [0,1,2]
    if(n == 4):
        order = [3,0,1,2]
    if(n == 5):
        order = [3,4,0,1,2]
    if(n == 6):
        order = [3,4,5,0,1,2]
    if(n == 7):
        order = [3,4,5,6,0,1,2]
    if(n == 8):
        order = [3,4,5,6,7,0,1,2]
    if(n == 9):
        order = [3,4,5,6,7,8,0,1,2]
    
    for i in order:
        for key, value in positions.items():
            if(i == value):
                IndexOrder.append(key)
    return IndexOrder
    
def getpositions(button,n):
    print("THE BUTTON IS:", button)
    positions.clear()
    print(n)
    position = 0
    #if(button != -1):
    for i in range(button,n):
        positions[i] = position
        position += 1
    if(button != 0):
        for i in range(button):
            positions[i] = position
            position += 1
    """else:
        positions[n-1] = position
        position += 1
        for i in range(n-1):
            positions[i] = position
            position += 1"""
    print(positions)
    return

def Positiontranslator(position,n):
    real_position = ""
    if(n == 2):
        if(position == 0):
            real_position = "sb"
        elif(position == 1):
            real_position = "bb"
    elif(n == 3):
        if(position == 0):
            real_position = "button"
        elif(position == 1):
            real_position = "sb"
        elif(position == 2):
            real_position = "bb"   
    elif(n == 4):
        if(position == 0):
            real_position = "button"
        elif(position == 1):
            real_position = "sb"
        elif(position == 2):
            real_position = "bb"   
        elif(position == 3):
            real_position = "CO"
    elif(n == 5):
        if(position == 0):
            real_position = "button"
        elif(position == 1):
            real_position = "sb"
        elif(position == 2):
            real_position = "bb"   
        elif(position == 3):
            real_position = "HJ"
        elif(position == 4):
            real_position = "CO"
    elif(n == 6):
        if(position == 0):
            real_position = "button"
        elif(position == 1):
            real_position = "sb"
        elif(position == 2):
            real_position = "bb"   
        elif(position == 3):
            real_position = "LJ"
        elif(position == 4):
            real_position = "HJ"
        elif(position == 5):
            real_position = "CO"
    elif(n == 7):
        if(position == 0):
            real_position = "button"
        elif(position == 1):
            real_position = "sb"
        elif(position == 2):
            real_position = "bb"   
        elif(position == 3):
            real_position = "UTG+2"
        elif(position == 4):
            real_position = "LJ"
        elif(position == 5):
            real_position = "HJ"
        elif(position == 6):
            real_position = "CO"
    elif(n == 8):
        if(position == 0):
            real_position = "button"
        elif(position == 1):
            real_position = "sb"
        elif(position == 2):
            real_position = "bb"   
        elif(position == 3):
            real_position = "UTG+1"
        elif(position == 4):
            real_position = "UTG+2"
        elif(position == 5):
            real_position = "LJ"
        elif(position == 6):
            real_position = "HJ"
        elif(position == 7):
            real_position = "CO"
    elif(n == 9):
        if(position == 0):
            real_position = "button"
        elif(position == 1):
            real_position = "sb"
        elif(position == 2):
            real_position = "bb"   
        elif(position == 3):
            real_position = "UTG"
        elif(position == 4):
            real_position = "UTG+1"
        elif(position == 5):
            real_position = "UTG+2"
        elif(position == 6):
            real_position = "LJ"
        elif(position == 7):
            real_position = "HJ"
        elif(position == 8):
            real_position = "CO"
    return real_position