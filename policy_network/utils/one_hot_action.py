
from pokerface._actions import FoldAction, CheckCallAction, BetRaiseAction

"""
action array --> [fold,check,call,bet,bet ammount] types --> [binary,binary,binary,binary,0-1 -fraction of bet range]
"""


def scale_betamount(player,scaled_bet=None,absolue_bet=None):
    if absolue_bet is None:  # return absolute bet
        return min(player.bet_raise_max_amount, max(int(scaled_bet * (player.bet_raise_max_amount - player.bet_raise_min_amount)) + player.bet_raise_min_amount, player.bet_raise_min_amount))
    elif scaled_bet is None:        # return scaled bet 0-1
        betrange = player.bet_raise_max_amount - player.bet_raise_min_amount
        if betrange == 0:
            return 1
        return (absolue_bet - player.bet_raise_min_amount)/betrange

def encode_action(action,player):
    act_dis = [0,0,0,0,0] # --> [fold,check,call,bet,bet ammount]
    if action==player.fold:
        act_dis[0] = 1
    elif action==player.check_call:
        if player.check_call_amount > 0:
            act_dis[2] = 1
        else:
            act_dis[1] = 1

    elif isinstance(action,int) or isinstance(action,float): 

        act_dis[3] = 1
        act_dis[4] = scale_betamount(player,absolue_bet=action)
    return act_dis



def decode_action(action_idx,scaled_bet,player):
    if action_idx == 0:
        return player.fold,1
    elif action_idx == 1:
        return player.check_call,1
    elif action_idx == 2:
        return player.check_call,1
    elif action_idx == 3:
        return player.bet_raise, scale_betamount(player,scaled_bet=scaled_bet)
