from policy_network.utils.game2array import game2array
import numpy as np
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
    if game.stage != None:
        p_iter = 0
        while game.stage.is_betting_stage():
            if game.players[p_iter].is_actor():
                game_info,opp_info = game2array(game,game.players[p_iter],max_players=game.players[p_iter].max_opp,starting_stack=game.players[p_iter].starting_stack)
                temp = game.players[p_iter].network.network.predict([game_info.reshape(1,-1), opp_info.reshape(1,-1)])
                act_dis = temp[0][0]
                bet_value = temp[1][0]
                act_dis = np.append(act_dis,bet_value)
                act_dis = game.players[p_iter].mask_actions(act_dis)
                players_data[p_iter]['game'].append(game_info)
                players_data[p_iter]['opp'].append(opp_info)
                players_data[p_iter]['act_dis'].append(act_dis)
                game.players[p_iter].act()
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