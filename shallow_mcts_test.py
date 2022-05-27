from cgitb import reset
import numpy as np
import copy
from pokerface import *
from random_agent import RandomAgent
from random import Random, shuffle
from game_actions import deal_board, deal_cards, bet_stage, showdown_stage

class ShallowMCTS(PokerPlayer):
    def __init__(self, game):
        super().__init__(game)
        # Set number of simulations per action
        self.n_sims_per_action = 500
        self.agent_index = 0
        self.reset_player_index(self.game)

        shadow_player_type = RandomAgent
        stacks = ()

        for player in game.players:
            stacks = (*stacks, player.total)
        self.shadow_game = NoLimitTexasHoldEm(game.stakes, stacks)
        
        for i, p in enumerate(self.shadow_game._players):
            player_instance = shadow_player_type(self.shadow_game)
            player_instance._stack = self.shadow_game.players[i].stack
            self.shadow_game._players[i] = player_instance
            self.shadow_game._players[i]._game = self.shadow_game
        self.shadow_game._verify()
        self.shadow_game._setup()
        print("Shadow game setup with", self.shadow_game.players)
        # print("stacks", stacks)
        

    def get_possible_actions(self, game):
        # Return a list of possible actions
        possible_actions = []
        if self.can_check_call():
            possible_actions.append(["check_call"])
        for i in [1/4, 2/4, 3/4, 1]:
            if self.can_bet_raise():           
                raise_amount = max(min(self.stack, int(i * game.pot)), self.bet_raise_min_amount)
                if self.can_bet_raise(raise_amount):
                    raise_action = ["raise", raise_amount]
                    if raise_action not in possible_actions:
                        possible_actions.append(raise_action)
        if self.can_fold():
            possible_actions.append(["fold"])
        return possible_actions
    
    def reset_player_index(self, game):
        # Update player index value to the value linked in the game
        for i, player in enumerate(game.players):
            if player == self:
                self.agent_index = i

    def set_players2random(self, game):
        # TODO: this function has to turn the pokeragents into random bots
                
        # for p in game.players:
        #     p.act = self.callbot2copy.act
        return game
    
    def shuffle_opponents(self, game):
        index2skip = []
        # Add opponent cards to deck
        for i, p in enumerate(game.players):
            if i != self.agent_index:
                if len(p.hole) == 2:
                    game._deck.append(p.hole[0])
                    game._deck.append(p.hole[1])
                else:
                    # Opponent has folded and doesnt have cards
                    index2skip.append(i)

        # Shuffle deck
        shuffle(game._deck)

        # Redeal cards to opponents
        for i, p in enumerate(game.players):
            if i != self.agent_index and i not in index2skip:
                p._hole = tuple(game._deck.draw(2))
        return game
    
    def playout(self, game):
        # Perform simulations of an action with different cards
        results = []
        for i in range(self.n_sims_per_action):
            # print("performing simulation", i)
            playout_copy = copy.deepcopy(game)
            playout_copy = self.shuffle_opponents(playout_copy)

            # TODO: THE FOLLOWING STILL NEEDS TO BE MADE INTO RANDOM ACTIONS NOT CALLING
            # Preferably, this synergises with set_players2random
            while playout_copy.stage != None:
                for p in playout_copy.players:
                    # print(p.hole)
                    if p.is_actor():
                    #     p.act()
                    # if p.can_check_call():
                    #     p.check_call()
                        # if p.can_showdown():
                        #     print("stages", playout_copy.stage, playout_copy.stages[-1], playout_copy.players[-1].hole)
                        #     p.showdown(True)
                        # else:
                        p.act()
                if playout_copy.nature.can_deal_board():
                    playout_copy.nature.deal_board()
                if playout_copy.stage.is_showdown_stage():
                    print(playout_copy.pot)
                    for p in playout_copy.players:
                        print(p.bet)
                    # for side_pot in playout_copy._side_pots:
                    #     print(side_pot)
                    players = sorted(playout_copy.players, key=PokerPlayer._put.fget, reverse=True)
                    side_pots = []
                    pot = 0
                    prev = 0

                    while pot < playout_copy.pot:
                        total = 0
                        # for pl in playout_copy.players:
                        print(players, pot, playout_copy.pot)
                        print(playout_copy.pot, players[-1].bet)
                        cur = players[-1]._put
                        print("cur prev", cur, prev, pot, playout_copy.pot)

                        amount = len(players) * (cur - prev)

                        side_pots.append(playout_copy._SidePot(
                            filter(PokerPlayer.is_active, players), amount,
                        ))

                        pot += amount
                        prev = players.pop()._put

                    # for p in playout_copy.players:
                    #     if p.can_showdown():
                    #         p.showdown(True)
            results.append(playout_copy.players[self.agent_index].payoff)
        # res = (len([ele for ele in test_list if ele > 0]) / len(test_list))
        return np.mean(results)

    def update_shadow_game(self):
        # THIS IS BAD CODE, YOU HAVE BEEN WARNED
        self.reset_player_index(self.game)
        if len(self.hole) == 0:
            print("Assume the agent has folded, this should never be triggered")
            return
        else:
            # Hole dealing stage, deal random cards to opponents, own cards to ourselves
            self.shadow_game._pot = self.game.pot
            # self.shadow_game._side_pots = []
            # self.shadow_game.
            # self.shadow_game.
            print("updated shadow pot")
            if self.hole[0] in self.shadow_game._deck or self.hole[1] in self.shadow_game.deck:
                # Our cards are still in the deck
                print("deal shadow cards")
                self.shadow_game.players[self.agent_index]._hole = self.shadow_game._deck.draw(self.hole)
                for j, p in enumerate(self.shadow_game.players):
                    if j != self.agent_index:
                        p._hole = self.shadow_game._deck.draw(2)

            if self.shadow_game.board != self.game.board:
                # Update board
                print("Update shadow board")
                for card in self.game.board:
                    if card not in self.shadow_game.board:
                        print("Shadow board card missing")
                        # A card is missing on the shadow board, check if card is in deck
                        if card in self.shadow_game.deck:
                            print("Shadow board card retrieved from deck")
                            self.shadow_game._board.append(self.shadow_game._deck.draw(card))
                        else:
                            # Card not in deck, must be in opponents' hands
                            for j, p in enumerate(self.shadow_game.players):
                                for hole_card in p._hole:
                                    if hole_card == card:
                                        print("Found player with shadow board card, current hand", p.hole)
                                        self.shadow_game._board.append(hole_card)
                                        hole_card = self.shadow_game._deck.draw(1)
                                        print("New hand", p.hole)


            for i, p in enumerate(self.shadow_game.players):
                p._bet = self.game.players[i].bet
                p._starting_stack = self.game.players[i].starting_stack
                p._total = self.game.players[i].total
                print("updated shadow bets")
            
            # while self.shadow_game.stage.is_hole_dealing_stage() or self.shadow_game.stage.is_board_dealing_stage():
                # CHECK IF Big = True
                # self.shadow_game._stage = BettingStage(True, self.shadow_game)
            while not self.shadow_game.stage.is_betting_stage():
                self.shadow_game._update()
                print("Shadow stage set to betting stage")
            print(self.shadow_game.actor)
            
            while self.shadow_game.stage.is_betting_stage():
                for i, p in enumerate(self.shadow_game.players):
                    if p.is_actor():
                        if i == self.agent_index:
                            print("Arrived at true status")
                            self.shadow_game._verify()
                            return
                        else:
                            if len(p.hole) == 0:
                                print("A player folded")
                                p.fold()
                            else:
                                print("A player called")
                                p.check_call()

    def act(self):
        print("sMCTS is evaluating options, this takes a couple of seconds")
        # print("SMCTS has", self.hole, "\tBoard is", self.game.board)
        game_copy = copy.deepcopy(self.game)
        game_copy._verify()
        # self.reset_player_index(self.game)
        self.update_shadow_game()
        action_scores = []

        game_copy = self.set_players2random(game_copy)
        possible_actions = self.get_possible_actions(game_copy)

        for action in possible_actions:
            reset_state = copy.deepcopy(self.shadow_game)
            reset_state._verify()
            if action[0] == "fold":
                reset_state.players[self.agent_index].fold()
            elif action[0] == "check_call":
                reset_state.players[self.agent_index].check_call()
            elif action[0] == "raise":
                reset_state.players[self.agent_index].bet_raise(action[1])
            
            action_score = self.playout(reset_state)
            action_scores.append(action_score)
            print(action, action_score)
            
        best_action_i = np.argmax(action_scores)
        best_action = possible_actions[best_action_i]

        if best_action[0] == "fold":
            self.fold()
            print("SMCTS:\t\t folds")

        elif best_action[0] == "check_call":
            self.check_call()
            print("SMCTS:\t\t calls")

        elif best_action[0] == "raise":
            self.bet_raise(best_action[1])
            print("SMCTS:\t\t raises", best_action[1])
