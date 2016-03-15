        
from datastruct import *
import cPickle
import enum



class GameState:
     def __init__(self,stacksize, num_called, num_to_call, bet,hand_eval, potsize ):
        self.stacksize = stacksize  #stacksize relative to others in the hand. on some scale 1-5? 1-10? spread of total money on table?
        self.num_called = num_called #number of players already called the bet to you
        self.num_to_call = num_to_call #number of players to call the bet after you. num_called + num_to_call + 1 should equal the amount of players in hand
        self.bet = bet #this is the bet amount to you. the bet should be relative to your stacksize on some scale
        self.hand_eval = hand_eval #the evaluation of your hand by deuces
        self.card_info = card_info #the state of the cards. prob follow same format as datastruct. Predeal should be ignored  PREDEAL = 0 PREFLOP = 1 FLOP = 2 TURN = 3 RIVER = 4 
        self.potsize = potsize  #the size of the current pot. relative to the table? relative to your stacksize?


def hands_in_list(tablelist):
    numhands = 0
    for table in tablelist:
        numhands += table.numhands()
    return numhands

    
def count_known_cards(tablelist):
    i = 0
    for table in tablelist:
        for hand in table.hands:
            for winner in hand.winners:
                if winner.hand != None:
                    i+= 1
                    
    return i

    
def find_top_players(tablelist):
    #[net, amount of hands]
    playerlist = {}
    for table in tablelist:
        for hand in table.hands:
            for player in hand.players:
                if player.name in playerlist:
                    playerlist[player.name][0] += player.net()
                    playerlist[player.name][1] += 1
                else:
                    playerlist[player.name] = [player.net(), 0]
                    
    return  sorted(playerlist.items(), key=lambda value: value[1][0], reverse=True)[0:10]
            


if __name__ == "__main__":

    filename = './ABSdata/ABSdata_1.pkl'
    print "Opening", filename, "this may take a minute"
    pfile = open(filename, 'rb')
    tablelist = cPickle.load(pfile)
    
    """find the number of hands in tablelist"""
    print "There is", hands_in_list(tablelist), "hands in this file."
    
    
    print count_known_cards(tablelist)
    print find_top_players(tablelist)
    
