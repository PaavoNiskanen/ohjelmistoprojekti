import pygame
from States.GameState import GameState
from States.MainMenuState import MainMenuState
from Valikot.NextLevel import NextLevel


class LevelCompleteState(GameState):

    def __init__(self, manager, level_manager=None):
        super().__init__(manager)
        self.level_manager = level_manager
        
        # Get current level number from manager, if available
        current_level = 1 if not level_manager else level_manager.get_current_level_number()
        max_level = 5 if not level_manager else level_manager.num_levels
        next_level = current_level + 1 if current_level < max_level else current_level
        
        self.next_level_menu = NextLevel(
            current_level=current_level,
            max_level=max_level,
            display_current_level=current_level,
            display_next_level=next_level,
            screen=manager.screen,
        )

    def update(self, events):
        action = self.next_level_menu.handle_events_from(events)
        result = self.next_level_menu.resolve_action(action)

        if isinstance(result, int):
            # Next level selected
            if self.level_manager:
                has_next = self.level_manager.next_level()
                if has_next:
                    # Continue with next level
                    from States.PlayState import PlayState
                    self.manager.set_state(PlayState(self.manager, level_manager=self.level_manager))
                    return
                else:
                    # All levels completed
                    self.manager.set_state(MainMenuState(self.manager))
                    return
            else:
                # Fallback: restart PlayState if no level manager
                from States.PlayState import PlayState
                self.manager.set_state(PlayState(self.manager))
                return

        if result == "game_completed":
            self.manager.set_state(MainMenuState(self.manager))
            return

        if result == "settings":
            try:
                from Valikot.SettingsMenu import main as settings_menu_main
                settings_menu_main()
            except Exception as exc:
                print(f"Could not open settings menu: {exc}")
            return

        if result == "quit":
            self.manager.running = False
            return

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.manager.set_state(MainMenuState(self.manager))
                return

    def draw(self, screen):
        self.next_level_menu.draw(screen)