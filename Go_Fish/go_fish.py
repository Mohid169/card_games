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

    def draw(self, num_cards=1):
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
                self.hand = [card for card in self.hand if card.rank != rank]

    def check_hand(self):
        if not self.hand:
            return True
        return False

    def ask_for_card(self, rank, player):
        return player.give_cards(rank)


class Game:
    def __init__(self, num_players):
        self.deck = DeckofCards()
        self.deck.shuffle()
        self.players = []
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]

        if len(self.players) < 2:
            raise ValueError("There must be at least 2 players")

        if len(self.players) > 6:
            raise ValueError("There can be at most 6 players")

        if len(self.players) < 3:
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

    def is_game_over(self):
        if (
            all(player.check_hand() for player in self.players) and len(self.deck.cards)
            == 0
        ):
            return True
        return False

    def choose_opponent(self, current_player):
        opponents = [
            player
            for player in self.players
            if player != current_player and player.hand
        ]
        if not opponents:
            return None  # Skip to the next player's turn
        return random.choice(opponents)

    def choose_rank(self, player):
        if player.check_hand():
            return None
        good_ranks = [card.rank for card in player.hand]
        return random.choice(good_ranks)

    def play(self):
        while not self.is_game_over():
            for current_player in self.players:
                if current_player.check_hand():
                    if len(self.deck.cards) > 0:
                        if len(self.deck.cards) > 5:
                            current_player.hand.extend(self.deck.draw(5))
                        else:
                            current_player.hand.extend(self.deck.draw(len(self.deck.cards)))

                opponent = self.choose_opponent(current_player)
                if opponent is None:
                    continue
                rank_choice = self.choose_rank(current_player)
                if rank_choice is None:
                    continue
                successful = self.take_turn(current_player, opponent, rank_choice)
                if successful:
                    print(f"{current_player.name} got cards from {opponent.name}!")
                else:
                    print(f"{current_player.name} goes fishing and draws a card.")
        print("game over")
        self.display_winner()

    def display_winner(self):
        scores = {player.name: len(player.books) for player in self.players}
        winner = max(scores, key=scores.get)
        print("Game Results:")
        for player, score in scores.items():
            print(f"{player}: {score} books")   
        print(f"The winner is {winner}!")

if __name__ == "__main__":
    num_players = int(input("Enter number of players (2-6): "))
    game = Game(num_players)
    game.play()
