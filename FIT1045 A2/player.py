from __future__ import annotations
from cards import Card, Rank, Suit

class Player:
    """
    This class initializes a player (name, hand, round_score, total score) in the init method and represent
    the object as the name of the player. This class also checks if a card inputted is valid to be played through the
    method check_valid_play()
    """

    def __init__(self, name: str) -> None:
        """
        Initializes 4 variables
            self.name (stores the name of the player)
            self.hand (list of cards that each player has in his hands)
            self.round_score (the score of each round)
            self.total_score (the total score at the end of the round)

        Parameter: name being passed is stored in instance variable self.name

        Return: None
        """
        self.name = name
        self.hand = []
        self.round_score = 0
        self.total_score = 0

    def __repr__(self) -> str:
        """
        This function stores the object of the class as the return value / representation

        Parameters: self (to access attributes and methods of class in python)

        Returns string
        """

        return self.__str__()  # return the str representation

    def __str__(self) -> str:
        """
        This function allows the user to see the same string of their card

        Parameters: self (to access attributes and methods of class in python)

        Returns string
        """

        return self.name  # return the name of the player

    def check_valid_play(self, card: Card, trick: list[Card], broken_hearts: bool) -> (bool, str):
        """
        Checks if a card is valid to be played based on the trick_list and broken_hearts
        If no cards in trick
            If Two of Clubs in hand it must be played.
            If hearts played, but broken hearts is False, the card can only be played if there is no cards of other suits in hand

        If there is card in hand
            If the suit of the first trick is in hand, that card must be played
            If it is the very first round, Hearts or Queen of Spades cannot be played



        Parameter: card (the card that the player intends to play)
                   trick (has the cards that has been played by each player before its the turn of this player)
                   broken_hearts (if true, hearts have been broken -> hearts has been played)

        Return: a tuple of (boolean{True/False}, Text{Valid Play/ Error Message})
        """
        if len(trick) == 0:  # if player leads the trick
            if Card(Rank.Two, Suit.Clubs) != card and Card(Rank.Two, Suit.Clubs) in self.hand:  # returns False if Two of Clubs in hand but not played
                return (False, 'Two of Clubs is still in hand! Please play Two of Clubs!')

            elif card.suit.name == "Hearts" and broken_hearts == False:
                for card_in_hand in self.hand:  # if broken hearts is False and cards played is hearts, but there is still cards of other suits in hand, return False
                    if card_in_hand.suit.name != "Hearts":
                        return (False, 'Player still has cards of other suit that can be played as hearts is still not broken yet!')

                return (True, "Card is valid to play")  # return True as the hearts card can be played
            else:
                return (True, "Card is valid to play")  # all other cards played is valid since the False conditions is already taken care off

        else:  # if player not leading the trick
            if card.suit == trick[0].suit:
                return (True, "Card is valid to play")  # return True if the card played is off the same suit as the trick

            else:
                for card_in_hand in self.hand:  # if first trick's suit is not equals to card's suit, check if in hand there is card of the same suit as trick
                    if card_in_hand.suit == trick[0].suit:
                        return (False, 'Player still has cards from the suit of the current trick!')  # if yes, return False

                if Card(Rank.Two, Suit.Clubs) == trick[0] and (card.suit.name == "Hearts" or card == Card(Rank.Queen, Suit.Spades)):  # Check if the card in first Trick is Two of Clubs, if it is then if the card played is hearts or Queen of Spades return False
                    return (False, 'Hearts and Queen of Spades is not allowed in the first round!')
                else:
                    return (True, "Card is valid to play")  # all other cards played is valid since the False conditions is already taken care off
