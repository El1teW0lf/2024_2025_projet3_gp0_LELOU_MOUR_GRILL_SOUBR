import random
from modules.ai.tools import check_if_valid_tile, are_ais_at_war

frame_count = 0  # Global variable to track frames and slow expansion

def expand_ai(map, ai):
    # Get the current position of the AI's territory
    for x in range(100):
        for y in range(100):
            if map[y, x].has_ai and map[y, x].ai == ai:
                # Check adjacent tiles for possible expansion
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy

                    # Check if the new coordinates are within bounds
                    if 0 <= nx < 100 and 0 <= ny < 100:
                        tile = map[ny, nx]

                        # Check if the tile is valid for expansion (not occupied by friendly AI)
                        if tile.has_ai and tile.ai != ai:
                            # If the tile belongs to an enemy AI and they are at war, expand there
                            if are_ais_at_war(ai, tile.ai):  # Check if AI is at war with the tile's owner
                                # Conquer the tile: change ownership to the AI
                                tile.color = ai.color
                                tile.ai = ai
                                tile.has_ai = True
                                print(f"{ai.name} expanded into enemy territory at ({nx}, {ny})")
                        elif not tile.has_ai:  # If the tile is unoccupied, expand there
                            tile.color = ai.color
                            tile.ai = ai
                            tile.has_ai = True
                            print(f"{ai.name} expanded into empty territory at ({nx}, {ny})")
