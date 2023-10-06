import pygame
from pygame.sprite import Sprite


class Card(Sprite):
    """ Class for Card objects. Inheriting from Pygame's Sprite Class. """
    def __init__(self, colour, number, screen):
        super(Card, self).__init__()
        # Colour is red, blue, yellow, green or wild
        self.colour = colour
        # Number is 0-9 and also includes special cards +2, +4, R = Reverse, S = Skip and CC = Change Colour
        self.number = number
        self.screen = screen

        self.image = pygame.image.load(f"images/{colour}{number}.png")
        self.rect = self.image.get_rect()
        self.back_image = pygame.image.load("images/back.png")
        self.card_playable = False

    def display_card(self, front_or_back, x, y):
        """Function to display a card on the screen. """
        # Top left x and y coordinates of the card
        self.rect.x = x
        self.rect.y = y

        # Draw the card depending on whether the image of the front of the card or the back of the card is required.
        if front_or_back == "front":
            # If the card is currently playable, make it pop up above the other cards in the hand
            if self.card_playable:
                self.rect.y -= 10
            # If the colour of the card is a coloured wild card update the wild cards image
            if self.colour in ["wildred", "wildyellow", "wildgreen", "wildblue"]:
                self.image = pygame.image.load(f"images/{self.colour}{self.number}.png")
                self.screen.blit(self.image, self.rect)
            # Else, display the stored image
            else:
                self.screen.blit(self.image, self.rect)
        # If the back is required, display the back image
        elif front_or_back == "back":
            self.screen.blit(self.back_image, self.rect)

    def rotate_card(self, degree_of_rotation):
        """ Function to rotate a card. """
        self.back_image = pygame.transform.rotate(pygame.image.load("images/back.png"), degree_of_rotation)
        self.rect = self.back_image.get_rect()

    def set_card_playable(self):
        """ In place function to set a card to playable. """
        self.card_playable = True

    def reset_card_playable(self):
        """ In place function to set a card to not playable. """
        self.card_playable = False

    def reset_card_display(self):
        """ To reset the display for the card. """
        colour_dict = {"wildred": "red", "wildgreen": "green", "wildyellow": "yellow", "wildblue": "blue"}
        if self.colour in colour_dict:
            self.colour = "wild"
        self.image = pygame.image.load(f"images/{self.colour}{self.number}.png")
        self.back_image = pygame.image.load("images/back.png")
        self.rect = self.image.get_rect()

