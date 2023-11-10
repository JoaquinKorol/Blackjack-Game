from classes.deck import Deck


class Croupier:
    def __init__(self):
        # Initializing the croupier's hand
        self.hand = []

    def reset(self):
        # Resetting the croupier's hand
        self.hand = []

    def get_hand(self, num_cards, deck):
        # Getting a specified number of cards from the deck for the croupier's hand
        deck.deal(num_cards, self.hand)

    def logic(self, deck):
        # Implementing the croupier's logic for the game
        while deck.calculate_hand_value(self.hand) <= 21:
            hand_value = deck.calculate_hand_value(self.hand)
            if hand_value >= 17:
                # Croupier stands when hand value is 17 or higher
                return "Stand", hand_value
            elif hand_value <= 16:
                self.get_hand(1, deck)  # Drawing another card for the croupier
                croupier_hand_value = deck.calculate_hand_value(self.hand)
                return croupier_hand_value  # Returning the new hand value

            return "Bust", hand_value  # Croupier busts if hand value exceeds 21
