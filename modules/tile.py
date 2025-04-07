import random
import math
from modules.generation.biomes import biomes


class Tile():
    def __init__(self, x, y, biome):
        self.x = x
        self.y = y
        self._biome = biome
        self.color = biomes[self.biome]["color"]
        self.original_color = biomes[self.biome]["color"]
        self._nation = None
        self.value = -0 # <-- -0 c'est quand même une dinguerie

    def combine_hex_values(self, d):
    # Ensure the hex colors are 6 characters long (without the '#')
        def ensure_full_hex(hex_value):
            # Remove the '#' and pad with zeros if necessary
            hex_value = hex_value.lstrip('#')
            if len(hex_value) == 3:  # e.g., 'abc' -> 'a00b00c'
                hex_value = ''.join([c * 2 for c in hex_value])
            return hex_value.zfill(6)  # Ensure the hex is 6 characters long
        
        # Apply ensure_full_hex to all items in d
        d_items = {ensure_full_hex(k): v for k, v in d.items()}
        
        tot_weight = sum(d.values())
        
        # Extract the red, green, and blue components
        red = int(sum([int(k[:2], 16) * v for k, v in d_items.items()]) / tot_weight)
        green = int(sum([int(k[2:4], 16) * v for k, v in d_items.items()]) / tot_weight)
        blue = int(sum([int(k[4:6], 16) * v for k, v in d_items.items()]) / tot_weight)
        
        # Pad single digit hex values with leading zeroes
        zpad = lambda x: x if len(x) == 2 else '0' + x
    
        # Return combined hex value (without the '#')
        return zpad(hex(red)[2:]) + zpad(hex(green)[2:]) + zpad(hex(blue)[2:])


    @property
    def biome(self):
        return self._biome
    
    @biome.setter
    def biome(self,biome):
        self._biome = biome
        self.color = biomes[self.biome]["color"]
        self.original_color = biomes[self.biome]["color"]
        self._generate_ressources()
        self._generate_other()

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
        self.value = self.score_tile()

    def print_debug(self):
        print(self.get_debug())
        
    def get_debug(self):
        return f"Tile {self.x} {self.y} {self.biome} \n "+f"Resources: {self.mine_ressources} {self.surface_ressources} \n "+ f"Population: {self.pop} \n Temperature: {self.temp} \n Value: {self.value}"
            

    def score_tile_resources(self):
        score = 0

        resources_ranking = [
            "Flowers", "Sand", "Snow", "Algae", "Cactus", "Wood", "Water", "Ice",
            "Coal", "Iron", "Redstone", "Gold", "Magma", "Diamond", "Emerald"
        ]

        combined_resources = {}

        for res, qty in self.surface_ressources.items():
            combined_resources[res] = combined_resources.get(res, 0) + qty

        for res, qty in self.mine_ressources.items():
            combined_resources[res] = combined_resources.get(res, 0) + qty

        for resource, quantity in combined_resources.items():
            if resource in resources_ranking:
                weight = resources_ranking.index(resource) + 1
                score += weight * quantity

        return score

    def score_tile_biome(self):
        biomes_score = {
            "plains": 5,
            "forest": 4,
            "mountain": 3,
            "desert": 2,
            "volcano": 0,
            "snow": 1,
            "water": 0
        }
        return biomes_score.get(self.biome, 0) * 50


    def score_tile_temperature(self):
        t = self.temp
        score = (-0.1 * t) * (t - 40)
        return score

    def score_tile(self):
        score = 0
        score += self.score_tile_resources()
        score += self.score_tile_biome()
        score += self.score_tile_temperature()
        return int(score)