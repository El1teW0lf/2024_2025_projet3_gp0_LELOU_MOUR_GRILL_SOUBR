import random
import math
from modules.generation.biomes import biomes


class Tile:
    def __init__(self, x, y, biome):
        # Tile position
        self.x = x
        self.y = y

        # Biome info
        self._biome = biome
        self.color = biomes[self.biome]["color"]
        self.original_color = biomes[self.biome]["color"]

        # Nation the tile belongs to
        self._nation = None

        # Value of the tile (used for scoring/AI)
        self.value = -0  # Yes, -0 is a curious but valid float in Python

    def combine_hex_values(self, d):
        """
        Combines hex colors weighted by values in dictionary `d`
        Example: { "#ff0000": 0.3, "#00ff00": 0.7 }
        Returns the blended hex color as a string.
        """
        def ensure_full_hex(hex_value):
            hex_value = hex_value.lstrip('#')
            if len(hex_value) == 3:
                hex_value = ''.join([c * 2 for c in hex_value])
            return hex_value.zfill(6)

        d_items = {ensure_full_hex(k): v for k, v in d.items()}
        tot_weight = sum(d.values())

        red = int(sum([int(k[:2], 16) * v for k, v in d_items.items()]) / tot_weight)
        green = int(sum([int(k[2:4], 16) * v for k, v in d_items.items()]) / tot_weight)
        blue = int(sum([int(k[4:6], 16) * v for k, v in d_items.items()]) / tot_weight)

        zpad = lambda x: x if len(x) == 2 else '0' + x
        return zpad(hex(red)[2:]) + zpad(hex(green)[2:]) + zpad(hex(blue)[2:])

    # --- Properties ---

    @property
    def biome(self):
        return self._biome

    @biome.setter
    def biome(self, biome):
        # When biome changes, update colors and regenerate resources/attributes
        self._biome = biome
        self.color = biomes[self.biome]["color"]
        self.original_color = biomes[self.biome]["color"]
        self._generate_ressources()
        self._generate_other()

    @property
    def nation(self):
        return self._nation

    @nation.setter
    def nation(self, nation):
        self._nation = nation
        # Blend tile color with nation color to show ownership
        self.color = self.combine_hex_values({self.color: 0.1, nation.color: 1})

    # --- Resource and attribute generation ---

    def _generate_ressources(self):
        self.mine_ressources = {}
        self.surface_ressources = {}

        for i in biomes[self.biome]["resources"]["surface"]:
            self.surface_ressources[i] = random.randint(5, 15)

        for i in biomes[self.biome]["resources"]["underground"]:
            self.mine_ressources[i] = random.randint(5, 15)

    def _generate_other(self):
        # Generate population and temperature within biome-specific ranges
        self.pop = max(0, random.randint(
            int(biomes[self.biome]["population"] / 2),
            int(biomes[self.biome]["population"] * 2)
        ))
        self.temp = random.randint(
            biomes[self.biome]["temperature"] - 5,
            biomes[self.biome]["temperature"] + 5
        )

    def setup(self):
        # Called to (re)initialize resources and attributes and compute tile value
        self._generate_ressources()
        self._generate_other()
        self.value = self.score_tile()

    # --- Debugging helpers ---

    def print_debug(self):
        print(self.get_debug())

    def get_debug(self):
        return (
            f"Tile {self.x} {self.y} {self.biome} \n "
            f"Resources: {self.mine_ressources} {self.surface_ressources} \n "
            f"Population: {self.pop} \n Temperature: {self.temp} \n Value: {self.value}"
        )

    # --- Scoring logic for AI/economy/etc. ---

    def score_tile_resources(self):
        score = 0
        # Ranked resource list by importance
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
        # Static biome score mapping
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
        # A quadratic curve to simulate ideal temperature
        t = self.temp
        score = -1/5 * t**2 + 6*t
        return score

    def score_tile(self):
        # Final score is a weighted sum of all scoring factors
        score = 0
        score += 2 * self.score_tile_resources()
        score += 1.5 * self.score_tile_biome()
        score += 1.25 * self.score_tile_temperature()
        return int(score)
