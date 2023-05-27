import pygame
import random

import boardSettings
from boardSettings import *

# Set the number of battleships
SHIP_LENGTHS = [5, 4, 3, 3, 2]

pygame.display.set_caption("Battleship Game")

# Place battleships randomly on the grids
def place_ships_AI(grid, ship_lengths):
    for length in ship_lengths:
        placed = False
        while not placed:
            orientation = random.randint(0, 1)  # 0 for horizontal, 1 for vertical
            if orientation == 0:
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - length)
                if all(grid[row][col + i] == 0 for i in range(length)):
                    for i in range(length):
                        grid[row][col + i] = 4  # Set player's battleship value to 4
                    placed = True
            else:
                row = random.randint(0, GRID_SIZE - length)
                col = random.randint(0, GRID_SIZE - 1)
                if all(grid[row + i][col] == 0 for i in range(length)):
                    for i in range(length):
                        grid[row + i][col] = 4  # Set player's battleship value to 4
                    placed = True


# Place battleships manually on the grids
def place_ships(grid, ship_lengths):
    for length in ship_lengths:
        placed = False
        blink = False  # Toggle variable for blinking effect
        while not placed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Clear the window
            window.fill(BLACK)

            # Draw player 1 grid
            boardSettings.draw_grid(0, 0, player1_grid)

            # Update the display
            pygame.display.update()

            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Get the row and column of the mouse position
            row = mouse_pos[1] // CELL_SIZE
            col = mouse_pos[0] // CELL_SIZE

            # Toggle the blink variable
            if pygame.time.get_ticks() % 1000 < 500:
                blink = True
            else:
                blink = False

            # Draw the current ship placement with blinking effect
            for i in range(length):
                if col + i < GRID_SIZE and pygame.mouse.get_pressed()[0] == 1:
                    if blink:
                        pygame.draw.rect(
                            window,
                            BLUE,
                            (
                                (col + i) * CELL_SIZE,
                                row * CELL_SIZE,
                                CELL_SIZE,
                                CELL_SIZE,
                            ),
                        )
                elif row + i < GRID_SIZE and pygame.mouse.get_pressed()[2] == 1:
                    if blink:
                        pygame.draw.rect(
                            window,
                            BLUE,
                            (
                                col * CELL_SIZE,
                                (row + i) * CELL_SIZE,
                                CELL_SIZE,
                                CELL_SIZE,
                            ),
                        )
                elif col + i < GRID_SIZE and row < GRID_SIZE:
                    if blink:
                        pygame.draw.rect(
                            window,
                            GRAY,
                            (
                                (col + i) * CELL_SIZE,
                                row * CELL_SIZE,
                                CELL_SIZE,
                                CELL_SIZE,
                            ),
                        )
                elif row + i < GRID_SIZE and col < GRID_SIZE:
                    if blink:
                        pygame.draw.rect(
                            window,
                            GRAY,
                            (
                                col * CELL_SIZE,
                                (row + i) * CELL_SIZE,
                                CELL_SIZE,
                                CELL_SIZE,
                            ),
                        )
            pygame.display.update()

            # Draw ship length label
            font = pygame.font.Font(None, 24)
            length_label = font.render("Length: " + str(length), True, WHITE)
            window.blit(length_label, (10, WINDOW_HEIGHT - 30))

            # Check for mouse click events
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the mouse click is within the grid bounds and the ship can be placed horizontally
                    if (
                        pygame.mouse.get_pressed()[0] == 1
                        and col + length <= GRID_SIZE
                        and all(grid[row][col + i] == 0 for i in range(length))
                    ):
                        for i in range(length):
                            grid[row][col + i] = 4

                        placed = True
                    # Check if the mouse click is within the grid bounds and the ship can be placed vertically
                    elif (
                        pygame.mouse.get_pressed()[2] == 1
                        and row + length <= GRID_SIZE
                        and all(grid[row + i][col] == 0 for i in range(length))
                    ):
                        for i in range(length):
                            grid[row + i][col] = 4

                        placed = True
                    else:
                        print("Invalid ship placement. Please try again.")