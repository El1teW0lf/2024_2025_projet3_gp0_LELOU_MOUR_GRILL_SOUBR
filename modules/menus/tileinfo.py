class TileInfo:
    def __init__(self, tile_pos, tile):
        self.tile_pos = tile_pos
        self.tile = tile

    def get_info_lines(self):
        lines = [
            f"Tile : ({self.tile_pos[0]}, {self.tile_pos[1]})",
            f"Biome : {self.tile.biome}"
            f"Nation : {self.tile.nation.name if self.tile.nation else 'None'}",
            f"Value : {self.tile.value}"
        ]

        if self.tile.nation : 
            lines.append("--- Nation Info ---")
            lines.append(f"Population : {self.tile.nation.ressources['population']}")
            lines.append(f"Money : {self.tile.nation.ressources['money']}")
            lines.append(f"Score : {self.tile.nation.score}")

        return lines
    
    def to_string(self):
        return "\n".join(self.get_info_lines())