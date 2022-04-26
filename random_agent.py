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
        actions = ['fold', 'check_call', 'bet_raise', 'discard_draw', 'showdown']
        weight_options = [0.1, 0.5, (0.1, 0.3), 0.05, 0.05]

        possible_actions = []
        weights = []

        for i in range(len(actions)):
            can_action = 'can_' + actions[i]

            if can_action == 'can_bet_raise':
                # Select a random possible raise value; allows for all-in
                maximum = min(self.stack, self.bet_raise_max_amount + self.game.stakes.small_bet)
                if maximum <= self.bet_raise_min_amount:
                    chips_raise = self.stack
                else:
                    chips_raise = random.randrange(self.bet_raise_min_amount, maximum)

                possible_actions.append(getattr(self, actions[i]))
                if chips_raise == maximum:
                    weights.append(weight_options[i][0])
                else:
                    weights.append(weight_options[i][1])
            else:
                if getattr(self, can_action):
                    possible_actions.append(getattr(self, actions[i]))
                    weights.append(weight_options[i])

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