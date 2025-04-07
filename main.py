from modules.map import Map
import pygame
import numpy as np
from modules.ai.ai import AI
from modules.nation import Nation
import time


class Main():
    def __init__(self):
        
        pygame.init()
        
        self.WIDTH, self.HEIGHT = 1000, 800
        self.CELL_SIZE = 8
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.font = pygame.freetype.Font("Blazma-Regular.ttf", 17)
        pygame.display.set_caption("Not your life.")
        
        self.seed = 0
        
        self.map = Map(self.seed)
        self.nations = [Nation(self.map) for _ in range(10)]
        self.ai = []
        for i in self.nations:
            self.ai.append(AI(self.map,i))
            
        self.running = True
        self.clock = pygame.time.Clock()
        
    def _draw_map(self):
        for x in range(100):
            for y in range(100):
                tile = self.map.map[x, y]
                
                rgb_color = pygame.Color(f"#{tile.color}")  
                
                rect = pygame.Rect(x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.screen, rgb_color, rect)

    def _draw_text(self):
        tile = self.map.map[self.tile_pos[0],self.tile_pos[1]]
        
        text_surface, rect = self.font.render(f"Tile ({self.tile_pos[0]},{self.tile_pos[1]})", (255,255, 255))
        self.screen.blit(text_surface, (810, 20))
        
        text_surface, rect = self.font.render(f"Biome {tile.biome}", (255,255, 255))
        self.screen.blit(text_surface, (810, 40))
        
        text_surface, rect = self.font.render(f"Nation", (255,255, 255))
        self.screen.blit(text_surface, (810, 60))
        
        text_surface, rect = self.font.render(f"{tile.nation.name if tile.nation != None else None}", (255,255, 255))
        self.screen.blit(text_surface, (810, 80))
        
        text_surface, rect = self.font.render(f"Value {tile.value}", (255,255, 255))
        self.screen.blit(text_surface, (810, 100))

    def update(self):
        self.screen.fill((0, 0, 0)) 
        self._draw_map()

        self.tile_pos = (min(99,pygame.mouse.get_pos()[0]//self.CELL_SIZE),min(99,pygame.mouse.get_pos()[1]//self.CELL_SIZE))

        self._draw_text()
    
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


            self.update()  
            pygame.display.flip() 
            self.clock.tick(60) 

        pygame.quit()
        print("Game closed.")






game = Main()
game.run()
