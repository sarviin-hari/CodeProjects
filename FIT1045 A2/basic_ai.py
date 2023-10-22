from __future__ import annotations
from cards import Card
from player import Player


class BasicAIPlayer(Player):
    """
    This class deals with the basic AI player (computer) who will play against the player
    """

    def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:
        """
        This function deals with playing a card_in_hand

        Parameter: trick (has the cards that has been played by each player before its the turn of this player)
                   broken_hearts (if true, hearts have been broken -> hearts has been played)

        Return: card_in_hand that can be played by Basic AI
        """
        sorted_hand_list = sorted(self.hand)                        # sorts the hand of cards in increasing order of suits, then ranks
        for card_in_hand in sorted_hand_list:                                  # for each card_in_hand in the sorted hand
            if self.check_valid_play(card_in_hand, trick, broken_hearts)[0]:   # calls check_valid_play for validity check
                self.hand.remove(card_in_hand)                                 # removes the card_in_hand from player's hand
                return card_in_hand

    def pass_cards(self) -> list[Card]:
        """
        This function deals with passing the 3 cards at the beginning of each round.

        Parameter: self

        Return: list of 3 cards to pass
        """
        index = len(self.hand) - 3                                  # less by 3 cards (have been passed)
        sorted_hand_list = sorted(self.hand)                        # sorts the current hand
        card_to_remove = sorted_hand_list[index:]
        for index in range(len(card_to_remove)):
            self.hand.remove(card_to_remove[index])                     # removes the card from the hand

        return card_to_remove
