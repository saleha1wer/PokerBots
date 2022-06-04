
import re
from chess import Board
from pandas import array
from pokerface import *
from random_agent import RandomAgent
import numpy as np
import math

# def encode_cards(cards):
#     """
#     Encodes a players cards with one-hot encoding
#     """
#     cards_array = []
#     for card in cards:
#         card_array = np.zeros(14)
#         if card.rank == Rank.ACE: 
#             idx = 12
#         elif card.rank == Rank.KING:
#             idx = 11
#         elif card.rank == Rank.QUEEN:
#             idx = 10
#         elif card.rank == Rank.JACK:
#             idx = 9
#         elif card.rank == Rank.TEN:
#             idx = 8
#         elif card.rank == Rank.NINE:
#             idx = 7
#         elif card.rank == Rank.EIGHT:
#             idx = 6
#         elif card.rank == Rank.SEVEN:
#             idx = 5
#         elif card.rank == Rank.SIX:
#             idx = 4
#         elif card.rank == Rank.FIVE:
#             idx = 3
#         elif card.rank == Rank.FOUR:
#             idx = 2
#         elif card.rank == Rank.THREE:
#             idx = 1
#         elif card.rank == Rank.TWO:
#             idx = 0
#         if card.suit == Suit.CLUB:
#             suit_value = 0
#         elif card.suit == Suit.SPADE:
#             suit_value = 1
#         elif card.suit == Suit.DIAMOND:
#             suit_value = 2
#         elif card.suit == Suit.HEART:
#             suit_value = 3
#         card_array[idx] = 1
#         card_array[13] = suit_value
#         cards_array.append(card_array)
#     return np.array(cards_array)

# def encode_board(board):
#     """
#     Encodes the cards on the board with one-hot encoding
#     """
#     board = list(board)
#     board_array = []

#     if len(board) < 5:
#         to_go = 5 - len(board)
#         no_card = np.array([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])
#         for i in range(to_go):
#             board_array.append(no_card)
            
#     board_encoded = encode_cards(board)
#     for card in board_encoded:
#         board_array.append(card)

#     return np.array(board_array)

def hand_combination(hole, board):
    ranks = [i[0] for i in hole] + [j[0] for j in board]
    suits = [i[1] for i in hole] + [j[1] for j in board]
    for i in range(len(ranks)):
        if ranks[i] == 'J':
            ranks[i] = 11
        elif ranks[i] == 'Q':
            ranks[i] = 12
        elif ranks[i] == 'H':
            ranks[i] = 13
        elif ranks[i] == 'A':
            ranks[i] = 14
    pairs = list(set([k for k in ranks if ranks.count(k) == 2]))

    # Determine the hand combination
    if hole[0][0] == hole[1][0]:
        hand = 'pocket_pair'

    elif len(pairs) == 1:
        hand = 'one_pair'

    elif len(pairs) == 2:
        hand = 'two_pair'

    elif list(set([k for k in ranks if ranks.count(k) == 3])):
        hand = 'three_of_a_kind'

    elif len(ranks) >= 4:
        sorted_ranks = sorted(list(set(ranks)))

        if any(sorted_ranks[3 + i] - sorted_ranks[i] == 3 for i in range(len(sorted_ranks) - 3)) and # suits are equal:
            hand = 'open_ended_straight_flush_draw'

        # When we have four consecutive numbers OR three consecutive numbers, break, 1 more OR two consecutive numbers, break, 2 more
        elif any(sorted_ranks[3 + i] - sorted_ranks[i] == 3 for i in range(len(sorted_ranks) - 3)) or

            # When we have three consecutive numbers, break, 1 more
            any(ranks[2 + i] - ranks[i] == 2 for i in range(len(ranks) - 2)) and

            # When we have two consecutive numbers, break, 2 more

    elif hole[0][0] != hole[1][0]:
        hand = 'unmatched_pocket_cards'

    return hand

