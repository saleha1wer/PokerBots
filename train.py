
from policy_network.network import Network
from policy_network.utils.game2array import game2array
import numpy as np 
from game import play_game, play_round
from pokerface import Stakes, NoLimitShortDeckHoldEm,NoLimitTexasHoldEm
from random_agent import RandomAgent
import EVhands
from policy_network.network_agent import NetworkAgent


# testing script - just testing if network agent runs fine 
# commented code tests the training of the network
button = 0
no_players = 4
if(no_players == 2):
    stakes = Stakes(0, {button+1: 1, button: 2})
else:
    stakes = Stakes(0, {button + 1: 1, button + 2: 2})
starting_stacks = 200, 200, 200, 200
n_rounds = 100
net = Network([(7),(10)],4)
net.initialize_network()
#nls = NoLimitShortDeckHoldEm(stakes,starting_stacks)
nls = NoLimitTexasHoldEm(stakes,starting_stacks)
ra1 = RandomAgent(nls)
ra3 = RandomAgent(nls)
ra4 = RandomAgent(nls)
na1 = NetworkAgent(nls,net)
players = [ra1, ra3, ra4,na1]
ranges = [200,200,200,200]

for i in range(len(ranges)):
    print(i)
    EVhands.player_range[i] = ranges[i]
    print(EVhands.player_range)

play_game(n_rounds, players, nls, starting_stacks, button)




    
# games = []
# opps = []
# act_ds = []
# for i in range(3):
#     my_player = players[1]
#     stacks, players = play_round(players,nls)
#     game_info,opp_info = game2array(nls,my_player)
#     games.append(game_info)
#     opps.append(opp_info)
#     act_ds.append(np.random.uniform(size=4))
#     starting_stacks = stacks
#     nls = NoLimitTexasHoldEm(Stakes(0, {button + 1: 1, button: 2}), starting_stacks)
# print(games[0])
# print(games[0].shape)

# print(opps[0])
# print(opps[0].shape)


# net.train_network(np.array(games),np.array(opps),np.array(act_ds),20)