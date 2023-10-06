import pygame


class ColourSelectButton:
    """ Colour Select Button Class for when the player chooses a wild card colour. """
    def __init__(self, colour, screen):
        self.colour = colour
        self.screen = screen
        self.image = pygame.image.load(f"images/{colour}button.png")
        self.rect = self.image.get_rect()

    def display_button(self, x, y):
        """ Displays the button on the screen. Top left coordinated of rect is x,y. """
        self.rect.x = x
        self.rect.y = y
        self.screen.blit(self.image, self.rect)
