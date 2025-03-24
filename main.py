from modules.tile import Tile
from modules.generation.generation import generate_map

new_map = generate_map()
print(new_map)


test = Tile(0,0,'volcano')
test.setup()
test.print_debug()