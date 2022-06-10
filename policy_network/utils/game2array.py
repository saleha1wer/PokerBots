from pokerface import Stage, Stakes, NoLimitShortDeckHoldEm,NoLimitTexasHoldEm,PokerPlayer,Rank,Suit,RankEvaluator,StandardEvaluator,Card,PokerPlayer,stages
import numpy as np
import os
import multiprocessing as mp
import time
import math

class Player(PokerPlayer):
    def __init__(self, game,agent_id):
        super().__init__(game)
        self.id = agent_id

def takeFirst(elem):
    return elem[0]


# def StraightDraw(cards):
#     ranking = []
#     draw_type = 0  # No draw
#     for card in cards:
#         rank = self.StraightRank(card[0])
#         ranking.append(rank)
#     minimum = [12, 0, 1, 2, 3, 4, 5, 6, 7, 8]
#     maximum = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
#     max_count = 0

#     for i in range(len(minimum)):
#         count = 0
#         for j in range(minimum[i], maximum[i] + 1):
#             for k in ranking:
#                 if (j == k):
#                     count += 1
#             if (count > max_count):
#                 max_count = count

#     if (max_count == 4):
#         ranking.sort()
#         for i in range(len(ranking) - 2):  # Does not include double end 1 - 3 - 1 or 2 - 2 - 2
#             if (ranking[i] == ranking[i + 1] - 1 and ranking[i + 1] == ranking[i + 2] - 1 and ranking[i + 2] != 12):
#                 draw_type = 4  # Open ended straight draw
#             else:
#                 draw_type = 2  # Inside straight draw
#     return draw_type

# def hand_combination(hole, board):
#     ranks = [i[0] for i in hole] + [j[0] for j in board]
#     for i in range(len(ranks)):
#         if ranks[i] == 'J':
#             ranks[i] = 11
#         elif ranks[i] == 'Q':
#             ranks[i] = 12
#         elif ranks[i] == 'H':
#             ranks[i] = 13
#         elif ranks[i] == 'A':
#             ranks[i] = 14
#         else:
#             ranks[i] = int(ranks[i])
#     pairs = list(set([k for k in ranks if ranks.count(k) == 2]))

#     # Determine the hand combination
#     if hole[0][0] == hole[1][0]:
#         hand = 'pocket_pair'

#     elif len(pairs) == 1:
#         hand = 'one_pair'

#     elif len(pairs) == 2:
#         hand = 'two_pair'

#     elif list(set([k for k in ranks if ranks.count(k) == 3])):
#         hand = 'three_of_a_kind'

#     elif len(ranks) >= 4:
#         if StraightDraw(ranks) == 4:
#             hand = 'open_ended_straight_flush_draw'

#         elif StraightDraw(ranks) == 2:
#             hand = 'insight_straight'

#     elif hole[0][0] != hole[1][0]:
#         hand = 'unmatched_pocket_cards'
#     return hand

# def win_rate(hole,board):
#     # https://www.pokerlistings.com/online-poker-odds-calculator#:~:text=To%20calculate%20your%20poker%20equity,(%2B4)%20%3D%2040%25.
#     hole = [[i.rank,i.suit] for i in hole]
#     board = [[i.rank,i.suit] for i in board]
#     hand = hand_combination(hole, board)

#     # Probability of getting these combinations after 7 cards
#     probabilities = {
#         "royal_flush" : 4324 / math.comb(52, 7),
#         "straight_flush" : 37260 / math.comb(52, 7),
#         "four_of_a_kind" : 224848 / math.comb(52, 7),
#         "full_house" : 3473184 / math.comb(52, 7),
#         "flush" : 4047644 / math.comb(52, 7),
#         "straight" : 6180020 / math.comb(52, 7),
#         "three_of_a_kind" : 6461620 / math.comb(52, 7),
#         "two_pair" : 31433400 / math.comb(52, 7),
#         "one_pair" : 58627800 / math.comb(52, 7),
#         "no_pair" : 23294460 / math.comb(52, 7)
#     }

