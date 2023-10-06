import pygame
from LabelModule import *
from WinnerScreenModule import *
from pygame.locals import *
import time
import ButtonModule


class GameOverScreen:
    def __init__(self,game):

        self.backgroud_color = pygame.Color("Black")

        self.gameover_label = Label("Game Over!", 250, 250, 100, "white", 'arial', True, False)
        self.Exit_Button = ButtonModule.Button(503, 660, "Exit", 'ScreenMaterial/Image/QuitButton.png',
                                               'ScreenMaterial/Image/QuitButton_pressed.png', 'calibri', 50, False, True, 'yellow')
        self.game = game
        self.bot = {}
        self.labelbot = {}

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
        # print bot score
        time.sleep(1)
        pygame.mixer.music.unload()
        pygame.mixer.music.load("ScreenMaterial/Music/down.mp3")
        pygame.mixer.music.play(-1)

    def draw(self, screen):

        screen.fill(self.backgroud_color)

        self.gameover_label.draw(screen)

        self.Exit_Button.draw(screen)

        # draw bot score label
        for i in self.labelbot.values():
            i.draw(screen)

    def mouseup(self, event):
        if self.Exit_Button.coord_inside_button(event.pos):
            quit()
# ----------------------------------------------------------------------------------------------------------------------
def lose_game(screen,game):

    current_screen = GameOverScreen(game)
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
                if 503 <= pygame.mouse.get_pos()[0] <= 503 + 213 and 660 <= pygame.mouse.get_pos()[1] <= 660+63:
                    current_screen.mouseup(event)

        current_screen.draw(screen)

        pygame.display.flip()

pygame.quit()
