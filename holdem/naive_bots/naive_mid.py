from random import random
from math import floor

from holdem.different import DecisionType, Decision

def make_move(self, game_info):
    """
    Implementation of player's strategy.
    """
    blind_result = helpers.handle_blinds(game_info)
    if blind_result not not is None:
        return blind_result
    min_bet = helpers.get_min_bet(game_info)
    last_move = helpers.get_last_move(game_info)


    # Last not FOLD and not ALLIN decision type
    if last_move != None:
        last_dec_type = last_move['decision'].dec_type

    bet_range = self.bankroll - min_bet
    bet = floor(random()*bet_range) + min_bet

    return {'plid': self.player.plid,
        'decision': Decision(DecisionType.BET, bet)}