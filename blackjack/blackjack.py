import random


class Card:
    VALID_RANKS = [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "ace",
        "jack",
        "queen",
        "king",
    ]
    VALID_SUITS = ["clubs", "spade", "ace", "hearts"]

    def __init__(self, rank, suit):
        if rank not in self.VALID_RANKS:
            raise ("invalid rank")

        if rank not in self.VALID_SUITs:
            raise ("invalid suit")

        self.rank = rank
        self.suit = suit

    def name(self):
        return f"{self.rank, self.suit}"


class DeckOfCards:
    def __init__(self):
        self.cards = []

        for rank in Card.VALID_RANKS:
            for suit in Card.VALID_SUITS:
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, num_cards=1):
        drawn_cards = []
        for _ in range(num_cards):
            if not self.cards:
                print("deck is empty")
                return []

            drawn_cards.append(self.cards.pop())

        return drawn_cards


class Player:
    def __init__(self, name, hand=None):
        self.name = name
        self.hand = []

    pass


class Game:
    pass
