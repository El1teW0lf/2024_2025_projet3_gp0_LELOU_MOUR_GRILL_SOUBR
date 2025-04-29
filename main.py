import pygame
import pygame.freetype
from modules.map import Map
from modules.ai.ai import AI
from modules.ai.trainer import Trainer
from modules.nation import Nation
from modules.menus.menu_start import GameMenu
from modules.menus.loading_screen import LoadingScreen  # Adjust path as needed


class Main:
    def __init__(self, headless=False):
        self.WIDTH, self.HEIGHT = 1792, 1008
        self.CELL_SIZE = 8
        self.GRID_SIZE = 100  # 100x100 grid

        self.headless = headless

        if not self.headless:
            pygame.init()
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            pygame.display.set_caption("Not your life.")
            self.font = pygame.freetype.Font("Blazma-Regular.ttf", 17)
            self.clock = pygame.time.Clock()

        self.running = True
        self.seed = 0
        self.tick = 0
        self.day_tick = 0

        # Calculate map offset for centering
        self.x_offset = (self.WIDTH - self.GRID_SIZE * self.CELL_SIZE) // 2
        self.y_offset = (self.HEIGHT - self.GRID_SIZE * self.CELL_SIZE) // 2

        # Initialize loading screen
        if not self.headless:
            self.loading = LoadingScreen(self.screen, self.font, width=self.WIDTH, height=self.HEIGHT)
            self.loading.show("Generating world...", progress=0.0)

        # Generate the game world
        self._generate_world()
        self.reset()

    def _generate_world(self):
        self.map = Map(self.seed)
        if not self.headless:
            self.loading.show("Generating world...", progress=0.2)

        self.nations = []
        for i in range(1):
            nation = Nation(self.map)
            self.nations.append(nation)
            progress = 0.2 + (i + 1) / 10 * 0.4  # 0.2–0.6 range
            if not self.headless:
                self.loading.show(f"Spawning nations... ({i + 1}/10)", progress=progress)

        self.ai = []
        for i, nation in enumerate(self.nations):
            self.ai.append(AI(self.map, nation))
            progress = 0.6 + (i + 1) / 10 * 0.4  # 0.6–1.0 range
            if not self.headless:
                self.loading.show(f"Initializing AI... ({i + 1}/10)", progress=progress)

        self.trainer = Trainer(self)

    def _draw_map(self):
        # Optional: draw a border around the map
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),  # White border
            pygame.Rect(
                self.x_offset - 1,
                self.y_offset - 1,
                self.GRID_SIZE * self.CELL_SIZE + 2,
                self.GRID_SIZE * self.CELL_SIZE + 2
            ),
            2  # Border thickness
        )

        # Draw the map tiles
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
        tile = self.map.map[self.tile_pos[0], self.tile_pos[1]]

        def draw_line(text, y_offset):
            surface, _ = self.font.render(text, (255, 255, 255))
            self.screen.blit(surface, (20, y_offset))  # Moved text to the left side

        draw_line(f"Tile ({self.tile_pos[0]},{self.tile_pos[1]})", 20)
        draw_line(f"Biome: {tile.biome}", 40)
        draw_line(f"Nation: {tile.nation.name if tile.nation else 'None'}", 60)
        draw_line(f"Value: {tile.value}", 80)

        if tile.nation:
            draw_line("--- Nation Info ---", 120)
            draw_line(f"Population: {tile.nation.ressources['population']}", 140)
            draw_line(f"Money: {tile.nation.ressources['money']}", 160)
            draw_line(f"Score: {tile.nation.score}", 180)

    def update(self):
        if not self.headless:
            self.screen.fill((0, 0, 0))
            self._draw_map()

            mouse_x, mouse_y = pygame.mouse.get_pos()
            map_x = (mouse_x - self.x_offset) // self.CELL_SIZE
            map_y = (mouse_y - self.y_offset) // self.CELL_SIZE

            if 0 <= map_x < self.GRID_SIZE and 0 <= map_y < self.GRID_SIZE:
                self.tile_pos = (map_x, map_y)
            else:
                self.tile_pos = (0, 0)

            self._draw_text()

        for nation in self.nations:
            nation.tick()
        self.trainer.tick()

    def run(self):
        while self.running:
            if not self.headless:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

            self.update()
            if not self.headless:
                pygame.display.flip()
                self.clock.tick(60)

            self.tick += 1
            if self.tick % 60 == 0:
                self.day_tick += 1

        pygame.quit()
        print("Game closed.")

    def reset(self):
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

        for i, nation in enumerate(self.nations):
            self.ai[i].map = self.map
            self.ai[i].init_nation(nation)


if __name__ == "__main__":
    headless = False

    if not headless:
        pygame.init()
        menu = GameMenu()
        menu.main_menu()

    game = Main(headless=headless)
    game.run()
