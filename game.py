#!/usr/bin/python
# -*- coding: utf-8 -*-
''' Note that the above encoding (utf-8) must be specified in order for the special characters to be printed correctly. '''

import random
from collections import deque

''' The following three classes define the abstractions that will be used to play a game of Blackjack.
    They will be called in our main Blackjack class, and their methods will simulate a game being played. '''

class Card:
    ''' Initializing a playing card. Every card is defined by a specific value and suit. '''
    def __init__(self, value, suit):
        self.val = value
        self.suit = suit

class Deck:
    ''' Initializing a deck of cards. Note that the list comprehension will create a total of
        52 (4 * 13) cards with two for loops. I chose to use a double ended queue (deque) to
        represent our deck of cards because it is optimized for card removal from the front,
        which is analogous to dealing the cards. Also, 'deque' kind of sounds like 'deck' :) '''
    def __init__(self):
        self.vals = ['A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.suits = ['♣', '♥', '♠', '♦']
        self.deck = deque([Card(val, suit) for val in self.vals for suit in self.suits])
        self.size = 52

    ''' Using our deque's popleft() feature to deal the top most card from our deck of cards. '''
    def deal_card(self):
        if self.size > 1:
            card = self.deck.popleft()
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
        self._value_of_hand()
        return self.hand_value

    ''' Printing out the current hand of individual (dealer/player). Note that the 'offset' variable is used to
        account for the misalignment in card positions resulting from the different numbers of characters used
        to represent each card value. For example, '10' uses 2 characters while the rest use just 1. '''
    def show_hand(self, offset=' '):
        if self.player:
            print_card = [[] for _ in range(7)]

            for index, card in enumerate(self.hand):
                if card.val == '10':
                    offset = ''  # If we write "10" on the card, the edge will be misaligned.

                # Add each card in the current hand line by line to make it all fit horizontally.
                # The {} are being used to fill in the cards with their specific values, suits, and offsets.
                print_card[0].append('┌─────────┐')
                print_card[1].append('│{}{}       │'.format(card.val, offset))
                print_card[2].append('│         │')
                print_card[3].append('│    {}    │'.format(card.suit))
                print_card[4].append('│         │')
                print_card[5].append('│       {}{}│'.format(offset, card.val))
                print_card[6].append('└─────────┘')

            # Turning print_card into a contiguous string with line breaks to make the cards human readable.
            my_hand = '\n'.join([''.join(line) for line in print_card])

            print(my_hand)
            print("TOTAL VALUE: {0}".format(self.get_hand_value()))

        # If the current hand is a dealers, we want to hide the first card and show the rest (standard Blackjack rules).
        # The rest of the logic is the same as above.
        else:
            # Creating a HIDDEN card.
            print_card = [['│░░░░░░░░░│'] for _ in range(7)]
            print_card[0], print_card[6] = ['┌─────────┐'], ['└─────────┘']

            for index, card in enumerate(self.hand[1:]):
                if card.val == '10':
                    offset = ''

                print_card[0].append('┌─────────┐')
                print_card[1].append('│{}{}       │'.format(card.val, offset))
                print_card[2].append('│         │')
                print_card[3].append('│    {}    │'.format(card.suit))
                print_card[4].append('│         │')
                print_card[5].append('│       {}{}│'.format(offset, card.val))
                print_card[6].append('└─────────┘')

            dealer_hand = '\n'.join([''.join(line) for line in print_card])
            print(dealer_hand)

''' Main class called when playing a game of Blackjack. This class is at the top of our abstraction and will call
    all of the classes defined above (for creating a deck of cards, dealing out two hands, etc.) Note that we
    instantiate the class with several variables, most of which are placeholder values. These placeholders will be
    redefined in the start_game() method. self.playing and self.game_ended are two booleans used to continue our
    inner game loops - self.playing will loop until the user specifies that they no longer want to play, and self.game_ended
    will indicate whether the current game being played has terminated. '''
class Blackjack:
    def __init__(self):
        self.playing = True
        self.game_ended = False
        self.current_deck = None
        self.my_hand = None
        self.dealer_hand = None
        self.possible_actions = {'h': 1, 'hit': 1, 's': 0, 'stand': 0}
        self.play_again_options = {'y': True, 'yes': True, 'n': False, 'no': False}

    ''' Helper method that takes a hand and returns a boolean corresponding to whether it has Blackjack. '''
    def has_blackjack(self, hand):
        return hand.get_hand_value() == 21

    ''' Helper method that simulates a 'hit' in Blackjack. It adds a random card to a hand. '''
    def hit(self, hand):
        hand.add_to_hand(self.current_deck.deal_card())
        return

    ''' Helper method that returns whether the current player's hand value has gone over 21. '''
    def bust(self):
        return self.my_hand.get_hand_value() > 21

    ''' Helper method that takes in two booleans (corresponding to whether any player got Blackjack). Only called when
        either the dealer or the player has Blackjack. Returns the corresponding phrase. '''
    def blackjack_reached(self, player, dealer):
        if player and not dealer:
            print("\nCONGRATULATIONS. YOU HAVE BLACKJACK!")
        if dealer and not player:
            print("\nDEALER HAS BLACKJACK. SORRY!")
        if player and dealer:
            print("\nYOU BOTH HAVE BLACKJACK. WELL DONE!")

    ''' Helper method that is called when a player decides to stand and the game is judged based on who has more points. '''
    def check_for_win(self, player_value, dealer_value):
        if player_value > dealer_value:
            print("YOU WIN! WELL DONE.")
        elif dealer_value > player_value:
            print("THE DEALER WINS. BETTER LUCK NEXT TIME!")
        else:
            print("GAME IS A TIE! NICE.")
        # Reset self.game_ended because the current game is now done.
        self.game_ended = True

    ''' Main game method that is called to simulate a full game of Blackjack. There is unfortunately, no functionality for betting. '''
    def start_game(self):
        # Main game loop. Will loop again if player wants to play again.
        while self.playing:
            self.current_deck = Deck()
            self.current_deck.shuffle_deck()

            self.my_hand, self.dealer_hand = Hand(), Hand(player=False)

            # Initial hits for player and dealer.
            for _ in range(2):
                self.hit(self.my_hand)
                self.hit(self.dealer_hand)

            # Printing out both hands to our terminal display.
            print("\nYOUR HAND: ")
            self.my_hand.show_hand()
            print("==================================")
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

                user_input = input("\nDO YOU WANT TO HIT OR STAND? (H/S) \n").lower()
                while user_input not in self.possible_actions.keys():
                    user_input = input("INVALID INPUT. PLEASE ENTER 'H' OR 'S'.")

                # If the user wants to hit:
                if self.possible_actions[user_input]:
                    self.hit(self.my_hand)
                    print("\nYOUR HAND: ")
                    self.my_hand.show_hand()

                    if self.dealer_hand.get_hand_value() < 17:
                        self.hit(self.dealer_hand)

                    print("==================================")
                    print("DEALER'S HAND: ")
                    self.dealer_hand.show_hand()

                    if self.bust():
                        print("YOU BUSTED!")
                        self.game_ended = True

                # If user wants to stand:
                else:
                    my_result = self.my_hand.get_hand_value()
                    dealer_result = self.dealer_hand.get_hand_value()

                    print("\nGAME RESULTS:")
                    print("==================================")
                    print("YOUR HAND VALUE: {0}".format(my_result))
                    print("DEALER HAND VALUE: {0}".format(dealer_result))
                    print("==================================")

                    self.check_for_win(my_result, dealer_result)

            play_again = input("DO YOU WANT TO PLAY AGAIN? (Y/N) \n").lower()
            while play_again not in self.play_again_options:
                play_again = input("INVALID INPUT. PLEASE ENTER 'Y' OR 'N'. \n")

            # If user wishes to play another game, self.game_ended is reset to False so the loop continues.
            if self.play_again_options[play_again]:
                self.game_ended = False
            else:
                self.playing = False

if __name__ == "__main__":
    blackjack = Blackjack()
    blackjack.start_game()
