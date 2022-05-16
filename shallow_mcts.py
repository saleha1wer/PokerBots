from cgitb import reset
import numpy as np
import copy
from pokerface import *
from random_agent import RandomAgent
from random import Random, shuffle
from game_actions import deal_board, deal_cards, bet_stage, showdown_stage

class ShallowMCTS(PokerPlayer):
    def __init__(self, game):
        super().__init__(game)
        # Set number of simulations per action
        self.n_sims_per_action = 500
        self.agent_index = 0
        self.reset_player_index(self.game)

    def get_possible_actions(self, game):
        # Return a list of possible actions
        possible_actions = []
        if self.can_check_call():
            possible_actions.append(["check_call"])
        for i in [1/4, 2/4, 3/4, 1]:
            if self.can_bet_raise():           
                raise_amount = max(min(self.stack, int(i * game.pot)), self.bet_raise_min_amount)
                if self.can_bet_raise(raise_amount):
                    raise_action = ["raise", raise_amount]
                    if raise_action not in possible_actions:
                        possible_actions.append(raise_action)
        if self.can_fold():
            possible_actions.append(["fold"])
        return possible_actions
    
    def reset_player_index(self, game):
        # Update player index value to the value linked in the game
        for i, player in enumerate(game.players):
            if player == self:
                self.agent_index = i

    def set_players2random(self, game):
        # TODO: this function has to turn the pokeragents into random bots
                
        # for p in game.players:
        #     p.act = self.callbot2copy.act
        return game
    
    def shuffle_opponents(self, game):
        index2skip = []
        # Add opponent cards to deck
        for i, p in enumerate(game.players):
            if i != self.agent_index:
                if len(p.hole) == 2:
                    game._deck.append(p.hole[0])
                    game._deck.append(p.hole[1])
                else:
                    # Opponent has folded and doesnt have cards
                    index2skip.append(i)

        # Shuffle deck
        shuffle(game._deck)

        # Redeal cards to opponents
        for i, p in enumerate(game.players):
            if i != self.agent_index and i not in index2skip:
                p._hole = tuple(game._deck.draw(2))
        return game
    
    def playout(self, game):
        # Perform simulations of an action with different cards
        results = []
        for i in range(self.n_sims_per_action):
            # print("performing simulation", i)
            playout_copy = copy.deepcopy(game)
            playout_copy = self.shuffle_opponents(playout_copy)

            # TODO: THE FOLLOWING STILL NEEDS TO BE MADE INTO RANDOM ACTIONS NOT CALLING
            # Preferably, this synergises with set_players2random
            while playout_copy.stage != None:
                for p in playout_copy.players:
                    if p.can_check_call():
                        p.check_call()
                    if p.can_showdown():
                        p.showdown()
                if playout_copy.nature.can_deal_board():
                    playout_copy.nature.deal_board()
            results.append(playout_copy.players[self.agent_index].payoff)
        # res = (len([ele for ele in test_list if ele > 0]) / len(test_list))
        return np.mean(results)

    def act(self):
        print("sMCTS is evaluating options, this takes a couple of seconds")
        # print("SMCTS has", self.hole, "\tBoard is", self.game.board)
        game_copy = copy.deepcopy(self.game)
        game_copy._verify()
        self.reset_player_index(self.game)
        action_scores = []

        game_copy = self.set_players2random(game_copy)
        possible_actions = self.get_possible_actions(game_copy)

        for action in possible_actions:
            reset_state = copy.deepcopy(game_copy)
            reset_state._verify()
            if action[0] == "fold":
                reset_state.players[self.agent_index].fold()
            elif action[0] == "check_call":
                reset_state.players[self.agent_index].check_call()
            elif action[0] == "raise":
                reset_state.players[self.agent_index].bet_raise(action[1])
            
            action_score = self.playout(reset_state)
            action_scores.append(action_score)
            print(action, action_score)
            
        best_action_i = np.argmax(action_scores)
        best_action = possible_actions[best_action_i]

        if best_action[0] == "fold":
            self.fold()
            print("SMCTS:\t\t folds")

        elif best_action[0] == "check_call":
            self.check_call()
            print("SMCTS:\t\t calls")

        elif best_action[0] == "raise":
            self.bet_raise(best_action[1])
            print("SMCTS:\t\t raises", best_action[1])
