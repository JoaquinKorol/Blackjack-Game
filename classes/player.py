from classes.deck import Deck


class Player:
    def __init__(self, balance=2500):
        # Initializing player attributes
        self.hand = []  # Player's current hand of cards
        self.balance = balance  # Player's balance/amount of money
        self.total_bet = 0  # Total bet made by the player
        self.wins_displayed = (
            False  # Indicator if the player's wins have been displayed
        )

    def reset(self):
        # Resetting player attributes to default values
        self.hand = []  # Clearing the hand
        self.balance = self.balance  # Setting the balance back to the original value
        self.total_bet = 0  # Resetting total bet to zero
        self.wins_displayed = False  # Setting wins_displayed back to default

    def set_winnings_added(self, value):
        # Setting the value for winnings added
        self.winnings_added = value

    def bet(self, bet_amount):
        # Placing a bet
        if bet_amount > self.balance:
            print("Invalid bet. Bet is greater than balance.")
        else:
            self.balance -= bet_amount  # Deducting the bet from the balance
            self.total_bet += bet_amount  # Adding the bet to the total bet

    def get_hand(self, num_cards, deck):
        # Getting a specified number of cards from the deck and adding them to the player's hand
        deck.deal(num_cards, self.hand)

   
