import random

class AI:
    def __init__(self, color, civ_names):
        self.color = color
        self.start_pos = (random.randint(0, 100), random.randint(0, 100)) # Random start position
        self.name = random.choice(civ_names)
    