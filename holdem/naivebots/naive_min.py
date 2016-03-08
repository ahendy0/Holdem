from holdem.different import DecisionType, Decision
import helpers

def make_move(self, game_info):
    """
    Implementation of player's strategy.
    """
    print "hi"
    blind_result = helpers.handle_blinds(game_info)
    if blind_result is not None:
        return blind_result
    min_bet = helpers.get_min_bet(game_info)
    last_move = helpers.get_last_move(game_info)

    # Last not FOLD and not ALLIN decision type
    if last_move != None:
        last_dec_type = last_move['decision'].dec_type


    if last_dec_type == DecisionType.CHECK:
        return {'plid': self.player.plid,
                'decision': Decision(DecisionType.CHECK, min_bet)}
    else:
        return {'plid': self.player.plid,
                'decision': Decision(DecisionType.CALL, min_bet)}