import pygame
import pygame_gui as pg_g
from frontiersman.client.GuiConstants import CARD_SIZE, SPACING

CARDS = ['Brick', 'Ore', 'Sheep', 'Wheat', 'Wood']
TITLE_SPACING = 28


class CardPickerGui(pg_g.elements.UIWindow):
    def __init__(self, top_left, manager, callback):
        super().__init__(pygame.Rect(top_left, ((CARD_SIZE[0] + SPACING) * 5 + 10 * SPACING, CARD_SIZE[1] + 10 * SPACING + TITLE_SPACING)), manager)
        self.manager = manager
        self.callback = callback
        self.cards = []
        self.close_window_button.disable()

        for i, card in enumerate(CARDS):
            self.cards.append(pg_g.elements.UIButton(
                relative_rect=pygame.Rect((i * (CARD_SIZE[0] + SPACING), 0), CARD_SIZE),
                text="",
                manager=self.manager,
                container=self,
                object_id="#" + card
            ))

    def handle_ui_button_pressed(self, event):
        try:
            index = self.cards.index(event.ui_element)
            self.callback(CARDS[index])
        except ValueError:
            pass
