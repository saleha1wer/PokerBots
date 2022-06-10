from pokerface import PokerPlayer
import numpy as np
import random
from policy_network.utils.one_hot_action import encode_action

"""
This is our random agent that will play poker randomly. The class inherits everything
from the PokerPlayer class. The act function is used to select and perform an action.

TODO: have a look at the weights we want to use per action
"""


class RandomAgent(PokerPlayer):
    def __init__(self, game,agent_id,game_starting_stack=200,max_opp=4):
        super().__init__(game)
        self.id = agent_id
        self.g_starting_stack = game_starting_stack
        self.max_opp = max_opp

    def act(self,return_action=False):
        possible_actions = []
        weights = []

        if self.can_fold():
            possible_actions.append(self.fold)
            weights.append(0.1)

        if self.can_check_call():
            possible_actions.append(self.check_call)
            weights.append(0.5)

        if self.can_bet_raise():
            # Select a random possible raise value; allows for all-in
            maximum = min(self.stack, self.bet_raise_max_amount + self.game.stakes.small_bet)
            if maximum <= self.bet_raise_min_amount:
                # Call if you can only bet less then the minimum bet size
                possible_actions.append(self.check_call)
                weights.append(0.5)

            else:
                betrange = int(maximum) - int(self.bet_raise_min_amount)
                if betrange > 0:
                    chips_raise = random.randrange(int(self.bet_raise_min_amount), int(maximum))
                else: 
                    chips_raise = int(self.bet_raise_min_amount)
                possible_actions.append(self.bet_raise)
                if chips_raise == maximum:
                    weights.append(0.1)
                else:
                    weights.append(0.3)

        #if self.can_discard_draw(): #Not applicable in holdem
        #    possible_actions.append(self.discard_draw)
        #    weights.append(0.05)

        # Normalize weights if they don't sum to 1
        if np.sum(weights) != 1:
            weights = weights / np.sum(weights)
            
        # if self.can_showdown():
        #     f = self.showdown
        #     f()
        #     print("Showdown")
        #    possible_actions.append(self.showdown)
        #    weights.append(0.05)

        # Select a random action from the possible_actions list
        if len(possible_actions) != 0:
            f = np.random.choice(possible_actions, p = weights)
            if f == self.bet_raise:
                act_dis = encode_action(chips_raise,self)
                self.bet_raise(chips_raise)
            else:
                act_dis = encode_action(f,self)
                f()
            if return_action:
                return act_dis
        else:
            pass
