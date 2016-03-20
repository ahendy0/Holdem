from deuces import Card, Evaluator
from datastruct import *
import cPickle
import enum
import math
from random import randint
import os
import numpy as np
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

class GameState:
    def __init__(self, stacksize, num_called, num_to_call, bet,hand_eval, potsize,raises, card_info, decision, amount):
        self.stacksize = stacksize  #stacksize relative to others in the hand. on some scale 1-5? 1-10? spread of total money on table?
        self.num_called = num_called #number of players already called the bet to you
        self.num_to_call = num_to_call #number of players to call the bet after you. num_called + num_to_call + 1 should equal the amount of players in hand
        self.bet = bet #this is the bet amount to you. the bet should be relative to your stacksize on some scale
        self.hand_eval = hand_eval #the evaluation of your hand by deuces
        self.card_info = card_info #the state of the cards. prob follow same format as datastruct. Predeal should be ignored  PREDEAL = 0 PREFLOP = 1 FLOP = 2 TURN = 3 RIVER = 4 
        self.potsize = potsize  #the size of the current pot. relative to the table? relative to your stacksize?\
        self.raises = raises
        self.decision = decision # the y value basically, the decision they made based on all of this info
        self.amount = amount # on a bet, this will include how much they bet. as percent of stack. BETWEEN 0 - 1 (not inclusive, 1 would be all in, 0 would be check)
        
        self.debug = None
        
    def __str__(self):
        return "stack size: " + str(self.stacksize) + "\nnum called: " + str(self.num_called) + "\nnum to call: " + str(self.num_to_call) + "\nbet: " + str(self.bet) + "\nhand eval: " + str(self.hand_eval) + "\ncard info: " + str(self.card_info) + "\npotsize: " + str(self.potsize) + "\nDECISION: " + str(self.decision)
     
    
    
def process(handlist, top_player_names):
    #commented out folded, num_to_call, num_called for debuggin
    gamestates = []
    evaluator = Evaluator()
    for hand in handlist:
        for player in hand.players:
            raises = 0
            if player != None:     
                if player.name in top_player_names:
                    infostate = ActionInfo.PREDEAL
                    runningstack = player.origstack
                    num_called = 0
                    folded = 0
                    num_to_call = len(hand.players) - 1
                    bet = 0
                    potsize = 0   
                    commited = 0             
                    for action in hand.actions:
                        potsize += action.amount
                        #STATE
                        if action.info != infostate:
                            commited = 0
                            bet = 0
                            num_called = 0
                            num_to_call
                            num_to_call = len(hand.players) - 1 - folded
                            infostate = action.info 
                        name = ''
                        if action.player != None:
                            name = action.player.name
                        if player.name == name and player.hand != None:
                            #Hero
                            if action.type in [ActionType.FOLD, ActionType.BET, ActionType.CALL, ActionType.CHECK, ActionType.ALLIN]:

                                gs = create_gamestate(runningstack, num_to_call, num_called, potsize, raises, bet, action, player, hand, evaluator)
                                gamestates.append(gs)
                                runningstack -= action.amount
                                potsize += action.amount
                                commited += action.amount
                            elif action.type == ActionType.ANTE:
                                runningstack -= action.amount
                                potsize += action.amount
                            elif action.type == ActionType.POST:
                                runningstack -= action.amount
                                potsize += action.amount
                                commited += action.amount
                                bet = 0
                        else:
                            #Enemy
                           if action.type == ActionType.POST:
                                bet = action.amount - commited
                           if action.type in [ActionType.BET, ActionType.RAISE, ActionType.ALLIN]:
                                raises += 1
                                #Dealing with allins bet is still the same
                                if(action.amount - commited >= 0):
                                    bet = action.amount - commited
                                num_called = 0
                                num_to_call = len(hand.players) - 1 - folded
                           if action.type in [ActionType.CALL, ActionType.CHECK]:
                               num_called += 1
                               num_to_call -= 1
                           if action.type == ActionType.FOLD:
                               folded += 1
                    
                          
        
    return gamestates

