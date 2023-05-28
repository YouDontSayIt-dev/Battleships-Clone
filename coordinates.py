grid_size = 20

# Generate the list of coordinates
coordinates = []
for row in range(grid_size):
    for col in range(grid_size):
        coordinates.append((row, col))

# Print the list of coordinates
for coordinate in coordinates:
    print(coordinate)