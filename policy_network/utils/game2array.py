
from pokerface import Stakes, NoLimitShortDeckHoldEm,NoLimitTexasHoldEm,PokerPlayer,Rank,Suit,RankEvaluator
from game_actions import deal_cards, bet_stage,deal_board
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

def get_opponent_stacks(game,player):
    """
    returns an array of the opponent stacks of maximum 7 opponents
    """
    players = list(game.players)
    players.remove(player)
    stacks = [p.stack/player.starting_stack for p in players]
    n_opp = len(stacks)
    if n_opp > 7:
        raise ValueError('More than 7 opponents')
    temp = [0,0,0,0,0,0,0]
    temp[:n_opp] = stacks
    stacks = temp
    return stacks

def game2array(game,player):
    """
    Encodes a game object to two arrays:                            where parameter 'player' is the main player
        - [win_percentage, pot, stack, to_call,player_stacks]
        - [player_position, players_in_hand]
    """

    # player_cards = encode_cards(player.hole)
    # board = encode_board(game.board)

    win_percentage = calc_win(player.hole, game.board)
    opponent_stacks = get_opponent_stacks(game,player)

    if player.can_check_call():
        to_call = player.check_call_amount
    else:
        to_call = 0

    array_one = [win_percentage,  game.pot/player.starting_stack,player.stack/player.starting_stack,to_call]
    array_one.extend(opponent_stacks)
    print(array_one)

    array_two = []
    return array_one,array_two
