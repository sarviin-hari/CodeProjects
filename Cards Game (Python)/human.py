from __future__ import annotations


from cards import Card, Rank, Suit
from player import Player


class Human(Player):
    """
    The purpose of this class is to initialize a human player with his name and to allow the users to play or pass the
    card they would decide to. This class has a init method that
    """

    def __init__(self) -> None:
        """
        1. Ask for player to input his name
        2. Call Player class's __init__ method
        """
        player_name = str(input("Please enter your name: "))
        Player.__init__(self, player_name)

    def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:
        """
        Call self.hand_image() --> to print the card's in the hand of the player
        Asks player to select a card to play (Validate so that an integer >0 and <len(self.hand) is entered)
        check_valid_play of the card chosen. If valid, return card, else, print error message and asks to input again

        Parameter: trick (has the cards that has been played by each player before its the turn of this player)
                   broken_hearts (if true, hearts have been broken -> hearts has been played)

        Return: card that can be played by Human Player
        """

        # prints the cards and its index in current hand
        print("It's your turn to play a card. Please select an index representing the card you wish to play.")
        print("Your current hand:")
        print(self.hand_image())
        print("")

        # while loop again and again until a valid card is entered
        while True:
            card_to_play = input("Select a card to play: ")  # input card to play

            # checks if it is an integer, if not print error message and loops again
            try:
                card_to_play = int(card_to_play)
            except:
                print("Please enter an Integer!")
                continue

            # checks if the number is > 0 and < (number of cards in hand - 1) and check_valid_play == True
            if len(self.hand) > card_to_play >= 0 and (self.check_valid_play(self.hand[card_to_play], trick, broken_hearts))[0] == True:
                # If yes remove the card from hand and returns the card
                card_to_send = self.hand[card_to_play]
                self.hand.remove(card_to_send)
                print("")
                return card_to_send

            # if number is >= number of cards in hand, print error message
            elif card_to_play >= len(self.hand):
                print("Card selected is not in hand!")
            elif card_to_play < 0:
                print("Please enter a valid positive index value!")
            # prints error message (Why card entered is not valid to play)
            else:
                print((self.check_valid_play(self.hand[card_to_play], trick, broken_hearts))[1])

    def hand_image(self):
        """
        Gets the correct suit_symbol and rank_symbol
        Use for loop and string concatenation to get the correct card image side by side
        Use string concatenation to get the index string image

        Parameter: self

        Return: card as text_image and index line:
        """

        die_face_list = [""] * 5  # stores the concatenated string in five indexes
        index_line = ""           # stores the line of index
        card_diagram = ""         # stores the diagram of the card

        # changes the design of ranks of the card
        def the_rank(rank_num):
            """
            This is a sub function inside the main hand_image function that turns the rank numbers into their respective characters
            to be printed on the card image
            Parameter: An integer between 2-14 representing the rank of cards (unique characters are printed for cards ranked 11-14 while the same rank number is printed on the card image for the rest)
            Return: rank_num storing a character that symbolizes the corresponding rank
            """
            if rank_num == 11:
                rank_num = 'J'
            elif rank_num == 12:
                rank_num = 'Q'
            elif rank_num == 13:
                rank_num = 'K'
            elif rank_num == 14:
                rank_num = 'A'
            return rank_num

        # changes the design of suits of the card
        def the_suit(suit_num):
            """
            This is a sub function inside the main hand_image function that turns the suit numbers into their respective symbol
            to be printed on the card image
            Parameter: An integer between 1-4 representing the suit of cards (unique symbols are used to represent each different suits)
            Return: suit_num storing symbol that represents the corresponding suit
            """

            img_clubs = "♧"
            img_diamonds = "♢"
            img_spades = "♤"
            img_hearts = "♡"

            if suit_num == 1:
                suit_num = img_clubs
            elif suit_num == 2:
                suit_num = img_diamonds
            elif suit_num == 3:
                suit_num = img_spades
            else:
                suit_num = img_hearts
            return suit_num

        # loop len(self.hand) number of times to get the roll dice value and its corresponding text-image
        for num_of_cards in range(len(self.hand)):

            # gets the corresponding rank_symbol and suit_symbol
            rank_symbol = the_rank(self.hand[num_of_cards].rank.value)
            suit_symbol = the_suit(self.hand[num_of_cards].suit.value)

            # formatting for the card image
            new_art = ["┌─────┐", "│{}    │".format(rank_symbol), "│  {}  │".format(suit_symbol), "│    {}│".format(rank_symbol),
                       "└─────┘"]
            new_art_2 = ["┌─────┐", "│{}   │".format(rank_symbol), "│  {}  │".format(suit_symbol), "│   {}│".format(rank_symbol),
                         "└─────┘"]

            # formatting for the index line
            number_format = "|--{}--|".format(num_of_cards)
            number_format_2 = "|-{}--|".format(num_of_cards)

            # changes the style of index based on the index value
            if num_of_cards >= 10:
                index_line += number_format_2
            else:
                index_line += number_format

            # for every card, the corresponding text_line will be added to their corresponding indexes in the die_face_list
            for line_num in range(5):
                if str(rank_symbol) == "10":
                    die_face_list[line_num] += new_art_2[line_num]
                else:
                    die_face_list[line_num] += new_art[line_num]

        # loops five times to convert the strings in the lists into a string where each of the indexes are separated by \n (makes the following strings in a new line when printed)
        for num_of_cards in range(len(die_face_list)):
            card_diagram += die_face_list[num_of_cards] + "\n"

        return card_diagram + index_line  # return the card diagram and index line

    def pass_cards(self, passing_to: str) -> list[Card]:
        """
        Call self.hand_image() to print the current cards in hand
        Asks player to select 3 cards to play (Validate so that all integers are of the correct format, are integers, within the index range and no duplicates)
        Remove the passing cards from hand

        Parameter: self as the instance variables from the Player class inherited by Better AI will be used

        Return: list of 3 cards to pass
        """
        print("Your current hand:")
        print(self.hand_image())
        print("")

        bool = False

        # while loop again and again until a valid card is entered (bool == True)
        while not bool:
            card_to_play = input("Select three cards to pass off to {} (e.g. '0, 4, 5'): ".format(passing_to))

            # checks if 3 digits separated by "," is inputted, if not print error message and loops again
            try:
                assert type(card_to_play.strip().split(",")) == list and len(card_to_play.strip().split(",")) == 3
                num_list = card_to_play.strip().split(",")
            except:
                print("Wrong format of index of cards is entered!")
                continue

            # checks if all 3 digits are an integer, if not print error message and loops again
            try:
                for index in range(3):
                    num_list[index] = int(num_list[index])
            except:
                print("Non-Integer value detected in input!")
                continue

            # checks if all 3 digits are within the index range and are distinct integers, if not print error message and loops again
            try:
                # check if numbers within range, and then check if numbers within range check if both numbers are the same (check for duplicates)
                counter = 0
                for index in range(3):
                    assert int(num_list[index]) < len(self.hand) and int(num_list[index]) >= 0, "Index not within range!"
                    for index_2 in range(3):
                        if num_list[index] == num_list[index_2]:
                            counter += 1

                assert counter == 3, "Duplicate index value is identified!"

                bool = True  #  if all conditions are fulfilled, set bool to True to terminate the loop

            except Exception as e:
                print(e)
                continue

            # gets the cards to remove based on its index and remove the cards from hand
            card_list_remove = []
            for index in range(3):
                card_list_remove.append(self.hand[num_list[index]])

            for index in range(len(num_list)):
                self.hand.remove(card_list_remove[index])

            return card_list_remove  # return the cards that has been passed


