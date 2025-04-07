import pygame
import numpy as np
from modules.map import Map


pygame.init()

# --- Config ---
WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Not your life.")
frame_count = 0

# --- Variables globales ---
running = True
seed = 0
game_map = None

# --- UI: Texte ---
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# --- Menu Principal avec boutons images ---
def main_menu():
    menu_running = True
    font = pygame.font.SysFont(None, 60)
    clock = pygame.time.Clock()
    bg_shift = 0

    # Charger les images de boutons
    play_img = pygame.image.load("image1.png").convert_alpha()
    quit_img = pygame.image.load("image2.png").convert_alpha()
    play_img = pygame.transform.scale(play_img, (240, 60))
    quit_img = pygame.transform.scale(quit_img, (240, 60))

    # Rects pour détection clic
    play_rect = play_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    quit_rect = quit_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))

    while menu_running:
        # Animation de fond
        # Image de fond
        background = pygame.image.load("image2.png").convert()
        ackground = pygame.transform.scale(background, (WIDTH, HEIGHT))


        draw_text("Not your life.", font, (255, 255, 255), screen, WIDTH // 2, HEIGHT // 4)

        # Affichage des boutons
        screen.blit(play_img, play_rect.topleft)
        screen.blit(quit_img, quit_rect.topleft)

        # Détection survol
        hovered_play = play_rect.collidepoint(pygame.mouse.get_pos())
        hovered_quit = quit_rect.collidepoint(pygame.mouse.get_pos())

        # Gestion des événements
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
        clock.tick(60)

