from pokerface import PokerPlayer
import numpy as np
import random

"""
This is our random agent that will play poker randomly. The class inherits everything
from the PokerPlayer class. The act function is used to select and perform an action.

TO DO: have a look at the weights we want to use per action
"""


class RandomAgent(PokerPlayer):
    def __init__(self, game):
        super().__init__(game)

    def act(self):
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
            maximum = np.min(self.stack, self.bet_raise_max_amount + self.game.stakes.small_bet)
            if maximum <= self.bet_raise_min_amount:
                chips_raise = self.stack
            else:
                chips_raise = random.randrange(self.bet_raise_min_amount, maximum)

            possible_actions.append(self.bet_raise)
            if chips_raise == maximum:
                weights.append(0.1)
            else:
                weights.append(0.3)

        if self.can_discard_draw():
            possible_actions.append(self.discard_draw)
            weights.append(0.05)

        if self.can_showdown():
            possible_actions.append(self.showdown)
            weights.append(0.05)

        # Normalize weights if they don't sum to 1
        if np.sum(weights) != 1:
            weights = weights / np.sum(weights)

        # Select a random action from the possible_actions list
        if len(possible_actions) != 0:
            f = np.random.choice(possible_actions, p = weights)
            if f == self.bet_raise:
                self.bet_raise(chips_raise)
                print('action: ', f.__name__, chips_raise)
            else:
                f()
                print('action: ', f.__name__)
        else:
            pass

