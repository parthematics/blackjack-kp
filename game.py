import random

class Card:
    ''' Initializing a card. Every card is defined by a specific value and suit. '''
    def __init__(self, value, suit):
        self.val = value
        self.suit = suit

    def __repr__(self):
        return "{0} - {1}".format(self.val, self.suit)
