
def handle_blinds(game_info):
    mrounds = game_info['moves']
    # Making a list of moves in current round
    moves = mrounds[-1]
    if len(mrounds) == 1 and len(moves) == 0:
        #### print"Player's move: small blind - %r" %game_info['sbl']
        return {'plid': self.player.plid,
                'decision': Decision(DecisionType.BET, game_info['sbl'])}
    if len(mrounds) == 1 and len(moves) == 1:
        #### print"Player's move: big blind - %r" %game_info['bbl']
        return {'plid': self.player.plid,
                'decision': Decision(DecisionType.RAISE, game_info['bbl'])}

def get_min_bet(game_info):
    mrounds = game_info['moves']
    # Calculate current maximum pot share, that will be minumum bet
    shares = {}
    for mround in mrounds:
        for move in mround:
            if move['plid'] not in shares.keys():
                shares[move['plid']] = move['decision'].value
            else:
                shares[move['plid']] += move['decision'].value

    lshares = shares.items()
    lshares.sort(key = lambda el: el[1])
    # Minimum bet is a maximum current share minus player's share
    min_bet = 0
    if lshares != []:
        if self.plid in shares.keys():
            min_bet = lshares[-1][1] - shares[self.plid]
        else:
            min_bet = lshares[-1][1]
    return min_bet

def get_last_move(game_info):
    mrounds = game_info['moves']
    moves = mrounds[-1]
    last_move = None
    for move in reversed(moves):
        if move['decision'].dec_type == DecisionType.FOLD:
            continue
        if move['decision'].dec_type == DecisionType.ALLINLOWER:
            continue
        last_move = move
        break
    return last_move
