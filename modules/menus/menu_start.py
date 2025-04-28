import pygame
import numpy as np
from modules.map import Map

class GameMenu:
    def __init__(self, width=1000, height=800):
        pygame.init()

        # Config
        self.WIDTH, self.HEIGHT = width, height
        self.CELL_SIZE = self.WIDTH // 100
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Not your life.")
        self.frame_count = 0

        # Globals
        self.running = True
        self.seed = 0
        self.game_map = None

        # Load resources
        self.font = pygame.font.SysFont(None, 60)
        self.clock = pygame.time.Clock()

        # Load images - Remplacer les images
        self.play_img = pygame.image.load("image/image4.png").convert_alpha()
        self.quit_img = pygame.image.load("image/image5.png").convert_alpha()
        self.play_img = pygame.transform.scale(self.play_img, (240, 60))
        self.quit_img = pygame.transform.scale(self.quit_img, (240, 60))

        # Button rects
        self.play_rect = self.play_img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 20))
        self.quit_rect = self.quit_img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 70))

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
        surface.blit(textobj, textrect)

    def main_menu(self):
        menu_running = True

        while menu_running:
            # Fond animé ou image de fond - Aussi à remplacer
            background = pygame.image.load("image/image2.png").convert()
            background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
            self.screen.blit(background, (0, 0))

            self.draw_text("Not your life.", self.font, (255, 255, 255), self.screen, self.WIDTH // 2, self.HEIGHT // 4)

            # Affichage des boutons
            self.screen.blit(self.play_img, self.play_rect.topleft)
            self.screen.blit(self.quit_img, self.quit_rect.topleft)

            # Survol
            hovered_play = self.play_rect.collidepoint(pygame.mouse.get_pos())
            hovered_quit = self.quit_rect.collidepoint(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if hovered_play:
                        menu_running = False
                    elif hovered_quit:
                        pygame.quit()
                        exit()

            pygame.display.update()
            self.clock.tick(60)

# --- Utilisation ---
if __name__ == "__main__":
    menu = GameMenu()
    menu.main_menu()