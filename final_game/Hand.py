from time import sleep
from game_functions import special_cards
from WinnerScreenModule import win_game
from game_functions import winner
from GameOverScreenModule import lose_game
from random import choice


class Hand:
    """ Class for a player's hand object. """
    def __init__(self, player_number, deck, screen):
        # This is "Player 1" or "Player 2" for example
        self.player_number = player_number
        self.screen = screen
        # This is a list of Card objects to represent the cards in a players hand
        self.drawn_cards = []
        self.deck = deck
        self.score = 0

    def draw_cards(self, deck, number_of_cards):
        """ Removes x Card objects from the main deck and adds it to the hand. Where x = number of cards. """
        for _ in range(number_of_cards):
            self.drawn_cards.append(deck.deck.pop(-1))

    def draw_discard(self, deck, number_of_cards):
        """ Removes a Card object from the discard pile and adds it to the player hand.
            This function is here for testing purposes only. """
        for _ in range(number_of_cards):
            self.drawn_cards.append(deck.discard_pile.pop(-1))

    def display_hand(self, game):
        """ Function to display the players Hand on the screen. """
        # Dictionary to store the position based on player number
        player_position = {"Player 1": "bottom", "Player 2": "right", "Player 3": "top", "Player 4": "left"}
        # Calculates the required x position for the first card in the hand. (1/2 screen_width - 1/2 total_hand_width)
        card_x = self.screen.get_width()/2 - (
                    ((len(self.drawn_cards) + 1) / 2) * self.drawn_cards[0].rect.width / 2)
        # Calculates the required y position for the first card in the hand. (1/2 screen_height - 1/2 total_hand_height)
        card_y = self.screen.get_height() / 2 - (
                ((len(self.drawn_cards) + 1) / 2) * self.drawn_cards[0].rect.height / 2)
        # Adjusts x and y coordinates based on hand locations
        if player_position[self.player_number] == "bottom":
            front_or_back = "front"
            card_y = self.screen.get_height() - 50 - self.drawn_cards[0].rect.height
        elif player_position[self.player_number] == "top":
            front_or_back = "back"
            card_y = 50
        # For the left and right positions, the rotate_card function is called
        elif player_position[self.player_number] == "left":
            front_or_back = "back"
            [card.rotate_card(90) for card in self.drawn_cards]
            card_x = 50
        elif player_position[self.player_number] == "right":
            front_or_back = "back"
            [card.rotate_card(270) for card in self.drawn_cards]
            card_x = self.screen.get_width() - 50 - self.drawn_cards[0].rect.width

        # Loops over the hand and displays each card on the screen
        for card in self.drawn_cards:
            card.display_card(front_or_back, card_x, card_y)
            if player_position[self.player_number] in ["bottom", "top"]:
                card_x += card.rect.width/2
            elif player_position[self.player_number] in ["right", "left"]:
                card_y += card.rect.height/2

    def play_card(self, card, deck, game, screen):
        """ Function which takes a card from the player hand and adds it to the discard pile
            and control the logic to advance a turn, and reset playable cards. """
        global have_winner
        # Check if the selected card is playable
        if card.card_playable:
            # Remove the card from the hand, and add it to the discard pile (leftCards)
            self.drawn_cards.remove(card)
            deck.discard_pile.append(card)
            # Check if player's hand is empty, if so they win and the game ends. THIS IS WHERE GAMEOVER MENU IS NEEDED.
            if winner(game.players, game.current_turn):
                if game.current_turn == 0:
                    win_game(screen, game)
                else:
                    lose_game(screen, game)
            # Reset the played card to unplayable
            card.reset_card_playable()
            # Update the card on top of the discard pile
            game.update_current_card()
            # Check if a wild card has been played, if so run the select colour function
            if game.current_card.colour == "wild":
                if game.current_card.number == "SP":
                    game.game_direction = choice([1, -1])
                    game.current_card.colour = "wild" + choice(["red", "blue", "green", "yellow"])
                else:
                    game.select_colour(screen, game, deck)
            # Check if a special card has been played and special card action
            special_cards(screen, game, deck)
            # Finally, advance the current turn to the next player
            game.advance_turn()
            # Loop through the player hand and reset all the cards to not playable
            [c.reset_card_playable() for c in self.drawn_cards]

    def swap_first_card(self, card, deck):
        """ Function for the extended rule, swaps a card from player hand and puts it to the bottom of the deck """
        self.drawn_cards.remove(card)
        card.reset_card_display()
        sleep(1)
        deck.discard_pile.insert(0, card)
        self.draw_cards(deck, 1)

    def get_score(self):
        for card in self.drawn_cards:
            if card.colour == 'wild':
                self.score += 25
            elif card.number in ['+2', 'S', 'R']:
                self.score += 10
            else:
                self.score += int(card.number)


