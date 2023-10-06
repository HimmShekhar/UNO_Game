import pygame
from pygame.sprite import Sprite
from time import sleep


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

    def move_card(self, end_pos, screen, game, deck, bg):
        """ Function to move a card from a starting pos to end pos in a straight line """
        starting_x, starting_y = self.rect.x, self.rect.y
        print(str(starting_x))
        print(str(starting_y))
        end_pos_x, end_pos_y = end_pos
        print(str(end_pos_x))
        print(str(end_pos_y))
        # if starting_x >= end_pos_x:
        #     direction = -1
            # Finds y = mx + c between two card x,y coordinates
        m = starting_y - end_pos_y / starting_x - end_pos_x
        c = starting_y - m * starting_x
        # elif starting_x < end_pos_x:
        #     m = starting_y - end_pos_y / starting_x - end_pos_x
        #     c = starting_y - m * starting_x
        #     direction = 1

        # Display the card at each coordinate along the line
        self.card_moving = True
        clock = pygame.time.Clock()

        while self.card_moving:
            if starting_y > end_pos_y:
                for y in range(int(starting_y), int(end_pos_y), -6):
                    # new_y = m * x + c
                    # y = mx +c
                    # y - c = mx
                    # y- c /m
                    new_x = (y - c)/m
                    # update_display(screen, game, deck, bg)
                    screen.blit(bg, (0, 0))
                    deck.display_deck(game)
                    # Display hands for all players
                    for player in game.players:
                        player.display_hand(game)
                    # ------------------------------------动画， update animation, show avatar
                    # show_avatar(player, game)
                    # pygame.display.flip()
                    self.display_card("front", new_x, y)
                    pygame.display.update()
                    clock.tick(60)

                self.card_moving = False











# #---------------------------- add move_card_duration
#     def move_card_duration(self, endPos, duration):
#         self.card_moveing = True
#         self.card_move_time = 0
#         self.card_move_duration = duration
#         self.card_move_startPos = (self.rect.x, self.rect.y)
#         self.card_move_endPos = endPos
#         self.card_move_speed = ((endPos[0]-self.rect.x)/self.card_move_duration, (endPos[1]-self.rect.y)/self.card_move_duration)
#
#     def move_card_calc(self, dt):
#         if not self.card_moveing:
#             return
#
#         self.card_move_time = self.card_move_time + dt
#         new_x = self.card_move_startPos[0] + self.card_move_speed[0] * self.card_move_time
#         new_y = self.card_move_startPos[1] + self.card_move_speed[1] * self.card_move_time
#         self.display_card("front", new_x, new_y)
#         self.card_moveing = self.card_move_time <= self.card_move_duration
#         if not self.card_moveing:
#             Animations.remove_action(self)
#
#     def update(self, dt):
#         self.move_card_calc(dt)
