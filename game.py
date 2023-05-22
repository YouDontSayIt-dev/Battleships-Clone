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
ATTACK_SIZE = 20
CELL_SIZE = WINDOW_HEIGHT // GRID_SIZE

# Set the gap between the grids
GAP = 10

# Set the number of battleships
SHIP_LENGTHS = [5]

# Create the window
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Battleship Game")

# Create player 1 and player 2 grids
player1_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
AI_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Array for AI's used attacks
AI_shots = []
AI_hits = []

hitflag = 0


# Array for Player's used attacks
Player_shots = []

# Place battleships randomly on the grids
def place_ships_AI(grid, ship_lengths):
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
            draw_grid(0, 0, player1_grid)

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
                        pygame.draw.rect(window, BLUE, ((col + i) * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif row + i < GRID_SIZE and pygame.mouse.get_pressed()[2] == 1:
                    if blink:
                        pygame.draw.rect(window, BLUE, (col * CELL_SIZE, (row + i) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif col + i < GRID_SIZE and row < GRID_SIZE:
                    if blink:
                        pygame.draw.rect(window, GRAY, ((col + i) * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif row + i < GRID_SIZE and col < GRID_SIZE:
                    if blink:
                        pygame.draw.rect(window, GRAY, (col * CELL_SIZE, (row + i) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.display.update()

            # Draw ship length label
            font = pygame.font.Font(None, 24)
            length_label = font.render("Length: " + str(length), True, WHITE)
            window.blit(length_label, (10, WINDOW_HEIGHT - 30))

            # Check for mouse click events
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the mouse click is within the grid bounds and the ship can be placed horizontally
                    if pygame.mouse.get_pressed()[0] == 1 and col + length <= GRID_SIZE and all(
                            grid[row][col + i] == 0 for i in range(length)):
                        for i in range(length):
                            grid[row][col + i] = 4

                        placed = True
                    # Check if the mouse click is within the grid bounds and the ship can be placed vertically
                    elif pygame.mouse.get_pressed()[2] == 1 and row + length <= GRID_SIZE and all(
                            grid[row + i][col] == 0 for i in range(length)):
                        for i in range(length):
                            grid[row + i][col] = 4

                        placed = True
                    else:
                        print("Invalid ship placement. Please try again.")

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
                pygame.draw.rect(window, (0, 255, 0), (x, y, CELL_SIZE, CELL_SIZE))

def ai_turn(player1_grid):
    global AI_hits
    print("AI HITS: ", AI_hits)
    if len(AI_hits) == 0:
        row = random.randint(0, GRID_SIZE - 1)
        col = random.randint(0, GRID_SIZE - 1)
        if (row, col) not in AI_shots:
            print("RANDOM MODE")
            result = check_hit(row, col, player1_grid)
            print("AI's Attack Coordinates: ", row, col, result)
            if result == "MISS":
                AI_shots.append((row, col))
                
            elif result == "HIT":
                AI_shots.append((row, col))
                AI_hits.append((row, col))
                if check_game_over(player1_grid):
                    game_over = True
                    return game_over
    else:
        last_shot = AI_hits[-1]
        print("SEARCH MODE")
        row, col = search_neighboring_cells(last_shot, player1_grid)
        result = check_hit(row, col, player1_grid)
        if result == "MISS":
                AI_shots.append((row, col))
        elif result == "HIT":
                AI_shots.append((row, col))
                AI_hits.append((row, col))
            
        print("AI's Attack Coordinates: ", row, col, result)
        if check_game_over(player1_grid):
            game_over = True
            return game_over

   
    # if (row, col) not in AI_shots:
    #         result = check_hit(row, col, player1_grid)
    #         print(result)
    #         if result == "MISS":
    #             AI_shots.append((row, col))
                
    #         elif result == "HIT":
    #             AI_shots.append((row, col))
    #             AI_hits.append((row, col))
    #             if check_game_over(player1_grid):
    #                 game_over = True
    #                 return game_over

def search_neighboring_cells(last_shot, player1_grid):
    print("SEARCHING")
    global hitflag
    row, col = last_shot
    dx = 0
    dy = 0
    
    # Define possible directions: up, down, left, right
    # directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    negHit = -1
    posHit = 1
    neutral = 0
    new_row = row
    new_col = col
    while True:
        # Keep moving in the current direction until an unexplored cell is found
        print("hitflag: ", hitflag)
        if hitflag == 0:
                    dx += negHit
                    dy += neutral
        elif hitflag == 1:
                    dx += posHit
                    dy += neutral
        elif hitflag == 2:
                    dx += neutral
                    dy += negHit
        elif hitflag == 3:
                    dx += neutral
                    dy += posHit
        else:
            hitflag = 0
            break
                    
        # Check if the new coordinates are valid and unexplored
        print("BEFORE CHECKING")
        print(new_row, new_col)
        new_row += dx
        new_col += dy
        if is_valid_coordinate(new_row, new_col) and (new_row, new_col) not in AI_hits and (new_row, new_col) not in AI_shots:
        # If unexplored cell found, target it
            print ("FOUND")
            hitflag += 1
            return new_row, new_col
            
            
        # If the new coordinates are invalid or already explored, change direction
        elif not is_valid_coordinate(new_row, new_col) or (new_row, new_col) in AI_hits and (new_row, new_col) not in AI_shots:
            print ("NOT FOUND")
            hitflag = 0
            del AI_hits[0]
            break
            
            
            
                    
    return random.randint(0, GRID_SIZE - 1),random.randint(0, GRID_SIZE - 1)
    


# Function to check if the coordinate is within the grid
def is_valid_coordinate(row, col):
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE           


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
place_ships_AI(AI_grid, SHIP_LENGTHS)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = pygame.mouse.get_pos()
            clicked_row = mouse_pos[1] // CELL_SIZE
            clicked_col = mouse_pos[0] // CELL_SIZE
            # if (clicked_row, clicked_col) in Player_shots:
            #     print("You already shot here")
            #     mouse_pos = pygame.mouse.get_pos()
            #     clicked_row = mouse_pos[1] // CELL_SIZE
            #     clicked_col = mouse_pos[0] // CELL_SIZE
            # else:
            if clicked_row >= 0 and clicked_row < ATTACK_SIZE and clicked_col >= 0 and clicked_col < ATTACK_SIZE:
                    if turn == 1:
                        turn_label = font.render("PLAYER 1 TURN", True, WHITE)
                        print(clicked_row, clicked_col)
                        clicked_col -= ATTACK_SIZE
                        result = check_hit(clicked_row, clicked_col, AI_grid)
                        print("Player's Attack Coordinates: ", clicked_row, clicked_col, result)
                        Player_shots.append((clicked_row, clicked_col))
                        if result == "HIT":
                            if check_game_over(AI_grid):
                                game_over = True
                        turn = 2
                        ai_turn(player1_grid)
                        if check_game_over(player1_grid):
                            game_over = True
                        turn = 1
                        
                        
                        

    # Clear the window
    window.fill(BLACK)

    # Draw player 1 grid
    draw_grid(0, 0, player1_grid)

    # Draw player 2 grid
    draw_grid(GRID_SIZE * CELL_SIZE + GAP, 0, AI_grid)

    # Draw grid labels
    font = pygame.font.Font(None, 36)

    # Draw game over message
    if game_over:
        if check_game_over(player1_grid):
            game_over_label = font.render("AI Wins", True, WHITE)
        else:
            game_over_label = font.render("PLAYER 1 WINS", True, WHITE)
        window.blit(game_over_label, (WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 - 20))

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()

