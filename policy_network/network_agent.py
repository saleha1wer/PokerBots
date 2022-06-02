
import numpy as np
from pokerface import PokerPlayer
from policy_network.utils.game2array import game2array
from policy_network.utils.one_hot_action import decode_action

"""
not complete - write one_hot_action functions
"""
class NetworkAgent(PokerPlayer):
    def __init__(self, game,network):
        super().__init__(game)
        self.network = network
    
    def act(self):
        game_array, opponent_array = game2array(self.game,self)
        sample = [game_array.reshape(1,-1), opponent_array.reshape(1,-1)]
        act_dis = self.network.network.predict(sample)
        act_dis = act_dis[0]
        print(act_dis)
        # mask ilegal actions with 0
        act_dis = self.mask_actions(act_dis)
        action_idx = np.argmax(act_dis)
        action,value = decode_action(action_idx,act_dis[action_idx],self)
        if action == self.bet_raise:
            self.bet_raise(value)
        else:
            action()

    def mask_actions(self,act_distribution):
        if not self.can_fold():
            act_distribution[0] = 0 

        if not self.can_check_call(): # no check or call 
            act_distribution[1] = 0 
            act_distribution[2] = 0 

        if self.can_check_call() and self.check_call_amount == 0: # can check but no call
            act_distribution[2] = 0

        if self.can_check_call() and self.check_call_amount > 0: # can call but no check
            act_distribution[1] = 0

        if not self.can_bet_raise():
            act_distribution[3] = 0 
        return act_distribution

        






