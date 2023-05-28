# Module imports
import pygame
import os

# File imports
import boardSettings
import shipPlacement
import splashScreen
import aiAgent

from globalVariables import *
from gameLogic import *
from boardSettings import *
from shipPlacement import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Call the main menu function to start the game
splashScreen.main_menu()
pygame.mixer.music.stop()

# Place ships on player 1 and player 2 grids
shipPlacement.place_ships(player1_grid, SHIP_LENGTHS)
shipPlacement.place_ships_AI(AI_grid, SHIP_LENGTHS)

# Header Height
pygame.display.set_mode((WINDOW_WIDTH + GAP, WINDOW_HEIGHT + HEADER_HEIGHT))

# Game BGM
battle = pygame.mixer.music.load(battle_bgm)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

while running:

    # Render the turn count text
    text = turnFont.render("Turn: {}".format(turnCount), True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (WINDOW_WIDTH // 2, 30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = pygame.mouse.get_pos()

            mouse_pos_0 = mouse_pos[0]
            mouse_pos_1 = mouse_pos[1]

            # Remove HEADER_HEIGHT from coordinate
            mouse_pos_1 -= HEADER_HEIGHT

            # Remove GAP from coordinate if it is in right grid
            if mouse_pos_0 > CELL_SIZE * GRID_SIZE:
                mouse_pos_0 -= GAP

            clicked_row = mouse_pos_1 // CELL_SIZE
            clicked_col = mouse_pos_0 // CELL_SIZE - GRID_SIZE
            modified_col = clicked_col + GRID_SIZE
            print(clicked_row, modified_col)
            if (clicked_row, modified_col) not in Player_shots:
                print("Invalid Shot")
                mouse_pos = pygame.mouse.get_pos()
                clicked_row = mouse_pos[1] // CELL_SIZE
                clicked_col = mouse_pos[0] // CELL_SIZE 
            else:
                playerPacked = (clicked_row, modified_col)
                Player_shots.remove(playerPacked)
                
                if (
                    clicked_row >= 0
                    and clicked_row < ATTACK_SIZE
                    and clicked_col >= 0
                    and clicked_col < ATTACK_SIZE
                ):
                    shooting_sound.play()
                    turn_label = font.render("PLAYER 1 TURN", True, WHITE)
                    print(clicked_col)
                    # clicked_col -= ATTACK_SIZE
                    print(clicked_row, clicked_col)
                    result = check_hit(clicked_row, clicked_col, AI_grid)
                    print("Player's Attack Coordinates: ", clicked_row, clicked_col, result)
                    Player_shots.append((clicked_row, clicked_col))
                    print("Player's Shots: ", Player_shots)
                    if result == "MISS":
                        missed_shot.play()
                        
                    elif result == "HIT":
                        hit_shot.play()
                        if check_game_over(AI_grid):
                            pygame.mixer.music.stop()
                            victory = pygame.mixer.music.load(victory_bgm)
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(0.5)
                            game_over = True

                    pygame.time.wait(50)
                    aiAgent.ai_turn(player1_grid)
                    if check_game_over(player1_grid):
                        pygame.mixer.music.stop()
                        victory = pygame.mixer.music.load(defeat_bgm)
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.5)
                        game_over = True
                    # Increment the turn count
                    turnCount += 1

    # Clear the window
    window.fill(VIOLET)

    # Draw the header
    pygame.draw.rect(window, VIOLET, (0, 0, WINDOW_WIDTH, HEADER_HEIGHT))
    window.blit(text, text_rect)

    # Draw player 1 grid
    boardSettings.draw_grid(0, HEADER_HEIGHT, player1_grid)

    # Draw player 2 grid
    boardSettings.draw_grid(GRID_SIZE * CELL_SIZE + GAP, HEADER_HEIGHT, AI_grid)

    # Draw grid labels
    font = pygame.font.Font(None, 36)

    # Draw the turn count text
    window.blit(text, text_rect)

    # Draw game over message
    if game_over:
        if check_game_over(player1_grid):
            game_over_message = "AI Wins"
            game_over_rect = pygame.Rect(0, 0, WINDOW_WIDTH, HEADER_HEIGHT)
            game_over_rect.center = (WINDOW_WIDTH // 2, HEADER_HEIGHT // 2)
            game_over_label = font.render(game_over_message, True, WHITE)
            game_over_label_rect = game_over_label.get_rect()
            game_over_label_rect.center = game_over_rect.center
            pygame.draw.rect(window, VIOLET, game_over_rect)
            window.blit(game_over_label, game_over_label_rect)
        else:
            game_over_message = "PLAYER 1 WINS"
            game_over_rect = pygame.Rect(0, 0, WINDOW_WIDTH, HEADER_HEIGHT)
            game_over_rect.center = (WINDOW_WIDTH // 2, HEADER_HEIGHT // 2)
            game_over_label = font.render(game_over_message, True, WHITE)
            game_over_label_rect = game_over_label.get_rect()
            game_over_label_rect.center = game_over_rect.center
            pygame.draw.rect(window, VIOLET, game_over_rect)
            window.blit(game_over_label, game_over_label_rect)
    
    #Update the game display
    pygame.display.update()


# Quit the game
pygame.quit()