import pygame
import sys
from random import choice, randint
from time import sleep


def updatePlayableCards(currentCard, players, playerTurn):
    """ Checks if there is a playable card in players hand and updates them. """
    wild_cards = {"wildred": "red", "wildblue": "blue", "wildyellow": "yellow", "wildgreen": "green"}
    # If there is a card in the discard pile
    if currentCard:
        # Loop over the player hand to check each card against the current_card on the discard pile
        for card in players[playerTurn].drawn_cards:
            if card.colour == 'wild':
                card.set_card_playable()
            elif card.colour == currentCard.colour or card.number == currentCard.number:
                card.set_card_playable()
            elif currentCard.colour in wild_cards:
                if card.colour == wild_cards[currentCard.colour]:
                    card.set_card_playable()
    # If the discard pile is empty, all cards are playable
    else:
        for card in players[playerTurn].drawn_cards:
            card.set_card_playable()


def canPlayCard(currentCard, players, playerTurn):
    """ Function to check if there is a playable card in the hand. """
    for card in players[playerTurn].drawn_cards:
        if card.card_playable:
            return True
    return False


def winner(players, playerTurn):
    """ Returns True if the players hand is empty. """
    return len(players[playerTurn].drawn_cards) == 0


def check_events(screen, hand, deck, game):
    """ Function to check for events and actions. """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Close and quit when window is closed
            game.game = False
            pygame.quit()
            sys.exit()

        # Check for mouse click events:
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check for mouse click on half visible cards in hand, [:-1] checks up until the last card
            for card in hand.drawn_cards[:-1]:
                # If the mouse coordinates are in the range of the visible coordinates of the card
                if card.rect.x <= mouse_x <= card.rect.x + card.rect.width/2 \
                        and card.rect.y <= mouse_y <= card.rect.y + card.rect.height:
                    # Check if the extended rule has been played
                    if not game.swapped_card:
                        # Swap the card that has been clicked
                        hand.swap_first_card(card, deck)
                        # Update the swapped card variable
                        game.swapped_card = True
                    # If the extended rule has been completed, play the selected card
                    elif game.swapped_card:
                        hand.play_card(card, deck, game, screen)

            # Checks for mouse click on the fully visible card in the hand, [-1] is the top card
            # The code is the same as above, but for the top card
            if hand.drawn_cards[-1].rect.collidepoint(pygame.mouse.get_pos()):
                if not game.swapped_card:
                    hand.swap_first_card(hand.drawn_cards[-1], deck)
                    game.swapped_card = True
                elif game.swapped_card:
                    hand.play_card(hand.drawn_cards[-1], deck, game, screen)

            # Checks for mouse clicks on the center deck, and allows player to draw a card if the player cannot play
            elif deck.deck[-1].rect.collidepoint(pygame.mouse.get_pos()) \
                    and not canPlayCard(game.current_card, game.players, game.current_turn):
                # Draw 1 card to the players hand, and check if the new card is playable
                game.players[game.current_turn].draw_cards(deck, 1)
                updatePlayableCards(game.current_card, game.players, game.current_turn)
                # If the new card is playable, the card is played
                if canPlayCard(game.current_card, game.players, game.current_turn):
                    game.players[game.current_turn].play_card(game.players[game.current_turn].drawn_cards[-1], deck, game, screen)
                # If it is not, advance the turn
                else:
                    game.advance_turn()

            # Check if the current card is a wild card
            elif game.current_card:
                if game.current_card.colour == "wild":
                    # Check for mouse click on the colour choice buttons
                    for button in game.buttons:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            game.current_card.colour = "wild" + button.colour


