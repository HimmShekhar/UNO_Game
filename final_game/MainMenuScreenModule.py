import pygame
from LabelModule import *
import ButtonModule
from GameOverScreenModule import *
from WinnerScreenModule import *
from pygame.locals import *


class MainMenuScreen:
    def __init__(self):
        self.image = pygame.image.load('ScreenMaterial/Image/UNO.png')  # size 1680 1050

        self.Start_Button = ButtonModule.Button(433, 475, "Start", 'ScreenMaterial/Image/StartButton.png',
                                                'ScreenMaterial/Image/StartButton_pressed.png', 'calibri',\
                                                100, False, True, 'yellow')
        self.Quit_Button = ButtonModule.Button(503, 635, "Quit", 'ScreenMaterial/Image/QuitButton.png',
                                               'ScreenMaterial/Image/QuitButton_pressed.png', 'calibri',\
                                               50, False, True, 'yellow')

    def draw(self, screen):
        screen.blit(self.image,(0,0))

        # draw buttons
        self.Start_Button.draw(screen)
        self.Quit_Button.draw(screen)

        # update position

    def mouseup(self, event):
        if self.Start_Button.coord_inside_button(event.pos):
            return False
        elif self.Quit_Button.coord_inside_button(event.pos):
            quit()
# ----------------------------------------------------------------------------------------------------------------------
def main_menu(screen):

    current_screen = MainMenuScreen()
    pygame.mixer.init()
    current_screen.draw(screen)

    pygame.display.flip()

    pygame.mixer.music.unload()
    pygame.mixer.music.load("ScreenMaterial/Music/Adventure-320bit.mp3")
    pygame.mixer.music.play(-1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == MOUSEBUTTONUP:
                if 433 <= pygame.mouse.get_pos()[0] <= 433 + 346 and 475 <= pygame.mouse.get_pos()[1] <= 475 + 114:
                    running = current_screen.mouseup(event)
                elif 503 <= pygame.mouse.get_pos()[0] <= 503 + 213 and 635 <= pygame.mouse.get_pos()[1] <= 635+63:
                    current_screen.mouseup(event)

        current_screen.draw(screen)

        pygame.display.flip()

pygame.quit()
