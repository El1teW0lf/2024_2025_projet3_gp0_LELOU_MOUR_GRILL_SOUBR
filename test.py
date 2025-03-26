import numpy as np
import random
import matplotlib.pyplot as plt
from noise import pnoise2

def generate_worley_noise(width, height, num_points):
    noise_matrix = np.zeros((height, width, 3))
    points = [(random.randint(0, width-1), random.randint(0, height-1)) for _ in range(num_points)]
    colors = [np.random.rand(3,) for _ in range(num_points)]
    
    for y in range(height):
        for x in range(width):
            min_dist = float('inf')
            color = None
            for i, (px, py) in enumerate(points):
                dist = np.sqrt((x - px)**2 + (y - py)**2)
                if dist < min_dist:
                    min_dist = dist
                    color = colors[i]
            noise_matrix[y, x] = color
    
    return noise_matrix


width, height = 100, 100
num_points = 10

noise = generate_worley_noise(width, height, num_points)

plt.imshow(noise)
plt.title('2D Worley Noise with Perlin Noise')
plt.axis('off')
plt.show()
