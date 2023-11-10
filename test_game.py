import pytest
from classes.player import Player
from classes.deck import Deck
from classes.croupier import Croupier

def test_initial_player_balance():
    player = Player()
    assert player.balance == 2500, "Player balance should be 2500 initially"

def test_player_bet():
    player = Player()
    initial_balance = player.balance
    bet_amount = 100
    player.bet(bet_amount)
    assert player.balance == initial_balance - bet_amount, "Player balance should decrease after a bet"

def test_deck_initialization():
    deck = Deck()
    assert len(deck.cards) == 104, "Deck should have 104 cards initially"