# Scoring des ressources
def score_tile_resources(tile):
    score = 0

    resources_ranking = [
        "Flowers", "Sand", "Snow", "Algae", "Cactus", "Wood", "Water", "Ice",
        "Coal", "Iron", "Redstone", "Gold", "Magma", "Diamond", "Emerald"
    ]

    combined_resources = {}

    # Combine surface and underground resources
    for res, qty in tile.surface_ressources.items():
        combined_resources[res] = combined_resources.get(res, 0) + qty

    for res, qty in tile.mine_ressources.items():
        combined_resources[res] = combined_resources.get(res, 0) + qty

    for resource, quantity in combined_resources.items():
        if resource in resources_ranking:
            # Higher index = more important = higher weight
            weight = resources_ranking.index(resource) + 1
            score += weight * quantity

    return score

# Scoring du biome
def score_tile_biome(tile):
    biomes_score = {
        "plains": 5,
        "forest": 4,
        "mountain": 3,
        "desert": 2,
        "volcano": 0,
        "snow": 1,
        "water": 0
    }
    return biomes_score.get(tile.biome, 0)

# Scoring de la température
def score_tile_temperature(tile):
    t = tile.temp
    score = (-0.1 * t) * (t - 40)
    return score

# Scoring total
def score_tile(tile):
    score = 0
    score += score_tile_resources(tile)
    score += score_tile_biome(tile)
    score += score_tile_temperature(tile)
    return score

# Choix de la meilleure tuile
def choose_best_tile(current_tile, neighbors):
    best_tile = current_tile
    best_score = score_tile(current_tile)

    for neighbor in neighbors:
        neighbor_score = score_tile(neighbor)
        if neighbor_score > best_score:
            best_score = neighbor_score
            best_tile = neighbor

    return best_tile

# Classe de l'explorateur intelligent
class Explorer:
    def __init__(self, current_tile):
        self.current_tile = current_tile

    def explore(self, neighbors):
        next_tile = choose_best_tile(self.current_tile, neighbors)
        if next_tile != self.current_tile:
            print("📦 Déplacement vers une meilleure tuile. Score:", score_tile(next_tile))
        else:
            print("✅ Rester sur la tuile actuelle. Score:", score_tile(self.current_tile))
        self.current_tile = next_tile
