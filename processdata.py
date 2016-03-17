        
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

def stack_size(bb, stacksize): 
    buy_in = 
    
        
        
        
        
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

def find_top_players(tablelist, netthresh, handsthresh):
    #[net, amount of hands]
    playerlist = {}
    for table in tablelist:
        for hand in table.hands:
            for player in hand.players:
                if player.name in playerlist:
                    playerlist[player.name][0] += player.net()/table.bb
                    if hand.has_known_hands():
                        playerlist[player.name][1] += 1
                else:
                    playerlist[player.name] = [player.net()/table.bb, 0]
                    
    list =  sorted(playerlist.items(), key=lambda value: value[1][0], reverse=True)
    return filter(lambda x: x[1][0] > netthresh and x[1][1] > handsthresh , list)


def find_top_players_ratio(tablelist, netthresh, handsthresh):
    #[net, amount of hands]
    playerlist = {}
    for table in tablelist:
        for hand in table.hands:
            for player in hand.players:
                if player.name in playerlist:
                    playerlist[player.name][0] += player.net()/table.bb
                    if hand.has_known_hands():
                        playerlist[player.name][1] += 1
                else:
                    playerlist[player.name] = [player.net()/table.bb, 0]
    # net/hands played
    list = sorted(playerlist.items(), key=lambda value: safe_weighted_division(value[1][0], value[1][1]), reverse=True)
    return filter(lambda x: safe_weighted_division(x[1][0], x[1][1]) > netthresh and x[1][1] > handsthresh, list)
    
    
def process(handlist, top_player_names):
    for hand in handlist:
        for action in hand.actions:
            if action.player.name in top_player_names:
                
                
    

def safe_weighted_division(net, hands):
    try:
        return net / hands
    except ZeroDivisionError:
        return 0

def get_good_hands(tablelist, playerlist):
    hands = []
    for table in tablelist:
        for hand in table.hands:
            for player in hand.players:
                if player.name in playerlist:
                    if hand.has_known_hands():
                        hands.append(hand)
    return hands      
    

if __name__ == "__main__":
    filename = './ABSdata/ABSdata_1.pkl'
    print "Opening", filename, "this may take a minute"
    pfile = open(filename, 'rb')
    tablelist = cPickle.load(pfile)
    
    """find the number of hands in tablelist"""
    # print "There is", hands_in_list(tablelist), "hands in this file."
    
    
    print count_known_cards(tablelist)
    top_players = find_top_players(tablelist, 200, 100) # first is profit threshold , number of cards threshold
    # table, minhands to be considered, number of players to return
    top_ratio_players = find_top_players_ratio(tablelist, 0.75,  100) # first is ratio threshold, number of cards threshold
    
    top_names = [i[0] for i in top_players]
    
    # change player list to top_player_names, if we use output from top_players instead
    good_hands = get_good_hands(tablelist, top_names)
    print "number of hands we will use:", len(good_hands)
    
    process(good_hands, top_names)
    
    
    
    
    
    
    