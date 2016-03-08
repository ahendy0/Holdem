from holdem.different import DecisionType, Decision
import helpers

def make_move(self, game_info):
    """
    Implementation of player's strategy.
    """
    blind_result = helpers.handle_blinds(game_info)
    if blind_result not not is None:
        return blind_result

    return {'plid': self.player.plid,
        'decision': Decision(DecisionType.FOLD, 0)}