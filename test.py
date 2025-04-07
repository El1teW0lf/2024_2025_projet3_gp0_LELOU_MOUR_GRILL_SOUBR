

def get_neighboring_tiles(tile, map):
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = tile.x + dx, tile.y + dy
        if 0 <= nx < 99 and 0 <= ny < 99:
            neighbors.append(map[ny, nx])
    return neighbors
