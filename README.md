# Design Document
The following is the design document for my simple console-based Python implementation of traditional Blackjack.

## Running the Game ##
To run the game in terminal, simply navigate to the directory where the code was downloaded and run the command `python3 game.py`. This should call the main function in the Python file and start up a new game of Blackjack. To execute specific actions (hit/stand), follow the instructions provided on the terminal output. This game is user-input based, meaning that you must type directly into the console to specify which actions you would like to make. 

## Rules and Modifications ##
The rules for the this rendition of Blackjack are exactly the same as the rules for a traditional game, except there is no feature to place wagers and bets. This means that there is no option to "double down," "split," or "surrender." This was done for the sake of saving time and would definitely be an interesting feature to implement in the future. The player only has the option to hit or stand, and must try their luck in an attempt to beat the computer (the dealer).

## Design Choices ##
### Writing Modular Code ###
Writing a functional game of Blackjack in a reasonable amount of time required that the code I wrote be well abstracted and modular, so that separate classes could call on other class methods reliably and efficiently. This would also make the code a lot more readable. For this, I had to design data structures that, when used together, could represent a deck of cards. To do this, I had to think about which features the deck of cards had to perform efficiently: shuffling the cards, dealing out hands, and adding **random** cards to someone's hand (a hit). To create my deck of cards implementation in a modular manner, I decided to create three separate classes:
* Bullet list
  * Nested bullet



Instructions for running your code and any tests you may have written
Rules for your card game, if not one of the three listed above
A brief explanation of your design choices and any data structures or algorithms that you implemented
Choice of tooling (language, libraries, test runner, etc.) and rationale behind those choices.
