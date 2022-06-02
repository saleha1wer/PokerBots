from game import play_game
from pokerface import Stakes, NoLimitShortDeckHoldEm,NoLimitTexasHoldEm
from random_agent import RandomAgent
from heuristic_agent import HeuristicAgent
from mcts_agent import MCTSAgent
from ev_agent import EVAgent
<<<<<<< HEAD
from shallow_mcts_test import ShallowMCTS
=======
from shallow_mcts import ShallowMCTS
import EVhands
>>>>>>> origin/main

button = 0
no_players = 4
if(no_players == 2):
    stakes = Stakes(0, {button: 1, button+1: 2})
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

players = [ra1, ra2, ra3, ev3]
ranges = [100,100,100,30]
for i in range(len(ranges)):
    print(i)
    EVhands.player_range[i] = ranges[i]
    print(EVhands.player_range)
play_game(n_rounds, players, nls, starting_stacks, button)
# play_game(n_rounds,players,nls,starting_stacks,stakes, button, no_players)
