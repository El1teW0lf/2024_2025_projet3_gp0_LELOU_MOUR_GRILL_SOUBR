import numpy as np
import noise
import matplotlib.pyplot as plt

def generate_perlin_noise(width, height, scale=10):
    noise_map = np.zeros((height, width))
    
    for y in range(height):
        for x in range(width):
            noise_value = noise.pnoise2(x / scale, y / scale, octaves=4, persistence=0.5, lacunarity=2.0)
            noise_map[y, x] = noise_value
    
    # Normalize to range 0-8 as integers
    noise_map = (noise_map - noise_map.min()) / (noise_map.max() - noise_map.min()) * 5
    noise_map = noise_map.astype(int)
    
    return noise_map

def display_noise_map(noise_map):
    plt.figure(figsize=(6,6))
    plt.imshow(noise_map, cmap='gray', interpolation='nearest')
    plt.colorbar()
    plt.show()

# Generate and display Perlin noise map
width, height = 100, 100
noise_map = generate_perlin_noise(width, height)
display_noise_map(noise_map)