def create_gamestate(runningstack, num_to_call, num_called, potsize, raises, bet, action, player, hand, evaluator):
    # get hand eval from deuces
    cards = parse_cards(player.hand)
    board = hand.board
    if board != None:
        board = parse_cards(str(hand.board))
    knowncards = known_cards(board, action.info)
    hand_eval = evaluator.evaluate(knowncards, cards)
    #create gamestate
    n_stacksize = normalize_stackandpot(runningstack, hand.showdown.bb * 100)
    n_potsize = normalize_stackandpot(potsize, hand.showdown.bb * 100)
    n_bet = normalize_bet(bet, runningstack)

    #process the decision
    decision = DecisionType.FOLD
    if action.type in [ActionType.BET, ActionType.RAISE]:
        decision = DecisionType.RAISE
    elif action.type == ActionType.ALLIN:
        decision = DecisionType.ALLIN
    elif action.type == ActionType.CALL:
        decision = DecisionType.CALL
    elif action.type == ActionType.CHECK:
        decision = DecisionType.CHECK
    #instantiate gamestate and add to list
    gs = GameState(n_stacksize, num_called, num_to_call, n_bet, hand_eval, n_potsize, raises, action.info, decision, normalize_bet(action.amount, runningstack))
    return gs
                
def known_cards( board, info):
    if info == ActionInfo.FLOP:
        return board[0:3]
    elif info == ActionInfo.TURN:
        return board [0:4]
    elif info == ActionInfo.RIVER:
        return board
    else:
        return []
                     
        
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
    
   
    

def safe_weighted_division(net, hands):
    try:
        return net / hands
    except ZeroDivisionError:
        return 0

def get_good_hands(tablelist, playerlist):
    hands = []
    for table in tablelist:
        for hand in table.hands:
            added = False
            for player in hand.players:
                if player.name in playerlist:
                    if hand.has_known_hands() and not added:
                        hand.showdown = table
                        added = True
                        hands.append(hand)
    return hands            
    
def parse_cards(cardstr):
    #have to replace 10 with T for deuces
    cardstr = cardstr.replace('10', 'T')
    cardlist = cardstr.split(' ')
    hand = []
    for card in cardlist:
        dcard = Card.new(card)
        hand.append(dcard)
    return hand
    
def normalize_stackandpot(stack, buyin):
    ratio = stack/float(buyin)
    if ratio < 1/5.0:
        return normalize.SMALL
    if ratio < 1/2.0:
        return normalize.SMALLMID
    if ratio < 1:
        return normalize.MID
    if ratio < 3:
        return normalize.MIDLARGE
    else:
        return normalize.LARGE
        
class normalize(Enum):
    SMALL = 1
    SMALLMID = 2
    MID = 3
    MIDLARGE = 4
    LARGE = 5
    
    
# returns percentage of bet to stack size, rounded up to nearest 10
# ex: bet = 20, stack = 500, bet is 4% of stack, return 10
def normalize_bet(bet, stack):
    if stack == 0:
        return 100
    return bet/float(stack)
    
def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

   
class DecisionType(Enum):
    FOLD = 0
    CALL = 1
    CHECK = 2
    RAISE = 3
    ALLIN = 4


def process_gamestates(gamestates):
    x = []
    y = []
    print len(gamestates)
    for gs in gamestates:
        temp = [gs.stacksize.value, gs.num_called, gs.num_to_call, gs.raises, gs.bet, gs.hand_eval, gs.card_info.value, gs.potsize.value]
        x.append(temp)
        y.append(gs.decision.value)
    return x, y

def process_raise_gamestates(gamestates):
    raisegs = []
    for gs in gamestates:
        if gs.decision == DecisionType.RAISE:
            raisegs.append(gs)
    print "Raise Hands", len(raisegs)
    x = []
    y = []
    for gs in raisegs:
        temp = [gs.stacksize.value, gs.num_called, gs.num_to_call, gs.raises, gs.bet, gs.hand_eval, gs.card_info.value, gs.potsize.value]
        x.append(temp)
        y.append(gs.amount)
    return x,y




