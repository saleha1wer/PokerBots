import numpy as np
import copy
from pokerface import PokerPlayer
from random_agent import RandomAgent
from game import deal_board, deal_cards, bet_stage, showdown_stage

# class MCTSNode:
#     def __init__(self, action=None, parent=None):
#         self.parent = parent
#         self.action = action
#         self.childen = []
#         self.evaluations = []
#         self.terminal = False
#         self.fully_expanded = False

#     def q(self):
#         return np.mean(self.evaluations)
        
#     def q(self):
#         return len(self.evaluations)
    
#     def visit(self, score):
#         self.evaluations.append(score)
    
#     def backprop(self, score):
#         self.visit(score)
#         if self.parent != None:
#             self.parent.backprop(score)
    
#     def best_child(self, c_val=0.1):
#         ucb_values = []
#         for child in self.children:
#             ucb_values.append(child.q() / child.n() + c_val * np.sqrt((2 * np.log(self.n()) / child.n())))
#         return self.childen[np.argmax(ucb_values)]
    
#     def best_action(self, c_val=0.1):
#         child = self.best_child(c_val)
#         return child.action



class MCTSAgent(PokerPlayer):
    def __init__(self, game):
        super().__init__(game)
        self.n_simulations = 1000
    
    def get_possible_actions(self, game):
        possible_actions = []
        raises_list = []
        if self.can_fold():
            possible_actions.append(self.fold)
        if self.can_check_call():
            possible_actions.append(self.can_check_call)
        if self.can_bet_raise():
            possible_actions.append(self.bet_raise)
            pot = game.pot
            for i in [1/4, 2/4, 3/4, 1]:
                raise_amount = max(min(self.stack, int(i * pot)), game.stakes.blinds[0])
                if raise_amount not in raises_list:
                    raises_list.append(raise_amount)
        return possible_actions, raises_list

    def make_random_players(self):
        pass

    def reshuffle_hands(self):
        pass

    def playout(self, nls, agent_index):
        prior_stack = nls.players[agent_index].stack
        results = []
        for i in range(self.n_simulations):
            playout_copy = copy.deepcopy(nls)
            playout_copy = deal_cards(playout_copy)
            playout_copy = bet_stage(playout_copy)
            playout_copy = deal_board(playout_copy)
            playout_copy = bet_stage(playout_copy)
            playout_copy = deal_board(playout_copy)
            playout_copy = bet_stage(playout_copy)
            playout_copy = deal_board(playout_copy)
            playout_copy = bet_stage(playout_copy)
            # Reshuffle cards here?
            # playout_copy = self.reshuffle_hands(playout_copy)
            playout_copy = showdown_stage(playout_copy)
            results.append(playout_copy.players[agent_index].stack - prior_stack)
        return np.mean(results)

    def sample_games(self, game_copy):
        agent_index = 0
        for i, player in enumerate(game_copy.players):
            if player == self:
                agent_index = i
        possible_actions, raises_list = self.get_possible_actions(game_copy)
        start_state = copy.deepcopy(game_copy)
        for action in possible_actions:
            action_state = copy.deepcopy(start_state)
            if action == self.bet_raise:
                for bet in raises_list:
                    action_state = copy.deepcopy(start_state)
                    action_state.players[agent_index].bet_raise(bet)
                    # averaged_results = playout(action_state, agent_index)
                    # results.append(averaged_results)
                
                # Get best best action
            else:
                action_state.players[agent_index].action()

        # Return possible_actions[argmax(averaged_results)], best_bet


    def act(self):
        # root_node = MCTSNode()
        game_copy = copy.deepcopy(self.game)
        # TODO reshuffle hands
        # TODO change players to random players or callbot players

        # action, best_bet= self.sample_games(game_copy)
        # if action = self.bet_raise:
        #     self.bet_raise(best_bet)
        # else:
        #     self.action()
        
        pass

    def traverse(self):
        pass

    def rollout(self, game_copy):
        pass

    def evaluate(self, game_copy):
        pass

    def get_action(self, game):
        pass