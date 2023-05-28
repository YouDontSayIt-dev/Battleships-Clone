from boardSettings import *


# Check if a coordinate is a hit or miss
def check_hit(row, col, target_grid):
    if target_grid[row][col] == 5 or target_grid[row][col] == 4:  # Check if the player's battleship is hit
        target_grid[row][col] = 2
        return "HIT"
    else:
        target_grid[row][col] = 3
        return "MISS"



# Check if all ships are hit on a grid
def check_game_over(grid):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 5:
                return False
            if grid[row][col] == 4:
                return False
            
    return True