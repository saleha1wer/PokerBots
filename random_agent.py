from pokerface import PokerPlayer
import numpy as np
import random
"""
This is our random agent that will play poker randomly. The class inherits everything
from the PokerPlayer class. The act function is used to select and perform an action.
"""
class RandomAgent(PokerPlayer):
    def __init__(self, game):
        super().__init__(game)
    
    def act(self):
        possible_actions = []
        if self.can_fold(): possible_actions.append(self.fold)
        if self.can_check_call(): possible_actions.append(self.check_call)
        if self.can_bet_raise():
            # Select a random possible raise value 
            chips_raise = random.randrange(self.bet_raise_min_amount, self.bet_raise_max_amount + self.game.stakes.small_bet, self.game.stakes.small_bet)
            possible_actions.append(self.bet_raise)

        if len(possible_actions) != 0:
            # Select random action, maybe should include weights to prevent folding or going all in instantly
            f = np.random.choice(possible_actions)
            if f == self.bet_raise:
                self.bet_raise(chips_raise)
                print('action: ',f.__name__, chips_raise)
            else:
                f()
                print('action: ',f.__name__)
        else:
            # print("No possible actions")
            pass

