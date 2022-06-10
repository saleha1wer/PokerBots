from policy_network.utils.game2array import game2array
import numpy as np
from policy_network.ev_agent import EVAgent
from policy_network.network_agent import NetworkAgent
from policy_network.utils.one_hot_action import encode_action
import PreFlop
from policy_network.network import Network
from policy_network.random_agent import RandomAgent
from policy_network.ev_agent import EVAgent

def increment_p_count(n, n_players):
    # Function used for looping through players
    n += 1
    n %= n_players
    return n

def deal_cards(game):
    # Deals cards at the start of the game
    if game.stage != None:
        while game.stage.is_dealing_stage():
            if not game.nature.can_deal_hole():
                break
            game.nature.deal_hole()
            if game.stage == None: return game
    return game

def deal_board(game):
    # Deals board cards during the game
    if game.stage != None:
        while game.stage.is_board_dealing_stage():
            game.nature.deal_board()
            if game.stage == None: return game
    return game

def bet_stage(game):
    # Allows for players to bet through the .act() function
    # Loops through all players until betting phase is done
    players_data = [{'game':[],'opp':[],'act_dis':[]} for i in range(len(game.players))]

    max_opp = game.players[0].max_opp
    starting_stack = game.players[0].g_starting_stack
    if game.stage != None:
        p_iter = 0
        while game.stage.is_betting_stage():
            if game.players[p_iter].is_actor():
                game_info,opp_info = game2array(game,game.players[p_iter],max_players=max_opp,starting_stack=starting_stack)
                call_amount = game.players[p_iter].check_call_amount
                before = game.players[p_iter].bet
                if isinstance(game.players[p_iter],NetworkAgent):
                    temp = game.players[p_iter].network.network.predict([game_info.reshape(1,-1), opp_info.reshape(1,-1)])
                    random_net = Network([7,2*game.players[p_iter].max_opp],5)
                    random_net.initialize_network()
                    random_temp = random_net.network.predict([game_info.reshape(1,-1), opp_info.reshape(1,-1)])
                    act_dis = temp[0][0]
                    bet_value = temp[1][0]
                    random_ad = random_temp[0][0]
                    random_bet = random_temp[1][0]
                    r =  np.random.uniform(low=0,high=0.2)
                    act_dis = (1-r) * act_dis + r * random_ad
                    bet_value = (1-r) * bet_value + r * random_bet
                    act_dis = np.append(act_dis,bet_value)
                    act_dis = game.players[p_iter].mask_actions(act_dis)
                    # act_dis[np.argmax(act_dis)] = 1
                    # if np.argmax(act_dis) != 3:
                    #     act_dis[4] = 0
                    #     act_dis[3] = 0
                    # if np.argmax(act_dis) != 2:
                    #     act_dis[2] = 0
                    # if np.argmax(act_dis) != 1:
                    #     act_dis[1] = 0
                    # if np.argmax(act_dis) != 0:
                    #     act_dis[0] = 0
                    game.players[p_iter].act(act_d=act_dis)
                elif isinstance(game.players[p_iter],EVAgent):
                    act_dis = game.players[p_iter].act(return_action=True)
                elif isinstance(game.players[p_iter],RandomAgent):
                    act_dis = game.players[p_iter].act(return_action=True)
                else:
                    raise ValueError('Agent is not Policy or EV or random')
                after = game.players[p_iter].bet
                if(len(game.board) == 0):
                    if(after-before > call_amount):
                        iterator = PreFlop.actions["i"]
                        action = str(iterator) + "-bet"
                        PreFlop.actions[p_iter] = action
                        PreFlop.actions["i"] += 1
                    elif(game.players[p_iter].starting_stack - game.players[p_iter].stack == before + call_amount):
                        PreFlop.actions[p_iter] = "call"
                    elif(game.players[p_iter].starting_stack - game.players[p_iter].stack != before + call_amount):
                        PreFlop.actions[p_iter] = "fold"
                players_data[p_iter]['game'].append(game_info), players_data[p_iter]['opp'].append(opp_info), players_data[p_iter]['act_dis'].append(act_dis)
                # print(p_iter, "acted", game.players[p_iter].act)
            p_iter = increment_p_count(p_iter, len(game._players))
            if game.stage == None:
                player_tuples = []
                for data in players_data:
                    if len(data['game']) > 0:
                        game_arrays = np.stack(data['game'])
                        opp_arrays = np.stack(data['opp'])
                        act_dis_arrays = np.stack(data['act_dis'])
                        player_tuples.append([game_arrays,opp_arrays,act_dis_arrays])
                    else:
                        player_tuples.append('')
                return game,player_tuples
            # print("piter", p_iter)
            # print(game.actor)
            # print(game.nature.is_nature(), game.nature.is_player())
            # for p in game.players:
            #     print(p)
    player_tuples = []
    for data in players_data:
        if len(data['game']) > 0:
            game_arrays = np.stack(data['game'])
            opp_arrays = np.stack(data['opp'])
            act_dis_arrays = np.stack(data['act_dis'])
            player_tuples.append([game_arrays,opp_arrays,act_dis_arrays])
        else:
            player_tuples.append('')
    return game,player_tuples

def showdown_stage(game):
    # Performs showdown on all players in order to distribute pot
    if game.stage != None:
        p_iter = 0
        if game.stage.is_showdown_stage():
            while game.stage.is_showdown_stage():
                if game.players[p_iter].can_showdown():
                    game.players[p_iter].showdown()
                p_iter = increment_p_count(p_iter, len(game._players))
                if game.stage == None: return game
    return game