# -*- coding: utf-8 -*-
"""
Created on Tue May  3 14:06:49 2022

@author: NatBr
"""

#https://www.splitsuit.com/simple-poker-expected-value-formula

from pokerface import PokerPlayer, Rank, Suit
import eval7
import EVhands
import holdem_calc
import PreFlop
import Ranges

class EVAgent(PokerPlayer):
    def __init__(self, game):
        super().__init__(game)
        
    def act(self): #Acting function
        active_players = 0
        Facing_bet = -1
        Facing_player = -1
        ActingOrder = EVhands.PreFlopAO(len(self.game.players)) #Get acting order of each player
        for i in ActingOrder:
            if(self.game.players[i].is_active()):
                active_players += 1
                if(self.game.players[i].bet > Facing_bet and self.game.players[i] != self.game.actor):
                    Facing_player = i
                    Facing_bet = self.game.players[i].bet
        possible_actions = []
        bet_sizes = []
        stack = self.stack
        pot = self.game.pot
        self.PossibleHands(active_players)
        if(len(self.game.board) == 0):
            action, bb = self.PreFlopAction(Facing_player, Facing_bet,active_players)
            if(action == "check/call" and self.can_check_call() or self.check_call_amount == 0):
                f = self.check_call
                print("EV:\t\t",f.__name__)
                f()
            elif(action == "bet"):
                if(PreFlop.actions['i'] == 2):
                    if(2.5*bb > stack):
                        f = self.check_call
                    else:
                        amount = 2.5*bb
                        f = self.bet_raise
                elif(PreFlop.actions['i'] == 3):
                    if(3*Facing_bet >= stack): #All-in Call
                        f = self.check_call
                    elif(Facing_bet * 3 <= self.bet_raise_max_amount):
                        amount = 3 * Facing_bet
                        f = self.bet_raise
                    else:
                        amount = self.bet_raise_max_amount
                        f = self.bet_raise
                elif(PreFlop.actions['i'] == 4):
                    if(2.5*Facing_bet >= stack): #All-in Call
                        f = self.check_call
                    elif(Facing_bet * 2.5 <= self.bet_raise_max_amount):
                        amount = 2.5 * Facing_bet
                        f = self.bet_raise
                    else:
                        amount = self.bet_raise_max_amount
                        f = self.bet_raise
                elif(PreFlop.actions['i'] == 5):
                    if(stack >= self.check_call_amount):
                        amount = stack
                        f = self.bet_raise
                    else:
                        f = self.check_call
                elif(PreFlop.actions['i'] >= 6):
                    if(stack >= self.check_call_amount):
                        amount = stack
                        f = self.bet_raise
                    else:
                        f = self.check_call
                print("EV:\t\t",f.__name__)
                if(f != self.check_call):
                    Min_stacks = True
                    for player in self.game.players:
                        if(player != self.game.actor and player.stack >= 2): 
                            Min_stacks = False
                    if(Min_stacks): #Cannot bet when opp. stack size gets too low
                        f = self.check_call
                        print("EV:\t\t",f.__name__)
                        f()
                    else:
                        f(amount)
                else:
                    f()
            elif(action == "fold" and self.can_fold()):
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
            if self.can_bet_raise():
                possible_actions.append(self.bet_raise)
                pot = pot + self.game.actor.check_call_amount
                min_bet = self.game.actor.bet_raise_min_amount
                max_bet = self.game.actor.bet_raise_max_amount
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
                Max_EV = 0 #Applicable if betting would occus post-flop
                W_per, L_per = self.EvaluateHand(Facing_player)
                for i in possible_actions:
                    EV = 0
                    if(i == self.check_call):
                        L_m = self.game.actor.check_call_amount
                        W_m = pot #Does not handle if we put money in and get raised
                        EV = (W_per*W_m) - (L_per*L_m)
                        if(EV >= 0):
                            f = self.check_call
                            print("EV:\t\t",f.__name__)
                            f()
                        else:
                            f = self.fold
                            print("EV:\t\t",f.__name__)
                            f()
                #self.HandEliminator()
            else:
                pass
            
    def HandEliminator(self): #The idea behind this function would be to narrow down ranges for post-flop play. This Function is not used
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
                        if(HandType == "Pair" or HandType == "Two Pair" or HandType == "Trips" or HandType == "Straight" or HandType == "Flush" or HandType == "Full House" or HandType == "Straight Flush" or FlushCount >= 3 or draw_type > 0):
                            print(HandType)
                            print(cards2)
                            #possible_hands.append(cards2)
                    if(len(self.game.board) == 4): #What hands would the opp continue with on the turn?
                        if(HandType == "Pair"):
                            print(HandType)
                            print(cards2)
                    if(len(self.game.board) == 5): #What hands would the opp call with on river?
                        if(HandType == "Pair"):
                            print(HandType)
                #Save all possible hands that call to key
                #EVhands.possible_hands[i] = possible_hands
        return

    def StraightDraw(self, cards): #This function is not used but would be able to check for possible straights on future streets
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
        if(max_count == 2 and len(ranking) == 6):
            count = 0
            for i in range(len(ranking)-1):
                if(ranking[i] == ranking[i+1]-1):
                    count += 1
            if(count == 3):
                draw_type = 3 # Double ended straight draw
        if(max_count == 3):
            for i in range(1,len(ranking)-2):
                if(ranking[i] == ranking[i+1]-1 and ranking[i+1] == ranking[i+2]-1 and ranking[i] == ranking[i-1]+2 and ranking[i+2] == ranking[i+3]-2):
                    draw_type = 3 #Double ended straight draw
                elif(ranking[i] == ranking[i+1]-1 and ranking[i+1] == ranking[i+2]-1 and (ranking[i] == ranking[i-1]+1 or ranking[i+2] == ranking[i+3]-1)):
                    draw_type = 1 #Gutshot straight draw
        if(max_count == 4):
            ranking.sort()
            for i in range(len(ranking)-2): #Does not include double end 1 - 3 - 1 or 2 - 2 - 2
                if(ranking[i] == ranking[i+1]-1 and ranking[i+1] == ranking[i+2]-1 and ranking[i+2] != 12):
                    draw_type = 4 #Open ended straight draw
                else:
                    draw_type = 2 #Inside straight draw
                
        return draw_type
    
    def FlushDraw(self, cards): #This function is not used but would be used to check for possible flushes on future streets
        suits = []
        for card in cards:
            suit = self.FlushRank(card[1])
            suits.append(suit)
        count = 0
        for i in range(4):
            if(suits.count(i) > count):
                count = suits.count(i)
        return count
            
    def PossibleHands(self,active_players): #Translates hand ranges into a list of possible hands
        Actorcards = self.game.actor.hole
        cards = []
        for card in Actorcards:
            new_card = self.ObjecttoString(card)
            cards.append(new_card)
        for i,player in enumerate(self.game.players):
            if i in EVhands.possible_hands.keys():
                if(len(self.game.board) == 0):
                    print("key already exists")
                else:
                    hands = []
                    for hand in EVhands.possible_hands[i]: #Remove board cards from opp range
                        allowed = True
                        for board_card in self.game.board:
                            board_card = self.ObjecttoString(board_card)
                            if(hand[0] == board_card or hand[1] == board_card):
                                allowed = False
                        if(allowed):
                            hands.append(hand)
                    EVhands.possible_hands[i] = hands
                    
            else:
                if(player.is_active()):
                    hands = []
                    Prange = eval7.HandRange(EVhands.hands(i,active_players))
                    for j in range(len(Prange)):
                        Oppcards = []
                        new_card = self.ObjecttoStringEval(Prange.hands[j][0][0])
                        Oppcards.append(new_card)
                        new_card2 = self.ObjecttoStringEval(Prange.hands[j][0][1])
                        Oppcards.append(new_card2)
                        allowed = True
                        for card in cards:
                            if(card == Oppcards[0] or card == Oppcards[1]): #Elimate EV starting cards from opponents range
                                allowed = False
                        if(allowed):
                            hands.append(Oppcards)
                    EVhands.possible_hands[i] = hands
        return
    
    def PreFlopAction(self, Facing_player, Facing_bet,n): #Find the best action for pre-flop
        print(PreFlop.actions)    
        Actorcards = self.game.actor.hole
        big_blind = 0
        for key, value in self.game.stakes.blinds.items():
            if(value > big_blind):
                big_blind = value
        count = 0
        for i,player in enumerate(self.game.players):
            if(player.bet == big_blind):
                count += 1
            if player == self.game.actor:
                my_index = i
        my_position = EVhands.positions[my_index]
        my_position = EVhands.Positiontranslator(my_position,len(self.game.players))
        Facing_player = EVhands.positions[Facing_player]
        Facing_position = EVhands.Positiontranslator(Facing_player,len(self.game.players))
        if(PreFlop.actions['i'] == 2):
            if(my_position == "sb"):
                if((my_position,"call") in PreFlop.RangeRFI.keys()):
                    CallRange = PreFlop.RangeRFI[my_position,"call"]
                    RaiseRange = PreFlop.RangeRFI[my_position,"raise"]
                else:
                    CallRange = PreFlop.RangeRFI[my_position,Facing_position,"call"]
                    RaiseRange = PreFlop.RangeRFI[my_position,Facing_position,"raise"]
            elif(my_position == "bb"):
                if((my_position,Facing_position,"call") in PreFlop.RangeRFI.keys()):
                    CallRange = PreFlop.RangeRFI[my_position,Facing_position,"call"]
                    RaiseRange = PreFlop.RangeRFI[my_position,Facing_position,"raise"]
                else:
                    CallRange = PreFlop.RangeFacing3bet[my_position,Facing_position,"call"]
                    RaiseRange = PreFlop.RangeFacing3bet[my_position,Facing_position,"raise"]
            else:
                MyRange = PreFlop.RangeRFI[my_position]
                if(n>3):
                    n = 3
                CallRange = ""
                RaiseRange = Ranges.Rangeselection(n,MyRange)
        elif(PreFlop.actions['i'] == 3):
            if((my_position,Facing_position,"call") in PreFlop.RangeFacingRFI.keys()): 
                if(Facing_bet/big_blind <15): #Cap the range for certain bet size as we want to narrow down the range if bet is too wild
                    CallRange = PreFlop.RangeFacingRFI[my_position,Facing_position,"call"]
                    RaiseRange = PreFlop.RangeFacingRFI[my_position,Facing_position,"raise"]
                else:
                    CallRange = ""
                    RaiseRange = PreFlop.RangeFacing4bet[my_position,Facing_position,"All-in"]
            else:
                if(Facing_bet/big_blind < 35):
                    CallRange = PreFlop.RangeFacing3bet[my_position,Facing_position,"call"]
                    RaiseRange = PreFlop.RangeFacing3bet[my_position,Facing_position,"raise"]
                else:
                    CallRange = ""
                    RaiseRange = PreFlop.RangeFacing5bet[my_position,Facing_position,"All-in"]
        elif(PreFlop.actions['i'] == 4):
            if((my_position,Facing_position,"call") in PreFlop.RangeFacing3bet.keys()):
                if(Facing_bet/big_blind < 35):
                    if(my_position != "sb" and Facing_position != "bb"):
                        CallRange = PreFlop.RangeFacing3bet[my_position,Facing_position,"call"]
                        RaiseRange = PreFlop.RangeFacing3bet[my_position,Facing_position,"raise"]
                    else:
                        if(my_index in PreFlop.actions.keys()):
                            if(PreFlop.actions[my_index] == 'call'):
                                CallRange = PreFlop.RangeFacing3bet[my_position,Facing_position,"limp/call"]
                                RaiseRange = PreFlop.RangeFacing3bet[my_position,Facing_position,"limp/raise"]
                else:
                    CallRange = ""
                    RaiseRange = PreFlop.RangeFacing5bet[my_position,Facing_position,"All-in"]
            else:
                CallRange = ""
                RaiseRange = PreFlop.RangeFacing4bet[my_position,Facing_position,"All-in"]
        elif(PreFlop.actions['i'] == 5):
            if((my_position,Facing_position,"All-in") in PreFlop.RangeFacing4bet.keys()):
                CallRange = ""
                RaiseRange = PreFlop.RangeFacing4bet[my_position,Facing_position,"All-in"]
            else:
                CallRange = ""
                RaiseRange = PreFlop.RangeFacing5bet[my_position,Facing_position,"All-in"]
        elif(PreFlop.actions['i'] >= 6):
            if((my_position,Facing_position,"All-in") in PreFlop.RangeFacing5bet.keys()):
                CallRange = ""
                RaiseRange = PreFlop.RangeFacing5bet[my_position,Facing_position,"All-in"]
            else:
                CallRange = ""
                RaiseRange = PreFlop.RangeFacing4bet[my_position,Facing_position,"All-in"]

        CallRange = eval7.HandRange(CallRange).hands
        RaiseRange = eval7.HandRange(RaiseRange).hands

        cards = []
        InCallRange = False
        InRaiseRange = False
        for card in Actorcards:
            new_card = self.ObjecttoString(card)
            cards.append(new_card)
        for i in range(len(CallRange)):
            cards2 = []
            cards2.append(self.ObjecttoStringEval(CallRange[i][0][0]))
            cards2.append(self.ObjecttoStringEval(CallRange[i][0][1]))
            if(cards[0] == cards2[0] and cards[1] == cards2[1]):
                InCallRange = True
            if(cards[1] == cards2[0] and cards[0] == cards2[1]):
                InCallRange = True
        for i in range(len(RaiseRange)):
            cards2 = []
            cards2.append(self.ObjecttoStringEval(RaiseRange[i][0][0]))
            cards2.append(self.ObjecttoStringEval(RaiseRange[i][0][1]))
            if(cards[0] == cards2[0] and cards[1] == cards2[1]):
                InRaiseRange = True
            if(cards[1] == cards2[0] and cards[0] == cards2[1]):
                InRaiseRange = True
                
        if(InCallRange == True):
            action = "check/call"
        elif(InRaiseRange == True):
            action = "bet"
        elif(InCallRange == False and InRaiseRange == False):
            action = "fold"
                
        return action, big_blind
            
    def EvaluateHand(self,opponent): #Evaluates hands to call post-flop
        W_per = 0
        L_per = 0
        N = 0
        hra = self.game.actor
        cards = []
        for card in hra.hole:
            new_card = self.ObjecttoString(card)
            cards.append(new_card)
        board = []
        for card in self.game.board:
            new_card = self.ObjecttoString(card)
            board.append(new_card)
        for i in EVhands.possible_hands[opponent]:
            cards2 = []
            cards2.append(i[0])
            cards2.append(i[1])
            N += 1
            equity = holdem_calc.calculate(board, True, 1, None, [cards[0], cards[1], cards2[0], cards2[1]], False)          
            W_per += equity[1]
            L_per += 1 - equity[1]
        W_per = W_per/N
        L_per = L_per/N  
        # print("W:%",W_per,"L%:",L_per)
        return W_per, L_per
    
    def ObjecttoString(self,card): #Converts cards to strings from Pokerface library
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
    
    def ObjecttoStringEval(self,card): #Converts cards to strings from Eval7 library
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
    
    def StraightRank(self,card): #Used to determine straight draws
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
    
    def FlushRank(self,card): #Used to determine flush draws
        if card == "c":
            suit = 0
        elif card == "d":
            suit = 1
        elif card == "h":
            suit = 2
        elif card == "s":
            suit = 3
            
        return suit

        