from modules.tile import Tile
import random
import numpy as np
import noise

biomes = ["plains", "forest", "mountain", "desert", "volcano", "snow", "water"]

def generate_perlin_noise(width=100, height=100, scale=10):
    noise_map = np.zeros((height, width))
    
    for y in range(height):
        for x in range(width):
            noise_value = noise.pnoise2(x / scale, y / scale, octaves=4, persistence=0.5, lacunarity=2.0)
            noise_map[y, x] = noise_value
    
    noise_map = (noise_map - noise_map.min()) / (noise_map.max() - noise_map.min()) * 6
    noise_map = noise_map.astype(int)
    
    return noise_map

