from game import play_game
from pokerface import Stakes, NoLimitTexasHoldEm
from random_agent import RandomAgent
from heuristic_agent import HeuristicAgent


stakes = Stakes(0, (1, 2))
starting_stacks = 200, 200, 200
n_rounds = 100

nls = NoLimitTexasHoldEm(stakes,starting_stacks)
ra1 = RandomAgent(nls)
ra2 = RandomAgent(nls)
ha3 = HeuristicAgent(nls)

players = [ra1, ra2, ha3]

play_game(n_rounds,players,nls,starting_stacks,stakes)
