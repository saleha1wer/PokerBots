
import re
from chess import Board
from pandas import array
from pokerface import Stakes, NoLimitShortDeckHoldEm,NoLimitTexasHoldEm,PokerPlayer,Rank,Suit,RankEvaluator,StandardEvaluator
from random_agent import RandomAgent
import numpy as np 

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

def calc_win(hole,board):
    return 0

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
        - [win_percentage,hand strength, pot, stack, to call,player position,game stage] example-->[0.3,1.2,0.3,0.1,0.25] 
                                                                30% win chance, 1.2 pot... 
                                                                player position = player.index/len(players)
        - [opponents in hand,opponents_stacks] --> example [1,0,1,1,0
                                                            1.3,1,1.7,0,0]
    """
    # player_cards = encode_cards(player.hole)
    # board = encode_board(game.board)
    win_percentage = calc_win(player.hole, game.board)
    hand_strength = 1 - (float(StandardEvaluator().evaluate_hand(player.hole,game.board).index)/7462)
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
