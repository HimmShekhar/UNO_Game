from Hand import *
from Deck import *
from ColourSelectButton import ColourSelectButton
from game_functions import canPlayCard, check_events, special_cards, updatePlayableCards, bot_play_card, \
    check_colour_quantity_play
import MainMenuScreenModule
from time import sleep
from random import choice


class GameState:
    """ A Class to initiate and store the game variables. The number of players needs to be  """
    # number of players needs to be 1 + computer players.
    def __init__(self, number_of_players, deck, screen):
        self.number_of_players = number_of_players
        self.deck = deck
        # Creates a list of Hand class objects for the number of players
        self.players = [Hand(f"Player {i}", self.deck, screen) for i in range(1, number_of_players+1)]
        # Deals the cards to each player hand
        [x.draw_cards(deck, 7) for x in self.players]
        # By default, the game starts on turn 0, and direction 1 (forwards)
        self.current_turn = 0
        self.game_direction = 1
        # If game is running:
        self.game = True
        self.current_card = None
        # Variable to track the extended rule of swapping a card before each turn
        self.swapped_card = False
        self.start = 1

        # Create Colour Select Button objects for when a wild card is played
        colours = ["red", "blue", "green", "yellow"]
        self.buttons = [ColourSelectButton(colour, screen) for colour in colours]

    def update_current_card(self):
        """ In place method to update the current card in play - the top card in the discard pile. """
        if len(self.deck.discard_pile) > 0:
            self.current_card = self.deck.discard_pile[-1]

    def advance_turn(self):
        """ Advances the current turn depending on game direction. """
        if self.game_direction == 1:
            if self.current_turn == self.number_of_players-1:
                self.current_turn = 0
            else:
                self.current_turn += 1

        elif self.game_direction == -1:
            if self.current_turn == 0:
                self.current_turn = self.number_of_players - 1
            else:
                self.current_turn -= 1
        # Reset swap card variable following every turn
        self.swapped_card = False

    def get_next_player(self):
        """ Function to return the index of the next player. For use with +2 and +4. """
        if self.game_direction == 1:
            if self.current_turn == self.number_of_players-1:
                next_player = 0
            else:
                next_player = self.current_turn + 1

        elif self.game_direction == -1:
            if self.current_turn == 0:
                next_player = self.number_of_players - 1
            else:
                next_player = self.current_turn - 1
        return next_player

    def reverse_direction(self):
        """ In place method to reverse the game direction. """
        self.game_direction *= -1


    def select_colour(self, screen, game, deck):
        """ Function to display the colour selection buttons following a wild card. """
        # Approximate button size
        radius = 35
        # Calculate center of button coordinates based on screen width and height
        circle_x = screen.get_width() / 2 - 3 * radius - 50
        circle_y = screen.get_height() - 250

        # Only draw the buttons when the player is choosing a colour
        if game.current_turn == 0:
            # Pause the main game loop while the player chooses a colour
            waiting = True
            # For each button in the list of Button objects, draw the button to the screen
            for button in self.buttons:
                button.display_button(circle_x, circle_y)
                pygame.display.flip()
                circle_x += radius + 50

            while waiting:
                # Wait for player to select a colour - check_events adjusts the colour of the wild card when clicked
                check_events(screen, self.players[game.current_turn], deck, game)
                # Update the centre card to display and update the colour
                game.update_current_card()
                # Set waiting to False when the wild card colour is updated
                if game.current_card.colour in ["wildred", "wildyellow", "wildblue", "wildgreen"]:
                    waiting = False
        else:
            # The bot will randomly pick a colour
            if game.current_card.number != "SP":
                game.current_card.colour = "wild" + check_colour_quantity_play(game)
                game.update_current_card()
            else:
                game.current_card.colour = "wild" + choice(["red","blue","green","yellow"])


