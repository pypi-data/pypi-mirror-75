import pygame
import pygame_gui as pg_g
from frontiersman.client.GuiConstants import CARD_SIZE, SPACING

CARDS = ['Brick', 'Ore', 'Sheep', 'Wheat', 'Wood']


class TraderGui(pg_g.elements.UIWindow):
    def __init__(self, top_left, resource_hand, trade_ratios, manager, callback, callback_close=None):
        super().__init__(pygame.Rect(top_left, ((CARD_SIZE[0] + SPACING) * 20, (CARD_SIZE[1] + SPACING) * 3 + 10 * SPACING + 28)), manager)
        self.resource_hand = resource_hand
        self.trade_ratios = trade_ratios
        self.manager = manager
        self.callback = callback
        self.callback_close = callback_close
        self.is_valid = False
        self.error_text = ""

        if self.callback_close is None:
            self.close_window_button.disable()

        self.give_panel = pg_g.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, self.relative_rect.width / 2, CARD_SIZE[1] + 2 * SPACING),
            starting_layer_height=1,
            manager=self.manager,
            container=self,
        )
        self.give_card_keys = []
        self.give_card_elements = []
        self.take_panel = pg_g.elements.UIPanel(
            relative_rect=pygame.Rect(self.give_panel.relative_rect.right, 0, self.relative_rect.width / 2,
                                      CARD_SIZE[1] + 2 * SPACING),
            starting_layer_height=1,
            manager=self.manager,
            container=self,
        )
        self.take_card_keys = []
        self.take_card_elements = []

        card_offset = (self.relative_rect.width / 2 - 5 * CARD_SIZE[0]) / 6

        self.give_buttons = [
            pg_g.elements.UIButton(
                relative_rect=pygame.Rect(
                    (self.give_panel.relative_rect.left + card_offset + i * (CARD_SIZE[0] + card_offset),
                     self.give_panel.relative_rect.bottom + SPACING), CARD_SIZE),
                text="",
                manager=self.manager,
                container=self,
                object_id="#" + card,
            ) for i, card in enumerate(CARDS)
        ]
        self.take_buttons = [
            pg_g.elements.UIButton(
                relative_rect=pygame.Rect(
                    (self.take_panel.relative_rect.left + card_offset + i * (CARD_SIZE[0] + card_offset),
                     self.take_panel.relative_rect.bottom + SPACING), CARD_SIZE),
                text="",
                manager=self.manager,
                container=self,
                object_id="#" + card
            ) for i, card in enumerate(CARDS)
        ]

        pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(
                self.give_buttons[0].relative_rect.left, self.give_buttons[0].relative_rect.bottom + SPACING,
                self.give_buttons[0].relative_rect.width, 35
            ),
            html_text=str(self.trade_ratios.brick) + ":1",
            manager=self.manager,
            container=self,
        )

        pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(
                self.give_buttons[1].relative_rect.left, self.give_buttons[1].relative_rect.bottom + SPACING,
                self.give_buttons[1].relative_rect.width, 35
            ),
            html_text=str(self.trade_ratios.ore) + ":1",
            manager=self.manager,
            container=self,
        )

        pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(
                self.give_buttons[2].relative_rect.left, self.give_buttons[2].relative_rect.bottom + SPACING,
                self.give_buttons[1].relative_rect.width, 35
            ),
            html_text=str(self.trade_ratios.wool) + ":1",
            manager=self.manager,
            container=self,
        )

        pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(
                self.give_buttons[3].relative_rect.left, self.give_buttons[3].relative_rect.bottom + SPACING,
                self.give_buttons[3].relative_rect.width, 35
            ),
            html_text=str(self.trade_ratios.grain) + ":1",
            manager=self.manager,
            container=self,
        )

        pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(
                self.give_buttons[4].relative_rect.left, self.give_buttons[4].relative_rect.bottom + SPACING,
                self.give_buttons[4].relative_rect.width, 35
            ),
            html_text=str(self.trade_ratios.lumber) + ":1",
            manager=self.manager,
            container=self,
        )

        button_width = 300
        button_spacing = (self.take_panel.relative_rect.width - 2 * button_width) / 3
        self.trade_with_bank_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect(
                self.take_panel.relative_rect.left + button_spacing,
                self.take_buttons[0].relative_rect.bottom + SPACING,
                button_width, 45
            ),
            text="Trade with bank",
            manager=self.manager,
            container=self,
        )
        self.trade_with_player_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect(
                self.take_panel.relative_rect.left + 2 * button_spacing + button_width,
                self.take_buttons[0].relative_rect.bottom + SPACING,
                button_width, 45
            ),
            text="Trade with players",
            manager=self.manager,
            container=self,
        )

        self.info_text = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(
                0, self.trade_with_bank_button.relative_rect.bottom, self.relative_rect.width - 2 * SPACING, 35
            ),
            html_text=self.error_text,
            manager=self.manager,
            container=self
        )

        self.validate_trade()

    def update_give_cards(self):
        for elem in self.give_card_elements:
            elem.kill()
        self.give_card_elements = []

        if len(self.give_card_keys) > 1:
            card_width = (self.give_panel.relative_rect.width - CARD_SIZE[0]) / (len(self.give_card_keys) - 1)
        else:
            card_width = CARD_SIZE[0] + SPACING
        if card_width >= CARD_SIZE[0] + SPACING:
            card_width = CARD_SIZE[0] + SPACING
            offset = (self.give_panel.relative_rect.width - card_width * len(self.give_card_keys)) / 2
        else:
            offset = 0

        for i, card in enumerate(self.give_card_keys):
            self.give_card_elements.append(pg_g.elements.UIButton(
                relative_rect=pygame.Rect((offset + i * card_width, SPACING), CARD_SIZE),
                text="",
                manager=self.manager,
                container=self.give_panel,
                object_id="#" + card
            ))

        self.validate_trade()

    def update_take_cards(self):
        for elem in self.take_card_elements:
            elem.kill()
        self.take_card_elements = []

        if len(self.take_card_keys) > 1:
            card_width = (self.give_panel.relative_rect.width - CARD_SIZE[0]) / (len(self.take_card_keys) - 1)
        else:
            card_width = CARD_SIZE[0] + SPACING
        if card_width >= CARD_SIZE[0] + SPACING:
            card_width = CARD_SIZE[0] + SPACING
            offset = (self.give_panel.relative_rect.width - card_width * len(self.take_card_keys)) / 2
        else:
            offset = 0

        for i, card in enumerate(self.take_card_keys):
            self.take_card_elements.append(pg_g.elements.UIButton(
                relative_rect=pygame.Rect((offset + i * card_width, SPACING), CARD_SIZE),
                text="",
                manager=self.manager,
                container=self.take_panel,
                object_id="#" + card
            ))

        self.validate_trade()

    def validate_trade(self):
        counts = [0, 0, 0, 0, 0]
        for card in self.give_card_keys:
            counts[CARDS.index(card)] += 1
        brick, ore, wool, grain, lumber = counts

        # check if player has enough resources
        if brick >= self.resource_hand.brick:
            self.give_buttons[0].disable()
        else:
            self.give_buttons[0].enable()

        if ore >= self.resource_hand.ore:
            self.give_buttons[1].disable()
        else:
            self.give_buttons[1].enable()

        if wool >= self.resource_hand.wool:
            self.give_buttons[2].disable()
        else:
            self.give_buttons[2].enable()

        if grain >= self.resource_hand.grain:
            self.give_buttons[3].disable()
        else:
            self.give_buttons[3].enable()

        if lumber >= self.resource_hand.lumber:
            self.give_buttons[4].disable()
        else:
            self.give_buttons[4].enable()

        # prevent too many cards in request hand
        if brick + ore + wool + grain + lumber > 7:
            for button in self.take_buttons:
                button.disable()
        else:
            for button in self.take_buttons:
                button.enable()

        # check if legal trade with bank
        points = 0
        while brick >= self.trade_ratios.brick:
            brick -= self.trade_ratios.brick
            points += 1
        while ore >= self.trade_ratios.ore:
            ore -= self.trade_ratios.ore
            points += 1
        while wool >= self.trade_ratios.wool:
            wool -= self.trade_ratios.wool
            points += 1
        while grain >= self.trade_ratios.grain:
            grain -= self.trade_ratios.grain
            points += 1
        while lumber >= self.trade_ratios.lumber:
            lumber -= self.trade_ratios.lumber
            points += 1

        delta_points = points - len(self.take_card_keys)
        counts = [brick, ore, wool, grain, lumber]
        self.is_valid = True

        for i, amount in enumerate(counts):
            if amount > 0:
                self.is_valid = False
                if delta_points < 0:
                    self.error_text = "The bank demands more " + CARDS[i].lower() + "."
                else:
                    self.error_text = "The bank refuses too much " + CARDS[i].lower() + "."
                break

        if self.is_valid:
            if delta_points > 0:
                self.is_valid = False
                self.error_text = "The bank refuses your overly generous offer."
            elif delta_points < 0:
                self.is_valid = False
                self.error_text = "The bank demands more for these resources."
            elif points == 0:
                self.is_valid = False
                self.error_text = "Offer a trade to the bank or to other players."
            else:
                self.error_text = "The bank likes your offer."

        self.info_text.kill()
        self.info_text = pg_g.elements.UITextBox(
            relative_rect=pygame.Rect(
                0, self.trade_with_bank_button.relative_rect.bottom, self.relative_rect.width - 2 * SPACING, 35
            ),
            html_text=self.error_text,
            manager=self.manager,
            container=self
        )
        if self.is_valid:
            self.trade_with_bank_button.enable()
        else:
            self.trade_with_bank_button.disable()

    def handle_ui_button_pressed(self, event):
        if event.ui_element in self.give_buttons:
            try:
                index = self.give_buttons.index(event.ui_element)
                self.give_card_keys.append(CARDS[index])
                self.update_give_cards()
            except ValueError:
                pass
        elif event.ui_element in self.take_buttons:
            try:
                index = self.take_buttons.index(event.ui_element)
                self.take_card_keys.append(CARDS[index])
                self.update_take_cards()
            except ValueError:
                pass
        elif event.ui_element in self.give_card_elements:
            try:
                index = self.give_card_elements.index(event.ui_element)
                self.give_card_keys.pop(index)
                self.update_give_cards()
            except ValueError:
                pass
        elif event.ui_element in self.take_card_elements:
            try:
                index = self.take_card_elements.index(event.ui_element)
                self.take_card_keys.pop(index)
                self.update_take_cards()
            except ValueError:
                pass
        elif event.ui_element == self.trade_with_bank_button:
            self.callback('tradebank', self.give_card_keys, self.take_card_keys)
        elif event.ui_element == self.trade_with_player_button:
            self.callback('tradeplayer', self.give_card_keys, self.take_card_keys)

    def process_event(self, event):
        if self.callback_close is not None and event.type == pygame.USEREVENT and event.user_type == 'ui_button_pressed' and event.ui_element == self.close_window_button:
            self.callback_close()
        super().process_event(event)
