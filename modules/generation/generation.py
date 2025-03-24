from modules.tile import Tile
import random
import numpy as np

biomes = ["plains", "forest", "mountain", "desert", "volcano", "snow", "water"]

def generate_map():
    # Create an empty 100x100 NumPy array of objects
    random_map = np.empty((100, 100), dtype=object)

    # Fill the array with Tile objects
    for x in range(100):
        for y in range(100):
            tile = Tile(x, y, random.choice(biomes)) 
            tile.setup() # Keeping the tile variable
            random_map[x, y] = tile.biome  # Storing the tile in the matrix
    
    return random_map



