from modules.map import Map
import pygame
import numpy as np
from modules.ai.spawn import handle_spawn


pygame.init()

# Window size
WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 100  # Adjust cell size to fit the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Not your life.")
frame_count = 0

running = True
seed = 0
game_map = None  # Define globally

def start():
    global game_map
    print("Game started!")
    
    colors = ["red", "blue", "green", "yellow", "purple", "cyan", "orange", "pink"]  # Example colors
    civ_names = ["Rome", "Greece", "Egypt", "Persia", "China", "India", "Maya", "Aztec"]  # Example civ names
    
    game_map = Map(seed)  # Initialize the map
    handle_spawn(colors, civ_names, game_map)  # Spawn AI civilizations


def draw_grid():
    """Draws the 100x100 grid, including AI civilizations."""
    if game_map is None or not hasattr(game_map, "map"):
        return

    for x in range(100):
        for y in range(100):
            tile = game_map.map[x, y]
            
            if tile.has_ai:  # If it's an AI color (e.g., "red")
                rgb_color = pygame.Color(tile.color)  # Convert name to RGB
            else:
                rgb_color = pygame.Color(tile.color)  # Normal terrain
            
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, rgb_color, rect)


def update():
    screen.fill((0, 0, 0))  # Clear screen
    draw_grid()  # Draw the grid
    tile_pos = (pygame.mouse.get_pos()[0]//CELL_SIZE,pygame.mouse.get_pos()[1]//CELL_SIZE)

    game_map.map[tile_pos[0],tile_pos[1]].print_debug()

def global_loop():
    global running
    clock = pygame.time.Clock()
    start()  # Initialize game elements
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        update()  # Update the screen
        pygame.display.flip()  # Refresh display
        clock.tick(60)  # 60 FPS

    pygame.quit()
    print("Game closed.")





global_loop()
