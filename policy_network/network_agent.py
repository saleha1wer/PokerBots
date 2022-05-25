
import imp
import numpy as np
from pokerface import PokerPlayer
from utils.game2array import game2array
from utils.one_hot_action import decode_action
"""
not complete - write one_hot_action functions
"""
class NetworkAgent(PokerPlayer):
    def __init__(self, game,network):
        super().__init__(game)
        self.network = network
    
    def act(self):
        game_array, opponent_array = game2array(self.game,self)
        act_dis = self.network.network.predict(game_array,opponent_array)
        print('action_dis: ', act_dis)
        action_idx = np.argmax(act_dis)
        action = decode_action(action_idx)
        action()




