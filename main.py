from game import play_game
from pokerface import Stakes, NoLimitShortDeckHoldEm
from random_agent import RandomAgent

stakes = Stakes(0, (1, 2))
starting_stacks = 200, 200, 200
n_rounds = 100

nls = NoLimitShortDeckHoldEm(stakes,starting_stacks)
ra1 = RandomAgent(nls)
ra2 = RandomAgent(nls)
ra3 = RandomAgent(nls)

players = [ra1, ra2, ra3]

play_game(n_rounds,players,nls,starting_stacks,stakes)

