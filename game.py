import random
from collections import deque

''' The following three classes define the abstractions that will be used to play a game of Blackjack.
    They will be called in our main Blackjack class, and their methods will simulate a game being played. '''

class Card:
    ''' Initializing a playing card. Every card is defined by a specific value and suit. '''
    def __init__(self, value, suit):
        self.val = value
        self.suit = suit

    ''' Magic method to printclass out a playing card. Called with 'print(...)'. '''
    def __repr__(self):
        return "{0} - {1}".format(self.val, self.suit)

class Deck:
    ''' Initializing a deck of cards. Note that the list comprehension will create a total of
        52 (4 * 13) cards with two for loops. I chose to use a double ended queue (deque) to
        represent our deck of cards because it is optimized for card removal from the front,
        which is analogous to dealing the cards. Also, 'deque' kind of sounds like 'deck' :) '''
    def __init__(self):
        self.vals = ['A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
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
        self.player = player
        self.hand = []
        self.hand_value = 0

    ''' Private helper method used while calculating total value of hand. '''
    def _reset_hand(self):
        self.hand_value = 0

    ''' Private helper method to find the total value of a hand so far. '''
    def _value_of_hand(self, seen_ace=False):
        self._reset_hand()
        for card in self.hand:
            if card.val not in {'A', 'J', 'Q', 'K'}:
                self.hand_value += int(card.val)
            else:
                if card.val != 'A':
                    self.hand_value += 10
                else:
                    # We start by treating all aces as 11s.
                    seen_ace = True
                    self.hand_value += 11

        # Accounting for the case where we want 'A' to be treated as a 1.
        if self.hand_value > 21 and seen_ace:
            while self.hand_value > 21:
                self.hand_value -= 10

    ''' Method that adds a new card to our hand of cards. '''
    def add_to_hand(self, card):
        self.hand.append(card)

    ''' Method that returns the total value of current hand. '''
    def get_hand_value(self):
        self.value_of_hand()
        return self.hand_value

    ''' Printing out the current hand of individual (dealer/player). '''
    def show_hand(self):
        if self.player:
            for card in self.hand:
                print(card)
            print("HAND VALUE: ", self.get_hand_value())
        else:
            print("HOLE CARD (HIDDEN)")
            print(self.hand[1])

class Blackjack:
    def __init__(self):
        self.playing = True
        self.game_ended = False
        self.current_deck = None
        self.my_hand = None
        self.dealer_hand = None
        self.possible_actions = {'h': 1, 'hit': 1, 's': 0, 'stand': 0}
        self.play_again_options = {'y': True, 'yes': True, 'n': False, 'no': False}

    def has_blackjack(self, hand):
        return hand.get_hand_value() == 21

    def hit(self, hand):
        hand.add_to_hand(self.current_deck.deal_card())
        return

    def bust(self):
        return self.my_hand.get_hand_value() > 21

    def blackjack_reached(self, player, dealer):
        if player and not dealer:
            print("CONGRATULATIONS. YOU HAVE BLACKJACK!")
        if dealer and not player:
            print("DEALER HAS BLACKJACK. SORRY!")
        if player and dealer:
            print("YOU BOTH HAVE BLACKJACK. WELL DONE!")

    def check_for_win(self, player_value, dealer_value):
        if player_value > dealer_value:
            print("YOU WIN! WELL DONE.")
        elif dealer_value < player_value:
            print("THE DEALER WINS. BETTER LUCK NEXT TIME!")
        else:
            print("GAME IS A TIE! NICE.")

        self.game_ended = True


    def start_game(self):
        # Main game loop. Will loop again if player wants to play again.
        while self.playing:
            self.current_deck = Deck()
            self.current_deck.shuffle_deck()

            self.my_hand, self.dealer_hand = Hand(), Hand(player=False)

            for _ in range(2):
                self.hit(self.my_hand)
                self.hit(self.dealer_hand)

            print("YOUR HAND: ")
            self.my_hand.show_hand()
            print("=================================")
            print("DEALER'S HAND: ")
            self.dealer_hand.show_hand()

            # Secondary game loop. This will loop so long as the current game is not over.
            while not self.game_ended:
                blackjack_me = self.has_blackjack(self.my_hand)
                blackjack_dealer = self.has_blackjack(self.dealer_hand)

                if blackjack_dealer or blackjack_me:
                    self.game_ended = True
                    self.blackjack_reached(blackjack_me, blackjack_dealer)
                    break

                user_input = input("DO YOU WANT TO HIT OR STAND? (H/S)").lower()
                while user_input not in self.possible_actions.keys():
                    user_input = input("INVALID INPUT. PLEASE ENTER 'H' OR 'S'.")

                # If the user wants to hit:
                if self.possible_actions[user_input]:
                    self.hit(self.my_hand)
                    self.my_hand.show_hand()
                    if self.bust():
                        print("YOU BUSTED!")
                        self.game_ended = True

                # If user wants to stand:
                else:
                    my_result = self.my_hand.get_hand_value()
                    dealer_result = self.dealer_hand.get_hand_value()

                    print("GAME RESULTS:")
                    print("=================================")
                    print("YOUR HAND VALUE: {0}".format(my_result))
                    print("DEALER HAND VALUE: {0}".format(dealer_result))
                    print("=================================")

                    self.check_for_win(my_result, dealer_result)

            play_again = input("DO YOU WANT TO PLAY AGAIN? (Y/N)").lower()
            while play_again not in self.play_again_options:
                play_again = input("INVALID INPUT. PLEASE ENTER 'Y' OR 'N'.")

            # If user wishes to play another game, self.game_ended is reset to False so the loop continues.
            if self.play_again_options[play_again]:
                self.game_ended = False
            else:
                self.playing = False