if __name__ == "__main__":
    player = Human()
    # print(player)
    player.hand.append(Card(Rank.King, Suit.Hearts))  # 0
    player.hand.append(Card(Rank.Four, Suit.Hearts))  # 1
    player.hand.append(Card(Rank.Ace, Suit.Hearts))  # 2
    player.hand.append(Card(Rank.Ten, Suit.Hearts))  # 3
    player.hand.append(Card(Rank.Ace, Suit.Hearts))  # 4
    player.hand.append(Card(Rank.Five, Suit.Hearts))  # 5
    player.hand.append(Card(Rank.King, Suit.Diamonds))  # 6
    player.hand.append(Card(Rank.Ace, Suit.Hearts))  # 7
    player.hand.append(Card(Rank.Two, Suit.Clubs))  # 8

    player.hand.append(Card(Rank.Ace, Suit.Hearts))  # 9
    player.hand.append(Card(Rank.Ten, Suit.Hearts))  # 3
    player.hand.append(Card(Rank.Ace, Suit.Hearts))  # 4
    player.hand.append(Card(Rank.Five, Suit.Hearts))  # 5
    player.hand.append(Card(Rank.King, Suit.Diamonds))  # 6
    player.hand.append(Card(Rank.Ace, Suit.Hearts))  # 7
    player.hand.append(Card(Rank.Two, Suit.Clubs))  # 8

    # print(player.hand_image())

    # print(player.pass_cards("Player 2"))

    # print(player.name)
