# Design Document
The following is the design document for my simple console-based Python implementation of traditional Blackjack.

## Running the Game ##
To run the game in terminal, simply navigate to the directory where the code was downloaded and run the command `python3 game.py`. This should call the main function in the Python file and start up a new game of Blackjack. To execute specific actions (hit/stand), follow the instructions provided on the terminal output. This game is user-input based, meaning that you must type directly into the console to specify which actions you would like to make. 

## Rules and Modifications ##
The rules for the this rendition of Blackjack are exactly the same as the rules for a traditional game, except there is no feature to place wagers and bets. This means that there is no option to "double down," "split," or "surrender." This was done for the sake of saving time and would definitely be an interesting feature to implement in the future. The player only has the option to hit or stand, and must try their luck in an attempt to beat the computer (the dealer).

## Design Choices ##
### Writing Modular Code ###
Writing a functional game of Blackjack in a reasonable amount of time required that the code I wrote be well abstracted and modular, so that separate classes could call on other class methods reliably and efficiently. This would also make the code a lot more readable. For this, I had to design data structures that, when used together, could represent a deck of cards. To do this, I had to think about which features the deck of cards had to perform efficiently: shuffling the cards, dealing out hands, and adding **random** cards to someone's hand (a hit). To create my deck of cards implementation in a modular manner, I decided to create three separate classes:
* `Card` class
  * This class was used to define a card object. I kept it simple. A card is identified by its suit and value.
* `Deck` class
  * This was a class used to define a collection of 52 playing cards, as well as certain functions related to the deck. When instantiated, this class called upon the `Card` class to populate the collection. A deck of cards needed two import functions: shuffling the cards randomly and dealing cards one by one. This was done using Python's `random` module and by using a queue, respectively. More information on this later.
* `Hand` class
  * This class was used to simulate a player's (or dealer's) hand of cards. It needed to support a few important features, including: adding a new card to the hand, determining the total value of the hand (including aces), and printing out a hand in a human-friendly way.
  
 ### Accounting for Edge Cases ###
A big consideration while coding this game was thinking about when it could possibly fail, and how I could mitigate this possibility. Some of the interesting cases to consider included: how do we correctly determine the value of a soft hand (one with an ace), how can we determine when the dealer should hit, and how do we deal with ties? 

To account for the case where aces were dealt into a hand, I decided to treat every ace as an 11 as soon as it was dealt into a hand. Then, whenever I called the `get_hand_value()`, I would check if an ace existed in the hand. If so, I would determine the total value of the hand treating aces as 11s, and then continuously subtract 10 (analogous to converting an 11 ace to a 1 ace) until the total hand value was under 21. 

As for determining when the dealer should hit, I didn't want to get too complicated. There are many interesting techniques that we could implement to maximize the expected value of the dealer's hand, but I decided to keep it simple for sake of time. In my implementation, a dealer will always hit on a hand whose total value is less than 17. Some casino's implement the "soft 17" rule, where a dealer hits on a 17 hand if there's the hand has an ace, but I decided not to so we could have a safer dealer. This wouldn't be too difficult to implement if someone wanted to, though.

### Designing the GUI ###
Any console-based game isn't going to look too pretty. Nevertheless, I wanted to try my best to make this game of Blackjack as human-friendly as possible. This meant figuring out a way to print out cards so that they looked like actual playing cards. After surfing StackOverflow for a little bit, I came across a technique for rendering playing cards that I thought would work well for my use case. Initially, I was printing cards out by simply outputting their value and suit on the console, i.e. "King of Diamonds." But with enough tweaking and debugging, I was finally able to have cards print out onto the console in the following format, which is much prettier and actually makes it feel like you're playing a card game.
                                             ┌─────────┐┌─────────┐┌─────────┐
                                             │8        ││J        ││3        │
                                             │         ││         ││         │
                                             │    ♥    ││    ♦    ││    ♣    │
                                             │         ││         ││         │
                                             │        8││        J││        3│
                                             └─────────┘└─────────┘└─────────┘

Instructions for running your code and any tests you may have written
Rules for your card game, if not one of the three listed above
A brief explanation of your design choices and any data structures or algorithms that you implemented
Choice of tooling (language, libraries, test runner, etc.) and rationale behind those choices.
