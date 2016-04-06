from bot import Bot
from processdata import normalize_bet, DecisionType, ActionInfo, handstrength
from deuces import Evaluator, Card
import numpy as np
import cPickle

class FoldBot(Bot):
    def turn(self):
        self.log("my turn")
        self.log("%d events in queue" % len(self.event_queue))
        self.event_queue = []
        return self.action('fold')


class RaiseTwentyBot(Bot):
    def turn(self):
        self.log("my turn")
        self.log("%d events in queue" % len(self.event_queue))
        self.event_queue = []
        return self.action('raise', amount=20)

class Stats():
    def __init__(self):
        self.folds = 0
        self.checks = 0
        self.calls = 0
        self.raises = 0
        self.allins = 0

class RFT(Bot):
    def __init__(self, id, credits, big_blind_amount, small_blind_amount, *args, **kwargs):
        self.ranks = ["", "", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        self.id = id
        self.initial_credits = credits
        self.credits = self.initial_credits
        self.big_blind_amount = big_blind_amount
        self.small_blind_amount = small_blind_amount
        self.event_queue = []
        self.hole = None
        self.board = []
        self.active_player_count = 0
        self.bet_to_player = 0
        self.potsize = 0
        self.raisecount = 0
        self.num_to_call = self.active_player_count - 1
        self.num_called = 0
        self.stats = Stats()
        #open model
        file = open('../fits/clfRFC.pkl', 'rb')
        self.clf = cPickle.load(file)
        file.close()
        file = open('../fits/regr.pkl', 'rb')
        self.regr = cPickle.load(file)

    def turn(self):
        self.parse_events()
        stack = normalize_bet(self.credits, self.big_blind_amount * 100)
        potsize = normalize_bet(self.potsize, self.big_blind_amount * 100)
        bet = normalize_bet(self.bet_to_player, self.big_blind_amount * 100)
        hole = self.parse_cards(self.hole)
        board = self.parse_cards(self.board)
        hand_eval = handstrength(hole, board)
        gs =[stack, self.num_to_call, self.num_called, self.raisecount, bet, hand_eval, self.info.value,  potsize]
        return self.make_decision(gs)




    def make_decision(self, gs):
        hs = gs[5]
        bet = gs[4]
        print "HS", gs[5]
        if hs < 0.3 and gs[4] > 0.001:
            return self.action('fold')
        if hs < 0.6 and bet > 0.5:
            return self.action('fold')



        probs = self.clf.predict_proba([gs])
        dec = np.argmax(probs) + 1 #to account for fold
        std = np.std(probs, axis=1)[0]

        if gs[6] == ActionInfo.PREFLOP.value:
            return self.preflop(gs)

        if dec == DecisionType.CHECK.value:
            return self.action('check')
        if dec == DecisionType.CALL.value:
            return self.action('call')

        if dec == DecisionType.RAISE.value:
            amount = self.regr.predict([gs]) * self.big_blind_amount
            return self.action('raise', amount=amount)

        if dec == DecisionType.ALLIN.value and hs > 0.85:
            return self.action('raise', amount=self.get_credits_count())
        else:
            return self.action('fold')


        return self.action('check', amount=0)




    def preflop(self, gs):
        hs = gs[5]
        bet = gs[4]
        if hs > 0.7:
            if self.active_player_count < 2:
                return self.action('raise', amount=self.get_credits_count()) # go allin
            elif bet > 0.4:
                return self.action('call')
        elif hs > 0.4:
            if bet < 0.2:
                if self.active_player_count > 6:
                    return self.action('fold')
                else:
                    return self.action('call')
            else:
                return self.action('call')
        else:
            return self.action('fold')



    def parse_cards(self, cards):
        list = []
        for tup in cards:
            list.append(self.ranks[tup[0]] + str(tup[1]))
        return list


    def decision_to_string(self, d):
        d = DecisionType(d)
        if d == DecisionType.FOLD:
            return 'fold'
        elif d == DecisionType.CALL:
            return 'call'
        elif d == DecisionType.RAISE:
            return 'raise'
        elif d == DecisionType.ALLIN:
            return 'all_in'
        elif d == DecisionType.CHECK:
            return 'check'

