import pygame

# Set the dimensions of the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Set the colors
BLACK = (76, 63, 84)
WHITE = (255, 255, 255)
GRAY = (218, 165, 32)  # Mustard
BLUE = (70, 130, 180)
RED = (138, 51, 36)
FIG = (138, 51, 36)  # for the ships
GREEN = (175, 224, 144)

# Set the size of the grids
GRID_SIZE = 10
ATTACK_SIZE = 20
CELL_SIZE = WINDOW_HEIGHT // GRID_SIZE

# Set the gap between the grids
GAP = 10

# Create player 1 and player 2 grids
player1_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
AI_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Create the window
window = pygame.display.set_mode(WINDOW_SIZE)


# Draw the grid
def draw_grid(x_offset, y_offset, grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = x_offset + col * CELL_SIZE
            y = y_offset + row * CELL_SIZE

            # Draw the cell
            pygame.draw.rect(window, BLUE, (x, y, CELL_SIZE, CELL_SIZE))

            # Draw the grid lines
            pygame.draw.rect(window, WHITE, (x, y, CELL_SIZE, CELL_SIZE), 1)

            # Draw different colors based on the grid value
            if grid[row][col] == 2:
                pygame.draw.rect(window, GRAY, (x, y, CELL_SIZE, CELL_SIZE))
            elif grid[row][col] == 3:
                pygame.draw.rect(window, RED, (x, y, CELL_SIZE, CELL_SIZE))
            elif grid[row][col] == 4:
                pygame.draw.rect(window, (159, 129, 112),
                                 (x, y, CELL_SIZE, CELL_SIZE))

    # Add instruction on the other side of the grid
    titleinstruction_font = pygame.font.Font(None, 68)
    instruction_font = pygame.font.Font(None, 52)
    subinstruction_font = pygame.font.Font(None, 28)

    titleinstruction = titleinstruction_font.render("Ship Placement", True, WHITE)
    titleinstruction_rect = titleinstruction.get_rect(center=(x_offset + GRID_SIZE * CELL_SIZE + 200, y_offset + GRID_SIZE * CELL_SIZE - 310))

    leftinstruction = instruction_font.render("Left Click", True, WHITE)
    leftinstruction_rect = leftinstruction.get_rect(center=(x_offset + GRID_SIZE * CELL_SIZE + 200, y_offset + GRID_SIZE * CELL_SIZE - 230))

    leftsubinstruction = subinstruction_font.render("Horizontal Alignment", True, GREEN)
    leftsubinstruction_rect = leftsubinstruction.get_rect(center=(x_offset + GRID_SIZE * CELL_SIZE + 200, y_offset + GRID_SIZE * CELL_SIZE - 200))

    rightinstruction = instruction_font.render("Right Click", True, WHITE)
    rightinstruction_rect = rightinstruction.get_rect(center=(x_offset + GRID_SIZE * CELL_SIZE + 200, y_offset + GRID_SIZE * CELL_SIZE - 150))

    rightsubinstruction = subinstruction_font.render("Vertical Alignment", True, GREEN)
    rightsubinstruction_rect = rightsubinstruction.get_rect(center=(x_offset + GRID_SIZE * CELL_SIZE + 200, y_offset + GRID_SIZE * CELL_SIZE - 120 ))
    
    window.blit(titleinstruction, titleinstruction_rect)
    window.blit(leftinstruction, leftinstruction_rect)
    window.blit(leftsubinstruction, leftsubinstruction_rect)
    window.blit(rightinstruction, rightinstruction_rect)
    window.blit(rightsubinstruction, rightsubinstruction_rect)
