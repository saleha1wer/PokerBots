"""
action array --> [fold,check,call,bet] types --> [binary,binary,binary,0-1 -fraction of stack to bet]
"""

def encode_action(action):
    pass

def decode_action(action_idx,value,player):
    if action_idx == 0:
        return player.fold,1
    elif action_idx == 1:
        return player.check_call,1
    elif action_idx == 2:
        return player.check_call,1
    elif action_idx == 3:
        return player.bet_raise, int(value * (player.bet_raise_max_amount - player.bet_raise_min_amount)) + player.bet_raise_min_amount
