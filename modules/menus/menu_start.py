import pygame
import numpy as np
from PIL import Image
from modules.map import Map

class GameMenu:
    def __init__(self, width=1792, height=1008):
        pygame.init()

        # Window and display config
        self.WIDTH, self.HEIGHT = width, height
        self.CELL_SIZE = self.WIDTH // 100  # Presumed grid scaling (not used directly here)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Not your life.")  # Window title
        self.frame_count = 0

        # Game state
        self.running = True
        self.seed = 0  # Placeholder for world generation seed
        self.game_map = None  # Placeholder for map object

        # Load fonts and clock
        self.font = pygame.font.SysFont(None, 60)
        self.clock = pygame.time.Clock()

        # Load static images for buttons and title
        self.play_img = pygame.image.load("image/Start.png").convert_alpha()
        self.quit_img = pygame.image.load("image/Quit.png").convert_alpha()
        self.title_img = pygame.image.load("image/Neural_Realms.png").convert_alpha()

        # Button positions
        self.play_rect = self.play_img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 20))
        self.quit_rect = self.quit_img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 120))
        self.title_rect = self.title_img.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 360))

        # Load animated GIF frames (for Polish cow animation)
        self.cow_frames = self.load_gif_frames("image/PolishCow8Bit.gif")
        self.current_cow_frame = 0
        self.cow_frame_duration = 100  # milliseconds per frame
        self.last_cow_frame_update = pygame.time.get_ticks()

    def load_gif_frames(self, path):
        # Loads all frames of a GIF and converts them to pygame surfaces
        pil_gif = Image.open(path)
        frames = []

        try:
            while True:
                frame = pil_gif.convert("RGBA")  # Convert each frame to RGBA
                pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
                frames.append(pygame.transform.scale(pygame_image, (150, 86)))  # Resize frame
                pil_gif.seek(pil_gif.tell() + 1)  # Move to next frame
        except EOFError:
            pass  # Reached end of GIF

        return frames

    def draw_text(self, text, font, color, surface, x, y):
        # Utility function to draw centered text on the screen
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
        surface.blit(textobj, textrect)

    def main_menu(self):
        # Main loop for the menu screen
        menu_running = True

        while menu_running:
            # Draw the background image
            background = pygame.image.load("image/background_def1.png").convert()
            background = pygame.transform.scale(background, (self.WIDTH, self.HEIGHT))
            self.screen.blit(background, (0, 0))

            # Update cow animation based on time
            now = pygame.time.get_ticks()
            if now - self.last_cow_frame_update >= self.cow_frame_duration:
                self.current_cow_frame = (self.current_cow_frame + 1) % len(self.cow_frames)
                self.last_cow_frame_update = now

            # Display animated cow
            cow_image = self.cow_frames[self.current_cow_frame]
            self.screen.blit(cow_image, (1300, self.HEIGHT - 500))  # Position of cow

            # Draw buttons and title
            self.screen.blit(self.play_img, self.play_rect.topleft)
            self.screen.blit(self.quit_img, self.quit_rect.topleft)
            self.screen.blit(self.title_img, self.title_rect.topleft)

            # Hover detection for buttons
            hovered_play = self.play_rect.collidepoint(pygame.mouse.get_pos())
            hovered_quit = self.quit_rect.collidepoint(pygame.mouse.get_pos())

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if hovered_play:
                        menu_running = False  # Start game
                    elif hovered_quit:
                        pygame.quit()
                        exit()  # Exit game

            # Refresh screen
            pygame.display.update()
            self.clock.tick(60)  # 60 FPS cap

# Entry point for the game
if __name__ == "__main__":
    menu = GameMenu()
    menu.main_menu()
