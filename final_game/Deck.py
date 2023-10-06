from Card import *
from random import shuffle


class Deck:
    """ Deck class to deal with a lists of Card objects to represent the game deck
        and store Deck functions. """
    def __init__(self, screen):
        # Empty list to be filled with Card objects
        self.deck = []
        self.screen = screen
        # Empty List to represent the discard pile
        self.discard_pile = []
        # Sets the positions of the Deck on the screen
        self.center_x = self.screen.get_width() / 2
        self.center_y = self.screen.get_height() / 2
        self.deck_x = self.center_x - 100 - 20
        self.deck_y = self.center_y - 110 / 2
        # Sets the positions of the discard pile on the screen
        self.discard_x = self.center_x + 20
        self.discard_y = self.center_y - 110 / 2

    def build_deck(self):
        """ Builds the standard deck of 112 Card objects. """
        colours = ['red', 'yellow', 'blue', 'green']
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+2', 'S', 'R']
        # Add a card object for each colour and number to the deck
        for colour in colours:
            for num in numbers:
                self.deck.append(Card(colour, num, self.screen))
                if num != 0:
                    self.deck.append(Card(colour, num, self.screen))
        # Add 4 of each wild card to the deck
        for _ in range(4):
            self.deck.append(Card("wild", "+4", self.screen))
            self.deck.append(Card("wild", "CC", self.screen))
            self.deck.append(Card("wild", "SP", self.screen))

    def shuffle_cards(self):
        """ Shuffles the list of Card objects "randomly". """
        shuffle(self.deck)
        self.discard_pile.append(self.deck.pop(-1))

    def display_deck(self,game):
        """ Function to display the deck in the center of the screen. """
        for card in self.deck:
            card.display_card("back", self.deck_x, self.deck_y)
         #show turn image
        if (game.game_direction == 1):
            self.image = pygame.image.load(f"images/left-1.png")
            self.screen.blit(self.image, (self.deck_x - 200, 280))
            self.image = pygame.image.load(f"images/right-1.png")
            self.screen.blit(self.image, (self.deck_x + 280, 280))
        if (game.game_direction == -1):
            self.image = pygame.image.load(f"images/left-2.png")
            self.screen.blit(self.image, (self.deck_x - 200, 280))
            self.image = pygame.image.load(f"images/right-2.png")
            self.screen.blit(self.image, (self.deck_x + 280, 280))

        # Display the discard pile in the center of the screen.
        if len(self.discard_pile) > 0:
            for card in self.discard_pile:
                card.display_card("front", self.discard_x, self.discard_y)

    def reset_deck(self):
        """ Function to reset the deck. """
        self.deck.extend(self.discard_pile)
        for card in self.deck:
            card.reset_card_display()
        self.discard_pile.append(self.deck.pop(-1))


