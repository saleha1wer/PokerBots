from game import play_game
from pokerface import Stakes, NoLimitShortDeckHoldEm,NoLimitTexasHoldEm
from random_agent import RandomAgent
from heuristic_agent import HeuristicAgent
from mcts_agent import MCTSAgent
from EV import EVAgent



button = 0
no_players = 3 
if(no_players == 2):
    stakes = Stakes(0, {button+1: 1, button: 2})
else:
    stakes = Stakes(0, {button + 1: 1, button + 2: 2})
starting_stacks = 200, 200, 200
n_rounds = 100

#nls = NoLimitShortDeckHoldEm(stakes,starting_stacks)
nls = NoLimitTexasHoldEm(stakes,starting_stacks)
ra1 = RandomAgent(nls)
ra2 = RandomAgent(nls)
ha3 = HeuristicAgent(nls)
mc4 = MCTSAgent(nls)
ev3 = EVAgent(nls)

players = [ra1, ra2,ev3]

play_game(n_rounds,players,nls,starting_stacks,stakes, button, no_players)
