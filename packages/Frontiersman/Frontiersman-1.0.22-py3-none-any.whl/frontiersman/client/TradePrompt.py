import pygame.gfxdraw
import pygame_gui
from pygame_gui.elements import UIWindow, UIImage


class TradePrompt(UIWindow):
    def __init__(self, manager, offer, cost, hand, callback1, callback2, size=(1000, 800), location=(100, 100)):
        print(offer)
        self.size = size
        self.offer = [0, 0, 0, 0, 0]
        self.offer[0] = offer[0]
        self.offer[1] = offer[3]
        self.offer[2] = offer[4]
        self.offer[3] = offer[1]
        self.offer[4] = offer[2]
        self.functional_offer = offer
        self.cost = [0, 0, 0, 0, 0]
        self.cost[0] = cost[0]
        self.cost[1] = cost[3]
        self.cost[2] = cost[4]
        self.cost[3] = cost[1]
        self.cost[4] = cost[2]
        self.functional_cost = cost
        self.hand = hand
        super().__init__(pygame.Rect(location, self.size), manager,
                         window_display_title='Trade Offer',
                         object_id='#help_window')

        surface_size = self.get_container().get_size()
        self.surface_element = UIImage(pygame.Rect((0, 0),
                                                   surface_size),
                                       pygame.Surface(surface_size).convert(),
                                       manager=manager,
                                       container=self,
                                       parent_element=self)

        self.text_color = (255, 255, 255)
        self.manager = manager
        self.menu_buttons = []

        self.callback1 = callback1
        self.callback2 = callback2

        self.screen_size = (size[0], size[1] - 50)
        pygame.display.set_caption('Frontiersman Menu')

        self.panel_art = []
        self.panel_art_scaled = [None, None, None, None, None, None]
        self.init_textures()

        self.graphics = self.generate_graphics()

        self.state = 'main'  # main, options, join

    def update(self, time_delta):
        super().update(time_delta)
        self.surface_element.image.blit(self.graphics, (0, 0))

    def handle_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.menu_buttons[0]:
                    self.kill()
                    self.callback1()
                if event.ui_element == self.menu_buttons[1]:
                    self.kill()
                    self.callback2()
        self.manager.process_events(event)

    def process_event(self, event):
        if event.type == pygame.USEREVENT and event.user_type == 'ui_button_pressed' and event.ui_element == self.close_window_button:
            self.callback2()
        super().process_event(event)

    def init_textures(self):
        # brick, ore, sheep, wheat, wood
        self.panel_art.append(pygame.image.load('./assets/cards/res/bricks.png'))
        self.panel_art.append(pygame.image.load('./assets/cards/res/ore.png'))
        self.panel_art.append(pygame.image.load('./assets/cards/res/sheep.png'))
        self.panel_art.append(pygame.image.load('./assets/cards/res/wheat.png'))
        self.panel_art.append(pygame.image.load('./assets/cards/res/wood.png'))

    def generate_graphics(self):
        # define center coordinates
        center = (self.screen_size[0] / 2, self.screen_size[1] / 2)

        # create surface and apply background color
        background_color = (61, 120, 180)
        background = pygame.Surface(self.screen_size)
        background.fill(background_color)

        # button dimensions
        button_width = self.screen_size[0] // 10 * 2
        button_height = self.screen_size[1] // 10

        self.menu_buttons = []

        # function to add menu buttons to UI manager
        def menu_button(location, text):
            self.menu_buttons.append(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(location, (button_width, button_height)),
                text=text, manager=self.manager,
                object_id='#menu_button_square_back', container=self))

        padding = button_width // 2 + 10

        menu_button((center[0] - button_width // 2 - padding, int(9 * self.screen_size[1] / 10) - button_height // 2),
                    'Accept')
        menu_button((center[0] - button_width // 2 + padding, int(9 * self.screen_size[1] / 10) - button_height // 2),
                    'Deny')
        for x in range(0, len(self.hand)):
            if (self.hand[x] - self.functional_cost[x] < 0):
                self.menu_buttons[0].disable()
                break

        pygame.font.init()
        label_font = pygame.font.Font("./data/fonts/impact.ttf", self.screen_size[1] // 20)
        label_surface = pygame.Surface(self.screen_size, pygame.SRCALPHA)

        offer_text = pygame.font.Font.render(pygame.font.Font(
            "./data/fonts/impact.ttf",
            self.screen_size[1] // 15),
            "Offering", True, (255, 255, 255), None)

        if offer_text.get_width() > self.screen_size[0]:
            scale = self.screen_size[0] / offer_text.get_width()
            title_text = pygame.transform.scale(offer_text,
                                                (int(offer_text.get_width() * scale),
                                                 int(offer_text.get_height() * scale)))

        price_text = pygame.font.Font.render(pygame.font.Font(
            "./data/fonts/impact.ttf",
            self.screen_size[1] // 15),
            "For", True, (255, 255, 255), None)

        if price_text.get_width() > self.screen_size[0]:
            scale = self.screen_size[0] / price_text.get_width()
            price_text = pygame.transform.scale(price_text,
                                                (int(price_text.get_width() * scale),
                                                 int(price_text.get_height() * scale)))

        card_width = self.screen_size[0] // 12
        card_height = int(card_width * 7 / 5)
        # scale cards
        index = 0
        for textures in self.panel_art:
            self.panel_art_scaled[index] = pygame.transform.scale(textures, (card_width, card_height))
            index += 1

        index = 0
        h_padding = self.screen_size[0] // 20
        v_padding = self.screen_size[1] // 20
        card_location = (h_padding * 6, v_padding * 4)

        amount_font = pygame.font.Font(
            "./data/fonts/impact.ttf",
            self.screen_size[1] // 20)

        # draw cards
        for index in range(0, 5):
            background.blit(self.panel_art_scaled[index], (
                int(card_location[0] + index * h_padding * 2 - self.panel_art_scaled[index].get_width() / 2),
                int(card_location[1] - self.panel_art_scaled[index].get_height() / 2)))
            background.blit(self.panel_art_scaled[index], (
                int(card_location[0] + index * h_padding * 2 - self.panel_art_scaled[index].get_width() / 2),
                int(card_location[1] - self.panel_art_scaled[index].get_height() / 2 + 8 * v_padding)))

        # draw amounts
        index = 0
        for offer in self.offer:
            text = pygame.font.Font.render(amount_font, str(offer), True, self.text_color, None)
            background.blit(text, (int(card_location[0] + index * h_padding * 2 - text.get_width() / 2),
                                   int(card_location[1] - text.get_height() / 2 + v_padding * 3)))
            index += 1

        index = 0
        for offer in self.cost:
            text = pygame.font.Font.render(amount_font, str(offer), True, self.text_color, None)
            background.blit(text, (int(card_location[0] + index * h_padding * 2 - text.get_width() / 2),
                                   int(card_location[1] - text.get_height() / 2 + v_padding * 11)))
            index += 1

        # create screen sized software surface
        title_surface = pygame.Surface(self.screen_size, pygame.SRCALPHA)

        # apply title to screen sized software surface
        title_surface.blit(offer_text,
                           (int(self.screen_size[0] / 2 - offer_text.get_width() / 2),
                            int(self.screen_size[1] / 20 - offer_text.get_height() / 2)))
        title_surface.blit(price_text,
                           (int(self.screen_size[0] / 2 - price_text.get_width() / 2),
                            int(self.screen_size[1] / 20 * 9 - price_text.get_height() / 2)))

        # apply title to background surface
        background.blit(title_surface, (0, 0))
        # apply buttons to background surface
        background.blit(label_surface, (0, 0))

        return background
