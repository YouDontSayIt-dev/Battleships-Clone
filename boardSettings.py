import pygame

# Set the dimensions of the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Set the colors
BLACK = (76, 63, 84)
WHITE = (255, 255, 255)
GRAY = (218, 165, 32)
BLUE = (70, 130, 180)
RED = (138, 51, 36)

# Set the size of the grids
GRID_SIZE = 10
ATTACK_SIZE = 20
CELL_SIZE = WINDOW_HEIGHT // GRID_SIZE

# Set the gap between the grids
GAP = 10

# Create player 1 and AI grids
player1_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
AI_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Create the window
window = pygame.display.set_mode(WINDOW_SIZE)


# Draw the grid
def draw_grid(x_offset, y_offset, grid, fog_of_war=True):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = x_offset + col * CELL_SIZE
            y = y_offset + row * CELL_SIZE

            # Draw the cell
            pygame.draw.rect(window, BLUE, (x, y, CELL_SIZE, CELL_SIZE))

            # Draw the grid lines
            pygame.draw.rect(window, WHITE, (x, y, CELL_SIZE, CELL_SIZE), 1)

            # Check if it's the AI grid and fog of war is enabled
            if x_offset != 0 and fog_of_war and grid[row][col] == 0:
                pygame.draw.rect(window, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
            else:
                # Draw different colors based on the grid value
                if grid[row][col] == 2:
                    pygame.draw.rect(window, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
                elif grid[row][col] == 3:
                    pygame.draw.rect(window, RED, (x, y, CELL_SIZE, CELL_SIZE))
                elif grid[row][col] == 4:
                    pygame.draw.rect(window, (159, 129, 112), (x, y, CELL_SIZE, CELL_SIZE))


# Main game loop
def game_loop():
    pygame.init()
    pygame.display.set_caption("Battleship Game")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(BLACK)

        # Draw player 1 grid without fog of war
        draw_grid(0, 0, player1_grid, fog_of_war=False)

        # Draw AI grid with fog of war
        draw_grid(GAP + GRID_SIZE * CELL_SIZE, 0, AI_grid, fog_of_war=True)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


# Run the game
game_loop()

