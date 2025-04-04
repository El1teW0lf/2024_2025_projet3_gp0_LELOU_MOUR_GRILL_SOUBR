

def check_if_valid_tile(tile, ai=None):
    # Tile is valid if it is either unoccupied or occupied by an enemy AI that the current AI is at war with
    if tile.has_ai or tile.biome in ["water", "volcano"]:
        return False
    # Add more conditions if there are other valid tile checks (e.g., terrain, obstacles)
    return True  # Tile is valid for expansion


def are_ais_at_war(ai1, ai2):
    return ai1.is_at_war(ai2) or ai2.is_at_war(ai1)

def are_ais_bordering(map, ai1, ai2):
    """
    Checks if two AIs are bordering each other.

    Parameters:
    map (2D array): The game map.
    ai1 (AI object): The first AI.
    ai2 (AI object): The second AI.

    Returns:
    bool: True if ai1 and ai2 are bordering, False otherwise.
    """
    # Define the directions to check (Up, Down, Left, Right, and Diagonals)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),  # Cardinal directions
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions

    for y in range(100):
        for x in range(100):
            if map[y, x].has_ai and map[y, x].ai == ai1:  # AI1's tile
                # Check all 8 neighboring tiles
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 100 and 0 <= ny < 100:
                        if map[ny, nx].has_ai and map[ny, nx].ai == ai2:
                            return True  # Found neighboring tile controlled by AI2
    return False  # No bordering tiles found