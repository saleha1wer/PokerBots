
from pokerface import NoLimitShortDeckHoldEm,NoLimitTexasHoldEm
from random_agent import RandomAgent
from heuristic_agent import HeuristicAgent
from mcts_agent import MCTSAgent
from ev_agent import EVAgent

def play_round(players,stacks,game):
    # TODO: Check out button blinds
    nls = game
    nls._players = players
    nls._verify()
    nls._setup()
    game_over = False

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
    print(nls.pot,nls.side_pots)
    for p in nls.players:
        print(p,p.can_showdown())
        if p.can_showdown():
                p.showdown()
        print(p)
    for p in nls.players:
        if p.stack != 0:
            new_stacks.append(p.stack)

    return new_stacks

def play_game(n_rounds,players,game,starting_stacks,stakes):
    # Play multiple rounds using same players 
    # Players is a list of the players
    stacks = starting_stacks
    for round in range(n_rounds):
        print('starting round ',round)
        stacks = play_round(players,stacks,game)
        if len(stacks) > 1:
            #game = NoLimitShortDeckHoldEm(stakes,stacks)
            game = NoLimitTexasHoldEm(stakes,stacks)
        new_players = []
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
    