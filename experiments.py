from game import play_game
from pokerface import Stakes, NoLimitShortDeckHoldEm
from random_agent import RandomAgent
from heuristic_agent import HeuristicAgent


""" 
Here we play many games (of n rounds each) using our bots and plot the results. 

TODO:
- Make the 'play_game' function return the result of the game (the winner)
- Plot results
- Heuristic bot creates an error in line 93, chip_raise referenced before assignment
"""

stakes = Stakes(0, (1, 2))
starting_stacks = 200, 200, 200
n_rounds = 50
n_games = 100

nls = NoLimitShortDeckHoldEm(stakes, starting_stacks)
ra = RandomAgent(nls)
ha = HeuristicAgent(nls)

players = [ra, ha]

for game in range(n_games):
    play_game(n_rounds, players, nls, starting_stacks, stakes)