def special_cards(screen, game, deck):
    """ Function to check for special cards, and control the action. """
    add_dict = {"+2": 2, "+4": 4}
    # If the centre card is a +2 or +4
    if game.current_card.number in add_dict:
        if game.start:
            game.players[0].draw_cards(deck, add_dict[game.current_card.number])
            if game.current_card.number == "+4":
                game.advance_turn()
        # Pseudocode: next_player_hand.draw_cards(dict[key])
        else:
            game.players[game.get_next_player()].draw_cards(deck, add_dict[game.current_card.number])
            if game.current_card.number == "+4":
                game.advance_turn()
    if game.current_card.colour == "wild":
        if game.current_card.number == "SP":
            game.game_direction = choice([1, -1])
            game.current_turn = randint(0, 3)
            game.current_card.colour = "wild" + choice(["red", "blue", "yellow", "green"])
        else:
            game.select_colour(screen, game, deck)
    if game.current_card.number == "R":
        game.reverse_direction()
    if game.current_card.number == "S":
        game.advance_turn()


def check_colour_quantity_play(game):
    """ Function to decide the colour the bot chooses when a wild card is played. """
    colour_dict = {'red': 0, 'yellow': 0, 'blue': 0, 'green': 0}
    red = 0
    yellow = 0
    blue = 0
    green = 0
    colour_result = []
    for card in game.players[game.current_turn].drawn_cards:
        if card.colour == 'red':
            red += 1
        elif card.colour == 'yellow':
            yellow += 1
        elif card.colour == 'blue':
            blue += 1
        elif card.colour == 'green':
            green += 1
    colour_dict["red"] = red
    colour_dict["yellow"] = yellow
    colour_dict["blue"] = blue
    colour_dict["green"] = green
    maxvalue = max(colour_dict.values())
    for key, value in colour_dict.items():
        if value == maxvalue:
            colour_result.append(key)
    play_colour = choice(colour_result)
    return play_colour

def bot_play_card(deck, game, screen):
    """ Function to control the bot actions upon the bot turn. """
    # Temporary variable to store playable cards
    bot_options = []
    # Get the player number for the bot - current_turn is an index
    bot_number = game.current_turn
    sleep(1)
    # Extended rule for the bot - randomly picks a card to swap
    game.players[bot_number].swap_first_card(choice(game.players[bot_number].drawn_cards), deck)
    updatePlayableCards(game.current_card, game.players, game.current_turn)
    [card.reset_card_display() for card in deck.deck]
    # Check the bot hand and append the playable cards to bot_options
    for card in game.players[bot_number].drawn_cards:
        if card.card_playable:
            bot_options.append(game.players[bot_number].drawn_cards)
    # If there are no playable cards
    if len(bot_options) == 0:
        sleep(2)
        # Draw a card from the deck
        game.players[bot_number].draw_cards(deck, 1)
        # Update if the new card is playable
        updatePlayableCards(game.current_card, game.players, game.current_turn)
        # If the card is playable
        if game.players[bot_number].drawn_cards[-1].card_playable:
            sleep(2)
            # Play the card
            game.players[bot_number].play_card(game.players[bot_number].drawn_cards[-1], deck, game, screen)
        # If it is not, advance the turn
        else:
            sleep(1.5)
            game.advance_turn()
    # If the bot has a playable card
    else:
        # Check the card quantity of next player if it is only 1
        if len(game.players[game.get_next_player()].drawn_cards) == 1:
            # Loop bots hand
            for card in game.players[bot_number].drawn_cards:
                if card.number in ['+4', '+2', 'S', 'R', 'CC']:
                    # if play wild card, bot should choose one colour determine by the quantity of colour
                    if card.colour == 'wild':
                        sleep(1.5)
                        game.players[bot_number].play_card(card, deck, game, screen)
                        break
                    # if play normal card
                    else:
                        if card.card_playable:
                            sleep(1.5)
                            game.players[bot_number].play_card(card, deck, game, screen)
                            break
        # Play a random playable card
        else:
            for card in game.players[bot_number].drawn_cards:
                if card.card_playable:
                    sleep(2.5)
                    game.players[bot_number].play_card(card, deck, game, screen)