if __name__ == "__main__":
    #parseFile = True
    parseFile = False
    data_folder = './ABSdata/'
    out_folder = 'gamestatedata/'
    filename = 'gamestate_'
    ext = '.pkl'
       #create dir if not exists
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    if parseFile:
        for x, file in enumerate( os.listdir(data_folder)):
            print "Opening", data_folder + file, "this may take a minute"
            pfile = open(data_folder +  file, 'rb')
            tablelist = cPickle.load(pfile)
            pfile.close()

            """find the number of hands in tablelist"""
            # print "There is", hands_in_list(tablelist), "hands in this file."


            print count_known_cards(tablelist)
            top_players = find_top_players(tablelist, 200, 100) # first is profit threshold , number of cards threshold
            # table, minhands to be considered, number of players to return
            #top_ratio_players = find_top_players_ratio(tablelist, 0.75,  300) # first is ratio threshold, number of cards threshold

            top_names = [i[0] for i in top_players]



            # change player list to top_player_names, if we use output from top_players instead
            good_hands = get_good_hands(tablelist, top_names)
            print "number of hands we will use:", len(good_hands)

            #clear tablelist
            tablelist = None


            gamestates = process(good_hands, top_names)

            top_names = None
            good_hands = None


            output = open('./' + out_folder + filename + str(x) + ext, 'wb')
            cPickle.dump(gamestates, output)

            #clear gamestates
            gamestates = None
            output.close()


    clf = BernoulliNB()
    xtest = None
    ytest = None

    classa = [0, 1, 2, 3, 4]
    gamestates = []
    for x, file in enumerate( os.listdir(out_folder)):
        print "Opening",out_folder + file, "this may take a minute"
        pfile = open(out_folder + file, 'rb')
        gamestates += cPickle.load(pfile)
        if len(gamestates) > 0:
            pfile.close()





    x, y, = process_gamestates(gamestates)
    num = len(x) - 10000
    xtest, ytest, =  x[num:], y[num:]
    x, y = x[:num], y[:num]

    clf = clf.fit(x, y)

    clf2_RFC = RandomForestClassifier(max_depth=len(xtest[0]), n_estimators=len(xtest[0]), max_features=len(xtest[0]))
    clf2_RFC = clf2_RFC.fit(x, y)


    #RAISE REGRESSION
    xr, yr = process_raise_gamestates(gamestates)
    num = len(xr) - 1000
    xrt, yrt = xr[num:], yr[num:]
    xr, yr = xr[:num], yr[:num]

    poly = PolynomialFeatures(degree=4)
    xr = poly.fit_transform(xr)
    xrt = poly.fit_transform(xrt)




    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(xr, yr)
    # The mean square error
    print("Residual sum of squares: %.2f"
          % np.mean((regr.predict(xrt) - yrt) ** 2))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % regr.score(xrt, yrt))


    #count regression error
    err2 = 0
    err5 = 0
    for i in xrange(len(xrt)):
        if abs(regr.predict([xrt[i]])[0] -  yrt[i]) > 0.02:
            err2 += 1
        if abs(regr.predict([xrt[i]])[0] -  yrt[i]) > 0.05:
            err5 += 1

    print "Reg Error2", err2 , "out of", len(xrt), err2/float(len(xrt))
    print "Reg Error5", err5 , "out of", len(xrt), err5/float(len(xrt))




    if not os.path.exists('./fits/'):
        os.makedirs('./fits/')
    pfile = open('./fits/clfNB.pkl', 'wb')
    cPickle.dump(clf, pfile)
    pfile = open('./fits/clfRFC.pkl', 'wb')
    cPickle.dump(clf2_RFC, pfile)




    print "Total Hands", sum
    print "------predictions-------\n0=fold, 1=call, 2=check, 3=raise, 4=allin"
    print "NB", clf.score(xtest,ytest)
    print "RF", clf2_RFC.score(xtest,ytest)





    """
    #More tests
    test_data = [
        [normalize.MIDLARGE.value, 0, 0, 0, 4000, ActionInfo.FLOP.value, normalize.MIDLARGE.value],
        [normalize.MIDLARGE.value, 0, 0, 15, 4000, ActionInfo.FLOP.value, normalize.MIDLARGE.value],
    ]

    for test in test_data:
        i = clf2_RFC.predict([test])
        print DecisionType(i)
    """




    """
    fold = 0
    for x in xrange(len(xtest)):
        decision = clf.predict([xtest[x]])[0]
        if decision == DecisionType.FOLD.value:
            fold+= 1
    print "Num folds", fold
    """





    """
    checkerr = 0
    for x in xrange(len(xtest)):
        decision = clf.predict([xtest[x]])[0]
        if decision == DecisionType.CHECK.value:
            if xtest[x][3] != 0.0:
                checkerr += 1
    print checkerr
    """




    """
    allinerr = 0
    for x in xrange(len(xtest)):
        decision = clf.predict([xtest[x]])[0]
        if decision == DecisionType.ALLIN and ytest:
    """






    