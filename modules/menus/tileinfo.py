class TileInfo:
    def __init__(self, tile_pos, tile):
        # Store the position (as a tuple like (x, y)) and the tile object itself
        self.tile_pos = tile_pos
        self.tile = tile

    def get_info_lines(self):
        # Collect basic tile information into a list of strings
        lines = [
            f"Tile : ({self.tile_pos[0]}, {self.tile_pos[1]})",  # Tile coordinates
            f"Biome : {self.tile.biome}",  # Tile's biome type
            f"Nation : {self.tile.nation.name if self.tile.nation else 'None'}",  # Nation name if claimed
            f"Value : {self.tile.value}"  # Economic or strategic value of the tile
        ]

        # If the tile belongs to a nation, include nation-related info
        if self.tile.nation:
            lines.append("")  # Blank line for spacing
            lines.append("--- Nation Info ---")
            lines.append(f"Population : {self.tile.nation.ressources['population']}")  # Total nation population
            lines.append(f"Money : {int(self.tile.nation.ressources['money'])}")  # Current money of the nation
            lines.append(f"Score : {int(self.tile.nation.score)}")  # Calculated score for the nation

        return lines  # Return the list of info strings

    def to_string(self):
        # Convert the list of info lines into a single formatted string
        return "\n".join(self.get_info_lines())
