
from pokerface import NoLimitShortDeckHoldEm,NoLimitTexasHoldEm, Stakes
from random_agent import RandomAgent
from heuristic_agent import HeuristicAgent
from mcts_agent import MCTSAgent
from EV import EVAgent
from EVhands import PossibleHands

def play_round(players,stacks,game):
    # TODO: Check out button blinds
    nls = game
    nls._players = players
    nls._verify()
    nls._setup()
    game_over = False
    print(players)
    # Deal to players
    while nls.nature.can_deal_hole():
        nls.nature.deal_hole()

    print("Players and hands:")
    for p in nls.players:
        print(p.index, p.hole)

    print("\nStart round:")
    # Initial betting
    if nls.stage != None:
        while not game_over and nls.stage.is_betting_stage():
            for p in nls.players:
                if p.is_active() and p.is_actor and p.is_player:
                    p.act()
                    if nls.is_terminal():
                        game_over = True
                        break
    # Flop
    if not game_over:
        nls.nature.deal_board()
        print("flop", nls.board, nls.stage)
        # Flop betting
        if nls.stage != None:
            while not game_over and nls.stage.is_betting_stage():
                for p in nls.players:
                    if p.is_active() and p.is_actor and p.is_player:
                        p.act()
                        if nls.is_terminal():
                            game_over = True
                            break
    # Turn
    if not game_over:
        nls.nature.deal_board()
        print("turn", nls.board, nls.stage)
        # Turn betting
        if nls.stage != None:
            while not game_over and nls.stage.is_betting_stage():
                for p in nls.players:
                    if p.is_active() and p.is_actor and p.is_player:
                        p.act()
                        if nls.is_terminal():
                            game_over = True
                            break
    # River
    if not game_over:
        nls.nature.deal_board()
        print("river", nls.board, nls.stage)
        # River betting (I don't think nls.stage != None at this point and am not sure if after river betting is supported)
        if nls.stage != None:
            while not game_over and nls.stage.is_betting_stage():
                for p in nls.players:
                    if p.is_active() and p.is_actor and p.is_player:
                        p.act()
                        if nls.is_terminal():
                            game_over = True
                            break
    # Showdown
    print("\n")
    new_stacks = []
    print(nls.pot)
    for pot in nls.side_pots:
        print("sidepot:", pot)
    print("Stage:",nls.stage)
    if nls.stage != None:
        while(nls.stage.is_showdown_stage()):
            for p in nls.players:
                print(p,p.can_showdown(),)
                if p.can_showdown():
                    p.showdown()
                    print(p)
            if(nls.stage == None):
                break
            print("Showdown stage:",nls.stage.is_showdown_stage())
    for p in nls.players:
        if p.stack != 0:
            new_stacks.append(p.stack)
    print(new_stacks)
    return new_stacks

def play_game(n_rounds,players,game,starting_stacks,stakes, button, no_players):
    # Play multiple rounds using same players 
    # Players is a list of the players
    stacks = starting_stacks
    blinds = (0,2,4)
    for round in range(n_rounds):
        print('starting round ',round)
        stacks = play_round(players,stacks,game)
        for player in players:
            if player.stack != 0:
                no_players -= 1
        button += 1
        if(button == no_players-1):
            sb = 0
            bb = 1
            button = -1 #Reset button to 0
        elif(button == no_players-2):
            sb = button + 1
            bb = 0
        else:
            sb = button + 1
            bb = button + 2
        blinds = {sb: 1, bb: 2}
        if len(stacks) > 1:
            #game = NoLimitShortDeckHoldEm(stakes,stacks)
            game = NoLimitTexasHoldEm(Stakes(0, blinds),stacks)
        new_players = []
        blinds = {0: 1, 1: 2}

            
        for player in players:
            if player.stack != 0:
                if isinstance(player, RandomAgent):
                    new_players.append(RandomAgent(game))
                elif isinstance(player, HeuristicAgent):
                    new_players.append(HeuristicAgent(game))
                elif isinstance(player, MCTSAgent):
                    new_players.append(MCTSAgent(game))
                elif isinstance(player, EVAgent):
                    new_players.append(EVAgent(game))

        players = new_players
        if len(players) == 1:
            print('Winner :', type(players[0]))
            break
    