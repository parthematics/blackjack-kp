import random
from collections import deque

''' The following three classes define the abstractions that will be used to play a game of Blackjack.
    They will be called in our main Blackjack class, and their methods will simulate a game being played. '''

class Card:
    ''' Initializing a playing card. Every card is defined by a specific value and suit. '''
    def __init__(self, value, suit):
        self.val = value
        self.suit = suit

    ''' Magic method to print out a playing card. Called with 'print(...)'. '''
    def __repr__(self):
        return "{0} - {1}".format(self.val, self.suit)

class Deck:
    ''' Initializing a deck of cards. Note that the list comprehension will create a total of
        52 (4 * 13) cards with two for loops. I chose to use a double ended queue (deque) to
        represent our deck of cards because it is optimized for card removal from the front,
        which is analogous to dealing the cards. Also, 'deque' kind of sounds like 'deck' :) '''
    def __init__(self):
        self.vals = ['A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Q', 'K']
        self.suits = ['Clubs (♣)', 'Hearts (♥)', 'Spades (♠)', 'Diamonds (♦)']
        self.deck = deque([Card(val, suit) for val in self.vals for suit in self.suits])
        self.size = 52

    ''' Using our deque's popleft() feature to deal the top most card from our deck of cards. '''
    def deal_card(self):
        if self.size > 1:
            card = self.cards.popleft()
            self.size -= 1
        return card

    ''' Using random module's built-in shuffle method to shuffle our deck of cards. '''
    def shuffle_deck(self):
        if self.size > 1:
            random.shuffle(self.deck)

class Hand:
    ''' Initializing a hand of cards. Slight differences exist if hand is for player or for dealer. '''
    def __init__(self, player=True):
        self.is_dealer = not player
        self.hand = []
        self.hand_value = 0