def show_avatar(player, game):
    """ Function to show the player avatar. """
    # player1
    if (game.current_turn + 1 == 1):
        if not game.swapped_card:
            image = pygame.image.load(f"images/tip2.png")
        else:
            image = pygame.image.load(f"images/tip1.png")
        player.screen.blit(image, (450, 480))
        image = pygame.image.load(f"images/tx1_dark.png")
        player.screen.blit(image, (905, 330))
        image = pygame.image.load(f"images/tx2_dark.png")
        player.screen.blit(image, (540, 155))
        image = pygame.image.load(f"images/tx3_dark.png")
        player.screen.blit(image, (155, 330))
    # player2
    if(game.current_turn + 1 == 2):
        image = pygame.image.load(f"images/tx1.png")
        player.screen.blit(image, (905, 330))
        image = pygame.image.load(f"images/tx2_dark.png")
        player.screen.blit(image, (540, 155))
        image = pygame.image.load(f"images/tx3_dark.png")
        player.screen.blit(image, (155, 330))
    # player3
    if (game.current_turn + 1 == 3):
        image = pygame.image.load(f"images/tx1_dark.png")
        player.screen.blit(image, (905, 330))
        image = pygame.image.load(f"images/tx2.png")
        player.screen.blit(image, (540, 155))
        image = pygame.image.load(f"images/tx3_dark.png")
        player.screen.blit(image, (155, 330))
    # player4
    if (game.current_turn + 1 == 4):
        image = pygame.image.load(f"images/tx1_dark.png")
        player.screen.blit(image, (905, 330))
        image = pygame.image.load(f"images/tx2_dark.png")
        player.screen.blit(image, (540, 155))
        image = pygame.image.load(f"images/tx3.png")
        player.screen.blit(image, (155, 330))

def update_display(screen,game,deck,background):
    """ Function to update the displayed objects """
    screen.blit(background, (0, 0))
    # Display the deck and discard pile
    deck.display_deck(game)
    # Display hands for all players
    for player in game.players:
        player.display_hand(game)
 # ------------------------------------动画， update animation, show avatar
    show_avatar(player, game)
    pygame.display.flip()

have_winner = False

def main():
    # Initialise the game and screen
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Uno")
    # Run main menu function
    MainMenuScreenModule.main_menu(screen)
    # Load the background
    bg = pygame.image.load("images/background.png")

    # Build the deck and shuffle the deck
    main_deck = Deck(screen)
    main_deck.build_deck()
    main_deck.shuffle_cards()

    # Set the Game variables and set the running variable to True
    # GameState is (Number of players, Deck being used, screen)
    game = GameState(4, main_deck, screen)
    # Update the starting discard pile
    game.update_current_card()
    # Variable to allow a special card to start the game
    # start = 1

    while game.game:
        """ Main game loop. """
        # Checks length of deck need to do this before events
        if len(main_deck.deck) <= 4:
            main_deck.reset_deck()
            main_deck.shuffle_cards()
            updatePlayableCards(game.current_card, game.players, game.current_turn)
            print("Deck reset")

        # Update screen and display
        update_display(screen, game, main_deck, bg)
        updatePlayableCards(game.current_card, game.players, game.current_turn)
        if game.start:
            # Checks if the first card is a special card and does the action, then sets start to 0
            special_cards(screen, game, main_deck)
            updatePlayableCards(game.current_card, game.players, game.current_turn)
            game.start = 0

        print(f"Player {game.current_turn + 1}") # This is a good place to call the label to indicate who's turn it is
        # If the player is Player 1
        if game.current_turn == 0:
            # Checks for the extended rule - if a card has been swapped
            while not game.swapped_card:
                # Waits for the player to select a card to swap, and updates the display
                check_events(screen, game.players[0], main_deck, game)
                update_display(screen, game, main_deck, bg)
            # Updates which cards in the players hand are playable
            updatePlayableCards(game.current_card, game.players, game.current_turn)
            update_display(screen, game, main_deck, bg)
            # While it is Player 1's turn
            while game.current_turn == 0:
                # If there is a playable card, wait for player 1 to play
                if canPlayCard(game.current_card, game.players, game.current_turn):
                    check_events(screen, game.players[0], main_deck, game)
                # Else wait for player 1 to draw a card
                else:
                    check_events(screen, game.players[0], main_deck, game)
            update_display(screen, game, main_deck, bg)
            updatePlayableCards(game.current_card, game.players, game.current_turn)
        # If the player is a bot (Player 2 - 4)
        elif game.current_turn != 0:
            # Update the playable cards in the bots hand
            updatePlayableCards(game.current_card, game.players, game.current_turn)
            # Bot takes its turn
            bot_play_card(main_deck, game, screen)
            update_display(screen, game, main_deck, bg)


main()












