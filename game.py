import pygame
import random

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Set the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Set the size of the grids
GRID_SIZE = 10
CELL_SIZE = WINDOW_HEIGHT // GRID_SIZE

# Set the gap between the grids
GAP = 40

# Set the number of battleships
NUM_SHIPS = 5
SHIP_LENGTHS = [5, 4, 3, 3, 2]

# Create the window
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Battleship Game")

# Create player 1 and player 2 grids
player1_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
player2_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Place battleships randomly on the grids
def place_ships(grid, ship_lengths):
    for length in ship_lengths:
        placed = False
        while not placed:
            orientation = random.randint(0, 1)  # 0 for horizontal, 1 for vertical
            if orientation == 0:
                row = random.randint(0, GRID_SIZE - 1)
                col = random.randint(0, GRID_SIZE - length)
                if all(grid[row][col+i] == 0 for i in range(length)):
                    for i in range(length):
                        grid[row][col+i] = 4  # Set player's battleship value to 4
                    placed = True
            else:
                row = random.randint(0, GRID_SIZE - length)
                col = random.randint(0, GRID_SIZE - 1)
                if all(grid[row+i][col] == 0 for i in range(length)):
                    for i in range(length):
                        grid[row+i][col] = 4  # Set player's battleship value to 4
                    placed = True

# Draw the grid
def draw_grid(x_offset, y_offset, grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = x_offset + col * CELL_SIZE
            y = y_offset + row * CELL_SIZE

            if grid[row][col] == 0 or grid[row][col] == 1:
                pygame.draw.rect(window, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
            elif grid[row][col] == 2:
                pygame.draw.rect(window, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
            elif grid[row][col] == 3:
                pygame.draw.rect(window, RED, (x, y, CELL_SIZE, CELL_SIZE))
            elif grid[row][col] == 4:
                pygame.draw.rect(window, (0, 255, 0), (x, y, CELL_SIZE, CELL_SIZE))


# Check if a coordinate is a hit or miss
def check_hit(row, col, target_grid):
    if target_grid[row][col] == 4:  # Check if the player's battleship is hit
                target_grid[row][col] = 2
                return "HIT"
    else:
        target_grid[row][col] = 3
        return "MISS"


# Check if all ships are hit on a grid
def check_game_over(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 4:
                return False
    return True


# Main game loop
running = True
turn = 1
game_over = False

# Place ships on player 1 and player 2 grids
place_ships(player1_grid, SHIP_LENGTHS)
place_ships(player2_grid, SHIP_LENGTHS)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = pygame.mouse.get_pos()
            clicked_row = mouse_pos[1] // CELL_SIZE
            clicked_col = mouse_pos[0] // CELL_SIZE

            if clicked_row >= 0 and clicked_row < GRID_SIZE and clicked_col >= 0 and clicked_col < GRID_SIZE:
                if turn == 1:
                    result = check_hit(clicked_row, clicked_col, player2_grid)
                    if result == "HIT":
                        if check_game_over(player2_grid):
                            game_over = True
                    turn = 2
                elif turn == 2:
                    result = check_hit(clicked_row, clicked_col, player1_grid)
                    if result == "HIT":
                        if check_game_over(player1_grid):
                            game_over = True
                    turn = 1

    # Clear the window
    window.fill(BLACK)

    # Draw player 1 grid
    draw_grid(0, 0, player1_grid)

    # Draw player 2 grid
    draw_grid(GRID_SIZE * CELL_SIZE + GAP, 0, player2_grid)

    # Draw grid labels
    font = pygame.font.Font(None, 36)

    # Draw game over message
    if game_over:
        if check_game_over(player1_grid):
            game_over_label = font.render("PLAYER 2 WINS", True, WHITE)
        else:
            game_over_label = font.render("PLAYER 1 WINS", True, WHITE)
        window.blit(game_over_label, (WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 - 20))

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()

