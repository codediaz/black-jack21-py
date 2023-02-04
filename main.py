import functions
from hand import Hand
import graphics
import pygame
from pygame.locals import *
import sys
import time

WINDOWWIDTH = 804
WINDOWHEIGHT = 402

rules = ""
# Start Game
graphics.window(WINDOWWIDTH, WINDOWHEIGHT)
# Ask if they want to see rules
graphics.displayText("*** BLACKJACK  ***", 400, 0)

graphics.displayText("Do you want to see the rules? (Y/N)", 5, 20)
pygame.display.update()

#uses Y or N keys to determine if the rules need to be displayed
while rules != "Y" and rules != "N":
    for event in pygame.event.get():
        if event.type == KEYUP:
            if event.key == K_y:
                rules = "Y"
            elif event.key == K_n:
                rules ="N"

#if y is pressed rules displayed. New graphics window set up blank screen and timer keeps it open
if rules == "Y":
    graphics.window(WINDOWWIDTH, WINDOWHEIGHT)
    graphics.displayText(" Both you and the computer are dealt 2 cards. ", 5,5)
    graphics.displayText("However, you can only see one of the computer's cards.",5, 25)
    graphics.displayText("All cards are face value except:", 5, 45)
    graphics.displayText("Jack (J), Queen (Q) and King (K) are all worth 10.", 10, 65)
    graphics.displayText("Ace (A) can be worth 11 or 1.", 10, 85)
    graphics.displayText("The aim of the game is to get closer to 21 points than the computer without going over (busting).", 5, 105)
    graphics.displayText("You can twist ( press t) to get another card (so you have three) or stick ( press s) to stay with the cards you have.", 5, 125)
    graphics.displayText("If you are dealt with two card with the same face (e.g: two queens), you can press 2 to play two hands.", 5, 145)
    graphics.displayText("You go first.", 5, 165)
    graphics.displayText("Have fun and good luck!", 5, 185)

    pygame.display.update()
    time.sleep(15)

# game loop - will run into red x clicked
while True:

    # Uses Hand class to make a hand for the player and a hand for the computer.
    playerHand = Hand("player")
    compHand = Hand("comp")
    player2hand = Hand("player2")

    # card positions
    playerXpos = 5
    PLAYER_Y_POS = 200
    compXpos = 5
    COMP_Y_POS = 25
    PLAYER_TOTAL_Y = 185
    COMP_TOTAL_Y = 13
    # reset window
    graphics.window(WINDOWWIDTH, WINDOWHEIGHT)

    # indicate where each players hand is
    graphics.displayText("Player:", 5, PLAYER_Y_POS - 15)
    graphics.displayText("Computer:", 5, COMP_Y_POS - 15)
    # picks two cards for each hand
    for card in range(2):
        functions.deal_Card(playerHand)
        playerXpos = functions.draw(playerXpos, PLAYER_Y_POS, playerHand)

    functions.deal_Card(compHand)
    compXpos = functions.draw(compXpos, COMP_Y_POS,compHand)



    #gets and displays the total of player hand and comphand
    compTotal =str(functions.get_total(compHand))
    playerTotal =str(functions.get_total(playerHand))
    player2Total = str(functions.get_total(player2hand))

    graphics.displayText(playerTotal, playerXpos, PLAYER_TOTAL_Y)
    graphics.displayText(compTotal, compXpos, COMP_TOTAL_Y)
    pygame.display.update()

    #Players turn is first
    turn = "player"
    playerMove = ""
    player2Move = ""

    # gets first 2 cards to check if you can split them
    playerCards = playerHand.get_card_faces()
    firstCard = playerCards[0]
    secondCard = playerCards[1]

            #Player picks move. if t pressed, new card added until either total is over 21 or s is  pressed. 2 pressed splits into 2 new hands
    while player2Move != "stick" and int(compTotal) <= 21:
        if turn == playerHand.get_user():
            
            for event in pygame.event.get():
                if event.type == KEYUP:
                    if event.key == K_t:
                        playerMove = "twist"
                    elif event.key == K_s:
                        playerMove = "stick"
                    elif event.key == K_2:
                        if len(playerCards) == 2 and firstCard[0] == secondCard[0]:
                            playerMove = "split cards"
                            # renames cards so won't allow split again
                            firstCard= "XX"
                            secondCard= "YY"



            if playerMove == "twist":
                playerTotal = functions.get_total(playerHand)
                if playerTotal < 21:
                    playerXpos, playerMove, playerTotal = functions.playerGo(playerHand, playerXpos, PLAYER_Y_POS, PLAYER_TOTAL_Y)
                    if playerTotal >= 21:
                        turn = "player2"
                else:
                    playerMove = "stick"

            elif playerMove == "stick":
                turn = "player2"

            elif playerMove == "split cards":
                # extend screen
                #add another playable hand
                WINDOWWIDTH = WINDOWWIDTH*2
                cardFace, cardValue = playerHand.remove_last_card()
                player2hand.add_card_face(cardFace)
                player2hand.add_card_value(cardValue)

                #redraw board
                playerXpos, player2Xpos, compXpos = functions.redoBoard(WINDOWWIDTH, WINDOWHEIGHT, PLAYER_Y_POS, COMP_Y_POS, playerHand, player2hand, compHand)
                graphics.displayText("Player:", 5, PLAYER_Y_POS - 15)
                graphics.displayText("Computer:", 5, COMP_Y_POS - 15)

                playerTotal = str(functions.get_total(playerHand))
                graphics.displayText(playerTotal, playerXpos, PLAYER_TOTAL_Y)
                pygame.display.update()

                player2Total = str(functions.get_total(player2hand))
                graphics.displayText(player2Total, player2Xpos, PLAYER_TOTAL_Y)
                pygame.display.update()


                playerMove = ""
        #repeat with player's second hand
        if turn == player2hand.get_user():
            cardlist = player2hand.get_card_values()
            if len(cardlist) != 0:
                for event in pygame.event.get():
                    if event.type == KEYUP:
                        if event.key == K_t:
                            player2Move = "twist"
                        elif event.key == K_s:
                            player2Move = "stick"

                player2Total = functions.get_total(player2hand)

                if player2Move == "twist":
                    if player2Total < 21:
                        player2Xpos, player2Move, player2Total = functions.playerGo(player2hand, player2Xpos, PLAYER_Y_POS, PLAYER_TOTAL_Y)
                        if player2Total >= 21:
                            turn = "comp"
                    else:
                        player2Move = "stick"
                elif player2Move == "stick":
                    turn = "comp"
            else:
                player2Move = "stick"
                turn = "comp"


        if turn == compHand.get_user():
            #comp move
            compXpos = functions.comp_move(compHand, compXpos, COMP_Y_POS)
            #Displays comps new total
            compTotal =str(functions.get_total(compHand))
            graphics.displayText(compTotal, compXpos, COMP_TOTAL_Y)
            pygame.display.update()
            time.sleep(3)



    #reduce screen size if extended - reset for next game
    if WINDOWWIDTH != 804:
        WINDOWWIDTH = WINDOWWIDTH//2

    graphics.window(WINDOWWIDTH, WINDOWHEIGHT)
    # last total were strings - int needed for calculations
    playerTotal = functions.get_total(playerHand)
    compTotal = functions.get_total(compHand)
    player2Total = functions.get_total(player2hand)

