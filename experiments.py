from game import play_game
from pokerface import Stakes, NoLimitShortDeckHoldEm,NoLimitTexasHoldEm
from random_agent import RandomAgent
from heuristic_agent import HeuristicAgent
#from mcts_agent import MCTSAgent
from ev_agent import EVAgent
from shallow_mcts import ShallowMCTS
import EVhands

import sys

# A few constants
NUM_RANDOM_OPPONENTS = 2
NUM_ROUNDS = 20
NUM_GAMES = 1

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
    if agentType == "HeuristicAgent":
        players.append(HeuristicAgent(nls))
    elif agentType == "EVAgent":
        players.append(EVAgent(nls))
    elif agentType == "ShallowMCTS":
        players.append(ShallowMCTS(nls))
    else:
        print("Invalid agentType")
        exit()

    #ranges = [100,100,100,30]
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


    # Add the first agent
    # NEEDS ADDITION OF POLICY NETWORK
    players = []
    if agentType1 == "HeuristicAgent":
        players.append(HeuristicAgent(nls))
    elif agentType1 == "EVAgent":
        players.append(EVAgent(nls))
    elif agentType1 == "ShallowMCTS":
        players.append(ShallowMCTS(nls))
    else:
        print("Invalid agentType")
        exit()

    # Add the second agent
    # ALSO NEEDS ADDITION OF POLICY NETWORK
    if agentType2 == "HeuristicAgent":
        players.append(HeuristicAgent(nls))
    elif agentType2 == "EVAgent":
        players.append(EVAgent(nls))
    elif agentType2 == "ShallowMCTS":
        players.append(ShallowMCTS(nls))
    else:
        print("Invalid agentType")
        exit()

    ranges = [100, 100] # NOT SURE WHAT RANGES TO GIVE THE AGENTS PLAYING AGAINST EACHOTHER
    
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
    # NEEDS ADDITION OF POLICY NETWORK
    ra = RandomAgent(nls)
    ha = HeuristicAgent(nls)
    ev = EVAgent(nls)
    smcts = ShallowMCTS(nls)
    
    players = [ra, ha, ev, smcts]

    ranges = [100,100,100,30] # NOT SURE WHAT RANGES TO GIVE THE AGENTS PLAYING AGAINST EACHOTHER
    for i in range(len(ranges)):
        #print(i)
        EVhands.player_range[i] = ranges[i]
        #print(EVhands.player_range)
    play_game(n_rounds, players, nls, starting_stacks, button)

if __name__ == "__main__":
    for i in range(NUM_GAMES):
        print("START OF GAME NUMBER: {}".format(i))
        randomOpponents(NUM_RANDOM_OPPONENTS, "HeuristicAgent", NUM_ROUNDS)
        #agentVsAgent("EVAgent", "ShallowMCTS", NUM_ROUNDS)
        #allAgentSkirmish(NUM_ROUNDS)
        print("END OF GAME NUMBER: {}".format(i))

    #for i in range(10):
    #    try:
    #        randomOpponents(3, "HeuristicAgent", 10)
    #    except ValueError:
    #        print("VALUE ERROR DISREGARD GAME")
    #        exit()
    #    except UnboundLocalError:
    #        print("UNBOUND LOCAL ERROR DISREGARD GAME")
    #        exit()
    #    print("{}-------------------------------------".format(i))

