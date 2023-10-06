# Generating Deck of 108 cards.
'''This function builds deck for the game.
Logic : Using a for-loop within for-loop to make combinations of numbers and colours. Appending all the number twice except '0'
Also appending 4 wild cards in the deck with another for loop.

Parameter -> None
Returns -> The whole deck in a form of list.

'''
import random

def buildDeck():
    deck = []
    colors = ['Red', 'Yellow', 'Blue', 'Green']
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+2', 'Skip', 'Reverse']
    wilds = ['Wild +4', 'Wild CC']
    for color in colors:
        for num in numbers:
            deck.append('{} {}'.format(color, num))
            if num != 0:
                deck.append('{} {}'.format(color, num))
    for _ in range(4):
        deck.append(wilds[0])
        deck.append(wilds[1])

    return deck


# Shuffle Deck
'''
Shuffling the deck using shuffle function in random package.

Paramter -> list of cards
Returns -> list of cards
'''
from random import shuffle


def shuffleCards(cards):
    # Shufles a list of cards "randomly".
    shuffle(cards)
    return cards


# drawing N number of cards

'''
This function draws N number of cards from the maindeck.

paramter -> deck(list of cards in maindeck or discarded deck), number of cards to be drawn as integer.
returns -> list of drawn cards
'''


def drawCards(maindeck, num):
    drawnCards = []
    for _ in range(num):
        drawnCards.append(maindeck.pop(0))
    return drawnCards


# print cards in player hands

'''
This function prints the card in hand of any player.

Parameter -> integer(player turn-1 (I have initialized player turn at 0 to match the indices of list.)), dictionary of players.
Returns -> None

'''
def hand(playerNum, players):
    key = 'Player ' + str(playerNum + 1)

    print('Player ' + str(playerNum + 1) + ' turns. ')
    print("")
    for card in players[key]:
        print(card)

    print("")


# check player hand if he/she can play any card in that turn. Returns Boolean

'''
This function checks player hand if it can play any card in that turn.

parameter -> current card on top as String, players dictionary, player turn as integer 
returns -> Boolean
'''


def canPlayCard(currentCard, players, playerTurn):
    splitCard = currentCard.split()
    cardCurrentColor = splitCard[0]
    cardCurrentValue = splitCard[1]
    key = 'Player ' + str(playerTurn + 1)

    for card in players[key]:
        playerCardSplit = card.split()
        if playerCardSplit[0] == 'Wild':
            return True
        elif playerCardSplit[0] == cardCurrentColor or playerCardSplit[1] == cardCurrentValue:
            return True
    return False


# Validate if the card played by player is correct.

def validateChosenCard(chosenCard, currentCard):
    chosenCardColor = (chosenCard.split())[0]
    chosenCardValue = (chosenCard.split())[1]
    currentCardColor = (currentCard.split())[0]
    currentCardValue = (currentCard.split())[1]

    if chosenCardColor == 'Wild':
        return True
    elif chosenCardColor == currentCardColor or chosenCardValue == currentCardValue:
        return True
    else:
        return False


# check if player has won
'''
This function  check if any player has won the game.
parameters -> players as dictionary, player turn as an integer
Returns -> Boolean
'''


def winner(players, playerTurn):
    key = 'Player ' + str(playerTurn + 1)
    handLeft = players[key]
    if len(handLeft) == 0:
        return True
    else:
        return False


'''
This function implements the extended new rule asked for the project.
Parameters -> deck as list, player turn as integer, players as dictionary
Returns -> None

Logic -> This function takes the player as per its turn and retrieve the cards in its hand and 
removes the first card from its hand and append a new card taking the last card from the main deck. 
The card removed from the hand is appended in the main deck at the start. 
'''


def extendedRule(maindeck, playerTurn, players, replacedCard):
    key = 'Player ' + str(playerTurn + 1)
    cardInHand = players[key]
    cardPopped = cardInHand.pop(cardInHand.index(replacedCard))  # removing card from players hand.
    maindeck.insert(0, cardPopped)  # inserting the card at 0 index of the maindeck
    cardInHand.append(maindeck.pop(-1))  # adding a new card in players hand taking last card from the main deck.


