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
    # Load the splash screen image
    splash_image = pygame.image.load('splash_image.png')
    splash_rect = splash_image.get_rect()

    # Resize the image to fit the window size
    splash_image = pygame.transform.scale(splash_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # Blit the splash screen image onto the window surface
    window.blit(splash_image, splash_rect)

    # Update the display
    pygame.display.update()

def show_commands():
    global play_rect, quit_rect  # Declare the variables as global

    # Display the commands on the screen
    commands_font = pygame.font.Font(None, 65)

    play_text = commands_font.render("PLAY", True, (209, 174, 157))
    play_rect = play_text.get_rect()
    play_rect.center = (WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 + 60)
    window.blit(play_text, play_rect)

    quit_text = commands_font.render("QUIT", True, (209, 174, 157))
    quit_rect = quit_text.get_rect()
    quit_rect.center = (WINDOW_WIDTH // 2 + 80, WINDOW_HEIGHT // 2 + 60)
    window.blit(quit_text, quit_rect)

    # Check if the mouse is hovering over the play or quit text
    mouse_pos = pygame.mouse.get_pos()
    if play_rect.collidepoint(mouse_pos):
        play_text = commands_font.render("PLAY", True, (242, 103, 31))
        window.blit(play_text, play_rect)
    if quit_rect.collidepoint(mouse_pos):
        quit_text = commands_font.render("QUIT", True, RED)
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