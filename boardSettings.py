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

            # Draw different colors based on the grid value
            if grid[row][col] == 2:
                pygame.draw.rect(window, MUSTARD, (x, y, CELL_SIZE, CELL_SIZE))
            elif grid[row][col] == 3:
                pygame.draw.rect(window, DARKRED, (x, y, CELL_SIZE, CELL_SIZE))
            elif grid[row][col] == 4:
                pygame.draw.rect(window, (BROWN), (x, y, CELL_SIZE, CELL_SIZE))

    # Add instruction box on the other side of the grid
    instruction_box = pygame.Rect(x_offset + GRID_SIZE * CELL_SIZE + 20, y_offset + GRID_SIZE * CELL_SIZE - 245, 362, 110)
    pygame.draw.rect(window, CREAM, instruction_box)

    titleinstruction_font = pygame.font.SysFont('Impact', 50)
    instruction_font = pygame.font.SysFont('Impact', 35)
    subinstruction_font = pygame.font.SysFont('Impact', 20)

    titleinstruction = titleinstruction_font.render("SHIP PLACEMENT", True, CREAM)
    titleinstruction_rect = titleinstruction.get_rect(center=(x_offset + GRID_SIZE * CELL_SIZE + 200, y_offset + GRID_SIZE * CELL_SIZE - 270))

    leftinstruction = instruction_font.render("LEFT CLICK", True, (0,0,0))
    leftinstruction_rect = leftinstruction.get_rect(center=(x_offset + GRID_SIZE * CELL_SIZE + 100, y_offset + GRID_SIZE * CELL_SIZE - 215))

    leftsubinstruction = subinstruction_font.render("HORIZONTAL ALIGNMENT", True, BROWND)
    leftsubinstruction_rect = leftsubinstruction.get_rect(center=(x_offset + GRID_SIZE * CELL_SIZE + 275, y_offset + GRID_SIZE * CELL_SIZE - 215))

    rightinstruction = instruction_font.render("RIGHT CLICK", True, (0,0,0))
    rightinstruction_rect = rightinstruction.get_rect(center=(x_offset + GRID_SIZE * CELL_SIZE + 113, y_offset + GRID_SIZE * CELL_SIZE - 170))

    rightsubinstruction = subinstruction_font.render("VERTICAL ALIGMENT", True, BROWND)
    rightsubinstruction_rect = rightsubinstruction.get_rect(center=(x_offset + GRID_SIZE * CELL_SIZE + 290, y_offset + GRID_SIZE * CELL_SIZE - 170 ))
    
    window.blit(titleinstruction, titleinstruction_rect)
    window.blit(leftinstruction, leftinstruction_rect)
    window.blit(leftsubinstruction, leftsubinstruction_rect)
    window.blit(rightinstruction, rightinstruction_rect)
    window.blit(rightsubinstruction, rightsubinstruction_rect)
