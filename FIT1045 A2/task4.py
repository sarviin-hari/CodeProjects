from __future__ import annotations

import random

from cards import Card, Rank, Suit
from basic_ai import BasicAIPlayer
from task3 import Round             # Round is imported from task3.py since the codes in the original round.py file is altered to run Task 6(round.py, hearts.py)


class Hearts:
    """
    This class creates an object that prompts for two inputs upon initialisation, which are
        a target score to end the game, and
        desired number of players (3-5) for the game
    Runs the game (class Round) and updates the player name and score and finds the winner at the end of the game
    """

    def __init__(self) -> None:
        """
        This function initialises 4 instance variables which are
            self.start_index that helps to determine and rearrange the passing order of cards from one player to another before every round begins
            self.max_score stores the maximum score obtained among all players until current round, and serves as a comparison variable to determine if target score is met, thus end the game.
            self.num_of_min_score acts as a counter that checks if there's a tie between players with the lowest score and decides if another round is necessary to break the tie.
            self.round_num represent the number of round in a game

            The game then is begun by calling the self.target_score_input() method to get the target score to end game from user and return a validated input
            Followed by the calling of sel.num_of_players_input() method to get the desired number of players from user and return a validated input.
        """

        self.start_index = 0  # used to find the start index of the player that starts the round
        self.max_score = 0  # stores the max_score to find when to terminate the loop
        self.min_score = 1  # stores the num_of_min_score to check if two players have the same minimum score
        self.round_num = 1  # to store the round_num

        self.target_score = self.target_score_input()  # call self.target_score_input() to validate an input and returns once the input is valid
        self.num_of_players = self.num_of_players_input()  # call self.num_of_players_input() to validate an input and returns once the input is valid

        self.players = self.find_player_list()  # call self.find_player_list(self.num_of_players) to get the player list based on the num of players

        # while loop runs as long as max_score of the round is still less than target_score OR if there is two minimum total_score
        while self.max_score < self.target_score or self.min_score > 1:

            print(f"========= Starting round {self.round_num} =========")

            bool_val = self.get_correct_suit()              # get the player.hand for each players and checks if all the suits are valid, if valid return True, else return False

            while bool_val == False:                        # while loop runs to reshuffle the suits as long as one player does not have at least one card that isn't the Queen of Spades or from Hearts
                for player in self.players:
                    player.hand = []
                bool_val = self.get_correct_suit()

            for player in self.players:                     # prints the cards in hand of each player
                print(f"{player} was dealt {player.hand}")

            if self.round_num % self.num_of_players != 0:   # pass cards only if the round_number is not divisible by number of players
                pass_card_list = self.pass_card()
                self.passing_card(pass_card_list)

            Round(self.players)                             # plays the round by calling the Round class with the parameter self.players

            self.round_score_26_check()                     # checks if anyone shoots the moon, if yes, changes the round_score accordingly

            print(f"========= End of round {self.round_num} =========")

            for player in self.players:                     # updates total score and prints the total score of each player
                player.total_score += player.round_score
                print(f"{player}'s total score: {player.total_score}")
                player.round_score = 0                      # sets the round score of each player to 0

            for player in self.players:                     # finds the max total score after each rounds (to terminate or continue the loop)
                if player.total_score > self.max_score:
                    self.max_score = player.total_score

            min_score = self.players[0].total_score         # Both for loops is used to check if there is more than one same min score (to terminate or continue the loop)
            for player in self.players:
                if player.total_score < min_score:
                    min_score = player.total_score          # Stores the minimum score of player to num_of_min_score

            self.min_score = 0
            for player in self.players:
                if player.total_score == min_score:
                    self.min_score += 1                     # finds the number of players that has the same num_of_min_score

            self.round_num += 1                             # Increments the self.round_num by 1

        ##### End of while loop #####

        winner_score = self.players[0].total_score          # sets the winner_score and winning_player to the first player's and find the ultimate winner using for loop
        winning_player = self.players[0].name
        for player in self.players:
            if player.total_score < winner_score:           # updates the player's name and winning score for each loop to find the winner
                winner_score = player.total_score
                winning_player = player.name

        print(f"{winning_player} is the winner!")  # print the winner name

    ########################################################################################################################
    def pass_card(self):
        """
        This function gets a list containing three cards to be passed by each player based on the player type.

        Parameter: self

        Return: pass_card_list (List of 3 cards to pass)
        """
        pass_card_list = []
        for player in self.players:
            card_list = player.pass_cards()  # calls the pass card from the respective class of the player to get the list of card to pass
            pass_card_list.append(card_list)  # stores the list of cards to pass in pass_card_list

        return pass_card_list  # returns pass_card_list

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
                for play in self.players:  # the child loop runs through every player in the players list to update the players round score where the moon shooter gets 0 points and the rest get 26 points.
                    if play == player:
                        play.round_score = 0
                    else:
                        play.round_score = 26
                break

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

    def find_player_list(self):  # Gets the player list for num_of_players 3, 4, 5 respectively
        """
        This function creates a players list based on the input entered by the user for number of players.

        Parameter: self

        Return: The function returns the created players list.
        """
        if self.num_of_players == 3:
            players = [BasicAIPlayer("Player 1"), BasicAIPlayer("Player 2"), BasicAIPlayer("Player 3")]
        elif self.num_of_players == 4:
            players = [BasicAIPlayer("Player 1"), BasicAIPlayer("Player 2"), BasicAIPlayer("Player 3"),
                       BasicAIPlayer("Player 4")]
        else:
            players = [BasicAIPlayer("Player 1"), BasicAIPlayer("Player 2"), BasicAIPlayer("Player 3"),
                       BasicAIPlayer("Player 4"), BasicAIPlayer("Player 5")]

        return players

    def passing_card(self, pass_card_list):
        """
        This function determines the order in which cards are passed from one player to another based on the round number
        It passes the cards correctly to each respective players

        Parameter: pass_card_list that has the list of cards to pass

        Return: None
        """

        start_index = self.round_num % self.num_of_players  # start_index represents the index of the corresponding player in the players list who leads the order
        passing_order = self.players[self.round_num % self.num_of_players:] + self.players[:self.round_num % self.num_of_players]  # Rearrange the order of pass

        for player_index in range(len(self.players)):
            print(f"{self.players[player_index]} passed {pass_card_list[player_index]} to {passing_order[player_index]}")  # The print statement is executed before every round to state to whom did every player passed their cards to

            for j in range(len(pass_card_list[0])):  # All the passed cards in an inner list at the given index of the outer list is added to the other player's hand based on the passing order
                self.players[start_index].hand.append(pass_card_list[player_index][j])

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


if __name__ == "__main__":
    name = Hearts()
