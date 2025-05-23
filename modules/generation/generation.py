from modules.tile import Tile
import random
import numpy as np
import math
import noise

# List of possible biome types
biomes = ["plains", "forest", "mountain", "desert", "volcano", "snow", "water"]

def generate_perlin_noise(width=100, height=100, scale=10):
    """
    Generate a Perlin noise map scaled to integer values from 0 to ~20.

    :param width: Width of the map
    :param height: Height of the map
    :param scale: Controls the zoom level of the noise
    :return: 2D NumPy array of scaled integer noise values
    """
    noise_map = np.zeros((height, width))

    for y in range(height):
        for x in range(width):
            # Generate 2D Perlin noise
            noise_value = noise.pnoise2(
                x / scale, y / scale,
                octaves=4,
                persistence=0.5,
                lacunarity=2.0
            )
            noise_map[y, x] = noise_value

    # Normalize to 0-20 and convert to integer
    noise_map = (noise_map - noise_map.min()) / (noise_map.max() - noise_map.min()) * 20
    return noise_map.astype(int)

def generate_worley_noise(width=100, height=100, num_points=10):
    """
    Generate a custom biome map based on Worley noise, influenced by Perlin noise.

    :param width: Width of the map
    :param height: Height of the map
    :param num_points: Number of seed points for the Worley noise
    :return: 2D NumPy array of biome indices
    """
    noise_matrix = np.zeros((height, width))

    if num_points < 7:
        raise ValueError("num_points must be at least 7 to ensure every value 0-6 is used.")

    # Randomly generate seed points
    points = [(random.randint(0, width - 1), random.randint(0, height - 1)) for _ in range(num_points)]

    # Ensure all 7 biome indices are used at least once
    values = list(range(7))
    random.shuffle(values)
    assigned_values = values[:7]

    # Assign weighted biome values to remaining points
    weights = [5, 4, 1, 2, 1, 1, 5]  # Favor plains, forest, and water
    remaining_values = random.choices(values, weights=weights, k=num_points - 7)
    values = assigned_values + remaining_values
    random.shuffle(values)

    # Shuffle all possible tile positions for iteration
    positions = [(x, y) for y in range(height) for x in range(width)]
    random.shuffle(positions)

    # Generate a Perlin noise map to use as distance influence
    perlin_noise = generate_perlin_noise()

    # Assign each tile to the closest seed point influenced by Perlin noise
    for x, y in positions:
        min_dist = float('inf')
        value = None
        for i, (px, py) in enumerate(points):
            dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
            # Modify distance using Perlin noise (adds terrain variability)
            if dist < min_dist:
                min_dist = perlin_noise[y, x] * 1  # Optional weighting
                value = values[i]
        noise_matrix[y, x] = value

    return noise_matrix