# checks and displays the results of each hand compared to the computer

    if playerTotal > 21:
        if player2Total != 0:
            if player2Total > 21:
                graphics.displayText("Both hands bust! You lost.", 200, 200)
            elif player2Total == compTotal:
                graphics.displayText("Your first hand bust, your second hand drew with the computer", 200, 200)
            elif player2Total < compTotal:
                graphics.displayText("Your first hand bust and the computer beat your second hand", 200,200)
            elif player2Total > compTotal:
                graphics.displayText("Your first hand bust but your second hand beat the computer", 200,200)
        else:
            graphics.displayText("You bust! you lost.", 200,200)


    elif compTotal > 21:
        graphics.displayText("Comp bust! You won!", 200, 200)

    elif playerTotal == compTotal:
        if player2Total != 0:
            if player2Total > 21:
                graphics.displayText("Your first hand drew, your second hand bust.", 200, 200)
            elif player2Total == compTotal:
                graphics.displayText("Both hands drew", 200, 200)
            elif player2Total < compTotal:
                graphics.displayText("Your first hand drew and the computer beat your second hand", 200,200)
            elif player2Total > compTotal:
                graphics.displayText("Your first hand drew, your second hand beat the computer",200,200)
        else:
            graphics.displayText("You drew", 200,200)

    elif playerTotal > compTotal:
        if player2Total != 0 :
            if player2Total > 21:
                graphics.displayText("Your first hand beat the computer but your second hand bust",200,200)
            elif player2Total == compTotal:
                graphics.displayText("Your first hand beat the computer, the other drew",200,200)
            elif player2Total < compTotal:
                graphics.displayText("Your first hand beat the computer, the second hand lost",200,200)
            elif player2Total > compTotal:
                graphics.displayText("Both hands are closer to 21 then the computer. You won!", 200, 200)
        else:
            graphics.displayText("You won!", 200,200)

    elif playerTotal < compTotal:
        if player2Total != 0:
            if player2Total > 21:
                graphics.displayText("Your first hand lost and your second hand bust",200,200)
            elif player2Total == compTotal:
                graphics.displayText("Your first hand lost, the other drew",200,200)
            elif player2Total < compTotal:
                graphics.displayText("both hands lost",200,200)
            elif player2Total > compTotal:
                graphics.displayText("Your first hand lost, the second hand won", 200, 200)
        else:
            graphics.displayText("You lost.", 200,200)



    pygame.display.update()
    time.sleep(3)

    #exit sequence
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

