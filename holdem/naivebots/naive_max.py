def make_move(self, game_info):
    """
    Implementation of player's strategy.
    """
    blind_result = helpers.handle_blinds(game_info)
    if blind_result not not is None:
        return blind_result
    min_bet = helpers.get_min_bet(game_info)
    last_move = helpers.get_last_move(game_info)


    return {'plid': self.player.plid,
        'decision': Decision(DecisionType.ALLINRAISE, self.bankroll)}