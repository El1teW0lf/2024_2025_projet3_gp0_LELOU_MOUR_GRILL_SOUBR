import pygame
import numpy as np
from PIL import Image
from modules.map import Map

class GameMenu:
    def __init__(self, width=1792, height=1008):
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

        # Load images
        self.play_img = pygame.image.load("image/Start.png").convert_alpha()
        self.quit_img = pygame.image.load("image/Quit.png").convert_alpha()
        self.title_img = pygame.image.load("image/Neural_Realms.png").convert_alpha()

        # Button rects
        self.play_rect = self.play_img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 20))
        self.quit_rect = self.quit_img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 120))
        self.title_rect = self.title_img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 360))

        # Load GIF frames
        self.cow_frames = self.load_gif_frames("image/PolishCow8Bit.gif")
        self.current_cow_frame = 0
        self.cow_frame_duration = 100  # ms per frame (10 fps)
        self.last_cow_frame_update = pygame.time.get_ticks()

    def load_gif_frames(self, path):
        pil_gif = Image.open(path)
        frames = []

        try:
            while True:
                frame = pil_gif.convert("RGBA")
                pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                frames.append(pygame.transform.scale(pygame_image, (150, 86)))  # Resize if needed
                pil_gif.seek(pil_gif.tell() + 1)
        except EOFError:
            pass

        return frames

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
        surface.blit(textobj, textrect)

    def main_menu(self):
        menu_running = True

        while menu_running:
            # Fond
            background = pygame.image.load("image/background_def1.png").convert()
            background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
            self.screen.blit(background, (0, 0))

            # Mise à jour animation vache
            now = pygame.time.get_ticks()
            if now - self.last_cow_frame_update >= self.cow_frame_duration:
                self.current_cow_frame = (self.current_cow_frame + 1) % len(self.cow_frames)
                self.last_cow_frame_update = now

            # Affichage de la vache animée
            cow_image = self.cow_frames[self.current_cow_frame]
            self.screen.blit(cow_image, (100, self.HEIGHT - 200))  
            self.screen.blit(cow_image, (500, self.HEIGHT - 180))  
            self.screen.blit(cow_image, (780, self.HEIGHT - 420))  
            self.screen.blit(cow_image, (1000, self.HEIGHT - 250))  
            self.screen.blit(cow_image, (1500, self.HEIGHT - 140))  
            self.screen.blit(cow_image, (1620, self.HEIGHT - 820))  
            self.screen.blit(cow_image, (1300, self.HEIGHT - 500))  
            self.screen.blit(cow_image, (220, self.HEIGHT - 600))  
            # Boutons
            self.screen.blit(self.play_img, self.play_rect.topleft)
            self.screen.blit(self.quit_img, self.quit_rect.topleft)
            self.screen.blit(self.title_img, self.title_rect.topleft)

            # Gestion survol
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
