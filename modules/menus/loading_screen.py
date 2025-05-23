# loading_screen.py

import pygame.freetype

class LoadingScreen:
    def __init__(self, screen, font, width=1000, height=800):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.font = font  # Font for rendering the loading text

        # Colors for background and loading bar
        self.bg_color = (10, 10, 10)         # Background color (dark)
        self.bar_bg = (50, 50, 50)           # Loading bar background
        self.bar_fill = (0, 200, 0)          # Progress fill color (green)
        self.bar_border_color = (255, 255, 255)  # Border color (white)

        # Dimensions and position of the loading bar
        self.bar_width = 400
        self.bar_height = 30
        self.bar_position = (
            (self.WIDTH - self.bar_width) // 2,   # Center horizontally
            self.HEIGHT // 2 + 40                 # Slightly below center vertically
        )

    def show(self, message="Loading...", progress=0):
        """
        Renders the loading screen with a message and progress bar.

        :param message: Text to display above the loading bar
        :param progress: Progress as a float between 0 and 1
        """
        # Fill the screen background
        self.screen.fill(self.bg_color)

        # Render and center the loading message
        text_surface, rect = self.font.render(message, (255, 255, 255))  # White text
        self.screen.blit(text_surface, (
            self.WIDTH // 2 - rect.width // 2,
            self.HEIGHT // 2 - 40  # Position text above the bar
        ))

        # Draw the background of the progress bar
        pygame.draw.rect(self.screen, self.bar_bg, (*self.bar_position, self.bar_width, self.bar_height), border_radius=5)

        # Draw the filled portion of the progress bar
        fill_width = int(self.bar_width * progress)
        pygame.draw.rect(self.screen, self.bar_fill, (*self.bar_position, fill_width, self.bar_height), border_radius=5)

        # Optional: draw a border around the progress bar
        pygame.draw.rect(self.screen, self.bar_border_color, (*self.bar_position, self.bar_width, self.bar_height), 2, border_radius=5)

        # Update the display to show the new frame
        pygame.display.update()

        # Handle OS-level events to avoid "not responding" issues
        pygame.event.pump()
