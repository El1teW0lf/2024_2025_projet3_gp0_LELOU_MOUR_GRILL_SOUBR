from modules.tile import Tile
import random
import numpy as np
import math
import noise

biomes = ["plains", "forest", "mountain", "desert", "volcano", "snow", "water"]

def generate_perlin_noise(width=100, height=100, scale=10):
    noise_map = np.zeros((height, width))
    
    for y in range(height):
        for x in range(width):
            noise_value = noise.pnoise2(x / scale, y / scale, octaves=4, persistence=0.5, lacunarity=2.0)
            noise_map[y, x] = noise_value
    
    noise_map = (noise_map - noise_map.min()) / (noise_map.max() - noise_map.min()) * 20
    noise_map = noise_map.astype(int)
    
    return noise_map

def generate_worley_noise(width=100, height=100, num_points=10):
    noise_matrix = np.zeros((height, width))
    
    if num_points < 7:
        raise ValueError("num_points must be at least 7 to ensure every value 0-6 is used.")
    
    points = [(random.randint(0, width-1), random.randint(0, height-1)) for _ in range(num_points)]
    
    values = list(range(7))
    random.shuffle(values)
    assigned_values = values[:7]
    
    values = [0, 1, 2, 3, 4, 5, 6]
    weights = [5, 4, 1, 2, 1, 1, 5] 


    remaining_values = random.choices(values, weights=weights, k=num_points - 7)
    values = assigned_values + remaining_values
    random.shuffle(values)
    
    positions = [(x, y) for y in range(height) for x in range(width)]

    random.shuffle(positions)

    perlin_noise = generate_perlin_noise()

    for x, y in positions:
            min_dist = float('inf')
            value = None
            for i, (px, py) in enumerate(points):
                dist = math.sqrt((x - px)**2 + (y - py)**2)
                if dist < min_dist:
                    min_dist = perlin_noise[y,x]*1
                    value = values[i]
            noise_matrix[y, x] = value
    
    return noise_matrix