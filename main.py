from game import play_game
from pokerface import Stakes, NoLimitShortDeckHoldEm,NoLimitTexasHoldEm
from random_agent import RandomAgent
from heuristic_agent import HeuristicAgent
from mcts_agent import MCTSAgent
from ev_agent import EVAgent
from shallow_mcts_test import ShallowMCTS

button = 0
button = 0
no_players = 4
if(no_players == 2):
    stakes = Stakes(0, {button+1: 1, button: 2})
else:
    stakes = Stakes(0, {button + 1: 1, button + 2: 2})
starting_stacks = 200, 200, 200, 200
n_rounds = 1

#nls = NoLimitShortDeckHoldEm(stakes,starting_stacks)
nls = NoLimitTexasHoldEm(stakes,starting_stacks)
ra1 = RandomAgent(nls)
ra2 = RandomAgent(nls)
ra3 = RandomAgent(nls)
ha3 = HeuristicAgent(nls)
mc4 = MCTSAgent(nls)
ev3 = EVAgent(nls)
smcts = ShallowMCTS(nls)

players = [ra1, ra2, smcts, ev3]
play_game(n_rounds, players, nls, starting_stacks, button)
# play_game(n_rounds,players,nls,starting_stacks,stakes, button, no_players)
