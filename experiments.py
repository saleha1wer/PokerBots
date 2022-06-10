from game import play_game
from pokerface import Stakes, NoLimitShortDeckHoldEm,NoLimitTexasHoldEm
from random_agent import RandomAgent
from callbot_agent import CallbotAgent
from heuristic_agent import HeuristicAgent
#from mcts_agent import MCTSAgent
from ev_agent import EVAgent
from shallow_mcts import ShallowMCTS
from policy_network.network_agent import NetworkAgent
from policy_network.network import Network

import sklearn
import tensorflow as tf
import keras

import EVhands

import sys

# A few constants
NUM_RANDOM_OPPONENTS = 2
NUM_ROUNDS = 100
NUM_GAMES = 1

#TODO add callbot
def randomOpponents(numOpponents, agentType, numRounds):
    button = 0
    no_players = numOpponents + 1
    n_rounds = numRounds

    if(no_players == 2):
        stakes = Stakes(0, {button: 1, button+1: 2})
    else:
        stakes = Stakes(0, {button + 1: 1, button + 2: 2})

    # Create dynamic number of starting stacks
    starting_stacks = []
    for i in range(no_players):
        starting_stacks.append(200)
    starting_stacks = tuple(starting_stacks)

    nls = NoLimitTexasHoldEm(stakes,starting_stacks)

    # Add the number of random players
    players = []
    for i in range(numOpponents):
        players.append(RandomAgent(nls))

    # Add the "smarter" agent
    # NEEDS ADDITION OF POLICY NETWORK
    if agentType == "PolicyAgent":
        players.append(PolicyAgent(nls))
        print("TODO not implemented in experiments")
    elif agentType == "EVAgent":
        players.append(EVAgent(nls))
    elif agentType == "ShallowMCTS":
        players.append(ShallowMCTS(nls))
    else:
        print("Invalid agentType")
        exit()

    ranges = []
    for i in range(numOpponents):
        ranges.append(100)
    ranges.append(30)
    
    for i in range(len(ranges)):
        #print(i)
        EVhands.player_range[i] = ranges[i]
        #print(EVhands.player_range)
    play_game(n_rounds, players, nls, starting_stacks, button)

def agentVsAgent(agentType1, agentType2, numRounds):
    button = 0
    no_players = 2
    n_rounds = numRounds

    stakes = Stakes(0, {button: 1, button+1: 2})

    starting_stacks = 200, 200

    nls = NoLimitTexasHoldEm(stakes,starting_stacks)
    net = Network([(7), (2)], 5)
    net.network = keras.models.load_model("policy_network/saved_models/max_1_opp/trained_EVandRandom/final.tf")

    # Add the first agent
    players = []
    if agentType1 == "CallbotAgent":
        players.append(CallbotAgent(nls))
    elif agentType1 == "EVAgent":
        players.append(EVAgent(nls))
    elif agentType1 == "ShallowMCTS":
        players.append(ShallowMCTS(nls))
    elif agentType1 == "RandomAgent":
        players.append(RandomAgent(nls))
    elif agentType1 == "NetworkAgent":
        players.append(NetworkAgent(nls, net, 0))
    else:
        print("Invalid agentType")
        exit()

    # Add the second agent
    if agentType2 == "CallbotAgent":
        players.append(CallbotAgent(nls))
    elif agentType2 == "EVAgent":
        players.append(EVAgent(nls))
    elif agentType2 == "ShallowMCTS":
        players.append(ShallowMCTS(nls))
    elif agentType2 == "RandomAgent":
        players.append(RandomAgent(nls))
    elif agentType2 == "NetworkAgent":
        players.append(NetworkAgent(nls, net, 0))
    else:
        print("Invalid agentType")
        exit()

    ranges = [100, 50] 
    
    for i in range(len(ranges)):
        #print(i)
        EVhands.player_range[i] = ranges[i]
        #print(EVhands.player_range)
    play_game(n_rounds, players, nls, starting_stacks, button)

def allAgentSkirmish(numRounds):
    button = 0
    n_rounds = numRounds
    no_players = 4

    stakes = Stakes(0, {button + 1: 1, button + 2: 2})

    # Create dynamic number of starting stacks
    starting_stacks = []
    for i in range(no_players):
        starting_stacks.append(200)
    starting_stacks = tuple(starting_stacks)

    nls = NoLimitTexasHoldEm(stakes,starting_stacks)

    # Add all agents
    # NEEDS ADDITION OF POLICY NETWORK if working against SMCTS
    ra = RandomAgent(nls)
    ca = CallbotAgent(nls)
    smcts = ShallowMCTS(nls)
    ev = EVAgent(nls)
    
    players = [ra, ca, smcts, ev]

    ranges = [100,100,50,50] 
    for i in range(len(ranges)):
        #print(i)
        EVhands.player_range[i] = ranges[i]
        #print(EVhands.player_range)
    play_game(n_rounds, players, nls, starting_stacks, button)

if __name__ == "__main__":
    for i in range(NUM_GAMES):
        print("START OF GAME NUMBER: {}".format(i))
        #randomOpponents(NUM_RANDOM_OPPONENTS, "ShallowMCTS", NUM_ROUNDS)
        #agentVsAgent("RandomAgent", "EVAgent", NUM_ROUNDS)
        allAgentSkirmish(NUM_ROUNDS)
        print("END OF GAME NUMBER: {}".format(i))

