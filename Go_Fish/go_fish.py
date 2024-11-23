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

    def draw(self, num_cards = 1):
        drawn_cards = []
        for _ in range(num_cards):
            if not self.cards:
                raise ValueError("Cannot draw from an empty deck")
            drawn_cards.append(self.cards.pop())
        return drawn_cards


class Player:
    def __init__(self, name, hand=None):
        self.name = name
        self.hand = hand if hand is not None else []
        self.books = {}

    def give_cards(self, rank):
        cards_to_give = []
        remaining_hand = []
        for card in self.hand:
            if rank == card.rank:
                cards_to_give.append(card)

            else:
                remaining_hand.append(card)

        self.hand = remaining_hand
        if cards_to_give:
            return cards_to_give
        else:
            return False 

    def check_books(self):
        for rank in Card.VALID_RANKS:
            count = 0
            for card in self.hand:
                if card.rank == rank:
                    count += 1

            if count == 4:
                self.books[rank] = "complete"
                self.hand =[card for card in self.hand if card.rank != rank] 

    def check_hand(self):
        if not self.hand:
            return True
        return False
    
    def ask_for_card(self, rank, player):
        return player.give_cards(rank)

class Game():
    def __init__(self, num_players):
        self.deck = DeckofCards()
        self.deck.shuffle()
        self.players = []
        self.players = [Player(f"Player {i+1}") for i in range(num_players)] 

        if len(self.players) < 2:
            raise ValueError("There must be at least 2 players")
        
        if len(self.players) > 6:
            raise ValueError("There can be at most 6 players")
        
        if len(self.players) <3:
            for player in self.players:
                player.hand.extend(self.deck.draw(7)) 
        
        else:
            for player in self.players:
                player.hand.extend(self.deck.draw(5))

    def take_turn(self, player_1, player_2, rank):
        cards_to_give = player_1.ask_for_card(rank, player_2)
        if cards_to_give:
            player_1.hand.extend(cards_to_give)
            player_1.check_books()
            if not player_2.check_hand(): 
                if len(self.deck.cards) > 0:
                    if len(self.deck.cards) > 5:
                        player_2.hand.extend(self.deck.draw(5))
                    else:
                        player_2.hand.extend(self.deck.draw(len(self.deck.cards)))
                

            return True
        else:
            if len(self.deck.cards) > 0:
                player_1.hand.extend(self.deck.draw(1))
            player_1.check_books()
            return False

  

 
            







