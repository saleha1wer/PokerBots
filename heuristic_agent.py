from pokerface import PokerPlayer, Rank,Ranks
from pokerface.evaluators import ShortDeckEvaluator
import numpy as np
import random
"""
This is our heuristic agent that will play poker using some heuristics. The class inherits everything
from the PokerPlayer class. The act function is used to select and perform an action.


TODO:
- Make the raise/bet amount dependent on some heuristic (strength of hand maybe?)
- We can probably improve the heuristics 
- Debug, make sure running correctly. 
    - For example, the game winner does not always have stack = 600, which should be the case always I think, right?
"""

class HeuristicAgent(PokerPlayer):
    def __init__(self, game):
        super().__init__(game)
        
    def preflopevaluator(self):
        
        return
    
    def act(self):
        evaluator = ShortDeckEvaluator()
        low = self.get_lowest_card()
        high = self.get_highest_card()
        hasPair = self.has_pair()   
        total_pot = self.game.pot / 2 # pot in terms of big blinds
        hra = self.game.players[len(self.game.players)-1] # if hra is last player

        possible_actions = []
        if self.can_fold(): possible_actions.append(self.fold)
        if self.can_check_call(): possible_actions.append(self.check_call)
        if self.can_bet_raise():
            # Always raise by the minimum amount
            chips_raise = self.bet_raise_min_amount
            possible_actions.append(self.bet_raise)

        if len(possible_actions) != 0:
            print("Cards:", hra.hole)
            if(len(self.game.board) == 0):
                print("Deciding best action for pre-flop")
                if low < 9 and high < 12: # The paper used 'low < 7 and high < 11'. I slightly changed it as we are doing short deck poker. 
                    f = self.check_call
                elif total_pot <= 2 :
                    f = self.bet_raise
                elif hasPair and self.can_bet_raise():
                    f = self.bet_raise
                elif total_pot >= 6 and self.can_fold():
                    f = self.fold
                else:
                    f = self.check_call
            elif(len(self.game.board) == 3):
                print("Deciding best action for flop")
                x = evaluator.evaluate_hand(hra.hole, self.game.board)
                print("Im here:",x.__dict__) #Tried the pokerface evaluate function seems to be taking a long time.
                index = getattr(x,"_index")
                print(getattr(x,"_index"), type(getattr(x,"_index")))
                if(index<350 and self.can_bet_raise()):
                    f = self.bet_raise
                elif(index>850 and self.can_fold()):
                    f = self.fold
                else:
                    f = self.check_call
            elif(len(self.game.board) == 4):
                print("Deciding best action for turn")
                x = evaluator.evaluate_hand(hra.hole, self.game.board)
                print("Im here:",x.__dict__) #Tried the pokerface evaluate function seems to be taking a long time.
                index = getattr(x,"_index")
                if(index<=350 and self.can_bet_raise()):
                    f = self.bet_raise
                elif(index>850 and self.can_fold()):
                    f = self.fold
                else:
                    f = self.check_call
            elif(len(self.game.board) == 5):
                x = evaluator.evaluate_hand(hra.hole, self.game.board)
                print("Im here:",x.__dict__) #Tried the pokerface evaluate function seems to be taking a long time.
                print("Deciding best action for river")
                index = getattr(x,"_index")
                if(index<350 and self.can_bet_raise()):
                    f = self.bet_raise
                elif(index>850 and self.can_fold()):
                    f = self.fold
                else:
                    f = self.check_call
            # Heuristic is from : http://game.engineering.nyu.edu/wp-content/uploads/2018/05/generating-beginner-heuristics-for-simple-texas-holdem.pdf  
            # Figure 5: "The best 4-statement heuristic found with genetic programming"

            if f == self.bet_raise:
                self.bet_raise(chips_raise)
                print(f, chips_raise)
            else:
                f()
                print(f)
        else:
            # print("No possible actions")
            pass

    def has_pair(self):
        board = self.game.board
        player_cards = self.hole
        pair = False
        for card in board:
            if card.rank == player_cards[0].rank or card.rank == player_cards[1].rank:
                pair = True
        return pair

    def get_lowest_card(self): 
        # return lowest card from a set of cards as an integer (1 --> 14)
        cards = self.hole
        min = 15
        for card in cards:
            if card.rank == Rank.ACE: 
                rank = 14
            elif card.rank == Rank.KING:
                rank = 13
            elif card.rank == Rank.QUEEN:
                rank = 12
            elif card.rank == Rank.JACK:
                rank = 11
            elif card.rank == Rank.TEN:
                rank = 10
            elif card.rank == Rank.NINE:
                rank = 9
            elif card.rank == Rank.EIGHT:
                rank = 8
            elif card.rank == Rank.SEVEN:
                rank = 7
            elif card.rank == Rank.SIX:
                rank = 6 
            else:
                raise ValueError('No Rank Found')
            if rank < min:
                min = rank 
        return min

    def get_highest_card(self):
        # return highest card from a set of cards as an integer (1 --> 14)
        cards = self.hole
        max = 0
        for card in cards:
            if card.rank == Rank.ACE: 
                rank = 14
            elif card.rank == Rank.KING:
                rank = 13
            elif card.rank == Rank.QUEEN:
                rank = 12
            elif card.rank == Rank.JACK:
                rank = 11
            elif card.rank == Rank.TEN:
                rank = 10
            elif card.rank == Rank.NINE:
                rank = 9
            elif card.rank == Rank.EIGHT:
                rank = 8
            elif card.rank == Rank.SEVEN:
                rank = 7
            elif card.rank == Rank.SIX:
                rank = 6 
            else:
                raise ValueError('No Rank Found')
            if rank > max:
                max = rank 
        return max


