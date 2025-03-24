import random
import math
from modules.generation.biomes import biomes

class Tile():
    def __init__(self, x, y, biome):
        self.x = x
        self.y = y
        self.biome = biome

    def _generate_ressources(self):
        self.mine_ressources = {}
        self.surface_ressources = {} 

        for i in biomes[self.biome]["resources"]["surface"]:
            self.surface_ressources[i] = random.randint(5, 15)
        
        for i in biomes[self.biome]["resources"]["underground"]:
            self.mine_ressources[i] = random.randint(5, 15)

    def _generate_other(self):
        self.pop = max(0,random.randint(int(biomes[self.biome]["population"]/2),int(biomes[self.biome]["population"]*2)))
        self.temp = random.randint(biomes[self.biome]["temperature"]-5,biomes[self.biome]["temperature"]+5)

        
    def setup(self):
        self._generate_ressources()
        self._generate_other()

    def print_debug(self):
        print(f"Tile {self.x} {self.y} {self.biome}")
        print(f"ressources : {self.mine_ressources} {self.surface_ressources}")
        print(f"population : {self.pop}")
        print(f"temperature : {self.temp}")