
from policy_network.network import Network
from policy_network.utils.game2array import game2array
import numpy as np 
from pokerface import Stakes, NoLimitShortDeckHoldEm,NoLimitTexasHoldEm
from policy_network.utils.nn_game import play_game
from policy_network.network_agent import NetworkAgent
"""
1. Generate 2000 random networks
2. Initialize empty set of hall of fame
3. Simulate 400 tables with 5 players in each 
    - play 10 games at each table and gather (game_info,opp_info,act_dis) tuples from the winner of every game
    - if the same player wins more than 3 of the games, save in hall of fame
^ hall of famers and first set of data points gathered
4. Simulate len(hall_of_fame) tables (1 game each) between the hall of famer and 4 random bots
    - gather the data of the winning bot at each table 
^ second set of data points gathered
5. Train policy network on all the gathered data points 
^ Policy network training
6. Play a table (10 games) of policy network and 3 random hall of famers and 1 random bot (maybe also EV bot or MCTS bot).
    - gather data of winner of every game
7. Train policy network on the data
^ Further policy network training (repeat N times or until majority of games won)

- Optional 8. run games with PN and varrying number of opponents (1-5) and gather data from all of them
"""

def generate_networks(number):
    network_agents = []
    for i in range(number):
        net = Network([(7),(8)],5) # input shape 1 is 7, input shape 2 is 8 (4 max opponents) and action distribution length is 5
        net.initialize_network()
        temp_nls = NoLimitTexasHoldEm(Stakes(0, {1:1,2:2}),[200,200,200,200,200])
        agent = NetworkAgent(temp_nls,net,i)
        network_agents.append(agent)
    return network_agents

def same_agent(old_agent,new_game):
    """
    returns identical agent in a new game
    """
    return NetworkAgent(new_game,old_agent.network,old_agent.id)

def chunks(lst, n):
    """
    Yield successive n-sized chunks from lst. -https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def simulate_game(players):
    # play game with the list of players
    # save game arrays and network output of each player at each stage of the game
    # return the game arrays of the winner and the network outputs, also winner id
    button = 0
    no_players = len(players)
    if(no_players == 2):
        stakes = Stakes(0, {button+1: 1, button: 2})
    else:
        stakes = Stakes(0, {button + 1: 1, button + 2: 2})
    starting_stacks =[200 for i in range(len(players))]
    starting_stacks = tuple(starting_stacks)

    game = NoLimitTexasHoldEm(stakes,starting_stacks)
    temp_players = players
    players = []
    for p in temp_players:
        net = p.network
        p_id = p.id
        new_p = NetworkAgent(game,net,p_id)
        players.append(new_p)
    game_info,opp_info,act_dis, winner_id = play_game(players,game,starting_stacks,button,max_rounds=25)
    return game_info,opp_info,act_dis, winner_id

def simulate_games(n_games, players):
    wins = np.zeros(len(players)).tolist()
    player_ids = [player.id for player in players]
    games_matrix, opp_matrix,act_dis_matrix = [],[],[]
    for i in range(n_games):
        game_info,opp_info,act_dis, winner_id = simulate_game(players)
        winner_idx = player_ids.index(winner_id)
        print('game ', i, ' winner', winner_id)
        wins[winner_idx] = wins[winner_idx] + 1
        games_matrix.append(game_info), opp_matrix.append(opp_info),act_dis_matrix.append(act_dis)
    if max(wins) > 3: 
        winner_idx = np.argmax(wins)
        print('player added to hall of fame. Wins: ', max(wins))
        for player in players:
            if player.id == player_ids[winner_idx]:
                winner = player
    else:
        winner = None
    return np.vstack(games_matrix),np.vstack(opp_matrix),np.vstack(act_dis_matrix),winner

def save_hof(list_of_players):
    for idx,player in enumerate(list_of_players):
        net = player.network.network 
        net.save('policy_network/hall_of_fame/player'+str(idx)+'.tf')

def gather_initial(num): # --> (game_info,opp_info,act_dis), hall_of_fame
    """
    1. Generate 2000 random networks
    2. Initialize empty set of hall of fame
    3. Simulate 400 tables with 5 players in each 
        - play 10 games at each table and gather (game_info,opp_info,act_dis) tuples from the winner of every game
        - if the same player wins more than 3 of the games, save in hall of fame
    returns tuples of (game_info,opp_info,act_dis) and list of hall of fame agents
    """
    initial_agents = generate_networks(num)
    hall_of_fame = []
    games_players_list = list(chunks(initial_agents,5))
    games_matrix, opp_matrix,act_dis_matrix = [],[],[]
    for count,players in enumerate(games_players_list):
        print('table ', count)
        game_info,opp_info,act_dis, winner = simulate_games(10,players)
        if winner is not None:
            hall_of_fame.append(winner)
        games_matrix.append(game_info), opp_matrix.append(opp_info),act_dis_matrix.append(act_dis)
    print(len(hall_of_fame),' agents in the hall of fame list')
    games_matrix, opp_matrix,act_dis_matrix = np.vstack(games_matrix),np.vstack(opp_matrix),np.vstack(act_dis_matrix)
    return games_matrix, opp_matrix,act_dis_matrix, hall_of_fame

def train(arrays_tuple): # --> Policy Network
    policy_network = Network([(7),(8)],5)
    policy_network.initialize_network()
    games_matrix,opp_matrix,act_dis_matrix = arrays_tuple
    policy_network.train_network(games_matrix,opp_matrix,act_dis_matrix,50)
    policy_network.network.save('policy_network/saved_models/policy_net.tf')
    return policy_network

def policy_network_self_play(policy_network, N=None): # --> Policy Network
    pass

def main():
    games_matrix, opp_matrix,act_dis_matrix, hall_of_fame = gather_initial(1000)
    policy_network = train((games_matrix, opp_matrix,act_dis_matrix))
    # test policy network, save plots, save network 
    new_policy_network = policy_network_self_play(policy_network)
    # test policy network, save plots, save network 


games_matrix, opp_matrix,act_dis_matrix, hall_of_fame = gather_initial(100)
print(act_dis_matrix)
save_hof(hall_of_fame)
policy_network = Network([(7),(8)],5)
policy_network.initialize_network()
policy_network.train_network(games_matrix,opp_matrix,act_dis_matrix,50)
policy_network.network.save('policy_network/saved_models/policy_net.tf')




