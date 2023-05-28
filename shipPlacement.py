import pygame
import random

from globalVariables import *
from boardSettings import *

pygame.mixer.init()



# Set the number of battleships
SHIP_LENGTHS = [5, 4, 3, 3, 2]

pygame.display.set_caption("Battleship Game")

# Place battleships randomly on the grids
import random

GRID_SIZE = 10

def place_ships_AI(grid, ship_lengths):
    for length in ship_lengths:
        placed = False
        while not placed:
            orientation = random.randint(0, 1)  # 0 for horizontal, 1 for vertical
            if orientation == 0:
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - length)
                valid_position = True
                for i in range(length):
                    if grid[row][col + i] != 0 or (row > 0 and grid[row - 1][col + i] != 0) or \
                       (row < GRID_SIZE - 1 and grid[row + 1][col + i] != 0) or \
                       (col + i > 0 and grid[row][col + i - 1] != 0) or \
                       (col + i < GRID_SIZE - 1 and grid[row][col + i + 1] != 0):
                        valid_position = False
                        break
                if valid_position:
                    for i in range(length):
                        grid[row][col + i] = 5  # Set player's battleship value to 5
                    placed = True
            else:
                row = random.randint(0, GRID_SIZE - length)
                col = random.randint(0, GRID_SIZE - 1)
                valid_position = True
                for i in range(length):
                    if grid[row + i][col] != 0 or (row + i > 0 and grid[row + i - 1][col] != 0) or \
                       (row + i < GRID_SIZE - 1 and grid[row + i + 1][col] != 0) or \
                       (col > 0 and grid[row + i][col - 1] != 0) or \
                       (col < GRID_SIZE - 1 and grid[row + i][col + 1] != 0):
                        valid_position = False
                        break
                if valid_position:
                    for i in range(length):
                        grid[row + i][col] = 5  # Set player's battleship value to 5
                    placed = True



# Place battleships manually on the grids
def place_ships(grid, ship_lengths):
    
    placement = pygame.mixer.music.load(placement_bgm)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    for length in ship_lengths:
        placed = False
        blink = False  # Toggle variable for blinking effect
        invalid_placement = False  # Flag to indicate invalid placement
        while not placed:
            # Clear the window
            window.fill(VIOLET)

            # Load the instruction image
            instruction_image = pygame.image.load('instruction.png')

            # Blit the instruction image onto the window surface
            window.blit(instruction_image, (402, -65))

            # Draw player 1 grid
            draw_grid(0, 0, player1_grid)

            # Get the mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Get the row and column of the mouse position
            row = mouse_pos[1] // CELL_SIZE
            col = mouse_pos[0] // CELL_SIZE

            # Toggle the blink variable
            if pygame.time.get_ticks() % 250 < 125:
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
                            MUSTARD,
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
                            MUSTARD,
                            (
                                col * CELL_SIZE,
                                (row + i) * CELL_SIZE,
                                CELL_SIZE,
                                CELL_SIZE,
                            ),
                        )

            # Draw ship length label
            font = pygame.font.SysFont('Impact', 15)
            length_label = font.render("S H I P   L E N G T H : " + str(length), True, PINK)
            window.blit(length_label, (535, WINDOW_HEIGHT - 95))

            # Draw invalid placement message
            if invalid_placement:
                invalid_label = font.render(
                    "Invalid placement!! Try again.", True, (255,78,78)
                )
                window.blit(invalid_label, (510, WINDOW_HEIGHT - 50))

            # Update the display
            pygame.display.update()

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
                        invalid_placement = True  # Set the flag to indicate invalid placement

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()