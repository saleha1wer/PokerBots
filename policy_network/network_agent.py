
import numpy as np
from pokerface import PokerPlayer
from policy_network.utils.game2array import game2array
from policy_network.utils.one_hot_action import decode_action

"""
not complete - write one_hot_action functions
"""
class NetworkAgent(PokerPlayer):
    def __init__(self, game,network,agent_id):
        super().__init__(game)
        self.network = network
        self.id = agent_id
        self.max_opp = int(network.network.input[1].shape[1]/2)
    
    def act(self):
        game_array, opponent_array = game2array(self.game,self,max_players=self.max_opp,starting_stack=self.starting_stack)
        sample = [game_array.reshape(1,-1), opponent_array.reshape(1,-1)]
        temp = self.network.network.predict(sample)
        act_dis = temp[0][0]
        scaled_bet = temp[1][0]
        # mask ilegal actions with 0
        act_dis = np.append(act_dis,scaled_bet)
        act_dis = self.mask_actions(act_dis)
        action_idx = np.argmax(act_dis[:4])
        action,bet_value = decode_action(action_idx,scaled_bet,self)
        if action == self.bet_raise:
            self.bet_raise(bet_value)
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
            act_distribution[4] = 0 

        return act_distribution

        






