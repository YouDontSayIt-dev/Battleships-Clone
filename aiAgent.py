import random

import gameLogic

from globalVariables import *
from boardSettings import *

packed_item = ()

def ai_turn(player1_grid):
    global AI_hits
    print("AI SHOTS: ", AI_shots)
    if len(AI_hits) == 0:
        print("\t\tRANDOM MODE")
        random_choice = random.sample(AI_shots, len(AI_shots))
        print("Random Choice: ", random_choice)
        row, col = random_choice[0]
        
        result = gameLogic.check_hit(row, col, player1_grid)
        if result == "MISS":
            packed_item = (row,col)
            AI_shots.remove(packed_item)
            

        elif result == "HIT":
            packed_item = (row,col)
            AI_shots.remove(packed_item)
            AI_hits.append((row, col))
            if gameLogic.check_game_over(player1_grid):
                game_over = True
                return game_over
    else:
        last_shot = AI_hits[-1]
        print("\t\tSEARCH MODE")
        row, col = search_neighboring_cells(last_shot, player1_grid)
        result = gameLogic.check_hit(row, col, player1_grid)
        if result == "HIT":
            AI_hits.append((row, col))

        if gameLogic.check_game_over(player1_grid):
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
            del AI_hits[0]
            continue

        # Check if the new coordinates are valid and unexplored
        print(new_row, new_col)
        new_row += dx
        new_col += dy
        if (
            is_valid_coordinate(new_row, new_col)
            and (new_row, new_col) not in AI_hits
            and (new_row, new_col) in AI_shots
        ):
            # If unexplored cell found, target it
            print("\t\tDIRECTION CELL")
            hitflag += 1
            packed_item = (new_row,new_col)
            AI_shots.remove(packed_item)
            return new_row, new_col

        # If the new coordinates are invalid or already explored, change direction
        elif (
            not is_valid_coordinate(new_row, new_col)
            or (new_row, new_col) in AI_hits
            and (new_row, new_col) not in AI_shots
        ):
            print("\t\tRANDOM CELL")
            hitflag += 1
            random_choice = random.sample(AI_shots, len(AI_shots))
            print("Random Choice: ", random_choice)
            new_row, new_col = random_choice[0]
            packed_item = (new_row,new_col)
            AI_shots.remove(packed_item)
            break

    return new_row, new_col


# Function to check if the coordinate is within the grid
def is_valid_coordinate(row, col):
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE
