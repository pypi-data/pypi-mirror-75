import pygame
import pygame_gui as pg_g
from frontiersman.client.GuiConstants import CARD_SIZE, SPACING


class CardDiscarder:
    def __init__(self, rect, cards, manager, callback, layer_height, container=None):
        rect = pygame.Rect(rect.left, rect.top - rect.height, rect.width, rect.height * 2)
        self.manager = manager
        self.cards = sorted(cards)
        self.selected_cards = [False for _ in self.cards]
        self.num_discard_cards = 0
        self.card_elements = []
        self.callback = callback

        self.panel = pg_g.elements.UIPanel(
            relative_rect=rect,
            starting_layer_height=layer_height,
            manager=self.manager,
            container=container,
        )

        area_width = self.panel.relative_rect.width - CARD_SIZE[0] - 8
        if len(self.cards) == 1:
            offset = 0
        else:
            offset = min(area_width / (len(self.cards) - 1), CARD_SIZE[0] + SPACING)
        start = (area_width - offset * (len(self.cards) - 1)) / 2

        for i, card in enumerate(self.cards):
            self.card_elements.append(pg_g.elements.UIButton(
                relative_rect=pygame.Rect((start + i * offset, self.panel.rect.height / 2), CARD_SIZE),
                text="",
                manager=self.manager,
                container=self.panel,
                object_id="#" + card
            ))
            if card not in ['Brick', 'Ore', 'Sheep', 'Wheat', 'Wood']:
                self.card_elements[-1].disable()
            else:
                self.num_discard_cards += 1

        self.num_discard_cards //= 2

        self.submit_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((-CARD_SIZE[0], 0), CARD_SIZE),
            text="submit",
            manager=self.manager,
            container=self.panel,
            anchors={'left': 'right',
                     'right': 'right',
                     'top': 'top',
                     'bottom': 'top'}
        )
        self.submit_button.disable()

    def kill(self):
        self.panel.kill()

    def handle_ui_button_pressed(self, event):
        element = event.ui_element
        if element in self.card_elements:
            index = self.card_elements.index(element)
            self.selected_cards[index] = not self.selected_cards[index]
            if self.selected_cards[index]:
                element.rect.top -= self.panel.rect.height / 2
            else:
                element.rect.top += self.panel.rect.height / 2
            element.rebuild()
            count = 0
            for value in self.selected_cards:
                if value:
                    count += 1
            if count == self.num_discard_cards:
                self.submit_button.enable()
            else:
                self.submit_button.disable()
        elif element == self.submit_button:
            clicked_cards = []
            for i, value in enumerate(self.selected_cards):
                if value:
                    clicked_cards.append(self.cards[i])
            self.callback(clicked_cards)