def calc_win(hole,board):
    # https://www.pokerlistings.com/online-poker-odds-calculator#:~:text=To%20calculate%20your%20poker%20equity,(%2B4)%20%3D%2040%25.
    hand = hand_combination(hole, board)

    # Probability of getting these combinations after 7 cards
    probabilities = {
        "royal_flush" : 4324 / math.comb(52, 7),
        "straight_flush" : 37260 / math.comb(52, 7),
        "four_of_a_kind" : 224848 / math.comb(52, 7),
        "full_house" : 3473184 / math.comb(52, 7),
        "flush" : 4047644 / math.comb(52, 7),
        "straight" : 6180020 / math.comb(52, 7),
        "three_of_a_kind" : 6461620 / math.comb(52, 7),
        "two_pair" : 31433400 / math.comb(52, 7),
        "one_pair" : 58627800 / math.comb(52, 7),
        "no_pair" : 23294460 / math.comb(52, 7)
    }

    # Chance of improving your hand
    # When fold has happened
    if len(hole) == 2 & len(board) == 3:
        if hand == "three_of_a_kind":
            chance1 = 0.0430
            chance2 = 0.2780
            win_rate = probabilities["four_of_a_kind"] * chance1 \
                       + probabilities["full_house"] * chance2 \
                       + probabilities["three_of_a_kind"] * (1 - chance1 - chance2)

        elif hand == "pocket_pair" :
            chance = 0.0840
            win_rate = probabilities["three_of_a_kind"] * chance \
                       + probabilities["one_pair"] * (1- chance)

        elif hand == "one_pair":
            chance1 = 0.1250
            chance2 = 0.2040
            win_rate = probabilities["two_pair"] * chance1 \
                       + probabilities["three_of_a_kind"] * (chance2 - chance1) \
                       + probabilities["one_pair"] * (1- chance1 - chance2)

        elif hand == "unmatched_pocket_cards":
            chance = 0.2410
            win_rate = probabilities["one_pair"] * chance \
                       + probabilities["no_pair"] * (1 - chance)

        elif hand == "inside_straight":
            chance1 = 0.1650
            chance2 = 0.3840
            win_rate = probabilities["straight"] * chance1 \
                       + probabilities["one_pair"] * (chance2 - chance1) \
                       + probabilities["no_pair"] * (1 - chance1 - chance2)

        elif hand == "two_pair":
            chance = 0.1650
            win_rate = probabilities["full_house"] * chance \
                       + probabilities["two_pair"] * (1 - chance)

        elif hand == "open_ended_straight_flush_draw":
            chance1 = 0.5410
            chance2 = 0.7232
            win_rate = probabilities["straight"] + probabilities["flush"] * chance1 \
                       + probabilities["straight"] + probabilities["flush"] + probabilities["one_pair"]* chance2 \
                       + probabilities["no_pair"] + (1 - chance1 - chance2)

    # When fold and turn has happened
    elif len(hole) == 2 & len(board) == 4:
        if hand == "three_of_a_kind":
            chance1 = 0.0220
            chance2 = 0.1520
            win_rate = probabilities["four_of_a_kind"] * chance1 \
                       + probabilities["full_house"] * chance2 \
                       + probabilities["three_of_a_kind"] * (1 - chance1 - chance2)

        elif hand == "pocket_pair" :
            chance = 0.0430
            win_rate = probabilities["three_of_a_kind"] * chance \
                       + probabilities["one_pair"] * (1- chance)

        elif hand == "one_pair":
            chance1 = 0.0650
            chance2 = 0.1090
            win_rate = probabilities["two_pair"] * chance1 \
                       + probabilities["three_of_a_kind"] * (chance2 - chance1) \
                       + probabilities["one_pair"] * (1- chance1 - chance2)

        elif hand == "unmatched_pocket_cards":
            chance = 0.13
            win_rate = probabilities["one_pair"] * chance \
                       + probabilities["no_pair"] * (1 - chance)

        elif hand == "inside_straight":
            chance1 = 0.0870
            chance2 = 0.2170
            win_rate = probabilities["straight"] * chance1 \
                       + probabilities["one_pair"] * (chance2 - chance1) \
                       + probabilities["no_pair"] * (1 - chance1 - chance2)

        elif hand == "two_pair":
            chance = 0.0870
            win_rate = probabilities["full_house"] * chance \
                       + probabilities["two_pair"] * (1 - chance)

        elif hand == "open_ended_straight_flush_draw":
            chance1 = 0.3260
            chance2 = 0.4773
            win_rate = probabilities["straight"] + probabilities["flush"]  * chance1 \
                       + probabilities["straight"] + probabilities["flush"] + probabilities["one_pair"] * chance2 \
                       + probabilities["no_pair"] + (1 - chance1 - chance2)

    # When fold, turn, and river has happened
    elif len(hole) == 2 & len(board) == 5:
        # Win rate is same as hand strength when all cards are shown
        win_rate = 1 - (float(StandardEvaluator().evaluate_hand(hole, board).index) / 7462)

    return win_rate

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
    win_percentage = calc_win(player.hole, game.board)
    try :
        hand_strength = 1 - (float(StandardEvaluator().evaluate_hand(player.hole,game.board).index)/7462)
    except:
        print(player.hole,game.board)
        print('hand strength failed, board length: ', len(game.board))
        hand_strength = 0.5
    players_in_hand = get_players_in_hand(game,player,max=max_players)
    opponent_stacks = get_opponent_stacks(game,player,max=max_players, starting_stack=starting_stack)
    pos = (player.index)/len(game.players)
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
