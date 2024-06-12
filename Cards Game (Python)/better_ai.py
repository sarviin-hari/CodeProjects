from __future__ import annotations
from cards import Card, Rank, Suit
from player import Player


class BetterAIPlayer(Player):
    """
    This class deals with the better AI player (computer) who will play against the player with a better strategy
    and a higher chance to win the game
    """

    def play_card(self, trick: list[Card], broken_hearts: bool) -> Card:
        """
        if len(trick) == 0,
            a. Try to play clubs and diamonds
            b. if cannot, try to play any smallest card possible
        if len(trick) != 0,
            a. If first trick is Clubs or Diamonds try to play Queen or King or Ace of Spades
            b. If first trick is Hearts or Spades try to play the smallest card possible

        Parameter: trick (has the cards that has been played by each player before its the turn of this player)
                   broken_hearts (if true, hearts have been broken -> hearts has been played)

        Return: card that can be played by Better AI
        """

        sorted_hand = sorted(self.hand)     # sort the hands in ASC and store in sorted_hand

        heart = 0                           # declare and initialize heart, spade, diamond, and club and their respective lists
        spade = 0
        diamond = 0
        club = 0
        heart_list = []
        spade_list = []
        diamond_list = []
        club_list = []

        for card in self.hand:                 # updates heart, spade, diamond, and club and their respective lists based on the cards in hand
            if card.suit.name == "Hearts":
                heart_list.append(card)
                heart += 1
            elif card.suit.name == "Spades":
                spade_list.append(card)
                spade += 1
            elif card.suit.name == "Diamonds":
                diamond_list.append(card)
                diamond += 1
            elif card.suit.name == "Clubs":
                club_list.append(card)
                club += 1

        if len(trick) == 0:  # If player leads the round,

            # if number of club <= number of diamond, try to play clubs. If you can't try to play diamonds.
            # if can play, remove the card from hand and return the card
            if club <= diamond:
                while len(club_list) > 0:
                    if self.check_valid_play(max(club_list), trick, broken_hearts)[0] == True:
                        self.hand.remove(max(club_list))
                        return max(club_list)
                    club_list.remove(max(club_list))
            else:
                while len(diamond_list) > 0:
                    if self.check_valid_play(max(diamond_list), trick, broken_hearts)[0] == True:
                        self.hand.remove(max(diamond_list))
                        return max(diamond_list)
                    diamond_list.remove(max(diamond_list))

            # Try to play any smallest card possible (the smallest spades or hearts)
            # if can play, remove the card from hand and return the card
            for smallest_card in sorted_hand:
                if self.check_valid_play(smallest_card, trick, broken_hearts)[0]:
                    self.hand.remove(smallest_card)
                    return smallest_card

        else:
            danger_diamonds = [Card(Rank.Queen, Suit.Spades), Card(Rank.King, Suit.Spades), Card(Rank.Ace, Suit.Spades)]

            # If first trick is clubs or diamonds,
            if trick[0].suit.name == "Clubs" or trick[0].suit.name == "Diamonds":

                # Try to play Queen or King or Ace of Spades if they are in the hand
                # if can play, remove the card from hand and return the card
                for danger_diamond_card in danger_diamonds:
                    if danger_diamond_card in spade_list:
                        if self.check_valid_play(danger_diamond_card, trick, broken_hearts)[0]:
                            self.hand.remove(danger_diamond_card)
                            return danger_diamond_card

                # Try to play the biggest hearts card possible (Given no Queen or King or Ace of Spades in hand)
                # if can play, remove the card from hand and return the card
                reverse_heart = sorted(heart_list, reverse=True)
                for heart_card in reverse_heart:
                    if self.check_valid_play(heart_card, trick, broken_hearts)[0]:
                        self.hand.remove(heart_card)
                        return heart_card

                # Try to play the biggest value card possible (Given no Queen or King or Ace of Spades or Hearts)
                # if can play, remove the card from hand and return the card
                reverse_hand = sorted(self.hand, reverse=True)
                for card in reverse_hand:
                    if self.check_valid_play(card, trick, broken_hearts)[0]:
                        self.hand.remove(card)
                        return card

            # If first trick is hearts or spades, try to play the smallest card possible
            # if can play, remove the card from hand and return the card
            if trick[0].suit.name == "Hearts" or trick[0].suit.name == "Spades":
                for smallest_card in sorted_hand:
                    if self.check_valid_play(smallest_card, trick, broken_hearts)[0]:
                        self.hand.remove(smallest_card)
                        return smallest_card

    def pass_cards(self) -> list[Card]:
        """
        Checks if Ace of Spades and King of Spades in hand.
        If yes, pass the cards and call the self.next_pass_card(card_to_pass) to get the next card to pass
            -> Tries to get rid of Hearts first followed by any high value cards

        Parameter: self as the instance variables from the Player class inherited by Better AI will be used

        Return: list of 3 cards to pass
        """

        card_to_pass = []  # List of cards to pass

        # If Ace of Spades and King of Spades in hand, remove both cards and call self.next_pass_card(card_to_pass)
        if Card(Rank.Ace, Suit.Spades) in self.hand and Card(Rank.King, Suit.Spades) in self.hand:
            card_to_pass.append(self.hand.pop(self.hand.index(Card(Rank.Ace, Suit.Spades))))
            card_to_pass.append(self.hand.pop(self.hand.index(Card(Rank.King, Suit.Spades))))

            self.next_pass_card(card_to_pass)

        # If Ace of Spades or King of Spades in hand, remove the respective card and call self.next_pass_card(card_to_pass) twice
        elif Card(Rank.Ace, Suit.Spades) in self.hand or Card(Rank.King, Suit.Spades) in self.hand:
            if Card(Rank.Ace, Suit.Spades) in self.hand:
                card_to_pass.append(self.hand.pop(self.hand.index(Card(Rank.Ace, Suit.Spades))))
            else:
                card_to_pass.append(self.hand.pop(self.hand.index(Card(Rank.King, Suit.Spades))))

            for _ in range(2):
                self.next_pass_card(card_to_pass)

        # If Ace of Spades and King of Spades not in hand, call self.next_pass_card(card_to_pass) 3 times
        else:
            for _ in range(3):
                self.next_pass_card(card_to_pass)

        return card_to_pass  # return, list of card to pass

    def next_pass_card(self, card_to_pass):
        """
        Checks the number of heart, spade, diamond and club in the hand and store in lists respectively
        Try to pass high value hearts, diamonds, clubs in that order. If not possible, try to pass any high value cards
        Always try to keep Queen of Spades

        Parameter: card_to_pass list so that it can be updated (since list is a reference variable any update in this method updates the card_to_pass in pass_card as well)

        Return: None as the card_to_pass list is updated automatically from this method
        """

        sorted_hand = sorted(self.hand)     # sort the hands in ASC and store in sorted_hand

        heart = 0                           # declare and initialize heart, spade, diamond, and club and their respective lists
        spade = 0
        diamond = 0
        club = 0
        heart_list = []
        spade_list = []
        diamond_list = []
        club_list = []

        for card in self.hand:                 # updates heart, spade, diamond, and club and their respective lists based on the cards in hand
            if card.suit.name == "Hearts":
                heart_list.append(card)
                heart += 1
            elif card.suit.name == "Spades":
                spade_list.append(card)
                spade += 1
            elif card.suit.name == "Diamonds":
                diamond_list.append(card)
                diamond += 1
            elif card.suit.name == "Clubs":
                club_list.append(card)
                club += 1

        # if hearts in hand, pass the hearts card and update heart, heart_list and card_to_pass
        if heart >= 1:
            max_heart = max(heart_list)
            card_to_pass.append(self.hand.pop(self.hand.index(max_heart)))
            heart_list.remove(max_heart)
            heart -= 1
        else:
            # if diamonds in hand, pass the hearts card and update diamond, diamond_list and card_to_pass
            if diamond >= 1:
                max_diamond = max(diamond_list)
                card_to_pass.append(self.hand.pop(self.hand.index(max_diamond)))
                diamond_list.remove(max_diamond)
                diamond -= 1

            # if clubs in hand, pass the hearts card and update club, club_list and card_to_pass
            elif club >= 1:
                max_club = max(club_list)
                card_to_pass.append(self.hand.pop(self.hand.index(max_club)))
                club_list.remove(max_club)
                club -= 1

            # else, pass any high value card, except Queen of Spades
            else:
                if Card(Rank.Queen, Suit.Spades) in sorted_hand:
                    sorted_hand.remove(Card(Rank.Queen, Suit.Spades))
                    spade -= 1
                card_to_pass.append(max(sorted_hand))


if __name__ == "__main__":
    player = BetterAIPlayer("Better_AI")

    player.hand.append(Card(Rank.Four, Suit.Clubs))
    # player.hand.append(Card(Rank.Ace, Suit.Hearts))
    # player.hand.append(Card(Rank.King, Suit.Spades))
    player.hand.append(Card(Rank.Ten, Suit.Diamonds))
    player.hand.append(Card(Rank.Four, Suit.Diamonds))
    # player.hand.append(Card(Rank.Ace, Suit.Spades))
    # player.hand.append(Card(Rank.King, Suit.Hearts))
    player.hand.append(Card(Rank.Ten, Suit.Clubs))
    player.hand.append(Card(Rank.Five, Suit.Clubs))
    # player.hand.append(Card(Rank.Three, Suit.Hearts))
    # player.hand.append(Card(Rank.Queen, Suit.Diamonds))
    player.hand.append(Card(Rank.Two, Suit.Spades))
    # player.hand.append(Card(Rank.Three, Suit.Clubs))

    print(player.pass_cards())

    # print(player.play_card(trick=[Card(Rank.Ten, Suit.Clubs)], broken_hearts=False))


