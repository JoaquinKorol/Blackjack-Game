import os
import pygame

# List of suits and their corresponding values
suits = ["club", "Diamond", "Heart", "spade"]
numbers = [
    {"num": "A", "value": 11},
    {"num": "2", "value": 2},
    {"num": "3", "value": 3},
    {"num": "4", "value": 4},
    {"num": "5", "value": 5},
    {"num": "6", "value": 6},
    {"num": "7", "value": 7},
    {"num": "8", "value": 8},
    {"num": "9", "value": 9},
    {"num": "10", "value": 10},
    {"num": "J", "value": 10},
    {"num": "Q", "value": 10},
    {"num": "K", "value": 10},
]


class Card:
    IMAGE_DIRECTORY = "cards"

    def __init__(self, num, suit, value):
        # Initializing the card attributes
        self.num = num
        self.suit = suit
        self.value = value
        self.card = f"{num} of {suit} {value}"

    def __str__(self):
        return f"{self.card}"

    def get_image_path(self):
        # Getting the image path of the card
        image_filename = f"{self.suit}_{self.num}.png"
        image_path = os.path.join(Card.IMAGE_DIRECTORY, image_filename.replace("\\", "/"))
        return image_path

    @classmethod
    def get(cls):
        # Generating a list of cards with their suits and values
        cards = []
        for number in numbers:
            for suit in suits * 2:
                card = cls(number["num"], suit, number["value"])
                cards.append(card)
        return cards

    @classmethod
    def load_card_images(cls, cards):
        # Loading card images using Pygame
        card_images = []
        for card in cards:
            image_filename = f"{card.suit}_{card.num}.png"
            image_path = os.path.join(Card.IMAGE_DIRECTORY, image_filename)
            card_image = pygame.image.load(image_path)
            card_images.append(card_image)
        return card_images
