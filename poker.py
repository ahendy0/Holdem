from holdem.table import *
from holdem.player import *
from holdem.game import *
import datetime
import numpy as np

import matplotlib.pyplot as plt

start_time = datetime.datetime.now()



bankrolls = []
numplayers = 7
bankroll = 400
sb = 2
bb = 4
minbuy = 1

bankhistory = [[] for i in xrange(numplayers)]
numbhands = 1000

#initialize bankrolls
for plid in xrange(numplayers):
    bankrolls.append({'bankroll':bankroll, 'plid':plid})


for handid in xrange(numbhands):
    table = Table('table1', sb, bb, numplayers, minbuy)
    for player in bankrolls:
        #add player bots
        table.add_player(
            Player('p'+str(player['plid']), player['bankroll'], player['plid']),
            bot=True
        )

    #time counter
    if (handid % 1000) == 0:
        temp = datetime.datetime.now()
        print "current elapsed time: ", temp - start_time, " at hand ", handid
        # print "current elapsed time: ", temp - start_time, " at hand ", handid

    
    game = Game(table)
    br = game.play_hand()
    
    #interpert data
    for player in br:
        #normalize to multiples of bb
        bankhistory[player['plid']].append((player['bankroll'] - bankroll)/bb)
    
    
end_time = datetime.datetime.now()
print "time taken: ", end_time - start_time



#plot bankroll vs handid for all players

for i in xrange(numplayers):
    #cumalative sum
    plt.plot(np.cumsum(bankhistory[i]))

  
plt.ylabel('Stack size')
plt.xlabel('hands')
plt.show()