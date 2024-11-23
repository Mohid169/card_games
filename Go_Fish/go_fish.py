import random


class Card:
    VALID_RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    VALID_SUITS = ["spade", "ace", "hearts", "clubs"]

    def __init__(self, suit, rank):
        if rank not in self.VALID_RANKS:
            raise ValueError(f"Invalid Rank")
        if suit not in self.VALID_SUITS:
            raise ValueError(f"Invalid Suit")

        self.suit = suit
        self.rank = rank

    def name(self):
        return f"{self.rank}{self.suit}"


class DeckofCards:
    def __init__(self):
        self.cards = []

        for suit in Card.VALID_SUITS:
            for rank in Card.VALID_RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            raise ValueError("Cannot draw from an empty deck")
        return self.cards.pop()


class Player:
    def __init__(self, name, hand=None):
        self.name = name
        self.hand = hand if hand is not None else []
        self.books = []

    def give_cards(self, rank):
        cards_to_give = []
        remaining_hand = []
        for card in self.hand:
            if rank == card.rank:
                cards_to_give.append(card)

            else:
                remaining_hand.append(card)

        self.hand = remaining_hand

        return cards_to_give

    def check_books(self):
        pass
