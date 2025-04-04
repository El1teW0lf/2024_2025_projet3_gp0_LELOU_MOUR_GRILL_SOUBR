from modules.tile import Tile
from modules.generation.generation import generate_worley_noise,biomes
import numpy as np

class Map():
    def __init__(self,seed):
        
        self.size = (100,100)
        self.map =  np.empty(self.size, dtype=object)
        self.ais = None
        self.noise = generate_worley_noise(num_points = 100)
        self._populate_map()

        for i in range(5):
            self._smooth()


    
    def _populate_map(self):
        for y in range(self.map.shape[0]):
            for x in range(self.map.shape[1]): 
                self.map[y, x] = Tile(y,x,biomes[int(self.noise[y,x])])
                self.map[y, x].setup()

    def _smooth(self):
        h, w = self.map.shape
        for y in range(h):
            for x in range(w):
                neighbors = [
                    self.map[ny][nx].biome
                    for ny, nx in [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
                    if 0 <= ny < h and 0 <= nx < w
                ]

                if neighbors:
                    counts = {}
                    for val in neighbors:
                        counts[val] = counts.get(val, 0) + 1
                    most_common = max(counts, key=counts.get)

                    self.map[y][x].biome = most_common