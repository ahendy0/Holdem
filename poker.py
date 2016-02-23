from holdem.table import *
from holdem.player import *
from holdem.game import *


bankrolls = [{'plid': 1, 'bankroll': 300}, {'plid': 2, 'bankroll': 300}, {'plid': 3, 'bankroll': 300}]
while 1:
    table = Table('tT', 1, 2, 4, 1)
    for player in bankrolls:
        table.add_player(
            Player('p'+str(player['plid']), player['bankroll'], player['plid']),
            player['plid']-1
        )

    if len(table.players) == 1:
        print "WINNER IS: player %s" % table.players[0].plid
        break
    else:
        print "beginning next round"
    # player1 = Player('p1', 300, 1)
    # player2 = Player('p2', 300, 2)
    # player3 = Player('p3', 300, 3)
    # table.add_player(player1, 1)
    # table.add_player(player2, 0)
    # table.add_player(player3, 0)
    game = Game(table)
    bankrolls = game.play_game()
