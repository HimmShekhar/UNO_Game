import pygame
from LabelModule import *

import GameOverScreenModule
from GameOverScreenModule import *
import ButtonModule
from pygame.locals import *
import time

class WinnerScreen:
    def __init__(self, game):

        # load buttons images
        self.image = pygame.image.load('ScreenMaterial/Image/Winner.png')

        # create labels
        self.Con_lable = Label("Congratulation!", 30, 200, 100, "white", 'arial', True, True)
        self.bot = {}
        self.labelbot = {}
        self.game = game

        self.Exit_Button = ButtonModule.Button(503, 660, "Exit", 'ScreenMaterial/Image/QuitButton.png',
                                               'ScreenMaterial/Image/QuitButton_pressed.png', 'calibri', \
                                               50, False, True, 'yellow')
        time.sleep(1)
        pygame.mixer.music.unload()
        pygame.mixer.music.load("ScreenMaterial/Music/Weight_of_the_World_the_End_of_YoRHa.mp3")
        pygame.mixer.music.play(-1)

    def print_scores(self, players):
        """ Generates the bot score. """
        i = 0
        winner_score = 0
        for hand in players:
            hand.get_score()
            winner_score += hand.score


        for hand in players:
            if len(hand.drawn_cards) == 0:
                self.bot[hand.player_number] = f"Winner! {hand.player_number} score: {winner_score}"
                self.labelbot[hand.player_number] = Label(self.bot[hand.player_number], 900, 250 + i * 50, 25, "white",
                                                          'arial', True, False)
                i += 1
            elif len(hand.drawn_cards) != 0:
                self.bot[hand.player_number] = f"{hand.player_number} score: {hand.score}"
                self.labelbot[hand.player_number] = Label(self.bot[hand.player_number], 900, 250 + i * 50, 25, "white",
                                                          'arial', True, False)
                i += 1

    def draw(self, screen):

        screen.blit(self.image,(0,0))
        # draw buttons

        # draw labels
        self.Con_lable.draw(screen)
        self.Exit_Button.draw(screen)

        # draw bot score label
        for i in self.labelbot.values():
            i.draw(screen)

    def mouseup(self, event):
        if self.Exit_Button.coord_inside_button(event.pos):
            quit()
# ----------------------------------------------------------------------------------------------------------------------
def win_game(screen,game):

    current_screen = WinnerScreen(game)
    current_screen.print_scores(game.players)
    pygame.mixer.init()
    current_screen.draw(screen)

    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == MOUSEBUTTONUP:
                # Quit button
                if 503 <= pygame.mouse.get_pos()[0] <= 503 + 213 and 660 <= pygame.mouse.get_pos()[1] <= 660 + 63:
                    current_screen.mouseup(event)

        current_screen.draw(screen)

        pygame.display.flip()
