# -*- coding: utf-8 -*-
"""
Created on Tue May  3 14:06:49 2022

@author: NatBr
"""

#https://www.splitsuit.com/simple-poker-expected-value-formula

from pokerface import PokerPlayer, Rank, Suit
import eval7
import EVhands

class EVAgent(PokerPlayer):
    def __init__(self, game):
        super().__init__(game)
        
    def act(self):
        active_players = 0
        Facing_bet = -1
        Facing_player = -1
        for i,player in enumerate(self.game.players):
            if(player.is_active()):
                active_players += 1
                if(player.bet > Facing_bet and player != self.game.actor):
                    Facing_player = i
                    Facing_bet = player.bet
        print(active_players, Facing_player, Facing_bet)
        possible_actions = []
        bet_sizes = []
        stack = self.stack
        pot = self.game.pot
        # print(self.game.players)
        # print(stack,pot)
        if(len(self.game.board) == 0):
            self.PossibleHands(active_players)
            if self.can_check_call():
                if(self.game.actor.check_call_amount == 0 or self.PreFlop()):
                #print(self.game.players[len(self.game.players)-1].check_call_amount)
                    f = self.check_call
                else:
                    f = self.fold
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
                pot = pot + self.game.actor.check_call_amount
                min_bet = self.game.actor.bet_raise_min_amount
                max_bet = self.game.actor.bet_raise_max_amount
                # print("Min bet: {}".format(min_bet))
                # print("Max bet: {}".format(max_bet))
                # print(pot)
                if(self.game.actor.check_call_amount == 0): #Not facing bet
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
                W_per, L_per = self.EvaluateHand(Facing_player)
                for i in possible_actions:
                    EV = 0
                    if(i == self.check_call):
                        L_m = self.game.actor.check_call_amount
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
                self.HandEliminator()

            else:
                pass
            
    def HandEliminator(self):
        for i,player in enumerate(self.game.players):
            if(player.is_active() and player != self.game.actor):
                possible_hands = []
                for i in EVhands.possible_hands[i]:
                    cards = []
                    cards2 = []
                    cards.append(i[0])
                    cards.append(i[1])
                    cards2.append(i[0])
                    cards2.append(i[1])
                    for card in self.game.board:
                        new_card = self.ObjecttoString(card)
                        cards.append(new_card)
                    hand = [eval7.Card(s) for s in cards]
                    OpHand = eval7.evaluate(hand)
                    HandType = eval7.handtype(OpHand)
                    draw_type = self.StraightDraw(cards)
                    FlushCount = self.FlushDraw(cards)
                    if(len(self.game.board) == 3): #What hands would the opp continue with on the flop?
                        if(HandType == "Pair"):
                            print(HandType)
                            #possible_hands.append(cards2)
                    if(len(self.game.board) == 4): #What hands would the opp continue with on the turn?
                        if(HandType == "Pair"):
                            print(HandType)
                    if(len(self.game.board) == 5): #What hands would the opp call with on river?
                        if(HandType == "Pair"):
                            print(HandType)
                #Save all possible hands that call to key
                #EVhands.possible_hands[i] = possible_hands
        return

    def StraightDraw(self, cards): #Not Finished
        ranking = []
        draw_type = 0 # No draw
        for card in cards:
            rank = self.StraightRank(card[0])
            ranking.append(rank)
        minimum = [12,0,1,2,3,4,5,6,7,8]
        maximum = [3,4,5,6,7,8,9,10,11,12]
        max_count = 0
        for i in range(len(minimum)):
            count = 0
            for j in range(minimum[i],maximum[i]+1):
                for k in ranking:
                    if(j == k):
                        count += 1
                if(count > max_count):
                    max_count = count
        print(cards)
        print(max_count)
        if(max_count == 2 and len(ranking) == 6):
            count = 0
            for i in range(len(ranking)-1):
                if(ranking[i] == ranking[i+1]-1):
                    count += 1
            if(count == 3):
                draw_type = 3 # Double ended straight draw
        if(max_count == 3):
            for i in range(1,len(ranking)-1):
                if(ranking[i] == ranking[i+1]-1 and ranking[i+1] == ranking[i+2]-1 and ranking[i] == ranking[i-1]+2 and ranking[i+2] == ranking[i+3]-2):
                    draw_type = 3 #Double ended straight draw
                else:
                    draw_type = 1 #Gutshot straight draw
        if(max_count == 4):
            ranking.sort()
            for i in range(len(ranking)-2): #Does not include double end 1 - 3 - 1 or 2 - 2 - 2
                if(ranking[i] == ranking[i+1]-1 and ranking[i+1] == ranking[i+2]-1 and ranking[i+2] != 12):
                    draw_type = 4 #Open ended straight draw
                else:
                    draw_type = 2 #Inside straight draw
                
        #print(ranking)
        return draw_type
    
    def FlushDraw(self, cards):
        suits = []
        for card in cards:
            suit = self.FlushRank(card[1])
            suits.append(suit)
        count = 0
        for i in range(4):
            if(suits.count(i) > count):
                count = suits.count(i)
        return count
            
    def PossibleHands(self,active_players):
        for i,player in enumerate(self.game.players):
            if i in EVhands.possible_hands.keys():
                print("key already exists")
            else:
                if(player.is_active()):
                    hands = []
                    Prange = eval7.HandRange(EVhands.hands(i,active_players))
                    for j in range(len(Prange)):
                        cards = []
                        new_card = self.ObjecttoStringEval(Prange.hands[j][0][0])
                        cards.append(new_card)
                        new_card = self.ObjecttoStringEval(Prange.hands[j][0][1])
                        cards.append(new_card)
                        hands.append(cards)
                    EVhands.possible_hands[i] = hands
        #print(EVhands.possible_hands)
        return
    
    def PreFlop(self):
        Actorcards = self.game.actor.hole
        MyRange = EVhands.possible_hands[len(self.game.players)-1]
        cards = []
        InRange = False
        for card in Actorcards:
            new_card = self.ObjecttoString(card)
            cards.append(new_card)
        for i in range(len(MyRange)):
            if(cards[0] == MyRange[i][0] and cards[1] == MyRange[i][1]):
                InRange = True
            if(cards[1] == MyRange[i][0] and cards[1] == MyRange[i][1]):
                InRange = True
        return InRange
            
    def EvaluateHand(self,opponent):
        print("My Opponent is", opponent)
        hra = self.game.actor
        print("Cards:", hra.hole)
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
        #hr = eval7.HandRange("22+,A2s+,K2s+,Q2s+,J2s+,T2s+,92s+,82s+,72s+,62s+,52s+,42s+,32s,A2o+,K2o+,Q2o+,J2o+,T2o+,92o+,82o+,72o+,62o+,52o+,42o+,32o") #100%
        #hr = eval7.HandRange("AKd")
        # print(hr.hands)
        #print("Hello:",hr.hands[1][0][0])
        W = 0
        L = 0
        #print(hr.hands)
        #print(EVhands.possible_hands[opponent])
        #print(len(EVhands.possible_hands[opponent]))
        #print(len(hr))
        for i in EVhands.possible_hands[opponent]:
            cards2 = []
            #print(i)
            #new_card = self.ObjecttoStringEval(hr.hands[i][0][0])
            cards2.append(i[0])
            #new_card = self.ObjecttoStringEval(hr.hands[i][0][1])
            cards2.append(i[1])
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
        W_per = W/len(EVhands.possible_hands[opponent])
        L_per = L/len(EVhands.possible_hands[opponent])
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
    
    def StraightRank(self,card):
        if card == "A":
            rank = 12
        elif card == "K":
            rank = 11
        elif card == "Q":
            rank = 10
        elif card == "J":
            rank = 9
        elif card == "T":
            rank = 8
        elif card == "9":
            rank = 7
        elif card == "8":
            rank = 6
        elif card == "7":
            rank = 5
        elif card == "6":
            rank = 4
        elif card == "5":
            rank = 3
        elif card == "4":
            rank = 2
        elif card == "3":
            rank = 1
        elif card == "2":
            rank = 0
        
        return rank
    
    def FlushRank(self,card):
        if card == "c":
            suit = 0
        elif card == "d":
            suit = 1
        elif card == "h":
            suit = 2
        elif card == "s":
            suit = 3
            
        return suit

        