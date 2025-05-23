import pygame
import pygame.freetype
from modules.map import Map
from modules.ai.ai import AI
from modules.ai.trainer import Trainer
from modules.nation import Nation
from modules.menus.menu_start import GameMenu
from modules.menus.loading_screen import LoadingScreen  # Adjust path as needed
from modules.menus.tileinfo import TileInfo


class Main:
    def __init__(self, headless=False):
        # Game screen dimensions and map/grid size
        self.WIDTH, self.HEIGHT = 1792, 1008
        self.CELL_SIZE = 8
        self.GRID_SIZE = 100  # 100x100 tile grid

        self.headless = headless  # Run without graphics (useful for testing or training AI)

        if not self.headless:
            pygame.init()
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            pygame.display.set_caption("Neural Realms")
            self.font = pygame.freetype.Font("Blazma-Regular.ttf", 17)
            self.clock = pygame.time.Clock()

        self.running = True
        self.seed = 1
        self.tick = 0
        self.day_tick = 0  # Counter for in-game day progression

        # Center the map on the screen
        self.x_offset = (self.WIDTH - self.GRID_SIZE * self.CELL_SIZE) // 2
        self.y_offset = (self.HEIGHT - self.GRID_SIZE * self.CELL_SIZE) // 2

        # Display loading screen
        if not self.headless:
            self.loading = LoadingScreen(self.screen, self.font, width=self.WIDTH, height=self.HEIGHT)
            self.loading.show("Generating world...", progress=0.0)

        # Generate the map, nations, and AI
        self._generate_world()
        self.reset()

    def _generate_world(self):
        # Initialize the map
        self.map = Map(self.seed)
        if not self.headless:
            self.loading.show("Generating world...", progress=0.2)

        # Create nations and update progress on the loading screen
        self.nations = []
        for i in range(1):  # Currently only 1 nation
            nation = Nation(self.map)
            self.nations.append(nation)
            progress = 0.2 + (i + 1) / 10 * 0.4
            if not self.headless:
                self.loading.show(f"Spawning nations... ({i + 1}/10)", progress=progress)

        # Assign AI to each nation
        self.ai = []
        for i, nation in enumerate(self.nations):
            self.ai.append(AI(self.map, nation))
            progress = 0.6 + (i + 1) / 10 * 0.4
            if not self.headless:
                self.loading.show(f"Initializing AI... ({i + 1}/10)", progress=progress)

        # Initialize the training module
        self.trainer = Trainer(self)

    def _draw_map(self):
        # Draw a white border around the map
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            pygame.Rect(
                self.x_offset - 1,
                self.y_offset - 1,
                self.GRID_SIZE * self.CELL_SIZE + 2,
                self.GRID_SIZE * self.CELL_SIZE + 2
            ),
            2  # Border thickness
        )

        # Render each tile of the map with its color
        for x in range(self.GRID_SIZE):
            for y in range(self.GRID_SIZE):
                tile = self.map.map[x, y]
                rgb_color = pygame.Color(f"#{tile.color}")
                rect = pygame.Rect(
                    self.x_offset + x * self.CELL_SIZE,
                    self.y_offset + y * self.CELL_SIZE,
                    self.CELL_SIZE,
                    self.CELL_SIZE
                )
                pygame.draw.rect(self.screen, rgb_color, rect)

    def _draw_text(self):
        # Get the tile under the mouse and display info
        tile = self.map.map[self.tile_pos[0], self.tile_pos[1]]
        tile_info = TileInfo(self.tile_pos, tile)
        lines = tile_info.get_info_lines()

        line_height = 20  # Distance between lines
        total_height = len(lines) * line_height

        for i, line in enumerate(lines):
            surface, _ = self.font.render(line, (255, 255, 255))
            self.screen.blit(surface, (20, 20 + i * line_height))

    def update(self):
        # Called each frame; handles rendering and logic updates
        if not self.headless:
            self.screen.fill((0, 0, 0))  # Clear screen
            self._draw_map()  # Draw the map

            # Determine which tile the mouse is over
            mouse_x, mouse_y = pygame.mouse.get_pos()
            map_x = (mouse_x - self.x_offset) // self.CELL_SIZE
            map_y = (mouse_y - self.y_offset) // self.CELL_SIZE

            if 0 <= map_x < self.GRID_SIZE and 0 <= map_y < self.GRID_SIZE:
                self.tile_pos = (map_x, map_y)
            else:
                self.tile_pos = (0, 0)

            self._draw_text()  # Display tile information

        # Progress game logic for nations and AI trainer
        for nation in self.nations:
            nation.tick()
        self.trainer.tick()

    def run(self):
        # Main loop of the game
        while self.running:
            if not self.headless:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

            self.update()

            if not self.headless:
                pygame.display.flip()  # Update the display
                self.clock.tick(60)  # Cap at 60 frames per second

            self.tick += 1
            if self.tick % 60 == 0:
                self.day_tick += 1  # Update in-game days

        pygame.quit()
        print("Game closed.")

    def reset(self):
        # Regenerate the map and nations
        self.map = Map(self.seed)
        if not self.headless:
            self.loading.show("Generating world...", progress=0.2)

        self.nations = []
        for i in range(1):
            nation = Nation(self.map)
            self.nations.append(nation)
            progress = 0.2 + (i + 1) / 10 * 0.4
            if not self.headless:
                self.loading.show(f"Spawning nations... ({i + 1}/10)", progress=progress)

        # Reinitialize AI with the new map and nations
        for i, nation in enumerate(self.nations):
            self.ai[i].map = self.map
            self.ai[i].init_nation(nation)


if __name__ == "__main__":
    # Run the game unless in headless mode
    headless = False

    if not headless:
        pygame.init()
        menu = GameMenu()
        menu.main_menu()

    game = Main(headless=headless)
    game.run()
