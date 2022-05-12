# -*- coding: utf-8 -*-
"""
Created on Tue May  3 14:06:49 2022

@author: NatBr
"""

#https://www.splitsuit.com/simple-poker-expected-value-formula

from pokerface import PokerPlayer, Rank, Suit
import eval7

class EVAgent(PokerPlayer):
    def __init__(self, game):
        super().__init__(game)
        
    def act(self):
        possible_actions = []
        bet_sizes = []
        stack = self.stack
        pot = self.game.pot
        # print(self.game.players)
        # print(stack,pot)
        if(len(self.game.board) == 0):
            if self.can_check_call():
                #print(self.game.players[len(self.game.players)-1].check_call_amount)
                f = self.check_call
                print("EV:\t\t",f.__name__)
                f()
            else: 
                pass
        else:
            if self.can_fold():
                possible_actions.append(self.fold)
            if self.can_check_call():
                possible_actions.append(self.check_call)
                #print(self.game.players[len(self.game.players)-1].check_call_amount)
            if self.can_bet_raise():
                possible_actions.append(self.bet_raise)
                pot = pot + self.game.players[len(self.game.players)-1].check_call_amount
                min_bet = self.game.players[len(self.game.players)-1].bet_raise_min_amount
                max_bet = self.game.players[len(self.game.players)-1].bet_raise_max_amount
                # print("Min bet: {}".format(min_bet))
                # print("Max bet: {}".format(max_bet))
                # print(pot)
                if(self.game.players[len(self.game.players)-1].check_call_amount == 0): #Not facing bet
                    if(stack > 1/4 * pot and 1/4*pot > min_bet):
                        bet_sizes.append(int(1/4 * pot))
                    if(stack > 1/2 * pot):
                        possible_actions.append(int(1/2 * pot))
                    if(stack > 3/4 * pot):
                        bet_sizes.append(int(3/4 * pot))
                    if(stack > pot):
                        bet_sizes.append(pot)
                    if(stack < 1/4 * pot):
                        bet_sizes.append(stack) 
                else:
                    if(stack > 1/4 * pot and 1/4*pot > min_bet and 1/4*pot < max_bet):
                        bet_sizes.append(int(1/4 * pot))
                    if(stack > 1/2 * pot and 1/2*pot > min_bet and 1/2*pot < max_bet):
                        possible_actions.append(int(1/2 * pot))
                    if(stack > 3/4 * pot and 3/4*pot > min_bet and 3/4*pot < max_bet):
                        bet_sizes.append(int(3/4 * pot))
                    if(stack > pot and pot > min_bet and pot<max_bet):
                        bet_sizes.append(pot)
                    if(stack < min_bet):
                        bet_sizes.append(stack)
            if self.can_showdown():
                f = self.showdown
                print("EV:\t\t",f.__name__)
                f()

            elif(len(possible_actions) != 0):
                # print(possible_actions)
                # print(bet_sizes)
                Max_EV = 0
                W_per, L_per = self.EvaluateHand()
                for i in possible_actions:
                    EV = 0
                    if(i == self.check_call):
                        L_m = self.game.players[len(self.game.players)-1].check_call_amount
                        W_m = pot #Does not handle if we put money in and get raised
                        EV = (W_per*W_m) - (L_per*L_m)
                        # print(W_per, W_m, L_per, L_m)
                        # print("EV:",EV)
                        if(EV >= 0):
                            f = self.check_call
                            print("EV:\t\t",f.__name__)
                            f()
                        else:
                            f = self.fold
                            print("EV:\t\t",f.__name__)
                            f()

            else:
                pass
            
    def EvaluateHand(self):
        hra = self.game.players[len(self.game.players)-1]
        # print("Cards:", hra.hole)
        cards = []
        for card in hra.hole:
            new_card = self.ObjecttoString(card)
            cards.append(new_card)
        for card in self.game.board:
            new_card = self.ObjecttoString(card)
            cards.append(new_card)
        hand = [eval7.Card(s) for s in cards]
        MyHand = eval7.evaluate(hand)
        test = eval7.handtype(MyHand)
        hr = eval7.HandRange("22+,A2s+,K2s+,Q2s+,J2s+,T2s+,92s+,82s+,72s+,62s+,52s+,42s+,32s,A2o+,K2o+,Q2o+,J2o+,T2o+,92o+,82o+,72o+,62o+,52o+,42o+,32o") #100%
        #hr = eval7.HandRange("AKd")
        # print(hr.hands)
        #print("Hello:",hr.hands[1][0][0])
        W = 0
        L = 0
        for i in range(len(hr)):
            cards2 = []
            new_card = self.ObjecttoStringEval(hr.hands[i][0][0])
            cards2.append(new_card)
            new_card = self.ObjecttoStringEval(hr.hands[i][0][1])
            cards2.append(new_card)
            for card in self.game.board:
                new_card = self.ObjecttoString(card)
                cards2.append(new_card)
            hand = [eval7.Card(s) for s in cards2]
            OpHand = eval7.evaluate(hand)
            if(MyHand > OpHand):  ##What if same we have the same hand
                W += 1
            elif(MyHand < OpHand):
                L += 1
            test = eval7.handtype(OpHand)
        W_per = W/len(hr)
        L_per = L/len(hr)
        # print("W:%",W_per,"L%:",L_per)
        return W_per, L_per
    
    def ObjecttoString(self,card):
        if card.rank == Rank.ACE: 
            rank = "A"
        elif card.rank == Rank.KING:
            rank = "K"
        elif card.rank == Rank.QUEEN:
            rank = "Q"
        elif card.rank == Rank.JACK:
            rank = "J"
        elif card.rank == Rank.TEN:
            rank = "T"
        elif card.rank == Rank.NINE:
            rank = "9"
        elif card.rank == Rank.EIGHT:
            rank = "8"
        elif card.rank == Rank.SEVEN:
            rank = "7"
        elif card.rank == Rank.SIX:
            rank = "6"
        elif card.rank == Rank.FIVE:
            rank = "5"
        elif card.rank == Rank.FOUR:
            rank = "4"
        elif card.rank == Rank.THREE:
            rank = "3"
        elif card.rank == Rank.TWO:
            rank = "2"
            
        if card.suit == Suit.CLUB:
            suit = "c"
        elif card.suit == Suit.DIAMOND:
            suit = "d"
        elif card.suit == Suit.HEART:
            suit = "h"
        elif card.suit == Suit.SPADE:
            suit = "s"
        
        new_card = rank + suit
        return new_card
    
    def ObjecttoStringEval(self,card):
        if card.rank == 12: 
            rank = "A"
        elif card.rank == 11:
            rank = "K"
        elif card.rank == 10:
            rank = "Q"
        elif card.rank == 9:
            rank = "J"
        elif card.rank == 8:
            rank = "T"
        elif card.rank == 7:
            rank = "9"
        elif card.rank == 6:
            rank = "8"
        elif card.rank == 5:
            rank = "7"
        elif card.rank == 4:
            rank = "6"
        elif card.rank == 3:
            rank = "5"
        elif card.rank == 2:
            rank = "4"
        elif card.rank == 1:
            rank = "3"
        elif card.rank == 0:
            rank = "2"
            
        if card.suit == 0:
            suit = "c"
        elif card.suit == 1:
            suit = "d"
        elif card.suit == 2:
            suit = "h"
        elif card.suit == 3:
            suit = "s"
        
        new_card = rank + suit
        return new_card

        