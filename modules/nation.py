import random


class Nation():
    def __init__(self,map):
        self.ai = None
        self.map = map
        self.value = 0
        self.tiles = []
        self.ressources = {
            "money": 1000,
            "population":0
        }
        self.war = None
        self.name = self.create_name()
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.score = 0

        print(f"Created New Nation {self.name}")

    def create_name(self):
        names1 = ["ae", "ea", "ai", "au", "ou", "a", "e", "i", "o", "u"] * 3 + [""] * 60
        names2 = ["ae", "eo", "ea", "ai", "ui", "ou", "a", "e", "i", "o", "u"] * 2
        names3 = ["b", "c", "d", "g", "h", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z",
                "br", "cr", "dr", "gr", "kr", "pr", "tr", "vr", "wr", "st", "sl", "ch", "sh", "ph", "kh", "th"]
        names4 = ["b", "c", "d", "g", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z"] * 3 + \
                ["f", "bb", "cc", "dd", "ff", "gg", "kk", "ll", "mm", "nn", "pp", "rr", "ss", "tt", "zz", 
                "br", "cr", "dr", "gr", "kr", "pr", "sr", "tr", "zr", "st", "sl", "ch", "sh", "ph", "kh", "th"]
        names5 = ["ba", "bet", "bia", "borg", "burg", "ca", "caea", "can", "cia", "curia", "dal", "del", "dia", "dian", "do",
                "dor", "dora", "dour", "galla", "gary", "gia", "gon", "han", "kar", "kha", "kya", "les", "lia", "lon", "lan",
                "lum", "lux", "lyra", "mid", "mor", "more", "nad", "nait", "nao", "nate", "nada", "neian", "nem", "nia",
                "nid", "niel", "ning", "ntis", "nyth", "pan", "phate", "pia", "pis", "ra", "ral", "rean", "rene", "renth",
                "ria", "rian", "rid", "rin", "ris", "rith", "rus", "ryn", "sal", "san", "sea", "seon", "sha", "sian", "site",
                "sta", "ston", "teron", "terra", "tha", "thage", "then", "thia", "tia", "tis", "tish", "ton", "topia", "tor",
                "tus", "valon", "varia", "vell", "ven", "via", "viel", "wen", "weth", "wyth", "ya", "zar", "zia"]
        names6 = ["Kingdom", "Empire", "Dynasty", "Republic","Theocracy","Autocracy"]

        result = []

        for i in range(1):
            if i < 5:
                n = random.choice(names1) + random.choice(names3) + random.choice(names2) + random.choice(names5) + " " + random.choice(names6)
            else:
                rnd = random.choice(names1)
                rnd2 = random.choice(names3)
                rnd3 = random.choice(names2)
                while rnd3 in ["a", "e", "i", "o", "u", "ae"]:
                    rnd3 = random.choice(names2)
                rnd4 = random.choice(names4)
                rnd5 = random.choice(names2)
                while rnd5 in ["a", "e", "i", "o", "u", "ae"]:
                    rnd5 = random.choice(names2)
                rnd6 = random.choice(names5)
                rnd7 = random.choice(names6)
                n = rnd + rnd2 + rnd3 + rnd4 + rnd5 + rnd6 + " " + rnd7
            result = n.capitalize()

        return result

    def set_population(self):
        self.ressources["population"] = 0

        for i in self.tiles:
            self.ressources["population"] += i.pop
        
    def conquer(self,tile):
        if tile.nation == None and tile.value <= self.ressources["money"]:
            tile.nation = self
            self.tiles.append(tile)
            self.ressources["money"] -= tile.value
            return True
        return False