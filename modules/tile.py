import random
import math
from modules.generation.biomes import biomes
from modules.ai.training import score_tile

class Tile():
    def __init__(self, x, y, biome):
        self.x = x
        self.y = y
        self.biome = biome
        self.color = biomes[self.biome]["color"]
        self.original_color = biomes[self.biome]["color"]
        self._nation = None
        self.value = 100

    def combine_hex_values(self,d):
        d_items = sorted(d.items())
        tot_weight = sum(d.values())
        red = int(sum([int(k[:2], 16)*v for k, v in d_items])/tot_weight)
        green = int(sum([int(k[2:4], 16)*v for k, v in d_items])/tot_weight)
        blue = int(sum([int(k[4:6], 16)*v for k, v in d_items])/tot_weight)
        zpad = lambda x: x if len(x)==2 else '0' + x
        return zpad(hex(red)[2:]) + zpad(hex(green)[2:]) + zpad(hex(blue)[2:])

    @property
    def nation(self):
        return self._nation
    
    @nation.setter
    def nation(self,nation):
        self._nation = nation
        self.color = self.combine_hex_values({self.color: 0.1, nation.color: 1})

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
        print(f"Tile {self.x} {self.y} {self.biome} | "
            f"Resources: {self.mine_ressources} {self.surface_ressources} | "
            f"Population: {self.pop} | Temperature: {self.temp} | ")
            

tile = Tile(52, 24, "mountain")
tile.setup()
print(score_tile(tile))