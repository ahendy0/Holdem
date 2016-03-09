from datastruct import *
import cPickle

def hands_in_list(tablelist):
    numhands = 0
    for table in tablelist:
        numhands += table.numhands()
    return numhands

if __name__ == "__main__":
    """An example of how to access the data and work with it
    because the data is large it is partitioned into multiple files containing a little bit over 100000 hands each
    ABSdata_1 is a pickle file that contains a list of table objects which contain the list of hands"""
    
    """ Go to https://www.dropbox.com/s/vy9id8z8buva019/ABSdata.zip?dl=0 to download zip file of part of the data. Actual data so far is 12 files about 1.2 million hands and about 2.4 Gigabytes"""
    
    
    
    filename = './ABSdata/ABSdata_1.pkl'
    print "Opening", filename, "this may take a minute"
    pfile = open(filename, 'rb')
    tablelist = cPickle.load(pfile)
    
    """find the number of hands in tablelist"""
    print "There is", hands_in_list(tablelist), "hands in this file."
    print ""
    
    
    
    #print first 4 tables name/type
    print "Some tablenames:"
    for table in tablelist[0:4]:
        print table
    print ""
    
    
    """the table type can be used to filter tables
    you can filter it like this"""
    print "filtered tables"
    newlist = []
    for table in tablelist[0:10]:
        if "(1 on 1)" and "(Real Money)" in table.type:
            newlist.append(table)
            print table
   
    print ""
    
    """accessing a hand"""
    table = tablelist[0]
    hand = table.hands[21]
    
    """hand information"""
    
    print "hand id:" , hand.id
    print ""
    
    
    """Accessing the list of players"""
   
    playerlist = hand.players #first in list is dealer 2nd sb 3rd bb
    
    #print them
    for player in playerlist:
        print player
    print ""
    
    """some hands may have None for board as they did not go past preflop
    currently a string"""
    
    print hand.board    #first 3 cards flop,1 turn, 1 river
    print ""
    
    """Accessing which players won the hand"""
    
    winner_playerlist = hand.winners
    
    print "Winner/s of the hand is/are:"
    for player in winner_playerlist: 
        print player
    print ""
     
    """see if this hand went to showdown"""
    
    print "Did this hand go to showdown?", hand.showdown
    print ""
    
    print "Total pot:",  hand.totalpot
    print ""
    
    """you can also see all the actions done by players"""
    
    actionlist = hand.actions
    
    #print actions
    for action in actionlist:
        print action
    print ""
    
    
    
    """Player"""
    
    """you can also access individual players 
    to find out their net and cards"""
    
    player = hand.players[0]
    
    name = player.name
    
    """find the net in the hand"""
    net = player.net()
    print name, " net is:", net
    print ""
    
    """his hand (cards) as a string """
    cards = player.hand 
    print name, "hand was", cards
    
    #get winners hand instead
    print "Winners hand was", winner_playerlist[0].hand
    
    print ""
    
    """currently you cannot access the actions of a player from the player object but this is something I want to add. Probably inferred when processing the data""" 

    
    """currently does nothing"""
    player.seat 
    
    """ACTIONS"""
    
    """actions have player, info, type and amount"""
    
    action = actionlist[6]
    
    """info is how much information the player has from the cards. 
    enumerated as follows
    class ActionInfo(Enum):
        PREDEAL = 0
        PREFLOP = 1
        FLOP = 2
        TURN = 3
        RIVER = 4 """
        
    print "Action info", action.info 
    
    """action type is the type of actions enumerated like this
    class ActionType(Enum):
        FOLD = 0
        BET = 1
        CALL = 2
        RAISE = 3
        CHECK = 4
        ALLIN = 5
        ANTE = 6
        POST = 7
        TIMEOUT = 8
     we will probably be filtering by FOLD CALL RAISE (BET is type of raise?) CHECK ALLIN in our actual learning"""
        
    print "Action type", action.type
    
    
    """ player gives the player object of who made the action"""
    player = action.player
    print player
    
    """long/double type the amount is the amount of money for that action currently in dollars. After processing I think it should be normalized to bb's"""
    
    print action.amount
    
    print ""
    
    #you can also print the action just by using print
    print action
    
    
    
    
    
    
    