def extendedRuleCardValidation(replacedCard,players,playerTurn):
    key = 'Player ' + str(playerTurn + 1)
    cardsInHand = players[key]

    if replacedCard in cardsInHand:
        return True
    else:
        return False


def specialCards(splitCard,players,gameDirection,playerTurn,totPlayers,leftCards,maindeck):

    returnValues = []
    currentColour = splitCard[0]
    currentValue = splitCard[1]
    print(currentColour)
    print(currentValue)
    '''
    This part checks the special card played by player and integrates the functionality of special.
    '''
    if currentColour == 'Wild':

        key = 'Player ' + str(playerTurn + 1)
        colors = ['Red', 'Yellow', 'Blue', 'Green']
        if key == 'Player 1':
            newColor = input('Please choose a color between Red, Yellow, Blue or Green.')
        else:
            newColor = colors[random.randint(0, 3)]

        while newColor not in colors:
            newColor = input('Please choose a color between Red, Yellow, Blue or Green.')
        currentCard = newColor + ' Any'
        leftCards.append(currentCard)

    if currentValue == 'Reverse':
        gameDirection = gameDirection * -1  # changing the game direction if reverse card is played

    if currentValue == 'Skip':

        '''
        Logic:
        skipping the next player in the game direction and if player turns exceeds or equals to 
        total number of players it resets to 0 and 
        if game is in opposite direction it resets at the number of players playing the game.
        '''
        print('In Here')
        print(playerTurn)
        print(gameDirection)
        playerTurn += gameDirection
        if playerTurn >= totPlayers:
            playerTurn = 0
        elif playerTurn < 0:
            playerTurn = totPlayers - 1

    if currentValue == '+2':
        playerToDraw = playerTurn + gameDirection  # changing the pointer to next player to draw a card.

        # checking player to draw according to number of players playing the game and game direction.
        if playerToDraw >= totPlayers:
            playerToDraw = 0
        elif playerToDraw < 0:
            playerToDraw = totPlayers - 1

        playerHand = players[
            'Player ' + str(playerToDraw + 1)]  # taking the card from the player's hand as a list
        playerHand.extend(drawCards(maindeck, 2))  # drawing two cards from the maindeck

        # update the hand of player with the 2 new cards.
        updatedHand = {'Player ' + str(playerToDraw + 1): playerHand}
        players.update(updatedHand)

    if currentValue == '+4':
        playerToDraw = playerTurn + gameDirection  # changing the pointer to next player to draw a card.

        # checking player to draw according to number of players playing the game and game direction.
        if playerToDraw >= totPlayers:
            playerToDraw = 0
        elif playerToDraw < 0:
            playerToDraw = totPlayers - 1

        playerHand = players[
            'Player ' + str(playerToDraw + 1)]  # taking the card from the player's hand as a list
        playerHand.extend(drawCards(maindeck, 4))  # drawing two cards from the maindeck

        # update the hand of player with the 4 new cards.
        updatedHand = {'Player ' + str(playerToDraw + 1): playerHand}
        players.update(updatedHand)

    returnValues.append(splitCard)
    returnValues.append(players)
    returnValues.append(gameDirection)
    returnValues.append(leftCards)
    returnValues.append(playerTurn)
    returnValues.append(maindeck)

    return returnValues

