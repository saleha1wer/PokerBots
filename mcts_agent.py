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

    def act(self, n_simulations):
        # Create root node
        root_node = MCTSNode()

        # Get a copy of the game and simulate a MCTS leaf
        for i in range(n_simulations):
            game_copy = copy.deepcopy(self.game)
            leaf_node, game_copy = self.traverse(root_node, game_copy)
            game_copy = self.rollout(game_copy)
            score = self.evaluate(game_copy)
            leaf_node.backpropagate(score)

        # Select and perform the best action
        f = root_node.best_action(c_val=0.01)
        f()
        print('MCTS_action: ', f.__name__)

    def traverse(self, root_node, game_copy):
        current_node = root_node
        while not game_copy.is_terminal:
            if current_node.fully_expanded:
                if current_node.terminal:
                    return current_node, game_copy
                else:
                    current_node = current_node.best_child()
            else:
                # Retrieve all possible actions
                possible_actions = []

                for p in game_copy.players:
                    if issubclass(p, MCTSAgent):
                        # Add all available actions of agent in the game_copy to a list
                        if p.can_fold(): possible_actions.append(p.fold)
                        if p.can_check_call(): possible_actions.append(p.check_call)
                        if p.can_bet_raise():
                            bet_options = range(p.bet_raise_min_amount,
                                                p.bet_raise_max_amount + game_copy.stakes.small_bet)
                            for value in bet_options:
                                possible_actions.append(p.bet_raise(value))
                        if p.can_discard_draw(): possible_actions.append(p.discard_draw)
                        if p.can_showdown(): possible_actions.append(p.showdown)

                # Retry when there are no possible actions
                if len(possible_actions) == 0:
                    ...

                # Stop when the current node has a terminal game state
                if game_copy.is_terminal:
                    current_node.terminal = True
                    return current_node, game_copy

                # The poker game isn't terminal yet, new action is picked
                np.random.shuffle(possible_actions)
                action = None
                for a in possible_actions:
                    if a not in current_node.child_actions:
                        action = a

                # Current node is fully expanded, no action is taken
                if action == None:
                    current_node.fully_expanded = True
                    current_node = current_node.best_child()
                # Current node isn't fully expanded, action is taken to expand the tree
                else:
                    game_copy.action()
                    current_node = current_node.expand(action)
                    return current_node, game_copy

    def rollout(self, game_copy):
        """" Perform rollout until game is over """
        while not game_copy.is_terminal:
            possible_actions = []

            for p in game_copy.players:
                if issubclass(p, MCTSAgent):
                    # Add all available actions of agent in the game_copy to a list
                    if p.can_fold(): possible_actions.append(p.fold)
                    if p.can_check_call(): possible_actions.append(p.check_call)
                    if p.can_bet_raise():
                        bet_options = range(self.bet_raise_min_amount, p.bet_raise_max_amount + game_copy.stakes.small_bet)
                        for value in bet_options:
                            possible_actions.append(p.bet_raise(value))
                    if p.can_discard_draw(): possible_actions.append(p.discard_draw)
                    if p.can_showdown(): possible_actions.append(p.showdown)

                    # Pick a random action from the list and execute it in the game_copy
                    if(len(possible_actions) != 0):
                        f = np.random.choice(possible_actions)
                        f()
        return game_copy

    def evaluate(self, game_copy):
        """ Evaluate if the chosen leaf leads to win or loss """
        if game_copy.is_terminal:
            for p in game_copy.players:
                if p.stack != 0:
                    winner = p

                    if issubclass(winner, MCTSAgent):
                        score = 1
                    else:
                        score = 0
                    return score