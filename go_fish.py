class Card():
    VALID_RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
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
    

class DeckofCards():
    def __init__(self):
        self.cards = []

        for suit in Card.VALID_SUITS:
            for rank in Card.VALID_RANKS:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self):
        pass

    def draw(self):
        if self.cards:
            return self.cards.pop()
        else:
            return print("There are no cards left!")