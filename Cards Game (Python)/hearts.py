from __future__ import annotations

import random
import time

from cards import Card, Rank, Suit
from basic_ai import BasicAIPlayer
from better_ai import BetterAIPlayer
from human import Human
from round import Round


class Hearts:
    """
    This class creates an object that prompts for two inputs upon initialisation, which are
        a target score to end the game, and
        desired number of players (3-5) for the game
    Runs the game (class Round) and updates the player name and score and finds the winner at the end of the game
    """

    def valid_ai_input(self):
        """
        This function acts as a validation for the input entered for number of basic ai and better ai players
        Asks to input num of basic ai and num of better ai
        Checks if the inputs are valid by calling the methods self.num_of_better_ai_input() and self.num_of_basic_ai_input()
        If the total basic ai and better ai corresponds to the correct length of list prints valid message and break, else loop again

        Parameter: self

        Return: Only a valid integer input.
        """

        if self.num_of_players == 4 or self.num_of_players == 5:    # if num_of_players == 4 or 5, print the message below
            print("\n--> Human Player has been initialized. Now please enter the number of Basic AI player(s) and Better AI player(s) to play against.")
            print(f"--> The combination of Basic AI player(s) and Better AI player(s) must add up to {self.num_of_players - 1}!\n")

        while True:                                                             # while loops again and again until a valid input is entered
            if self.num_of_players == 4:                                        # if num of players == 4, ask user to input the number of basic ai and better ai that the player would play against and validate the input
                self.num_of_basic_ai = self.num_of_basic_ai_input([1, 2])
                self.num_of_better_ai = self.num_of_better_ai_input([1, 2])
            elif self.num_of_players == 5:
                self.num_of_basic_ai = self.num_of_basic_ai_input([1, 2, 3])    # if num of players == 5, ask user to input the number of basic ai and better ai that the player would play against and validate the input
                self.num_of_better_ai = self.num_of_better_ai_input([1, 2, 3])
            else:
                print("\n***** 1 Human player, 1 Basic AI player and 1 Better AI Player have been initialized *****\n")
                time.sleep(1)                                                   # time.sleep() is used to pause the program for the number of seconds stated in the parenthesis
                break

            if (self.num_of_basic_ai + self.num_of_better_ai) == self.num_of_players - 1:   # check if sum of basic ai and better ai entered corresponds to the total number of players (excluding Human)
                print(f"\n***** 1 Human player, {self.num_of_basic_ai} Basic AI player(s) and {self.num_of_better_ai} Better AI player(s) have been initialized *****\n")
                time.sleep(1)
                break
            else:
                print(f"The combination of {self.num_of_basic_ai} Basic AI player(s) and {self.num_of_better_ai} Better AI player(s) is not possible. Try again!")
                print("")

    def __init__(self) -> None:
        """
        A welcome statement for the game is prompted
        This function initialises 4 instance variables which are
            self.start_index that helps determine and rearrange the passing order of cards from one player to another before every round begins
            self.max_score stores the maximum score obtained among all players until current round, and serves as a comparison variable to determine if target score is met, thus end the game.
            self.num_of_min_score acts as a counter that checks if there's a tie between players with the lowest score and decides if another round is necessary to break the tie.
            self.round_num represent the number of round in a game

            The game then is begun by calling the self.target_score_input() method to get the target score to end game from user and return a validated input
            Followed by the calling of sel.num_of_players_input() method to get the desired number of players from user and return a validated input.
        """

        Card.pretty_print = True  # set to true so that when this file runs, the pretty print version of the card will be displayed instead of texts

        print("Welcome to ♥ HEARTS ♥")
        print("")
        self.start_index = 0        # used to find the start index of the player that starts the round
        self.max_score = 0          # stores the max_score to find when to terminate the loop
        self.num_of_min_score = 1   # stores the number of players with same num_of_min_score to check if two players have the same minimum score
        self.round_num = 1          # to store the round_num
        self.num_of_basic_ai = 1    # the initial number of basic ai is set to 1. Needed to get the player list
        self.num_of_better_ai = 1   # the initial number of better ai is set to 1. Needed to get the player list

        self.target_score = self.target_score_input()       # call self.target_score_input() to validate an input and returns once the input is valid
        self.num_of_players = self.num_of_players_input()   # call self.num_of_players_input() to validate an input and returns once the input is valid

        self.valid_ai_input()  # call this method that inputs the valid ai values so that can initialize the correct numbe rof players in self.players

        self.players = self.find_ai_player_list()  # call self.find_player_list(self.num_of_players) to get the player list based on the num of players and the type of players

        time.sleep(1)
        print("\nPlayers playing this round: ")  # Prints the player's name and the type of player playing the round
        print_list = []
        for player in self.players:
            print_list.append(player.name + " (" + player.__class__.__name__ + ")")
        print(print_list)
        print("")
        time.sleep(2)

        # while loop runs as long as max_score of the round is still less than target_score OR if there is two minimum total_score
        while self.max_score < self.target_score or self.num_of_min_score > 1:
            time.sleep(1)

            print(f"========= Starting round {self.round_num} =========\n")


            bool_val = self.get_correct_suit()  # get the player.hand for each players and checks if all the suits are valid, if valid return True, else return False

            while bool_val == False:  # while loop runs to reshuffle the suits as long as one player does not have at least one card that isn't the Queen of Spades or from Hearts
                for player in self.players:
                    player.hand = []
                bool_val = self.get_correct_suit()

            if self.round_num % self.num_of_players != 0:   # pass cards only if the round_number is not divisible by number of players
                pass_card_list = self.pass_card()           # Calls the pass card method from Hearts to get the list of cards to pass
                time.sleep(1)
                self.passing_card(pass_card_list)           # Calls the passing_card method from Hearts to update the hand of each players with the passed cards
                time.sleep(1)

                print("\n----- All Cards have been passed -----\n")

            for player in self.players:                     # sort the cards in the hands of the player for a better user experience
                player.hand = sorted(player.hand)

            Round(self.players)                             # plays the round by calling the Round class with the parameter self.players

            self.round_score_26_check()                     # checks if anyone shoots the moon, if yes, changes the round_score accordingly

            time.sleep(1)
            print(f"========= End of round {self.round_num} =========\n")

            for player in self.players:                     # updates total score and prints the total score of each player
                player.total_score += player.round_score
                print(f"{player}'s total score: {player.total_score}")
                player.round_score = 0                      # sets the round score of each player to 0
            print("")
            time.sleep(2)

            self.while_loop_condition_check()  # checks and updates self.max_score and self.num_of_min_score
            self.round_num += 1  # Increments the self.round_num by 1

        self.find_winner()  # prints the winner of the game

    def target_score_input(self):
        """
        This function acts as a validation for the input entered for target score to end the game.
        Accepts the input of target score as its argument.
        Checks if the type and range of input entered matches the requirement and runs on loop until its met.

        Parameter: self

        Return: Only a valid integer input.
        """
        while True:  # while loops again and again until a valid target score (Integer value, > 0) is entered
            target_score = input("Please enter a target score to end the game: ")
            try:
                target_score = int(target_score)
            except ValueError:
                print('Please enter a numeric value!')
                continue
            if target_score > 0:
                break
            else:
                print('Valid number, please')

        return target_score

    def num_of_players_input(self):  # Gets the num_of_players input value
        """
        This function acts as a validation for the input entered for number of players in the game.
        Accepts the input of num of players as its argument.
        Checks if the type and range of input entered matches the requirement and runs on loop until its met.

        Parameter: self

        Return: Only a valid integer input.
        """
        while True:  # while loops again and again until a valid number of players (Integer value, 3 or 4 or 5) is entered
            num_of_players = input("Please enter the number of players (3-5): ")
            try:
                num_of_players = int(num_of_players)
            except ValueError:
                print('Please enter a numeric value!')
                continue
            if num_of_players >= 3 and num_of_players <= 5:
                break
            else:
                print('Valid number, please')

        return num_of_players

    def num_of_basic_ai_input(self, valid_num_list):
        """
        This function acts as a validation for the input entered for number of basic ai in the game.
        Accepts the input of num of players as its argument.
        Checks if the type and range of input entered matches the requirement and runs on loop until its met.

        Parameter: self

        Return: Only a valid integer input.
        """
        while True:  # while loops again and again until a valid number of players (Integer value, within valid_num_list) is entered
            option = input("Please enter the number of Basic AI Player {}: ".format(" or".join(str(valid_num_list).split(","))))
            try:
                option = int(option)
            except:
                print('Please enter a numeric value!')
                continue
            if option in valid_num_list:
                break
            else:
                print('Valid number, please')

        return option

    def num_of_better_ai_input(self, valid_num_list):
        """
        This function acts as a validation for the input entered for number of better ai in the game.
        Accepts the input of num of players as its argument.
        Checks if the type and range of input entered matches the requirement and runs on loop until its met.

        Parameter: self

        Return: Only a valid integer input.
        """
        while True:  # while loops again and again until a valid number of players (Integer value, within valid_num_list) is entered
            option = input("Please enter the number of Better AI Player {}: ".format(" or".join(str(valid_num_list).split(","))))
            try:
                option = int(option)
            except ValueError:
                print('Please enter a numeric value!')
                continue
            if option in valid_num_list:
                break
            else:
                print('Valid number, please')

        return option

    def find_ai_player_list(self):  # Gets the player list for num_of_players 3, 4, 5 respectively
        """
        For num of players = 3 --> 1 Human, 1 Basic AI and 1 Better AI are initialized into the players list
        For num of players = 4 --> 1 Human, Basic AI and Better AI (based on the inputs) are initialized into the players list
        For num of players = 5 --> 1 Human, Basic AI and Better AI (based on the inputs) are initialized into the players list

        Parameter: self

        Return: players that has all the players that will be playing the round
        """
        if self.num_of_players == 3:
            # Game play with 1 Human, 1 Basic AI, 1 Better AI
            players = [Human(), BasicAIPlayer("Player 2"), BetterAIPlayer("Player 3")]

        elif self.num_of_players == 4:
            # Game play with 1 Human, 1/2 Basic AI, 2/1 Better AI
            players = [Human()]
            player_num = 2  # to update the player number
            for _ in range(self.num_of_basic_ai):
                players.append(BasicAIPlayer("Player {}".format(player_num)))  # Gets the object for Basic AI based on the number of players inputted
                player_num += 1
            for _ in range(self.num_of_better_ai):
                players.append(BetterAIPlayer("Player {}".format(player_num)))  # Gets the object for Basic AI based on the number of players inputted
                player_num += 1

        else:
            # Game play with 1 Human, 1/2/3 Basic AI, 3/2/1 Better AI
            players = [Human()]
            player_num = 2
            for _ in range(self.num_of_basic_ai):
                players.append(BasicAIPlayer("Player {}".format(player_num)))  # Gets the object for Basic AI based on the number of players inputted
                player_num += 1
            for _ in range(self.num_of_better_ai):
                players.append(BetterAIPlayer("Player {}".format(player_num)))  # Gets the object for Basic AI based on the number of players inputted
                player_num += 1

        return players


    def pass_card(self):
        """
        This function gets a list containing three cards to be passed by each player based on the player type.

        Parameter: self

        Return: pass_card_list (List of 3 cards to pass)
        """
        pass_card_list = []

        start_index = self.round_num % self.num_of_players  					 # gets the passing order
        passing_order = self.players[start_index:] + self.players[:start_index]  # Rearrange the order of pass

        card_list = self.players[0].pass_cards(passing_order[0].name)  			 # since pass_cards for Human() takes in an argument, call pass card function for it first and update sthenpass_card_list
        pass_card_list.append(card_list)

        for player_index in range(1, self.num_of_players):                        # Find's the card to pass for the specific classes of the players in list and updates pass_card_list
            card_list = self.players[player_index].pass_cards()
            pass_card_list.append(card_list)

        return pass_card_list  # returns pass_card_list

    def passing_card(self, pass_card_list):
        """
        This function determines the order in which cards are passed from one player to another based on the round number
        It passes the cards correctly to each respective players

        Parameter: pass_card_list that has the list of cards to pass

        Return: None
        """
        start_index = self.round_num % self.num_of_players

        for player_index in range(len(self.players)):
            for pass_index in range(len(pass_card_list[0])):  # All the passed cards in an inner list at the given index of the outer list is added to the other player's hand based on the passing order
                self.players[start_index].hand.append(pass_card_list[player_index][pass_index])

            if start_index == len(self.players) - 1:  # updates the start_index which determines the passing order for every next round based on the conditions.
                start_index -= len(self.players) - 1
            else:
                start_index += 1

    def get_correct_suit(self):
        """
        This function creates a standard deck of 52 cards, shuffles it and remove a number of cards if needed before being dealt to the players
        It returns a boolean value indicating if the cards are correctly dealt based on a set of requirements.

        """
        all_card_list = []

        for suit_of_card in [Suit.Clubs, Suit.Diamonds, Suit.Spades,
                             Suit.Hearts]:  # creates a card list that imitates a standard deck of 52 cards
            for rank_of_card in [Rank.Two, Rank.Three, Rank.Four, Rank.Five, Rank.Six, Rank.Seven, Rank.Eight,
                                 Rank.Nine, Rank.Ten, Rank.Jack, Rank.Queen, Rank.King, Rank.Ace]:
                all_card_list.append(Card(rank_of_card, suit_of_card))

        random.shuffle(all_card_list)  # shuffles the cards(elements) in the card list

        if self.num_of_players == 3:  # removes respective cards from the card list based on the number of players to ensure every player is dealt an even amount of cards
            all_card_list.remove(Card(Rank.Two, Suit.Diamonds))
        elif self.num_of_players == 5:
            all_card_list.remove(Card(Rank.Two, Suit.Diamonds))
            all_card_list.remove(Card(Rank.Two, Suit.Spades))

        while len(all_card_list) > 0:  # concurrently adds shuffled cards from the deck to each player's hand and removes the respective card from the deck immediately to update the card list
            for player in self.players:
                card = all_card_list.pop(0)
                player.hand.append(card)

        for player in self.players:
            player.hand = sorted(player.hand)

        return self.card_validation_check()  # executes this specific function and returns its return value

    def card_validation_check(self):
        """

        This function ensures every player has at least one card that isn't the Queen of Spades or from Hearts , as this rare situation would break the game.
        If the requirement is not met, the cards will be dealt again until a valid deal is confirmed.
        Return a boolean value indicating whether it is a valid deal or not

        """

        for player in self.players:
            heart_counter = 0
            for card in player.hand:
                if card.suit.name == "Hearts":
                    heart_counter += 1

            num_of_QS = player.hand.count(Card(Rank.Queen, Suit.Spades))

            if (num_of_QS + heart_counter) == len(player.hand):  # if this condition is true, it means that the cards in the player's hand are either all Hearts suit or has a Queen of Spades with the remaining being of Hearts.
                print("..........Re-shuffle..........")
                return False  # return value of False indicates that cards need to be dealt again
        return True

    def round_score_26_check(self):
        """
        This function checks if a player has shot the moon by earning all 26 points within the round,
        in which case they receive 0 for this round and all other players receive 26

        Parameter: self

        Return: None (This method only updates the score if necessary)
        """

        for player in self.players:  # the while loop runs through every player in the players list
            if player.round_score == 26:  # the if statement checks for player who has reached a score of 26 and when the condition is met, the print statement in the following line is executed.
                print(f"{player} has shot the mooon! Everyone else receives 26 points")
                print("")
                for play in self.players:  # the child loop runs through every player in the players list to update the players round score where the moon shooter gets 0 points and the rest get 26 points.
                    if play == player:
                        play.round_score = 0
                    else:
                        play.round_score = 26
                break

    def while_loop_condition_check(self):
        """
        Use a for loop to find the max_score of all players and update self.max_score
        use for loop to find the min_score and then another for loop to find the num_of_min_score

        Parameter: self (Only need the self.players list to find the player with lowest total score)

        Return: None
        """
        for player in self.players:  # finds the max total score after each rounds (to terminate or continue the loop)
            if player.total_score > self.max_score:
                self.max_score = player.total_score

        min_score = self.players[0].total_score  # Both for loops is used to check if there is more than one same min score (to terminate or continue the loop)
        for player in self.players:
            if player.total_score < min_score:
                min_score = player.total_score  # Stores the minimum score of player to num_of_min_score

        self.num_of_min_score = 0
        for player in self.players:
            if player.total_score == min_score:
                self.num_of_min_score += 1  # finds the number of players that has the same num_of_min_score


    def find_winner(self):
        """
        Use a for loop to find the player with the lowest total score
        If Human player won, print Congrats message
        If Human player lost, print You Lost message

        Parameter: self (Only need the self.players list to find the player with lowest total score)

        Return: None
        """
        winner_score = self.players[0].total_score  # sets the winner_score and winning_player to the first player's and find the ultimate winner using for loop
        winning_player = self.players[0].name
        for player in self.players:
            if player.total_score < winner_score:  # updates the player's name and winning score for each loop to find the winner
                winner_score = player.total_score
                winning_player = player.name

        if self.players[0].name == winning_player:  # if Human player is the winner, prints the player is the winner
            print("Congratulations {} 👏".format(winning_player))
            print("You are the winner of this round 🤩")
        else:
            print(
                f"{winning_player} is the winner of this round!")  # if Human player is NOT the winner, prints the player is the lost and prints the winner name
            print(f"{self.players[0].name}, you lost the round 😔")


if __name__ == "__main__":
    name = Hearts()
