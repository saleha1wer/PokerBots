
from pokerface import NoLimitTexasHoldEm, Stakes
from scipy.fft import idst
from policy_network.utils.nn_game_actions import *
from policy_network.network_agent import NetworkAgent
import numpy as np
import EVhands
import PreFlop


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
    nls, players_data_pre= bet_stage(nls)
    # Flop
    nls = deal_board(nls)
    # Flop betting
    nls,players_data_flop = bet_stage(nls)
    # Turn
    nls = deal_board(nls)
    # Turn betting
    nls,players_data_turn = bet_stage(nls)
    # River
    nls = deal_board(nls)
    # River betting
    nls,players_data_river = bet_stage(nls)
    # Showdown
    nls = showdown_stage(nls)

    # Translate results in new sets of stacks and players
    new_stacks = []
    new_players = []
    PlayeronButton["player"] = nls.players[PlayeronButton["button"]]
    Exist = False
    for i, p in enumerate(nls.players):
        if p.stack != 0:
            new_stacks.append(p.stack)
            if isinstance(p, NetworkAgent):
                new_p = NetworkAgent(nls,p.network,p.id)
            elif isinstance(p, EVAgent):
                new_p = EVAgent(nls,p.id)
            elif isinstance(p, RandomAgent):
                new_p = RandomAgent(nls,p.id)
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

    players_data = dict()
    for i in range(len(players_data_pre)):
        if players_data_pre[i]  != '':
            game_a, opp_a,acts_a = players_data_pre[i]
            game_a, opp_a,acts_a = game_a[0], opp_a[0],acts_a[0]
        if players_data_flop[i]  != '':
            f_game_a, f_opp_a,f_acts_a = players_data_flop[i]
            f_game_a, f_opp_a,f_acts_a = f_game_a[0], f_opp_a[0],f_acts_a[0]
            game_a, opp_a,acts_a = np.vstack((game_a,f_game_a)),np.vstack((opp_a,f_opp_a)),np.vstack((acts_a,f_acts_a))
        if players_data_turn[i]  != '':
            t_game_a, t_opp_a,t_acts_a = players_data_turn[i]
            t_game_a, t_opp_a,t_acts_a = t_game_a[0], t_opp_a[0],t_acts_a[0]
            game_a, opp_a,acts_a = np.vstack((game_a,t_game_a)),np.vstack((opp_a,t_opp_a)),np.vstack((acts_a,t_acts_a))
        if players_data_river[i]  != '':
            r_game_a, r_opp_a,r_acts_a = players_data_river[i]
            r_game_a, r_opp_a,r_acts_a = r_game_a[0], r_opp_a[0],r_acts_a[0]
            game_a, opp_a,acts_a = np.vstack((game_a,r_game_a)),np.vstack((opp_a,r_opp_a)),np.vstack((acts_a,r_acts_a))
        
        if players_data_pre[i]  != '':
            players_data[nls.players[i].id] = (game_a,opp_a,acts_a)

    return new_stacks, new_players,players_data

def play_game(players, game, starting_stacks, button=0,max_rounds=75):
    # Play n rounds of poker games (or until one wins) with the supplied agents
    # Returns (game_arrays,opp_arrays,act_dis) of winner, winner_id
    starting_stakes = get_stakes(players, button)
    # Set small blind and big blind
    sb_value = 1
    bb_value = 2
    blinds = (0, sb_value, bb_value)
    stacks = starting_stacks
    games_data = dict()
    for player in players:
        games_data[player.id] = []
    for round in range(max_rounds):
        EVhands.getpositions(button, len(players))
        if round == 0:
            # First round
            game = NoLimitTexasHoldEm(starting_stakes, stacks)
        else:
            # Other rounds, update based on new blind positions
            game = NoLimitTexasHoldEm(Stakes(0, blinds), stacks)
        # if round % 10 == 0:
            # print("\nStarting round:", round)
            # ids = [p.id for p in players]
            # print(ids)
        stacks, players,players_data = play_round(players, game)

        for p_id in players_data.keys():
            games_data[p_id].append(players_data[p_id])

        if len(players) == 1:
            # Game is over
            winner_id = players[0].id
            w_game, w_opp, w_acts = [],[],[]
            for data_tuples in games_data[players[0].id]:
                game_a, opp_a, acts_a = data_tuples
                w_game.append(game_a),w_opp.append(opp_a),w_acts.append(acts_a)
            w_game, w_opp, w_acts = np.vstack(w_game), np.vstack(w_opp),np.vstack(w_acts)
            EVhands.possible_hands.clear()
            PreFlop.actions.clear()
            PreFlop.actions["i"] = 2
            return w_game,w_opp,w_acts, winner_id
        # Update blinds positions
        button, blinds = increment_blinds(players, button, sb_value, bb_value) 
        EVhands.possible_hands.clear()
        PreFlop.actions.clear()
        PreFlop.actions["i"] = 2

    max_stack = 0
    for player in players:
        p_id = player.id
        if player.stack > max_stack:
            max_stack = player.stack
            max_id = player.id
    w_game, w_opp, w_acts = [],[],[]
    for data_tuples in games_data[max_id]:
        game_a, opp_a, acts_a = data_tuples
        w_game.append(game_a),w_opp.append(opp_a),w_acts.append(acts_a)
    w_game, w_opp, w_acts = np.vstack(w_game), np.vstack(w_opp),np.vstack(w_acts)
    return w_game,w_opp,w_acts,max_id