#     # Chance of improving your hand
#     # When fold has happened
#     if len(hole) == 2 & len(board) == 3:
#         if hand == "three_of_a_kind":
#             chance1 = 0.0430
#             chance2 = 0.2780
#             win_rate = probabilities["four_of_a_kind"] * chance1 \
#                        + probabilities["full_house"] * chance2 \
#                        + probabilities["three_of_a_kind"] * (1 - chance1 - chance2)

#         elif hand == "pocket_pair" :
#             chance = 0.0840
#             win_rate = probabilities["three_of_a_kind"] * chance \
#                        + probabilities["one_pair"] * (1- chance)

#         elif hand == "one_pair":
#             chance1 = 0.1250
#             chance2 = 0.2040
#             win_rate = probabilities["two_pair"] * chance1 \
#                        + probabilities["three_of_a_kind"] * (chance2 - chance1) \
#                        + probabilities["one_pair"] * (1- chance1 - chance2)

#         elif hand == "unmatched_pocket_cards":
#             chance = 0.2410
#             win_rate = probabilities["one_pair"] * chance \
#                        + probabilities["no_pair"] * (1 - chance)

#         elif hand == "inside_straight":
#             chance1 = 0.1650
#             chance2 = 0.3840
#             win_rate = probabilities["straight"] * chance1 \
#                        + probabilities["one_pair"] * (chance2 - chance1) \
#                        + probabilities["no_pair"] * (1 - chance1 - chance2)

#         elif hand == "two_pair":
#             chance = 0.1650
#             win_rate = probabilities["full_house"] * chance \
#                        + probabilities["two_pair"] * (1 - chance)

#         elif hand == "open_ended_straight_flush_draw":
#             chance1 = 0.5410
#             chance2 = 0.7232
#             win_rate = probabilities["straight"] + probabilities["flush"] * chance1 \
#                        + probabilities["straight"] + probabilities["flush"] + probabilities["one_pair"]* chance2 \
#                        + probabilities["no_pair"] + (1 - chance1 - chance2)

#     # When fold and turn has happened
#     elif len(hole) == 2 & len(board) == 4:
#         if hand == "three_of_a_kind":
#             chance1 = 0.0220
#             chance2 = 0.1520
#             win_rate = probabilities["four_of_a_kind"] * chance1 \
#                        + probabilities["full_house"] * chance2 \
#                        + probabilities["three_of_a_kind"] * (1 - chance1 - chance2)

#         elif hand == "pocket_pair" :
#             chance = 0.0430
#             win_rate = probabilities["three_of_a_kind"] * chance \
#                        + probabilities["one_pair"] * (1- chance)

#         elif hand == "one_pair":
#             chance1 = 0.0650
#             chance2 = 0.1090
#             win_rate = probabilities["two_pair"] * chance1 \
#                        + probabilities["three_of_a_kind"] * (chance2 - chance1) \
#                        + probabilities["one_pair"] * (1- chance1 - chance2)

#         elif hand == "unmatched_pocket_cards":
#             chance = 0.13
#             win_rate = probabilities["one_pair"] * chance \
#                        + probabilities["no_pair"] * (1 - chance)

#         elif hand == "inside_straight":
#             chance1 = 0.0870
#             chance2 = 0.2170
#             win_rate = probabilities["straight"] * chance1 \
#                        + probabilities["one_pair"] * (chance2 - chance1) \
#                        + probabilities["no_pair"] * (1 - chance1 - chance2)

#         elif hand == "two_pair":
#             chance = 0.0870
#             win_rate = probabilities["full_house"] * chance \
#                        + probabilities["two_pair"] * (1 - chance)

#         elif hand == "open_ended_straight_flush_draw":
#             chance1 = 0.3260
#             chance2 = 0.4773
#             win_rate = probabilities["straight"] + probabilities["flush"]  * chance1 \
#                        + probabilities["straight"] + probabilities["flush"] + probabilities["one_pair"] * chance2 \
#                        + probabilities["no_pair"] + (1 - chance1 - chance2)

