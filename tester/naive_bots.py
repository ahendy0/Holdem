from random import randint,choice

from bot import Bot


funclist = []


class FoldBot(Bot):
    def turn(self):
        return self.action('fold')
    funclist.append(turn)


class RandomBet(Bot):
    def turn(self):

        min_raise = self.big_blind_amount
        too_poor = False
        max_raise = self.get_credits_count()-self.bet_to_player

        if max_raise < min_raise:
            return choice([self.action('fold'), self.action('call')])

        bet_amount = randint(min_raise, max_raise)

        return self.action('raise', amount=bet_amount)

    funclist.append(turn)


class MinBet(Bot):
    def turn(self):
        return self.action('call')
    funclist.append(turn)


class AllIn(Bot):
    def turn(self):
        max_raise = self.get_credits_count()-self.bet_to_player
        return self.action('raise', amount=max_raise)
    funclist.append(turn)


class RandomBot(Bot):
    def turn(self):
        return choice(funclist)(self)
