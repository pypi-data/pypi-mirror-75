import pygame
import pygame_gui as pg_g

from frontiersman.client.GuiConstants import SPACING, INFO_WIDTH

WIDTH = INFO_WIDTH
HEIGHT = INFO_WIDTH / 5
TITLE_SPACING = 28


class PlayerSelector(pg_g.elements.UIWindow):
    def __init__(self, top_left, enemy_players, manager, text, callback_success, callback_close=None):
        size = (WIDTH + 3 * SPACING, (HEIGHT + SPACING) * (len(enemy_players) + 1) + SPACING + 2 * TITLE_SPACING)
        super().__init__(pygame.Rect(top_left, size), manager)
        self.enemy_players = enemy_players
        self.manager = manager
        self.text = text
        self.callback_success = callback_success
        self.callback_close = callback_close

        if self.callback_close is None:
            self.close_window_button.disable()

        self.info = pg_g.elements.UITextBox(self.text, pygame.Rect(0, 0, WIDTH, HEIGHT), self.manager, container=self)

        self.buttons = []
        for i, enemy_player in enumerate(enemy_players):
            self.buttons.append(pg_g.elements.UIButton(
                relative_rect=pygame.Rect(0, (i + 1) * (HEIGHT + SPACING), WIDTH, HEIGHT),
                manager=self.manager,
                text=enemy_player.name,
                object_id='#' + enemy_player.color.capitalize(),
                container=self
            ))

    def handle_ui_button_pressed(self, event):
        if event.ui_element in self.buttons:
            index = self.buttons.index(event.ui_element)
            self.callback_success(self.enemy_players[index])

    def process_event(self, event):
        if self.callback_close is not None and event.type == pygame.USEREVENT and event.user_type == 'ui_button_pressed' and event.ui_element == self.close_window_button:
            self.callback_close()
        super().process_event(event)
