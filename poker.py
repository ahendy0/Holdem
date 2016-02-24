from holdem.table import *
from holdem.player import *
from holdem.game import *

import matplotlib.pyplot as plt

bankrolls = []
numplayers = 10
bankroll = 400
seatscount = 10
sb = 2
bb = 4
minbuy = 100

bankhistory = [[] for i in xrange(numplayers)]
numbhands = 100000


#initialize bankrolls
for plid in xrange(numplayers):
    bankrolls.append({'bankroll':bankroll, 'plid':plid})


for handid in xrange(numbhands):
    table = Table('table1', sb, bb, seatscount, minbuy)
    for player in bankrolls:
        #add player bots
        table.add_player(
            Player('p'+str(player['plid']), player['bankroll'], player['plid']),
            bot=True
        )
        #add to bankhistory
        bankhistory[player['plid']].append(player['bankroll'])
        
        
        
    
    if len(table.players) == 1:
        print "WINNER IS: player %s" % table.players[0].plid
        break
    else:
        print "beginning next round"
    game = Game(table)
    bankrolls = game.play_hand()
    
    
    
#plot bankroll vs handid for all players
for i in xrange(numplayers):
    plt.plot(bankhistory[i])
plt.ylabel('Stack size')
plt.xlabel('hands')
plt.show()