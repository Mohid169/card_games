import pygame
import math
from go_fish import Game, Player, Card, DeckofCards


class CardSprite(pygame.sprite.Sprite):
    def __init__(self, card, x, y):
        super().__init__()
        self.card = card
        self.target_x = x
        self.target_y = y
        self.x = x
        self.y = y
        self.speed = 15
        self.moving = False

        # Create basic card surface
        self.image = self.create_default_card()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def create_default_card(self):
        # Create a basic card surface
        surface = pygame.Surface((71, 96))
        surface.fill((255, 255, 255))  # White background
        pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 2)  # Black border

        # Add rank
        font = pygame.font.Font(None, 36)
        rank_text = font.render(str(self.card.rank), True, (0, 0, 0))
        surface.blit(rank_text, (5, 5))

        # Add suit
        suit_text = font.render(str(self.card.suit), True, (0, 0, 0))
        surface.blit(suit_text, (5, 50))

        return surface

    def move_to(self, target_x, target_y):
        self.target_x = target_x
        self.target_y = target_y
        self.moving = True

    def update(self):
        if self.moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < self.speed:
                self.x = self.target_x
                self.y = self.target_y
                self.moving = False
            else:
                move_x = (dx / distance) * self.speed
                move_y = (dy / distance) * self.speed
                self.x += move_x
                self.y += move_y

            self.rect.x = int(self.x)
            self.rect.y = int(self.y)


class GameVisualizer:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Go Fish")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (34, 139, 34)
        self.BLUE = (0, 0, 255)

        # Font
        self.font = pygame.font.Font(None, 36)

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.card_sprites = {}  # Dictionary to track card sprites

        # Animation state
        self.animating = False

        # Message display
        self.message = ""
        self.message_timer = 0

        # Initialize card sprites
        self.initialize_card_sprites()

    def initialize_card_sprites(self):
        deck_x = self.width // 2
        deck_y = self.height // 2

        for player in self.game.players:
            for card in player.hand:
                sprite = CardSprite(card, deck_x, deck_y)
                self.card_sprites[card] = sprite
                self.all_sprites.add(sprite)

    def animate_card_movement(self, card, target_x, target_y):
        if card in self.card_sprites:
            sprite = self.card_sprites[card]
            sprite.move_to(target_x, target_y)
            return True
        return False

    def draw_player_hand(self, player, index):
        total_players = len(self.game.players)
        angle = (2 * math.pi * index) / total_players
        radius = 300

        center_x = self.width // 2
        center_y = self.height // 2

        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)

        # Draw player name
        name_text = self.font.render(player.name, True, self.BLACK)
        self.screen.blit(name_text, (x - 50, y - 30))

        # Update card positions
        for i, card in enumerate(player.hand):
            card_x = x + (i * 20) - (len(player.hand) * 10)
            card_y = y

            if card not in self.card_sprites:
                sprite = CardSprite(
                    card, self.width // 2, self.height // 2
                )  # Start from deck
                self.card_sprites[card] = sprite
                self.all_sprites.add(sprite)
                sprite.move_to(card_x, card_y)
            else:
                self.card_sprites[card].move_to(card_x, card_y)

        # Draw books
        books_text = self.font.render(f"Books: {len(player.books)}", True, self.BLUE)
        self.screen.blit(books_text, (x - 50, y + 100))

    def set_message(self, message):
        self.message = message
        self.message_timer = 60

    def draw(self):
        # Fill background
        self.screen.fill(self.GREEN)

        # Draw deck
        deck_text = self.font.render(
            f"Deck: {len(self.game.deck.cards)}", True, self.BLACK
        )
        self.screen.blit(deck_text, (self.width // 2 - 50, self.height // 2 - 20))

        # Update sprites
        self.all_sprites.update()

        # Draw all players
        for i, player in enumerate(self.game.players):
            self.draw_player_hand(player, i)

        # Draw sprites
        self.all_sprites.draw(self.screen)

        # Draw message
        if self.message_timer > 0:
            message_text = self.font.render(self.message, True, self.BLACK)
            self.screen.blit(message_text, (self.width // 2 - 100, 50))
            self.message_timer -= 1

        pygame.display.flip()

    def is_animating(self):
        return any(sprite.moving for sprite in self.all_sprites)


def play_visual_game():
    num_players = int(input("Enter number of players (2-6): "))
    game = Game(num_players)
    visualizer = GameVisualizer(game)

    clock = pygame.time.Clock()

    while not game.is_game_over():
        for current_player in game.players:
            # Handle pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Game logic
            if current_player.check_hand():
                if len(game.deck.cards) > 0:
                    cards_drawn = game.deck.draw(min(5, len(game.deck.cards)))
                    current_player.hand.extend(cards_drawn)
                    visualizer.set_message(
                        f"{current_player.name} draws {len(cards_drawn)} cards"
                    )

            opponent = game.choose_opponent(current_player)
            if opponent is None:
                continue

            rank_choice = game.choose_rank(current_player)
            if rank_choice is None:
                continue

            successful = game.take_turn(current_player, opponent, rank_choice)

            if successful:
                message = f"{current_player.name} got cards from {opponent.name}!"
            else:
                message = f"{current_player.name} goes fishing!"

            visualizer.set_message(message)

            # Wait for animations to complete
            while visualizer.is_animating():
                visualizer.draw()
                clock.tick(60)

            visualizer.draw()
            pygame.time.delay(1000)

    print("Game over!")
    game.display_winner()
    pygame.time.delay(3000)
    pygame.quit()


if __name__ == "__main__":
    play_visual_game()
