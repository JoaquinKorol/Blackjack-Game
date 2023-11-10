import pygame
from classes.player import Player
from classes.deck import Deck
from classes.croupier import Croupier
from classes.button import Button
from classes.chips import ChipDisplay


def main():
    pygame.init()

    # Define colors and set up the screen
    GREEN = (34, 139, 34)
    size = (1280, 720)
    screen = pygame.display.set_mode(size)

    # Loading various images for buttons, chips, and cards
    start_img = pygame.image.load("images/start-2.png").convert_alpha()
    exit_img = pygame.image.load("images/exit-2.png").convert_alpha()
    chip_images = [
        pygame.image.load("images/chipOrange.png").convert_alpha(),
        pygame.image.load("images/chipPurple.png").convert_alpha(),
        pygame.image.load("images/chipRed.png").convert_alpha(),
        pygame.image.load("images/chipBlack.png").convert_alpha(),
    ]
    deal_img = pygame.image.load("images/deal.png").convert_alpha()
    hit_img = pygame.image.load("images/hit.png").convert_alpha()
    stand_img = pygame.image.load("images/stand.png").convert_alpha()
    background_card = pygame.image.load("images/BackgroundRed.png").convert_alpha()

    center_x = size[0] // 2
    center_y = size[1] // 2

    # Setting game buttons
    start_button = Button(center_x, center_y, start_img, 1.5)
    exit_button = Button(center_x, center_y + start_img.get_height() * 1.5, exit_img, 1.5)
    deal_button = Button(center_x / 1.5, center_y, deal_img, 1.5)
    hit_button = Button(150, 315, hit_img, 1.2)
    stand_button = Button(250, 315, stand_img, 1.2)

    buttons = [start_button, exit_button]
    chip_values = [1, 10, 100, 500]
    chip_display = ChipDisplay(chip_images)
    custom_font = pygame.font.Font("images/Pragmatica-ExtraLight.ttf", 36)

    # Initialize player, croupier, and deck
    start_game = False
    player = Player()
    croupier = Croupier()
    deck = Deck()

    x_position = 100
    y_position = 400

    # Setting initial game state
    deal_button_pressed = False
    show_buttons = False
    run = True
    player_has_stood = False
    player_busted = False
    round_ended = False
    game_over = False
    restart_game = False

    #Game loop
    while run:
        screen.fill(GREEN) # Clear the screen

        for event in pygame.event.get(): # Event handling loop
            if event.type == pygame.QUIT:
                run = False # If the user quits, exit the loop
            elif event.type == pygame.MOUSEBUTTONDOWN: # Handling mouse click
                if event.button == 1: # Left mouse button clicked
                    x, y = event.pos
                    # Check if a chip is clicked and handle betting logic
                    is_over_chip, chip_index = chip_display.is_mouse_over_chip(screen, x, y)
                    if is_over_chip and not deal_button_pressed:
                        bet_amount = chip_values[chip_index]
                        player.bet(bet_amount)
                    if round_ended:  # Reset game for a new round if the previous round ended
                        round_ended = False
                        player.reset()  
                        croupier.reset()  
                        player_has_stood = False
                        player_busted = False
                        deal_button_pressed = False
                        chip_display.show()
                        if player.balance == 0:
                            game_over = True
                    if restart_game: # Restart game if the player balance = 0
                        deck = Deck()   
                        player.reset()  
                        croupier.reset()
                        player.balance = 2500  
                        player_has_stood = False
                        player_busted = False
                        deal_button_pressed = False
                        chip_display.show()
                        game_over = False
                        restart_game = False
                        
        if game_over:
                chip_display.hide()
                game_over_text = custom_font.render("Game Over!", True, (255, 255, 255))
                restart_again_text = custom_font.render("Click the screen to restart the game", True, (255, 255, 255))
                screen.blit(game_over_text, (center_x, center_y))
                screen.blit(restart_again_text, (center_x, 400))
                restart_game = True
                
                

        # Button interaction and game flow    
        for b in buttons:
            if b.draw(screen):
                if b == start_button:
                    buttons.remove(start_button)
                    buttons.remove(exit_button)
                    start_game = True
                elif b == exit_button:
                    run = False
        
        if start_game: # Game has started
            chip_display.draw_chips(screen)
            user_balance_text = custom_font.render(f"Balance: ${player.balance}", True, (255, 255, 255))
            total_bet_text = custom_font.render(f"Bet: ${player.total_bet}", True, (255, 255, 255))
            screen.blit(total_bet_text, (10, 10))
            screen.blit(user_balance_text, (565, 630))
            if player.total_bet >= 1 and not deal_button_pressed:
                if deal_button.draw(screen):
                    player.get_hand(2, deck)
                    deal_button_pressed = True
                    chip_display.hide()
                    croupier.get_hand(2, deck)

        # Display the croupier's and player's cards and handle game actions
        x_position_croupier = 800
        
        for card in croupier.hand:
            card_image = card.get_image_path()
            card_surface = pygame.image.load(card_image)
            screen.blit(card_surface, (x_position_croupier, 50))
            x_position_croupier += 95

        x_position = 100
        y_position = 400

        for card in player.hand:
            card_image = card.get_image_path()
            card_surface = pygame.image.load(card_image)
            screen.blit(card_surface, (x_position, y_position))
            x_position += 95
            player_hand_value = deck.calculate_hand_value(player.hand)
            player_hand_text = custom_font.render(f"{player_hand_value}", True, (255, 255, 255))
            screen.blit(player_hand_text, (190, 360))

            if not player_has_stood and not player_busted:
                screen.blit(background_card, (896, 50))
                first_card = croupier.hand[0]
                croupier_hand_value = deck.calculate_hand_value([first_card])
                croupier_hand_text = custom_font.render(f"{croupier_hand_value}", True, (255, 255, 255))
                screen.blit(croupier_hand_text, (925, 218))
                if hit_button.draw(screen):
                    player.get_hand(1, deck)
                    if deck.calculate_hand_value(player.hand) >= 22:
                        player_busted = True

                if stand_button.draw(screen):
                    player_has_stood = True
                    croupier.logic(deck)
                    
        start_again_text = custom_font.render("Click the screen to start again", True, (255, 255, 255))
        # Display results if the player busts or stands
        if player_busted:
            bust_text = custom_font.render("Bust", True, (255, 255, 255))
            screen.blit(bust_text, (235, 360))
            croupier_hand_value = deck.calculate_hand_value(croupier.hand)
            croupier_hand_text = custom_font.render(f"{croupier_hand_value}", True, (255, 255, 255))
            screen.blit(croupier_hand_text, (925, 218))
            user_new_balance = player.balance
            user_balance_text = custom_font.render(f"Balance: ${user_new_balance}", True, (255, 255, 255))
            pygame.draw.rect(screen, GREEN, (565, 630, 30, 30))
            screen.blit(user_balance_text, (565, 630))
            # Display text for player loss
            player_loss_text = custom_font.render("Player Loses!", True, (255, 255, 255))
            screen.blit(player_loss_text, (center_x, center_y))
            screen.blit(start_again_text, (center_x, 400))
            round_ended = True
            
        if player_has_stood:
            #Player stands
            croupier.logic(deck) # Croupier stands with 17
            croupier_hand_value = deck.calculate_hand_value(croupier.hand) 
            croupier_hand_text = custom_font.render(f"{croupier_hand_value}", True, (255, 255, 255))
            screen.blit(croupier_hand_text, (925, 218))
            
            if deck.calculate_hand_value(player.hand) == 21 and len(player.hand) == 2:
                # Condition for Blackjack: Player's hand total is 21 and has only two cards
                if not player.wins_displayed:
                    # Player gets a Blackjack: Balance updated to 3 times the initial bet
                    user_new_balance = player.total_bet * 3 + player.balance
                    player.balance = user_new_balance
                    user_balance_text = custom_font.render(f"Balance: ${player.balance}", True, (255, 255, 255))
                    pygame.draw.rect(screen, GREEN, (565, 630, 200, 300))
                    screen.blit(user_balance_text, (565, 630))
                blackjack_text = custom_font.render("Blackjack!", True, (255, 255, 255))
                screen.blit(blackjack_text, (center_x, center_y))
                player.wins_displayed = True
                round_ended = True # Indicates the round has ended

            elif deck.calculate_hand_value(croupier.hand) >= 22 or deck.calculate_hand_value(player.hand) > deck.calculate_hand_value(croupier.hand):
                # Player wins condition: Either croupier busts or player's hand is greater than croupier's
                if not player.wins_displayed:
                    user_new_balance = player.total_bet * 2 + player.balance
                    player.balance = user_new_balance
                    user_balance_text = custom_font.render(f"Balance: ${player.balance}", True, (255, 255, 255))
                    pygame.draw.rect(screen, GREEN, (565, 630, 200, 300))
                    screen.blit(user_balance_text, (565, 630))
                win_text = custom_font.render("Player wins!", True, (255, 255, 255))
                screen.blit(win_text, (center_x, center_y))
                player.wins_displayed = True
                round_ended = True # Indicates the round has ended

            elif deck.calculate_hand_value(croupier.hand) == deck.calculate_hand_value(player.hand): 
                # Push condition: Player and croupier have the same hand total
                if not player.wins_displayed:  
                    user_new_balance = player.total_bet + player.balance
                    player.balance = user_new_balance
                    user_balance_text = custom_font.render(f"Balance: ${user_new_balance}", True, (255, 255, 255))
                    pygame.draw.rect(screen, GREEN, (565, 630, 300, 300))
                    screen.blit(user_balance_text, (565, 630))
                push_text = custom_font.render("Push!", True, (255, 255, 255))
                screen.blit(push_text, (center_x, center_y))  
                player.wins_displayed = True
                round_ended = True # Indicates the round has ended
            else:
                # Player loses: None of the above conditions met
                if not player.wins_displayed:
                    user_new_balance = player.balance
                    user_balance_text = custom_font.render(f"Balance: ${user_new_balance}", True, (255, 255, 255))
                    pygame.draw.rect(screen, GREEN, (565, 630, 300, 300))
                    screen.blit(user_balance_text, (565, 630))
                # Display text for player loss
                player_loss_text = custom_font.render("Player Loses!", True, (255, 255, 255))
                screen.blit(player_loss_text, (center_x, center_y))
                player.wins_displayed = True
                round_ended = True # Indicates the round has ended
            
            screen.blit(start_again_text, (center_x, 400)) # Prompt to start a new round
            
        pygame.display.flip()


if __name__ == "__main__":
    main()
