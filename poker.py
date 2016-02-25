from holdem.table import *
from holdem.player import *
from holdem.game import *
import datetime

import matplotlib.pyplot as plt

start_time = datetime.datetime.now()
print "start time: ", start_time.time()

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

    if (handid % 1000) == 0:
        temp = datetime.datetime.now()
        print "current elapsed time: ", temp - start_time, " at hand ", handid
        # print "current elapsed time: ", temp - start_time, " at hand ", handid
        
        
    
    if len(table.players) == 1:
        #### print"WINNER IS: player %s" % table.players[0].plid
        break
    else:
        pass
        #### print"beginning next round"
    game = Game(table)
    bankroll2 = game.play_hand()
    #add to bankhistory
    # players werent actually updated (they are just used to create different types of players [cli or bot])
    # so had to grab a copy of bankrolls returned, and use that
    for player in bankroll2:
        bankhistory[player['plid']].append(player['bankroll'])
    
    
end_time = datetime.datetime.now()
print "time taken: ", end_time - start_time
#plot bankroll vs handid for all players
for i in xrange(numplayers):
    plt.plot(bankhistory[i])
plt.ylabel('Stack size')
plt.xlabel('hands')
plt.show()