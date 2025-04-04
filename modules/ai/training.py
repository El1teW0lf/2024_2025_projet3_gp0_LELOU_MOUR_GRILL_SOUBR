

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

def score_tile_temperature(tile):
    t = tile.temp
    score = (-0.1*t)*(t-40)
    return score

def score_tile(tile):
    score = 0
    score += score_tile_resources(tile)
    score += score_tile_biome(tile)
    score += score_tile_temperature(tile)
    return score


    
