from __future__ import annotations  # for type hints of a class in itself
from enum import Enum


class Rank(Enum):
    """
    Rank class has 13 class variables for each of the ranks.
    Enum create ranges of rank within a suit, from Two to Ace
    """
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14

    def __lt__(self, other: Rank) -> bool:
        """
        This function compares the ranks of the cards.

        Parameters: self (to access attributes and methods of class in python),Rank

        Returns boolean True when card Rank is of greater value
        """

        return self.value < other.value # return True if condition is met


class Suit(Enum):
    """
    Rank class has 4 class variables for each of the suits.
    Enum create ranges of suit within a deck of cards, from Clubs to Hearts    """
    Clubs = 1
    Diamonds = 2
    Spades = 3
    Hearts = 4

    def __lt__(self, other: Suit) -> bool:
        """
        This function compares the suits of the cards.

        Parameters: self (to access attributes and methods of class in python), Suit

        Returns boolean True when card Suit is of greater value
        """

        return self.value < other.value # return True if condition is met


class Card:
    """
    initializes 2 instance variables and changes the functionalities of 5 methods (init, repr, str, eq, lt)
    """

    pretty_print = False  # sets the pretty print version of cards to false

    def __init__(self, rank: Rank, suit: Suit) -> None:
        """
        This function initialises 2 instance variables which are
            self.rank that helps to determine the Card's rank
            self.suit that helps to determine the Card's suit

        Parameters: self (to access attributes and methods of class in python), Rank, Suit

        Returns None
        """

        self.rank = rank  # rank is stored in self.rank instance variable
        self.suit = suit  # suit is stored in self.suit instance variable

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
        It allows the user to view the card as text-image or just text based on the state of the class variable, pretty_print

        Parameters: self (to access attributes and methods of class in python)

        Returns string
        """

        card_diagram = "\n"

        die_face_list = ["","","","",""]

        img_clubs = "♧"                 # prints ♧ image for Clubs suit
        img_diamonds = "♢"              # prints ♢ image for Diamonds suit
        img_spades = "♤"                # prints ♤ image for Spades suit
        img_hearts = "♡"                # prints ♡ image for Hearts suit

        if self.rank.value == 11:       # J image is printed as a rank number if Rank value is 11
            rank_num = 'J'
        elif self.rank.value == 12:     # Q image is printed as a rank number if Rank value is 12
            rank_num = 'Q'
        elif self.rank.value == 13:     # K image is printed as a rank number if Rank value is 13
            rank_num = 'K'
        elif self.rank.value == 14:     # A image is printed as a rank number if Rank value is 14
            rank_num = 'A'
        else:
            rank_num = self.rank.value  # If the Rank value is 1-10, it'll print its own value as a rank number

        if self.suit.value == 1:        # If Suit value is 1, '♧' will be printed
            suit_num = img_clubs
        elif self.suit.value == 2:      # If Suit value is 2, '♢' will be printed
            suit_num = img_diamonds
        elif self.suit.value == 3:      # If Suit value is 3, '♤' will be printed
            suit_num = img_spades
        else:
            suit_num = img_hearts       # '♡' will be printed if the Suit value is not 1, 2 or 3

        new_art = ["┌─────┐", "│{}    │".format(rank_num), "│  {}  │".format(suit_num), "│    {}│".format(rank_num),
                   "└─────┘"]
        new_art_2 = ["┌─────┐", "│{}   │".format(rank_num), "│  {}  │".format(suit_num), "│   {}│".format(rank_num),
                     "└─────┘"]

        for line in range(5):  # for every dice value, the corresponding text_line will be added to their corresponding indexes in the die_face_list

            if str(self.rank.value) == "10":
                die_face_list[line] += new_art_2[line]
            else:
                die_face_list[line] += new_art[line]

        for index in range(len(die_face_list)):  # loops five times to convert the strings in the lists into a string where each of the indexes are separated by \n (makes the following strings in a new line when printed)
            card_diagram += die_face_list[index] + "\n"

        if self.pretty_print:       # if pretty_print set to True, the card diagram is printed
            return card_diagram                                       # if pretty_print set to true, the text-image of card is printed
        else:
            return '{} of {}'.format(self.rank.name, self.suit.name)  # if pretty_print set to False, the card text is printed

    def __eq__(self, other: Card) -> bool:
        """
        This function deals with cards of equal suit and rank

        Parameters: self (to access attributes and methods of class in python), Card

        Returns boolean True when the cards are equal only if the Rank and Suit are the same
        """
        return self.rank == other.rank and self.suit == other.suit  # return True if condition is met

    def __lt__(self, other: Card) -> bool:
        """
        This function compares the Suit value first.
        If both suits have equal value, then Rank value will determine whether a card is less than the other.

        Parameters: self (to access attributes and methods of class in python), Card

        Returns boolean True when the card's Suit or Rank is less than the other.
        """

        if self.suit.value < other.suit.value:      # if suit value is smaller than the other, return True
            return True
        elif self.suit.value == other.suit.value:   # if suit value is the same, check if the rank value is smaller than the other, return True
            if self.rank.value < other.rank.value:
                return True
            else:
                return False
        else:
            return False

if __name__ == "__main__":

    # r2 = Rank.Three
    # r3 = Rank.Three
    # print(r2 < r3)

    card1 = Card(Rank.Ace, Suit.Clubs)
    card2 = Card(Rank.Three, Suit.Clubs)

    # print(card1)


    # print(card1.rank.value)
    #
    # print(f"{card1}, {card2}")
    # print(card1 == card2)
    # print(card1 < card2)
    # print(card1.suit)