#     # When fold, turn, and river has happened
#     elif len(hole) == 2 & len(board) == 5:
#         # Win rate is same as hand strength when all cards are shown
#         win_rate = 1 - (float(StandardEvaluator().evaluate_hand(hole, board).index) / 7462)

#     return win_rate

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

def simulate_dealing(hole,board,n_opp):
    our_cards = list(hole)
    board = list(board)
    temp = np.ones(n_opp+1) *200
    stst = tuple(temp.tolist())
    game = NoLimitTexasHoldEm(Stakes(0, (1, 2)), stst)
    our_player = Player(game,0)
    opps = [Player(game,i+1) for i in range(n_opp)]
    #Deal hole cards
    game.nature.deal_hole(our_cards)
    while isinstance(game.stage,stages.HoleDealingStage):
        if game.nature.can_deal_hole():
            game.nature.deal_hole()
        else:
            break
    # Checks
    for i in range(n_opp+1):
        game.actor.check_call()
    # Deal flop
    if len(board) > 0:
        game.nature.deal_board(board[:3])
    else:
        game.nature.deal_board()
    # Checks
    for i in range(n_opp+1):
        game.actor.check_call()
    # Deal turn
    if len(board) > 3:
        game.nature.deal_board([board[3]])
    else:
        game.nature.deal_board()
    # Checks
    for i in range(n_opp+1):
        game.actor.check_call()
    # Deal river
    if len(board) > 4:
        game.nature.deal_board([board[4]])
    else:
        game.nature.deal_board()
    # Checks
    for i in range(n_opp+1):
        game.actor.check_call()

    for p in game.players:
        p.showdown()
    
    sts = [p.stack for p in game.players]

    if np.argmax(sts) == 0:
        return 1
    else:
        return 0

def temp_func(hole,board,n_opps):
    try: 
        win = simulate_dealing(hole,board,n_opps)
    except ValueError:
        win = 1/n_opps
    return win

def calc_win(hole,board,n_opps,n_sims=5,m_p=False):
    # n_cores = os.environ['SLURM_JOB_CPUS_PER_NODE'] # if on alice
    total = 0
    if m_p: 
        n_cores = os.cpu_count()
        pool = mp.Pool(processes=int(n_cores))
        total = pool.starmap(temp_func, [(hole,board,n_opps) for i in range(n_sims)])
        pool.close()
        pool.join()
        total = sum(total)
    else:
        for i in range(n_sims):
            try:
                win = simulate_dealing(hole,board,n_opps)
            except ValueError:
                win = 1/n_opps
            total = total + win
    # return (total/n_sims)*0.25 + 0.75* win_rate(hole,board)
    return total/n_sims


def get_opponent_stacks(game,player,max=5,starting_stack=200):
    """
    returns an array of the opponent stacks of maximum 5 opponents
    """
    players = list(game.players)
    players.remove(player)
    stacks = [p.stack/starting_stack for p in players]
    n_opp = len(stacks)
    if n_opp > max:
        raise ValueError('More than {} opponents'.format(max))
    temp = list(np.zeros(max))
    temp[:n_opp] = stacks
    stacks = temp
    return stacks

def get_players_in_hand(game,player, max = 5):
    """
    returns an array of 0s except for the indicies of the players in the current hand have a value of 1
    """
    players = list(game.players)
    players.remove(player)
    players_in_hand = np.zeros(max).tolist()
    for idx in range(len(players_in_hand)):
        if idx < len(players):
            if players[idx].is_active():
                players_in_hand[idx] = 1
    return players_in_hand

def get_opponent_bets(game,player,max=5,starting_stack=200):
    """
    should return the total stake of the opponents in this hand - not complete
    """
    players = list(game.players)
    players.remove(player)
    opponent_bets = np.zeros(max).tolist()
    for idx in range(len(opponent_bets)):
        if idx < len(players):
            if players[idx].is_active():
                opponent_bets[idx] = (players[idx].total - players[idx].stack) /starting_stack
    return opponent_bets

