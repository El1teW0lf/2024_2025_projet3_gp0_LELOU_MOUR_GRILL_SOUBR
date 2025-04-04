import random
from modules.ai.tools import check_if_valid_tile

class AI:
    def __init__(self, map,nation):
        self.nation = nation
        self.map = map
        self.start_pos = self.find_start_pos()
        
        self.nation.ai = self
        self.nation.conquer(self.map.map[self.start_pos[0],self.start_pos[1]])

    
    def find_start_pos(self):
        possible = (random.randint(0, 99), random.randint(0, 99))
        while self.map.map[possible[0],possible[1]] == "water":
            possible = (random.randint(0, 99), random.randint(0, 99))

        return possible
        