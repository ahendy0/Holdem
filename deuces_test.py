from deuces import Card, Evaluator, Deck


# create a board and hole cards
board = []

hand = [
    Card.new('2s'),
    Card.new('5c')
]
hand2 = [
    Card.new('2s'),
    Card.new('7c')
]



# create an evaluator
evaluator = Evaluator()

# and rank your hand
rank = evaluator.evaluate(board, hand)
rank2 = evaluator.evaluate(board, hand2)

print rank, rank2