import pygame
import pygame.freetype
from modules.map import Map
from modules.ai.ai import AI
from modules.nation import Nation
from modules.menus.menu_start import GameMenu
from modules.menus.loading_screen import LoadingScreen  # Adjust path as needed


class Main:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1000, 800
        self.CELL_SIZE = 8

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Not your life.")
        self.font = pygame.freetype.Font("Blazma-Regular.ttf", 17)
        self.clock = pygame.time.Clock()
        self.running = True

        self.seed = 0
        self.tick = 0
        self.day_tick = 0

        # Initialize loading screen
        self.loading = LoadingScreen(self.screen, self.font, width=self.WIDTH, height=self.HEIGHT)
        self.loading.show("Generating world...", progress=0.0)

        # Generate game world
        self._generate_world()

    def _generate_world(self):
        self.map = Map(self.seed)
        self.loading.show("Generating world...", progress=0.2)

        self.nations = []
        for i in range(10):
            nation = Nation(self.map)
            self.nations.append(nation)
            progress = 0.2 + (i + 1) / 10 * 0.4  # 0.2–0.6 range
            self.loading.show(f"Spawning nations... ({i + 1}/10)", progress=progress)

        self.ai = []
        for i, nation in enumerate(self.nations):
            self.ai.append(AI(self.map, nation))
            progress = 0.6 + (i + 1) / 10 * 0.4  # 0.6–1.0 range
            self.loading.show(f"Initializing AI... ({i + 1}/10)", progress=progress)

    def _draw_map(self):
        for x in range(100):
            for y in range(100):
                tile = self.map.map[x, y]
                rgb_color = pygame.Color(f"#{tile.color}")
                rect = pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.screen, rgb_color, rect)

    def _draw_text(self):
        tile = self.map.map[self.tile_pos[0], self.tile_pos[1]]

        def draw_line(text, y_offset):
            surface, _ = self.font.render(text, (255, 255, 255))
            self.screen.blit(surface, (810, y_offset))

        draw_line(f"Tile ({self.tile_pos[0]},{self.tile_pos[1]})", 20)
        draw_line(f"Biome : {tile.biome}", 40)
        draw_line(f"Nation : ", 60)
        draw_line(f"{tile.nation.name if tile.nation else None}", 80)
        draw_line(f"Value : {tile.value}", 100)

        if tile.nation:
            draw_line(f"{tile.nation.name}", 140)
            draw_line("Info panel", 160)
            draw_line(f"Population : {tile.nation.ressources['population']}", 180)
            draw_line(f"Money : {tile.nation.ressources['money']}", 200)
            draw_line(f"Score : {tile.nation.score}", 220)

    def update(self):
        self.screen.fill((0, 0, 0))
        self._draw_map()
        self.tile_pos = (
            min(99, pygame.mouse.get_pos()[0] // self.CELL_SIZE),
            min(99, pygame.mouse.get_pos()[1] // self.CELL_SIZE),
        )
        self._draw_text()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update()
            pygame.display.flip()
            self.clock.tick(60)
            self.tick += 1
            if self.tick % 60 == 0:
                self.day_tick += 1

        pygame.quit()
        print("Game closed.")


if __name__ == "__main__":
    pygame.init()
    menu = GameMenu()
    menu.main_menu()

    game = Main()
    game.run()
