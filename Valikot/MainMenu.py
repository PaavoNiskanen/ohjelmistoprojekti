import pygame
import os
from Valikot.menu_style import (
    MenuButton,
    draw_dim_overlay,
    draw_menu_panel,
)



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (52, 78, 91)

class MainMenu:
    """State-friendly main menu that draws to an external surface."""

    def __init__(self):
        if not pygame.get_init():
            pygame.init()

        if not pygame.font.get_init():
            pygame.font.init()

        self.button_width = 300
        self.button_height = 78
        self.button_spacing = 22
        self.panel_width = 760
        self.panel_height = 560
        self.buttons = []
        self.panel_rect = None
        self.background_image = None
        self._update_layout()

    def _update_layout(self):
        # Hae nykyinen ikkunan koko
        screen = pygame.display.get_surface()
        if screen is not None:
            width, height = screen.get_width(), screen.get_height()
        else:
            width, height = 1600, 800

        panel_left = width // 2 - self.panel_width // 2
        panel_top = height // 2 - self.panel_height // 2
        self.panel_rect = pygame.Rect(panel_left, panel_top, self.panel_width, self.panel_height)

        total_height = 3 * self.button_height + 2 * self.button_spacing
        start_y = self.panel_rect.top + 170 + (self.panel_rect.height - 240 - total_height) // 2
        center_x = width // 2 - self.button_width // 2

        self.buttons = [
            MenuButton(
                center_x,
                start_y,
                self.button_width,
                self.button_height,
                "START GAME",
                action="start",
            ),
            MenuButton(
                center_x,
                start_y + self.button_height + self.button_spacing,
                self.button_width,
                self.button_height,
                "SETTINGS",
                action="settings",
            ),
            MenuButton(
                center_x,
                start_y + 2 * (self.button_height + self.button_spacing),
                self.button_width,
                self.button_height,
                "QUIT",
                action="quit",
                variant="danger",
            ),
        ]

        # Päivitä taustakuva oikeaan kokoon
        try:
            project_root = os.path.dirname(os.path.dirname(__file__))
            bg_path = os.path.join(project_root, "images", "taustat", "avaruus.png")
            bg = pygame.image.load(bg_path).convert()
            self.background_image = pygame.transform.scale(bg, (width, height))
        except Exception:
            self.background_image = None

    def handle_events(self, events):
        """Handle a frame's events and return selected action or None."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button.is_clicked(event.pos):
                        return button.action

        return None

    def draw(self, surface):
        # Päivitä layout aina ennen piirtämistä, jos ikkunan koko on muuttunut
        self._update_layout()
        if self.background_image is not None:
            surface.blit(self.background_image, (0, 0))
        else:
            surface.fill(DARK_BLUE)
        draw_dim_overlay(surface)
        draw_menu_panel(surface, self.panel_rect, "ROCKET GAME", "Main Menu")

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            button.draw(surface)
