from __future__ import annotations
from cards import Card, Rank, Suit
from basic_ai import BasicAIPlayer

class Round:
    """
    This class contains the necessary functions for the round to play out
    - play_round function (which handles how each round is played out),
    - ori_start_index function (which gets the first start index where the two of clubs is still in the list),
    - and the next_start_index function (finds the player who puts down the highest card value in the trick and makes that player take the trick).
    - the round continues as long as there is card in the hands of the player
    """

    def __init__(self, players) -> None:
        """
        This function initializes 3 instance variables which are
           self.players (list of all the players playing the game),
           self.trick_list (list of cards that is played on each turn of a round) and
           self.broken_hearts_bool (to check if hearts is broken or not).

        Next it calls the method self.play_round() to play the game
        """

        self.players = players  # Initializes self.players and stores players in self.players
        self.trick_list = []  # Initializes self.trick_list that stores the cards for each trick
        self.broken_hearts_bool = False  # Initializes self.broken_hearts_bool to False to check if hearts have been broken or not

        self.play_round()  # Calls the method self.play_round to play the round

    def play_round(self):
        """
        This function deals with how the round will run.
        The while loop runs until the player has no more cards, and it deals with choosing the smallest card to play.
        Penalty points are imposed to players who take hearts cards or the Queen of spades wildcard.

        Parameters: self (to access attributes and methods of class in python)

        Returns played card (upon calling the play_card function)
        """

        first_player_index = self.ori_start_index()                                                     # gets the start index from the player list for the player that has Two of clubs
        self.players = self.players[first_player_index:] + self.players[:first_player_index]            # gets the list in order of the player playing the card (Ex: [P3, P4, P1, P2])

        while (len(self.players[0].hand)) > 0:                                                          # the while loop runs again and again until the self.hand of a player has 0 elements / cards

            for player_index in range(len(self.players)):
                player = self.players[player_index]                                                                # the player details (name, hand, roundscore, totalscore)
                smallest_card_to_play = player.play_card(self.trick_list, self.broken_hearts_bool)      # goes to the function play_card in basic_ai and does a validation of the correct card to play, removes the card from hand, and returns the playable card
                self.trick_list.append(smallest_card_to_play)                                           # store the playable card in self.trick_list

                print(f"{player} plays {(smallest_card_to_play)}")                                      # prints the player name and the card played

                if self.broken_hearts_bool == False and (smallest_card_to_play.suit.name == "Hearts"):  # if the broken hearts is False and the card played is a hearts, broken hearts is set to true and Hearts have been broken message is printed
                    self.broken_hearts_bool = True
                    print("Hearts have been broken!")

            next_player_index = self.next_start_index(self.trick_list)                                  # gets the start index from the player list of the player that takes the trick

            penalty = 0

            for trick_index in range(len(self.trick_list)):                                                       # if the self.trick_list has Hearts or Queen of Spades, the player's score is updated and the penalty is updated to find the penalty for the round for that player
                if self.trick_list[trick_index].suit.name == "Hearts":
                    self.players[next_player_index].round_score += 1        # 1 penalty point for each Hearts and update the round score of the player accordingly
                    penalty += 1

                if self.trick_list[trick_index] == Card(Rank.Queen, Suit.Spades):     # 13 penalty points for Queen of Spades and update the round score of the player accordingly
                    self.players[next_player_index].round_score += 13
                    penalty += 13

            print(f"{(self.players[next_player_index])} takes the trick. Points received: {penalty}")   # prints the player name and the penalty
            self.players = self.players[next_player_index:] + self.players[:next_player_index]          # gets the list in order of the player playing the card (Ex: [P3, P4, P1, P2])
            self.trick_list = []                                                                        # sets the self.trick_list back to a null set


    def ori_start_index(self):  # first start index where two of clubs still in list
        """
        This function gets the first start index where the two of clubs is still in the list.
        This function finds the player who has the two of clubs in hand, and assigns the start index to that player (the player with the two of clubs will be the one who starts the round)

        Parameters: self (to access attributes and methods of class in python

        Returns start_index
        """

        start_index = 0
        for player_index in range(len(self.players)):                              # loops through players in the list
            if Card(Rank.Two, Suit.Clubs) in self.players[player_index].hand:      # finds the player who has the two of clubs
                start_index = player_index                                         # assigns the start index to that player
        return start_index

    def next_start_index(self, trick_list):
        """
        This function finds the player who puts down the highest card value in the trick and makes that player take the trick.

         Arguments: trick_list (a list containing the 4 cards in a trick)

         Returns start index
        """
        start_index = 0
        cards_of_same_suit = []

        for trick_index in range(len(trick_list)):                            # for each one of the 4 cards in the trick list
            if trick_list[0].suit == trick_list[trick_index].suit:            # compares the cards of the same suit in the trick with the first played card in the trick
                cards_of_same_suit.append(trick_list[trick_index])            # gets the list of cards of the same suit

        max_card = max(cards_of_same_suit)                          # for the highest rank card in the list of cards of the same suit
        for trick_index in range(len(trick_list)):                            # for each card in the trick list
            if trick_list[trick_index] == max_card:                           # get the highest card value in the suit list and find the index of the card (which player)
                start_index = trick_index

        return start_index

if __name__ == "__main__":
    # using our basic AI player that always plays the least ranking valid card
    players = [BasicAIPlayer("Player 1"), BasicAIPlayer("Player 2"), BasicAIPlayer("Player 3"), BasicAIPlayer("Player 4")]

    players[0].hand = [Card(Rank.Four, Suit.Diamonds), Card(Rank.King, Suit.Clubs), Card(Rank.Nine, Suit.Clubs),
                       Card(Rank.Ace, Suit.Hearts)]
    players[1].hand = [Card(Rank.Two, Suit.Clubs), Card(Rank.Four, Suit.Spades), Card(Rank.Nine, Suit.Spades),
                       Card(Rank.Six, Suit.Diamonds)]
    players[2].hand = [Card(Rank.Seven, Suit.Diamonds), Card(Rank.Ace, Suit.Spades), Card(Rank.Jack, Suit.Diamonds),
                       Card(Rank.Queen, Suit.Spades)]
    players[3].hand = [Card(Rank.Queen, Suit.Hearts), Card(Rank.Jack, Suit.Clubs), Card(Rank.Queen, Suit.Diamonds),
                       Card(Rank.King, Suit.Hearts)]

    Round(players)
