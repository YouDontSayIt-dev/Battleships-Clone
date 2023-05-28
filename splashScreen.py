# Main menu
import pygame

from boardSettings import *
from globalVariables import *

pygame.mixer.init()

intro = pygame.mixer.music.load(intro_bgm)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)


def main_menu():
    splash_screen()
    show_commands()
    wait_for_input()


def splash_screen():
    # Clear the screen with a solid color
    window.fill((43,80,112))
    pygame.display.update()


def show_commands():
    global play_rect, quit_rect  # Declare the variables as global

    # Display the commands on the screen
    header_font = pygame.font.Font(None, 30)
    title_font = pygame.font.Font('freesansbold.ttf', 90)
    commands_font = pygame.font.Font(None, 40)
    sub_font = pygame.font.SysFont('Verdana', 13)

    header_text = header_font.render("WELCOME ABOARD!", True, (LIGHTB))
    header_rect = header_text.get_rect()
    header_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80)
    window.blit(header_text, header_rect)

    title_text = title_font.render("BATTLESHIPS", True, (232,187,149))
    title_rect = title_text.get_rect()
    title_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20)
    window.blit(title_text, title_rect)

    play_text = commands_font.render("Play", True, DARKPINK)
    play_rect = play_text.get_rect()
    play_rect.center = (WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2 + 70)
    window.blit(play_text, play_rect)

    quit_text = commands_font.render("Quit", True, DARKPINK)
    quit_rect = quit_text.get_rect()
    quit_rect.center = (WINDOW_WIDTH // 2 + 60, WINDOW_HEIGHT // 2 + 70)
    window.blit(quit_text, quit_rect)

    sub_text = sub_font.render("cruz mamorno muyco", True, CREAM)
    sub_rect = sub_text.get_rect()
    sub_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 160)
    window.blit(sub_text, sub_rect)

    # Check if the mouse is hovering over the play or quit text
    mouse_pos = pygame.mouse.get_pos()
    if play_rect.collidepoint(mouse_pos):
        play_text = commands_font.render("Play", True, GREEN)
        window.blit(play_text, play_rect)
    if quit_rect.collidepoint(mouse_pos):
        quit_text = commands_font.render("Quit", True, RED)
        window.blit(quit_text, quit_rect)

    pygame.display.update()


def wait_for_input():
    # Wait for the player to click on the text to start the game or quit
    while True:
        show_commands()  # Update the display to handle hovering effect
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    return
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()