def main():
    # building and shuffling the main deck.
    maindeck = buildDeck()
    maindeck = shuffleCards(maindeck)
    maindeck = shuffleCards(maindeck)

    # Asking the player with how many players he/she wants to play the game against and initializing a dictionary of players.
    players = {}
    numPlayers = int(input('How many players do you want to play against ? ----- '))
    totPlayers = numPlayers + 1  # total number of players including human.
    num = 1  # initializing a value to use it as a Name in dictionary key.

    # inserting data in player dictionary with players as key and cards in its hand as value.
    for player in range(totPlayers):
        playerCards = []
        players['Player ' + str(num)] = drawCards(maindeck,
                                                  7)  # drawing 7 cards from maindeck and assigning it in player's hand.
        num += 1

    gameDirection = 1  # initializing a game direction as 1.
    playerTurn = 0  # initializing player turn as 0 to match indices of list(done for ease).
    game = True  # initializing game boolean to start and end the game.
    leftCards = []  # discard pile as list of cards used to add the card played by players.
    leftCards.append(
        maindeck.pop(-1))  # initializing the discard pile as the last card from the main deck before the game starts.
    # leftCards.extend(maindeck)

    # starting the game
    while game:

        currentCard = leftCards[-1]  # the current card on top of discard pile.
        currentCardSplit = currentCard.split(' ')

        if currentCardSplit[0] == 'Wild' or (currentCardSplit[0] in ['Reverse', 'Skip']):
            maindeck.insert(0,currentCard)
            leftCards.append(maindeck.pop(-1))
            currentCard = leftCards[-1]

        # checking if the main deck gets empty and populating it after shuffling the discarded pile.
        if (len(maindeck) == 0):
            shuffleCards(leftCards)
            maindeck.extend(leftCards)

        print("")
        print('The Card on top of the pile is {}'.format(leftCards.pop(-1)))
        print("")
        # player is not bot
        if 'Player ' + str(playerTurn+1) == 'Player 1':
            # implementing extended rule of swapping a card from deck.
            print("")
            print('Player ' + str(playerTurn + 1) + ' hand before swapping is ')
            hand(playerTurn, players)

            replacedCard = input('Which card do you want to replace? ---- ')
            while not extendedRuleCardValidation(replacedCard, players, playerTurn):
                replacedCard = input('Invalid Card. Which card do you want to replace? ---- ')

            extendedRule(maindeck, playerTurn, players, replacedCard)
            print("")
            print('Player ' + str(playerTurn + 1) + ' hand after swapping is ')
            hand(playerTurn, players)

            # checking if the player is eligible to play any card from its hand by comparing the card on top of the pile.
            if canPlayCard(currentCard, players, playerTurn):
                chosenCard = input('Which card you wanna play ?')

                # validating the card played by player is correct or not.
                while not validateChosenCard(chosenCard, currentCard):
                    chosenCard = input('Invalid Card. Which card you wanna play ?')

                playerHand = players['Player ' + str(playerTurn + 1)]
                playerHand.pop(playerHand.index(chosenCard.strip()))  # removing the played card from player's hand.
                leftCards.append(chosenCard)  # appending the played card in the discard pile

                # check for win here.
                if winner(players, playerTurn):
                    print('Game Over ... Player ' + str(playerTurn + 1) + ' is the winner.')
                    game = False

                else:
                    # check for special cards
                    splitCard = leftCards[-1].split(" ")
                    specialListReturn = specialCards(splitCard, players, gameDirection, playerTurn, totPlayers,
                                                     leftCards, maindeck)
                    splitCard = specialListReturn[0]
                    players = specialListReturn[1]
                    gameDirection = specialListReturn[2]
                    leftCards = specialListReturn[3]
                    playerTurn = specialListReturn[4]
                    maindeck = specialListReturn[5]

            else:

                print('You cannot play, you have to draw a card and check if the drawn card can be played.')

                # drawing a card from main deck and appending it in the hand of the player.
                playerHand = players['Player ' + str(playerTurn + 1)]
                drawnCard = drawCards(maindeck, 1)
                playerHand.extend(drawnCard)
                updatedHand = {'Player ' + str(playerTurn + 1): playerHand}
                players.update(updatedHand)
                # showing the hand again with new added card.
                hand(playerTurn, players)

                # checking if the card drawn by the player is eligible to play.
                if canPlayCard(currentCard, players, playerTurn):
                    playerHand = players['Player ' + str(playerTurn + 1)]
                    playerHand.pop(playerHand.index(drawnCard[0]))

                    # checking winner.
                    if winner(players, playerTurn):
                        print('Game Over ... Player ' + str(playerTurn + 1) + ' is the winner.')
                        game = False
                    else:
                        # check for if the drawn card is a special card.
                        cardDrawn = drawnCard[0].split(" ")
                        specialListReturn = specialCards(cardDrawn, players, gameDirection, playerTurn, totPlayers,
                                                         leftCards, maindeck)
                        cardDrawn = specialListReturn[0]
                        players = specialListReturn[1]
                        gameDirection = specialListReturn[2]
                        leftCards = specialListReturn[3]
                        playerTurn = specialListReturn[4]
                        maindeck = specialListReturn[5]

                else:
                    leftCards.append(currentCard)


        #player is bot
        else:
            botPlayerName = 'Player ' + str(playerTurn + 1)
            # Bot exchange one card randomly and got a card from the maindeck, return new card list.
            currentCardBot = currentCard.split(' ')
            currentCardBotC = currentCardBot[0]
            currentCardBotV = currentCardBot[1]

            cardInBotsHand = players[botPlayerName]
            replaceCard = cardInBotsHand[random.randint(0, len(cardInBotsHand) - 1)]
            extendedRule(maindeck, playerTurn, players, replaceCard)

            # Bot check if it can play card
            if canPlayCard(currentCard, players, playerTurn):

                choseCard = ''
                for card in cardInBotsHand:
                    botCard = card.split(' ')
                    botCardC = botCard[0]
                    botCardV = botCard[1]

                    if botCardC == 'Wild':
                        choseCard = card

                    if botCardC == currentCardBotC or botCardV == currentCardBotV:
                        choseCard = card
                        break

                print(botPlayerName + " played " + choseCard)
                playerHand = players[botPlayerName]
                playerHand.pop(playerHand.index(choseCard.strip()))
                leftCards.append(choseCard)

                # check if bot win
                if len(playerHand) == 0:
                    print("The " + botPlayerName + " is the winner")
                    game = False

                # check for special cards
                else:
                    splitCard = leftCards[-1].split(" ")
                    specialListReturn = specialCards(splitCard, players, gameDirection, playerTurn, totPlayers, leftCards, maindeck)
                    splitCard = specialListReturn[0]
                    players = specialListReturn[1]
                    gameDirection = specialListReturn[2]
                    leftCards = specialListReturn[3]
                    playerTurn = specialListReturn[4]
                    maindeck = specialListReturn[5]

            # if Bot cannot play any card
            else:

                print('Bot cannot play, it has to draw a card and check if the drawn card can be played.')

                # drawing a card from main deck and appending it in the hand of the player.
                playerHand = players[botPlayerName]
                drawnCard = drawCards(maindeck, 1)
                playerHand.extend(drawnCard)
                updatedHand = {botPlayerName: playerHand}
                players.update(updatedHand)

                # showing the hand again with new added card.
                # hand(playerTurn, players)

                # checking if the card drawn by the player is eligible to play.
                if canPlayCard(currentCard, players, playerTurn):
                    playerHand = players[botPlayerName]
                    playerHand.pop(playerHand.index(drawnCard[0]))

                    # check if bot win
                    if len(playerHand) == 0:
                        print("The " + botPlayerName + " is the winner")
                        game = False
                    # check for special cards
                    else:
                        splitCard = leftCards[-1].split(" ")
                        specialListReturn = specialCards(splitCard, players, gameDirection, playerTurn, totPlayers,
                                                         leftCards, maindeck)
                        splitCard = specialListReturn[0]
                        players = specialListReturn[1]
                        gameDirection = specialListReturn[2]
                        leftCards = specialListReturn[3]
                        playerTurn = specialListReturn[4]
                        maindeck = specialListReturn[5]
                else:
                    leftCards.append(currentCard)


        playerTurn += gameDirection
        if playerTurn >= totPlayers:
            playerTurn = 0
        elif playerTurn < 0:
            playerTurn = totPlayers - 1

main()



