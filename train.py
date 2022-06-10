
from logging import exception
from policy_network.ev_agent import EVAgent
from policy_network.network import Network
from policy_network.utils.game2array import game2array
import numpy as np 
from pokerface import Evaluator, Stakes, NoLimitShortDeckHoldEm,NoLimitTexasHoldEm
from policy_network.utils.nn_game import play_game
from policy_network.network_agent import NetworkAgent
from policy_network.utils.buffer import Buffer
import EVhands
import os
import multiprocessing as mp
from policy_network.random_agent import RandomAgent
import keras
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


def simulate_game(players, max_rounds=25):
    # play game with the list of players
    # save game arrays and action distribution of each player at each stage of the game
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
        p_id = p.id
        if isinstance(p,NetworkAgent):
            net = p.network
            new_p = NetworkAgent(game,net,p_id,200)
        elif isinstance(p,EVAgent):
            new_p = EVAgent(game,p_id)
        elif isinstance(p,RandomAgent):
            new_p = RandomAgent(game,p_id)
        players.append(new_p)
    
    ranges = [100 for i in range(len(players))]
    for i in range(len(ranges)):
        EVhands.player_range[i] = ranges[i]

    game_info,opp_info,act_dis, winner_id = play_game(players,game,starting_stacks,button,max_rounds=max_rounds)
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


def temp_func(players,max_rounds):
    try:
        game_info,opp_info,act_dis, winner_id = simulate_game(players,max_rounds=max_rounds)
        print('winner id ', winner_id)
        return [game_info,opp_info,act_dis,winner_id]
    except exception as e:
        print('ERROR, ERROR, ERROR, ERROR, ERROR')
        print(e)
        return None
        
def policy_network_self_play(policy_network,n_opps, N=None, total=10, buffer_size=1000, sample_size=500,max_rounds=75,m_p=True,opp='EV'): # --> Policy Network
    """
    repeat 200 times:
        6. Play a table (n games) of policy network and 3 random bots and 1 EV bots. (or if max1opp -- > 1 EV bot or random bot)
            - gather data of winner of every game
        7. Train policy network on the data
    """
    wins = 0
    runs = 0
    button = 0
    buffer = Buffer(buffer_size)
    stakes = Stakes(0, {button+1: 1, button: 2})
    starting_stacks =(200,200,200)
    temp_nls = NoLimitTexasHoldEm(stakes,starting_stacks)
    players = []
    net_agent = NetworkAgent(temp_nls,policy_network,0)
    if opp == 'EV':
        ev1 = EVAgent(temp_nls,1)
        players.append(net_agent),players.append(ev1)
    elif opp == 'random':
        ra =RandomAgent(temp_nls,1)
        players.append(net_agent),players.append(ra)

    for i in range(n_opps-1):
        ra =RandomAgent(temp_nls,i+2) 
        players.append(ra)

    while runs<200:
        print('Run ', runs)
        runs = runs +1
        wins = 0
        if m_p: 
            n_cores = os.cpu_count()
            # n_cores = os.environ['SLURM_JOB_CPUS_PER_NODE'] # uncomment when running on ALICE
            pool = mp.Pool(processes=int(n_cores))
            all_games = pool.starmap(temp_func, [(players,max_rounds) for i in range(total)])
            for temp in all_games:
                if temp is not None:
                    buffer.add_to_buffer(tuple(temp[:3]))
                    if temp[3]==0:
                        wins+=1
        else:
            for i in range(total):
                game_info,opp_info,act_dis, winner_id = simulate_game(players,max_rounds=max_rounds)
                if winner_id == 0:
                    wins += 1
                print('winner id ', winner_id)
                buffer.add_to_buffer((game_info,opp_info,act_dis))
        print(total, ' games finished. PN-agent wins: ', wins)
        game_info,opp_info,act_dis = buffer.get_from_buffer(sample_size)
        players[0].network.train_network(game_info,opp_info,act_dis,5,batch_size =4)

        if runs % 10 == 0 or runs ==1:
            players[0].network.save_network('max_4_opp/run'+str(runs+20))
    return players[0].network

def main():
    # games_matrix, opp_matrix,act_dis_matrix, hall_of_fame = gather_initial(1000)
    # policy_network = train((games_matrix, opp_matrix,act_dis_matrix))
    # test policy network, save plots, save network 
    max_n_opp = 1 
    # max_n_opp = 4
    policy_network = Network([(7),(max_n_opp*2)],5)
    # policy_network.initialize_network()
    policy_network.network = keras.models.load_model('policy_network/saved_models/max_1_opp/trained_EVandRandom/final.tf')
    opp = 'EV'
    total = 10
    max_rounds = 35
    m_p=True
    buffer_size = 1000
    sample_size = 500
    new_policy_network = policy_network_self_play(policy_network,max_n_opp,total=total,max_rounds=max_rounds,
                                                opp=opp,m_p=m_p,buffer_size=buffer_size,sample_size=sample_size)
    new_policy_network.save_network('max_4_opp/final')

if __name__ == '__main__':
    main()



