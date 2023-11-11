import pytest
from classes.player import Player
from classes.deck import Deck
from classes.croupier import Croupier
from classes.card import Card

# Test initial player balance
def test_initial_player_balance():
    player = Player()
    assert player.balance == 2500, "Player balance should be 2500 initially"

# Test player betting functionality
def test_player_bet():
    player = Player()
    initial_balance = player.balance
    bet_amount = 100
    player.bet(bet_amount)
    assert player.balance == initial_balance - bet_amount, "Player balance should decrease after a bet"

# Test deck initialization
def test_deck_initialization():
    deck = Deck()
    assert len(deck.cards) == 104, "Deck should have 104 cards initially"

# Test card dealing logic
def test_card_dealing():
    deck = Deck()
    player = Player()
    croupier = Croupier()

    player.get_hand(2, deck)
    croupier.get_hand(2, deck)

    assert len(player.hand) == 2, "Player should have 2 cards after dealing"
    assert len(croupier.hand) == 2, "Croupier should have 2 cards after dealing"
    assert len(deck.cards) == 100, "Deck should have 100 cards remaining after dealing"

# Test win/lose conditions
def test_win_lose_conditions(value):
    player = Player()
    croupier = Croupier()
    deck = Deck()

    # Player and croupier hands to simulate win/lose conditions
    player.hand = [Card('A', 'Hearts'), Card(10, 'Spades')]
    croupier.hand = [Card(9, 'Diamonds'), Card(8, 'Clubs'), Card(7, 'Hearts')]

    assert deck.calculate_hand_value(player.hand) == 21, "Player should have 21 points"
    assert deck.calculate_hand_value(croupier.hand) == 24, "Croupier should have busted"

    # Player wins when the croupier busts or player's hand is greater
    assert deck.calculate_hand_value(player.hand) > deck.calculate_hand_value(croupier.hand), "Player should win"

# Test chip handling
def test_chip_selection_and_betting():
    player = Player()
    player.balance = 500
    chip_values = [1, 10, 100, 500]

    bet_amount = 100
    player.bet(bet_amount)
    assert player.total_bet == bet_amount, "Player should have bet the specified amount"
    assert player.balance == 400, "Player's balance should decrease after betting"

    # Testing chip selection logic
    for chip_value in chip_values:
        player.bet(chip_value)
        assert player.total_bet == bet_amount + chip_value, "Player should add the selected chip value to the bet"


