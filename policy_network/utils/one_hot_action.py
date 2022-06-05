"""
action array --> [fold,check,call,bet,bet ammount] types --> [binary,binary,binary,binary,0-1 -fraction of bet range]
"""

def encode_action(action):
    pass

def decode_action(action_idx,scaled_bet,player):
    if action_idx == 0:
        return player.fold,1
    elif action_idx == 1:
        return player.check_call,1
    elif action_idx == 2:
        return player.check_call,1
    elif action_idx == 3:
        return player.bet_raise, int(scaled_bet * (player.bet_raise_max_amount - player.bet_raise_min_amount)) + player.bet_raise_min_amount