def evaluate_holecards(cards):
    """
    calculates hand cards strength in pre flop positions. 
    could be improved
    """
    cards = list(cards)
    if cards[0].suit == cards[1].suit:
        suited =0.25
    else:
        suited = 0
    if cards[0].rank == cards[1].rank:
        pockets = True
    else:
        pockets = False
    diff = abs(cards[0].rank.index - cards[1].rank.index)
    if diff <3:
        cont = 0.15
    elif diff < 5:
        cont = 0.1
    else:
        cont = 0
    if pockets:
        pocket_hands = [0.3,0.35,0.4,0.43,0.45,0.47,0.5,0.53,0.55,0.56,0.57,0.59,0.65]
        return pocket_hands[cards[0].rank.index]
    return min(0.65,suited + ((cards[0].rank.index/12)/2.5 + (cards[1].rank.index/12)/2.5) + cont)


def game2array(game,player,max_players=5,starting_stack=200):
    """ 
    Parameter 'player' is the main player
    Encodes a game object to two arrays:                            
        - [win_percentage,hand strength, pot, stack, to call,player position,game stage] example-->[0.3,0.5,1.2,0.3,0.1,0.25,1] 
                                                                30% win chance, 0.5 hand strenght, 1.2 pot... 
                                                                player position = player.index/len(players)
                                                                game stage = [0,1/3,2/3,1] preflop,flop,turn,river
        - [opponents in hand,opponents_stacks] --> example [1,0,1,1,0
                                                            1.3,1,1.7,0,0]
    """
    # player_cards = encode_cards(player.hole)
    # board = encode_board(game.board)
    n_opps = 0
    for p in game.players:
        if p.is_active() and p != player:
            n_opps = n_opps + 1
    if n_opps == 0:
        win_percentage = 1
    else:
        win_percentage = calc_win(player.hole, game.board,n_opps,n_sims=35)
    try :
        hand_strength = 1 - (float(StandardEvaluator().evaluate_hand(player.hole,game.board).index)/7462)
    except:
        hand_strength = evaluate_holecards(player.hole)
    players_in_hand = get_players_in_hand(game,player,max=max_players)
    opponent_stacks = get_opponent_stacks(game,player,max=max_players, starting_stack=starting_stack)
    if player.index == 0 or player.index == 1:
        pos = len(game.players) - player.index
    else: 
        pos = player.index - 2
    pos = pos/len(game.players)
    if player.can_check_call():
        to_call = player.check_call_amount/starting_stack
    else:
        to_call = 0
    if len(game.board) == 0:
        stage = 0
    elif len(game.board) < 4:
        stage = 1/3
    elif len(game.board) == 4:
        stage = 2/3
    elif len(game.board) == 5:
        stage = 1
    # opponent_bets = get_opponent_bets(game,player,max=max_players, starting_stack=starting_stack)

    array_one = [win_percentage,hand_strength, game.pot/starting_stack,player.stack/starting_stack,to_call,pos,stage]

    array_two = players_in_hand
    array_two.extend(opponent_stacks)
    # array_two = np.vstack([array_two,opponent_stacks])
    return np.array(array_one),np.array(array_two)

# print(evaluate_holecards(c))

# game = NoLimitTexasHoldEm(Stakes(0, (1, 2)), (200, 200, 200))

# our_player = PokerPlayer(game)
# opp =  PokerPlayer(game)

# print(game.stage)

# print(game.stage)
if __name__ == '__main__': 

    c = [Card(Rank.TWO,Suit.SPADE),Card(Rank.SIX,Suit.DIAMOND)]
    board = []
    # print(calc_win(c,board,3,n_sims=200))
    # print(evaluate_holecards(c))

    n_sims =5000
    start = time.time()
    tot = 0
    res = calc_win(c,board,4,n_sims=n_sims,m_p=True)
    tot = tot + res
    now = time.time()
    print('Average win rate found: ', res)
    print('Time taken with mp: ', now-start)
    start = time.time()
    tot = 0
    res = calc_win(c,board,4,n_sims=n_sims,m_p=False)
    tot = tot + res
    now = time.time()
    print('Average win rate found: ', res)
    print('Time taken without mp: ', now-start)