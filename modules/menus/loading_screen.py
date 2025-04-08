# loading_screen.py

import pygame.freetype

class LoadingScreen:
    def __init__(self, screen, font, width=1000, height=800):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.font = font

        self.bg_color = (10, 10, 10)
        self.bar_bg = (50, 50, 50)
        self.bar_fill = (0, 200, 0)
        self.bar_border_color = (255, 255, 255)

        self.bar_width = 400
        self.bar_height = 30
        self.bar_position = (
            (self.WIDTH - self.bar_width) // 2,
            self.HEIGHT // 2 + 40
        )

    def show(self, message="Loading...", progress=0):
        self.screen.fill(self.bg_color)

        # Render message
        text_surface, rect = self.font.render(message, (255, 255, 255))
        self.screen.blit(text_surface, (
            self.WIDTH // 2 - rect.width // 2,
            self.HEIGHT // 2 - 40
        ))

        # Draw background bar
        pygame.draw.rect(self.screen, self.bar_bg, (*self.bar_position, self.bar_width, self.bar_height), border_radius=5)

        # Draw fill
        fill_width = int(self.bar_width * progress)
        pygame.draw.rect(self.screen, self.bar_fill, (*self.bar_position, fill_width, self.bar_height), border_radius=5)

        # Optional: draw border
        pygame.draw.rect(self.screen, self.bar_border_color, (*self.bar_position, self.bar_width, self.bar_height), 2, border_radius=5)

        pygame.display.update()
        pygame.event.pump()

