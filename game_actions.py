import PreFlop

def increment_p_count(n, n_players):
    # Function used for looping through players
    n += 1
    n %= n_players
    return n

def deal_cards(game):
    # Deals cards at the start of the game
    if game.stage != None:
        while game.stage.is_dealing_stage():
            if not game.nature.can_deal_hole():
                break
            game.nature.deal_hole()
            if game.stage == None: return game
    return game

def deal_board(game):
    # Deals board cards during the game
    if game.stage != None:
        while game.stage.is_board_dealing_stage():
            game.nature.deal_board()
            if game.stage == None: return game
    return game

def bet_stage(game):
    # Allows for players to bet through the .act() function
    # Loops through all players until betting phase is done
    if game.stage != None:
        p_iter = 0
        while game.stage.is_betting_stage():
            if game.players[p_iter].is_actor():
                call_amount = game.players[p_iter].check_call_amount
                before = game.players[p_iter].bet
                game.players[p_iter].act()
                after = game.players[p_iter].bet
                if(len(game.board) == 0):
                    if(after-before > call_amount):
                        iterator = PreFlop.actions["i"]
                        action = str(iterator) + "-bet"
                        PreFlop.actions[p_iter] = action
                        PreFlop.actions["i"] += 1
                    elif(game.players[p_iter].starting_stack - game.players[p_iter].stack == before + call_amount):
                        PreFlop.actions[p_iter] = "call"
                    elif(game.players[p_iter].starting_stack - game.players[p_iter].stack != before + call_amount):
                        PreFlop.actions[p_iter] = "fold"
            p_iter = increment_p_count(p_iter, len(game._players))
            if game.stage == None: return game
            # print("piter", p_iter)
            # print(game.actor)
            # print(game.nature.is_nature(), game.nature.is_player())
            # for p in game.players:
            #     print(p)

    return game

def showdown_stage(game):
    # Performs showdown on all players in order to distribute pot
    if game.stage != None:
        p_iter = 0
        if game.stage.is_showdown_stage():
            while game.stage.is_showdown_stage():
                if game.players[p_iter].can_showdown():
                    game.players[p_iter].showdown()
                p_iter = increment_p_count(p_iter, len(game._players))
                if game.stage == None: return game
    return game