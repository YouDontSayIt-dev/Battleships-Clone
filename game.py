import pygame
import random

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Set the colors
BLACK = (76, 63, 84) #pastelgreen137, 207, 240
WHITE = (255, 255, 255)
GRAY = (218, 165, 32) #Mustard
BLUE = (70, 130, 180) 
RED = (138, 51, 36)
FIG = (138, 51, 36) #for the ships

# Set the size of the grids
GRID_SIZE = 10
ATTACK_SIZE = 20
CELL_SIZE = WINDOW_HEIGHT // GRID_SIZE

# Set the gap between the grids
GAP = 10

# Set the number of battleships
SHIP_LENGTHS = [5, 4, 3, 3, 2]

# Create the window
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Battleship Game")

# Create player 1 and player 2 grids
player1_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
AI_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Array for AI's used attacks
AI_shots = []
AI_hits = []


# Hit flag
hitflag = 0

# Turn font
turnFont = pygame.font.Font(None, 36)

# Turn counter
turnCount = 1
countFlag = 0


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
                pygame.draw.rect(window, (159, 129, 112), (x, y, CELL_SIZE, CELL_SIZE))


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
    superPos = 2
    superNeg = -2
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
        # elif hitflag == 4:
        #             dx += superNeg
        #             dy += neutral
        # elif hitflag == 5:
        #             dx += neutral
        #             dy += superNeg
        else:
            hitflag = 0

        # Check if the new coordinates are valid and unexplored
        print("BEFORE CHECKING")
        print(new_row, new_col)
        new_row += dx
        new_col += dy
        if (
            is_valid_coordinate(new_row, new_col)
            and (new_row, new_col) not in AI_hits
            and (new_row, new_col) not in AI_shots
        ):
            # If unexplored cell found, target it
            print("FOUND")
            hitflag += 1
            return new_row, new_col

        # If the new coordinates are invalid or already explored, change direction
        elif (
            not is_valid_coordinate(new_row, new_col)
            or (new_row, new_col) in AI_hits
            and (new_row, new_col) in AI_shots
        ):
            print("NOT FOUND")
            hitflag = 0
            del AI_hits[0]
            break

    return random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)


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

# Global variables for text rectangles
play_rect = None
quit_rect = None


# Main menu
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

    header_text = header_font.render("WELCOME ABOARD!", True, (177,216,212))
    header_rect = header_text.get_rect()
    header_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80)
    window.blit(header_text, header_rect)

    title_text = title_font.render("BATTLESHIPS", True, (232,187,149))
    title_rect = title_text.get_rect()
    title_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20)
    window.blit(title_text, title_rect)

    play_text = commands_font.render("Play", True, (230,132,128))
    play_rect = play_text.get_rect()
    play_rect.center = (WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2 + 70)
    window.blit(play_text, play_rect)

    quit_text = commands_font.render("Quit", True, (230,132,128))
    quit_rect = quit_text.get_rect()
    quit_rect.center = (WINDOW_WIDTH // 2 + 60, WINDOW_HEIGHT // 2 + 70)
    window.blit(quit_text, quit_rect)

    sub_text = sub_font.render("cruz mamorno muyco", True, WHITE)
    sub_rect = sub_text.get_rect()
    sub_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 160)
    window.blit(sub_text, sub_rect)

    # Check if the mouse is hovering over the play or quit text
    mouse_pos = pygame.mouse.get_pos()
    if play_rect.collidepoint(mouse_pos):
        play_text = commands_font.render("Play", True, (63, 193, 136))
        window.blit(play_text, play_rect)
    if quit_rect.collidepoint(mouse_pos):
        quit_text = commands_font.render("Quit", True, (	213, 84, 64))
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


# Call the main menu function to start the game
main_menu()

# Main game loop
running = True
turnCount = 1
game_over = False

# Place ships on player 1 and player 2 grids
place_ships(player1_grid, SHIP_LENGTHS)
place_ships_AI(AI_grid, SHIP_LENGTHS)

HEADER_HEIGHT = 60
pygame.display.set_mode((WINDOW_WIDTH + GAP, WINDOW_HEIGHT + HEADER_HEIGHT))

while running:

    # Render the turn count text
    text = turnFont.render("Turn: {}".format(turnCount), True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (WINDOW_WIDTH // 2, 30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouse_pos = pygame.mouse.get_pos()

            mouse_pos_0 = mouse_pos[0]
            mouse_pos_1 = mouse_pos[1]

            # Remove HEADER_HEIGHT from coordinate
            mouse_pos_1 -= HEADER_HEIGHT

            # Remove GAP from coordinate if it is in right grid
            if mouse_pos_0 > CELL_SIZE * GRID_SIZE:
                mouse_pos_0 -= GAP

            clicked_row = mouse_pos_1 // CELL_SIZE
            clicked_col = mouse_pos_0 // CELL_SIZE
            # if (clicked_row, clicked_col) in Player_shots:
            #     print("You already shot here")
            #     mouse_pos = pygame.mouse.get_pos()
            #     clicked_row = mouse_pos[1] // CELL_SIZE
            #     clicked_col = mouse_pos[0] // CELL_SIZE
            # else:
            if (
                clicked_row >= 0
                and clicked_row < ATTACK_SIZE
                and clicked_col >= 0
                and clicked_col < ATTACK_SIZE
            ):
                turn_label = font.render("PLAYER 1 TURN", True, WHITE)
                print(clicked_row, clicked_col)
                clicked_col -= ATTACK_SIZE
                result = check_hit(clicked_row, clicked_col, AI_grid)
                print("Player's Attack Coordinates: ", clicked_row, clicked_col, result)
                Player_shots.append((clicked_row, clicked_col))
                if result == "HIT":
                    if check_game_over(AI_grid):
                        game_over = True
                ai_turn(player1_grid)
                if check_game_over(player1_grid):
                    game_over = True
                # Increment the turn count
                turnCount += 1

    # Clear the window
    window.fill(BLACK)

    # Draw the header
    pygame.draw.rect(window, BLACK, (0, 0, WINDOW_WIDTH, HEADER_HEIGHT))
    window.blit(text, text_rect)

    # Draw player 1 grid
    draw_grid(0, HEADER_HEIGHT, player1_grid)

    # Draw player 2 grid
    draw_grid(GRID_SIZE * CELL_SIZE + GAP, HEADER_HEIGHT, AI_grid)

    # Draw grid labels
    font = pygame.font.Font(None, 36)

    # Draw the turn count text
    window.blit(text, text_rect)

    # Draw game over message
    if game_over:
        if check_game_over(player1_grid):
            game_over_label = font.render("AI Wins", True, WHITE)
        else:
            game_over_label = font.render("PLAYER 1 WINS", True, WHITE)
        window.blit(game_over_label, (WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 - 20))
    
    #Update the game display
    pygame.display.update()


# Quit the game
pygame.quit()
