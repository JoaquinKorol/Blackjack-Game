from classes.card import Card
from random import choice, shuffle


class Deck:
    def __init__(self):
        # Initializing the deck with a set of cards
        self.cards = Card.get()

    def shuffle(self):
        # Shuffling the deck
        shuffle(self.cards)

    def deal(self, num_cards, hand):
        # Dealing a specified number of cards to a hand
        if num_cards > len(self.cards):
            print("Not enough cards in the deck.")
        else:
            for _ in range(num_cards):
                card = choice(self.cards)  # Selecting a random card
                hand.append(card)  # Adding the card to the hand
                self.cards.remove(card)  # Removing the card from the deck

    def calculate_hand_value(self, hand):
        # Calculating the total value of a hand
        hand_value = 0
        aces_count = 0

        for card in hand:
            hand_value += card.value  # Adding the card value to the hand value

            if card.num == "A":  # Checking for aces
                aces_count += 1

        # Adjusting ace values if the hand value exceeds 21
        while aces_count > 0 and hand_value > 21:
            hand_value -= 10  # Reducing an ace's value to 1
            aces_count -= 1

        return hand_value
