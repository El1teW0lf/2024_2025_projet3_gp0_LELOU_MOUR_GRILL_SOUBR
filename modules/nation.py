import random
import math

class Nation:
    def __init__(self, map):
        self.ai = None
        self.map = map
        self.value = 0
        self.tiles = []

        # Nation-wide resources
        self.ressources = {
            "money": 10000,
            "population": 0,
            "Flowers": 0,
            "Sand": 0,
            "Snow": 0,
            "Algae": 0,
            "Cactus": 0,
            "Wood": 0,
            "Water": 0,
            "Ice": 0,
            "Coal": 0,
            "Iron": 0,
            "Redstone": 0,
            "Gold": 0,
            "Magma": 0,
            "Diamond": 0,
            "Emerald": 0
        }

        self.war = None
        self.name = self.create_name()
        self.color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
        self.score = 0

        print(f"Created New Nation {self.name}")

    def create_name(self):
        # Generates a fantasy-style nation name
        names1 = ["ae", "ea", "ai", "au", "ou", "a", "e", "i", "o", "u"] * 3 + [""] * 60
        names2 = ["ae", "eo", "ea", "ai", "ui", "ou", "a", "e", "i", "o", "u"] * 2
        names3 = ["b", "c", "d", "g", "h", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z",
                  "br", "cr", "dr", "gr", "kr", "pr", "tr", "vr", "wr", "st", "sl", "ch", "sh", "ph", "kh", "th"]
        names4 = names3 * 3 + ["f", "bb", "cc", "dd", "ff", "gg", "kk", "ll", "mm", "nn", "pp", "rr", "ss", "tt", "zz"]
        names5 = [ # Location and suffix names
            "ba", "bet", "bia", "borg", "burg", "ca", "caea", "can", "cia", "curia", "dal", "del", "dia", "dian",
            "do", "dor", "dora", "dour", "galla", "gary", "gia", "gon", "han", "kar", "kha", "kya", "les", "lia", 
            "lon", "lan", "lum", "lux", "lyra", "mid", "mor", "more", "nad", "nait", "nao", "nate", "nada", "neian",
            "nem", "nia", "nid", "niel", "ning", "ntis", "nyth", "pan", "phate", "pia", "pis", "ra", "ral", "rean",
            "rene", "renth", "ria", "rian", "rid", "rin", "ris", "rith", "rus", "ryn", "sal", "san", "sea", "seon",
            "sha", "sian", "site", "sta", "ston", "teron", "terra", "tha", "thage", "then", "thia", "tia", "tis",
            "tish", "ton", "topia", "tor", "tus", "valon", "varia", "vell", "ven", "via", "viel", "wen", "weth",
            "wyth", "ya", "zar", "zia"
        ]
        names6 = ["Kingdom", "Empire", "Dynasty", "Republic", "Theocracy", "Autocracy"]

        # Construct one name per call
        name = random.choice(names1) + random.choice(names3) + random.choice(names2) + random.choice(names5)
        full_name = f"{name.capitalize()} {random.choice(names6)}"
        return full_name

    def set_population(self):
        # Updates total population from all owned tiles
        self.ressources["population"] = sum(tile.pop for tile in self.tiles)

    def conquer(self, tile):
        # Attempts to claim an unclaimed tile
        if tile.nation is None and tile.value <= self.ressources["money"]:
            tile.nation = self
            self.tiles.append(tile)
            self.ressources["money"] -= tile.value
            self.set_population()
            return True
        return False

    def _get_score(self):
        # Computes the score of a nation based on resources and tile values
        self.score = ((self.ressources["money"] + self.ressources["population"]) / 100000)**2
        multiplier = 1 + sum(tile.value for tile in self.tiles)/len(self.tiles)
        self.score *= multiplier

    def _possible_conquer(self):
        # Returns a list of tiles the nation could potentially conquer
        possibles = []
        for tile in self.tiles:
            directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                x, y = max(0, min(99, tile.x + dx)), max(0, min(99, tile.y + dy))
                new_tile = self.map.map[x, y]
                if new_tile.value <= self.ressources["money"] and new_tile.biome != "water":
                    possibles.append(new_tile)
        return possibles

    def _is_stuck(self):
        #Check if a tile is tiles can still be conquered in the futur.
        possibles = []
        for tile in self.tiles:
            directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                x, y = max(0, min(99, tile.x + dx)), max(0, min(99, tile.y + dy))
                new_tile = self.map.map[x, y]
                if new_tile.biome != "water":
                    possibles.append(new_tile)
        return len(possibles)<=0


    def tick(self):
        # Called every turn to update economic and scoring state
        self.ressources["money"] += self.ressources["population"] * 0.1
        self._get_score()
