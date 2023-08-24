from functions import *

deck32 = make_deck()
deck52 = make_deck(True)
deck = deck32.copy()
# deck_to_file('deck.txt', deck)
# deck = deck_from_file('deck.txt')
# auto_play(deck, True)
stack = manual_game(deck)
