import random
from modules.ai.tools import check_if_valid_tile

class AI:
    def __init__(self, color, civ_name):
        self.color = color
        self.start_pos = (random.randint(0, 100), random.randint(0, 100)) # Random start position
        self.name = civ_name

        