import pygame

# Set the dimensions of the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Set the colors
VIOLET = (76, 63, 84) #bg of the game
WHITE = (255, 255, 255) #grid lines
MUSTARD = (218, 165, 32)  # Mustard. intial color of the ships
BLUE = (70, 130, 180) #color of the grid
DARKRED = (225,0,0) #Miss
RED = (213, 84, 64) #Quit hover
BROWN = (75,42,8)  # for the ships
GREEN = (175, 224, 144) #Play hover
BEIGE = (255,233,214) #instruction 
LIGHTB = (177,216,212) #Menu title
CREAM = (239,233,227) #intruction title
ORANGE = (248,164,136) #instruction title
PINK = (235,175,175) #Ship length label
DARKPINK = (230,132,128) #Commands
BROWND = (106,68,50) #subinstruction

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
                pygame.draw.rect(window, MUSTARD, (x, y, CELL_SIZE, CELL_SIZE)) #initial color of the ship
            elif grid[row][col] == 3:
                pygame.draw.rect(window, DARKRED, (x, y, CELL_SIZE, CELL_SIZE)) #missed
            elif grid[row][col] == 4:
                pygame.draw.rect(window, (BROWN), (x, y, CELL_SIZE, CELL_SIZE)) #once the ship is placed