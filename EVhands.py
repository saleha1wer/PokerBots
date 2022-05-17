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

def hands(player,opp):
        HandRange = Rangeselection(opp, player_range[player])
        return HandRange