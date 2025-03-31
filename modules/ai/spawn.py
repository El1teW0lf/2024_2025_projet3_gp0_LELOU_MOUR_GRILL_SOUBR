from modules.ai.ai import AI
from modules.ai.tools import check_if_valid_tile
import random

def create_ais(number, colors, civ_names):
    ais = []
    for _ in range(number):
        color = random.choice(colors)
        colors.remove(color)
        name = random.choice(civ_names)
        civ_names.remove(name)
        ai = AI(color, name)
        ais.append(ai)
    return ais

def handle_spawn(colors, civ_names, map):
    number = 8
    ais = create_ais(number, colors, civ_names)
    map.ais = ais
    map = map.map
    for ai in ais:
        x, y = ai.start_pos  # Get starting position

        found = False

        # First, try shifting X only
        for _ in range(100):  
            if check_if_valid_tile(map[y, x], ai):
                found = True
                break
            x = (x + 1) % 100  # Wrap around horizontally if needed

        # If no valid X found, shift Y
        if not found:
            for _ in range(100):  
                if check_if_valid_tile(map[y, x], ai):
                    found = True
                    break
                y = (y + 1) % 100  # Wrap around vertically

        # Ensure a valid tile is assigned
        if found:
            ai.start_pos = (x, y)
            map[y, x].color = ai.color
            map[y, x].has_ai = True
            map[y, x].ai = ai
        else:
            print("No valid spawn found for AI:", ai.name)



