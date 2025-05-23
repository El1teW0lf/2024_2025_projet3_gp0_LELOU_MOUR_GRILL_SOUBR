from modules.tile import Tile
from modules.generation.generation import generate_worley_noise, biomes
import numpy as np
import random

class Map:
    def __init__(self, seed):
        random.seed(seed)  # Seed the RNG for reproducibility
        
        self.size = (100, 100)  # Size of the map (100x100 grid)
        self.map = np.empty(self.size, dtype=object)  # Initialize an empty numpy array to hold Tile objects
        self.ais = None  # Placeholder for AI systems, if any
        self.noise = generate_worley_noise(num_points=100)  # Generate a noise map to decide biome distribution

        self._populate_map()  # Fill the map with Tile objects

        # Smooth the map once to remove isolated biome tiles
        self._smooth()

    def _populate_map(self):
        # Iterate through the map and populate each position with a Tile object
        for y in range(self.size[0]):
            for x in range(self.size[1]):
                biome_index = int(self.noise[y, x])  # Get biome index from noise map
                biome = biomes[biome_index]  # Get biome data from biomes dictionary
                self.map[y, x] = Tile(y, x, biome)  # Create the tile
                self.map[y, x].setup()  # Generate resources, temperature, population, etc.

    def _smooth(self):
        h, w = self.map.shape  # Height and width of the map

        # Go through every tile in the map
        for y in range(h):
            for x in range(w):
                # Get the biomes of the 4 adjacent neighbors (N, S, E, W)
                neighbors = [
                    self.map[ny, nx].biome
                    for ny, nx in [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
                    if 0 <= ny < h and 0 <= nx < w  # Make sure the neighbor is within bounds
                ]

                if neighbors:
                    biome_counts = {}
                    # Count how many times each biome appears among the neighbors
                    for biome in neighbors:
                        biome_counts[biome] = biome_counts.get(biome, 0) + 1

                    # Find the most common biome among the neighbors
                    most_common = max(biome_counts, key=biome_counts.get)
                    most_count = biome_counts[most_common]

                    # If the most common biome appears 3 or more times, smooth the tile to match it
                    if most_count >= 3:
                        self.map[y, x].biome = most_common
