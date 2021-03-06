from pokerface import NoLimitTexasHoldEm, Stakes
from heuristic_agent import HeuristicAgent
from random_agent import RandomAgent
from callbot_agent import CallbotAgent
from ev_agent import EVAgent
from shallow_mcts import ShallowMCTS
from game_actions import *
import EVhands
import PreFlop

from policy_network.network_agent import NetworkAgent
from policy_network.network import Network

PlayeronButton = {
    "button":0
    }

def get_stakes(players, button, sb_value=1, bb_value=2):
    # Get the initial stakes based on button position
    # Button position should not exceed (n_players - 2)
    n_players = len(players)
    if n_players == 2:
        stakes = Stakes(0, {button: sb_value, button+1: bb_value})
    else:
        stakes = Stakes(0, {button + 1: sb_value, button + 2: bb_value})
    return stakes

def Keyarrange():
    ranges = []
    for i in EVhands.player_range:
        ranges.append(EVhands.player_range[i])
    EVhands.player_range.clear()
    for i in range(len(ranges)):
        EVhands.player_range[i] = ranges[i]
    return

def increment_blinds(players, button, sb_value=1, bb_value=2):
    # I am not entirely certain but I think there is a possibility of
    # more than 2 players going broke returning an error here
    # If more than 2 players stop playing, the button will pass along
    # with the else statement right?

    # Increment blinds by passing along the button.
    # Button is followed by small blind, then big blind
    n_players = len(players)
    #button += 1
    button = PlayeronButton["button"]
    if n_players > 1:
        if button >= n_players - 1:
            sb = 0
            bb = 1
            #button = -1
        elif button == n_players - 2:
            sb = button + 1
            bb = 0
        else:
            sb = button + 1
            bb = button + 2
        
        if(n_players != 2):
            blinds = {sb: sb_value, bb: bb_value}
        else:
            blinds = {bb: sb_value, sb: bb_value}
        print(button, blinds)
        return button, blinds

def play_round(players, game):
    # Play a single poker round 
    nls = game
    for i, p in enumerate(nls._players):
        # Set game players and stacks
        players[i]._stack = nls._players[i].stack
        nls._players[i] = players[i]
        nls._players[i]._game = game
        # print("Stack of player", i, nls._players[i].stack)
    nls._verify()
    nls._setup()

    # Deal cards to players
    nls = deal_cards(nls)
    # Preflop betting
    nls = bet_stage(nls)
    # Flop
    nls = deal_board(nls)
    print(nls.board)
    # Flop betting
    nls = bet_stage(nls)
    # Turn
    nls = deal_board(nls)
    print(nls.board)
    # Turn betting
    nls = bet_stage(nls)
    # River
    nls = deal_board(nls)
    print(nls.board)
    # River betting
    nls = bet_stage(nls)
    # Showdown
    nls = showdown_stage(nls)
    for player in nls.players:
        print(type(player), "has", player.hole, nls.board)

    # Translate results in new sets of stacks and players
    new_stacks = []
    new_players = []
    PlayeronButton["player"] = nls.players[PlayeronButton["button"]]
    Exist = False
    for i, p in enumerate(nls.players):
        if p.stack != 0:
            new_stacks.append(p.stack)
            for t in [RandomAgent, HeuristicAgent, EVAgent, ShallowMCTS, CallbotAgent]: # DO NOT FORGET TO ADD NEW BOTS HERE
                if isinstance(p, t):
                    # If you want to transfer information between the old and new agent,
                    # besides the stack, do it here!
                    new_p = t(nls)
                    new_p._stack = p.stack

            if isinstance(p, NetworkAgent):
                new_p = NetworkAgent(nls, p.network, p.id)
                new_p._stack = p.stack

            new_players.append(new_p)
            if(p == PlayeronButton["player"]):
                PlayeronButton["player"] = new_p
                Exist = True
        else:
            del EVhands.player_range[i]
            
                
    Keyarrange()
    for i, p in enumerate(new_players):
        if(p == PlayeronButton["player"]):
            if(i >= len(new_players) - 1): #Increment button
                PlayeronButton["button"] = 0
            else:
                PlayeronButton["button"] = i + 1
    if(Exist):
       PlayeronButton["button"] = 0 

    return new_stacks, new_players

def play_game(n_rounds, players, game, starting_stacks, button=0):
    # Play n rounds of poker games with the supplied agents
    starting_stakes = get_stakes(players, button)
    # Set small blind and big blind
    sb_value = 1
    bb_value = 2
    blinds = (0, sb_value, bb_value)
    stacks = starting_stacks
    for round in range(n_rounds):
        EVhands.getpositions(button, len(players))
        if round == 0:
            # First round
            game = NoLimitTexasHoldEm(starting_stakes, stacks)
        else:
            # Other rounds, update based on new blind positions
            game = NoLimitTexasHoldEm(Stakes(0, blinds), stacks)

        print("\nStarting round:", round)
        stacks, players = play_round(players, game)
        print("Round finished with results:")
        for p in players:
            print(type(p), p.stack)
            

        if len(players) == 1:
            # Game is over
            print("Winner!", type(players[0]))
            break

        # Update blinds positions
        button, blinds = increment_blinds(players, button, sb_value, bb_value)
        EVhands.possible_hands.clear()
        PreFlop.actions.clear()
        PreFlop.actions["i"] = 2
