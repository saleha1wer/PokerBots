import copy
from pokerface import PokerPlayer
import numpy as np

"""
This is our mcts agent that will play poker using a monte carlo tree search. The class inherits everything
from the PokerPlayer class. The act function is used to select and perform an action.
"""
class MCTSNode:
    def __init__(self, action=None, parent=None):
        self.parent = parent
        self.action = action
        self.children = []
        self.child_actions = []
        self.evaluations = []
        self.terminal = False
        self.fully_expanded = False

    def q(self):
        return np.mean(self.evaluations)

    def n(self):
        return len(self.evaluations)

    def visit(self, score):
        self.evaluations.append(score)

    def backpropagate(self, score):
        self.visit(score)
        if self.parent != None:
            self.parent.backpropagate(score)

    def expand(self, action):
        child = MCTSNode(action=action, parent=self)
        self.children.append(child)
        self.child_actions.append(action)
        return child

    def is_terminal(self):
        return self.terminal

    def is_fully_expanded(self):
        return self.fully_expanded

    def best_child(self, c_val=0.1):
        ucb_values = []
        for child in self.children:
            ucb_values.append(child.q() / child.n() + c_val * np.sqrt((2 * np.log(self.n()) / child.n())))
        return self.children[np.argmax(ucb_values)]

    def best_action(self, c_val=0.1):
        child = self.best_child(c_val)
        return child.action


class MCTSAgent(PokerPlayer):
    def __init__(self, game):
        super().__init__(game)
        self.n_simulations = 1000

    def act(self):
        # Create root node
        root_node = MCTSNode()

        # Get a copy of the game and simulate a MCTS leaf
        for i in range(self.n_simulations):
            game_copy = copy.deepcopy(self.game)
            leaf_node, game_copy = self.traverse(root_node, game_copy)
            game_copy = self.rollout(game_copy)
            score = self.evaluate(game_copy)
            leaf_node.backpropagate(score)

        # Select and perform the best action
        action = root_node.best_action(c_val=0.01)
        action()
        print('MCTS_action: ', action.__name__)

    def traverse(self, root_node, game_copy):
        current_node = root_node
        while not game_copy.is_terminal():
            if current_node.fully_expanded:
                if current_node.terminal:
                    return current_node, game_copy
                else:
                    current_node = current_node.best_child()
            else:
                # Retrieve all possible actions for the MCTSAgent in the game_copy
                bet_options, action = self.get_action(game_copy)

                # If no action is returned, go to next state until we can play
                while not game_copy.is_terminal and action == None:
                    game_copy.step() # TODO: change this to going to a next state
                    bet_options, action = self.get_action(game_copy)

                # If the game has ended, report that this node ends in terminal and stop traversal
                if game_copy.is_terminal:
                    current_node.terminal = True
                    return current_node, game_copy

                # If the selected action is in the child node actions, set it to None
                if action in current_node.child_actions:
                        action = None

                # Current node is fully expanded, no action is taken
                if action == None:
                    current_node.fully_expanded = True
                    current_node = current_node.best_child()
                # Current node isn't fully expanded, action is taken to expand the tree
                elif action == self.bet_raise:
                    value = np.random.choice(bet_options)
                    action(value)
                else:
                    action()
                    current_node = current_node.expand(action)
                    return current_node, game_copy

    def rollout(self, game_copy):
        """" Perform rollout until game is over """
        while not game_copy.is_terminal():
            bet_options, action = self.get_action(game_copy)

            if action == self.bet_raise:
                value = np.random.choice(bet_options)
                action(value)
            else:
                action()
        return game_copy

    def evaluate(self, game_copy):
        """ Evaluate if the chosen leaf leads to win or loss """
        if game_copy.is_terminal():
            for p in game_copy.players:
                if p.stack != 0:
                    winner = p

                    if isinstance(winner, MCTSAgent):
                        score = 1
                    else:
                        score = 0
                    return score

    def get_action(self, game):
        """ Get a list with possible actions """
        # TODO: check if this action works in both self.game as game_copy
        bet_options = action = None
        possible_actions = []

        for p in game.players:
            if isinstance(p, MCTSAgent) and p.is_actor():
                # Add all available actions of agent in the game_copy to a list
                if p.can_fold(): possible_actions.append(self.fold)
                if p.can_check_call(): possible_actions.append(self.check_call)
                if p.can_bet_raise():
                    bet_options = range(p.bet_raise_min_amount,
                                        p.bet_raise_max_amount + game.stakes.small_bet)
                    possible_actions.append(self.bet_raise)
                if p.can_discard_draw(): possible_actions.append(self.discard_draw)
                if p.can_showdown(): possible_actions.append(self.showdown)

        # Pick a random action from the list and execute it in the game_copy
        if(len(possible_actions) != 0):
            action = np.random.choice(possible_actions)
        return bet_options, action