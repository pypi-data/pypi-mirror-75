import sys

import pygame
import pygame.gfxdraw
import pygame_gui
from pygame_gui.elements import UIDropDownMenu

sys.path.insert(0, '../frontiersman')


class TitleScreen:

    def __init__(self):
        self.children = []
        STARTING_RESOLUTION = "720p"
        RESOLUTION_DICT = {
            "1080p": (1920, 1080),
            "720p": (1280, 720)
        }

        self.resolution_translate_table = {
            "1920 x 1080": (1920, 1080),
            "1280 x 720": (1280, 720),
            "1600 x 1200": (1600, 1200),
            "800 x 600": (800, 600)
        }

        self.resolution = RESOLUTION_DICT.get(STARTING_RESOLUTION)
        self.menu_buttons = []
        pygame.init()

        self.screen_size = RESOLUTION_DICT.get(STARTING_RESOLUTION)
        pygame.display.set_caption('Frontiersman Menu')

        self.panel_circle_art = []
        self.panel_art_scaled = [None, None, None, None, None, None]
        self.panel_wood_texture = []
        self.init_textures()

        self.window = self.init_window(self.screen_size)
        self.manager = self.init_manager(self.screen_size)

        self.graphics = self.generate_graphics_main()
        # self.graphics = self.generate_graphics_options()

        self.state = 'main'  # main, options, join

        running = True
        clock = pygame.time.Clock()

        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                # close if X is clicked
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    self.resize()
                # close if ESC is pressed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                if event.type == pygame.USEREVENT:
                    if self.state == 'main':
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            # action if client is pressed
                            if event.ui_element == self.menu_buttons[2]:
                                running = False
                            if event.ui_element == self.menu_buttons[0]:
                                self.state = 'game'
                                self.change_state()
                            if event.ui_element == self.menu_buttons[1]:
                                self.state = 'options'
                                self.change_state()
                    if self.state == 'options':
                        if (
                                event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.resolution_drop_down):
                            self.resolution = self.resolution_translate_table.get(
                                self.resolution_drop_down.selected_option)
                        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                            if event.ui_element == self.menu_buttons[0]:
                                self.state = 'main'
                                self.change_state()

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.window.blit(self.graphics, (0, 0))
            self.manager.draw_ui(self.window)
            pygame.display.update()

        pygame.quit()

    @staticmethod
    def init_window(size):
        return pygame.display.set_mode(size, flags=pygame.RESIZABLE)

    @staticmethod
    def init_manager(size):
        return pygame_gui.UIManager(size, '../themes/main_menu.json')

    def init_textures(self):
        # brick, ore, sheep, wheat, wood
        self.panel_circle_art.append(pygame.image.load('../assets/cards/res/brick_circle.png'))
        self.panel_circle_art.append(pygame.image.load('../assets/cards/res/ore_circle.png'))
        self.panel_circle_art.append(pygame.image.load('../assets/cards/res/sheep_circle.png'))
        self.panel_circle_art.append(pygame.image.load('../assets/cards/res/wheat_circle.png'))
        self.panel_circle_art.append(pygame.image.load('../assets/cards/res/wood_circle.png'))
        self.panel_circle_art.append(pygame.image.load('../assets/cards/res/card_back_square.png'))

        self.panel_wood_texture.append(pygame.image.load('../assets/main/wood_texture.png'))

    def change_state(self):
        self.graphics = self.generate_graphics()

    def generate_graphics(self):
        if self.state == 'options':
            return self.generate_graphics_options()

        if self.state == 'main':
            return self.generate_graphics_main()

        if self.state == 'options':
            pass
            # return self.generate_graphics_join()

        if self.state == 'game':
            return self.generate_graphics_gameui()

    def generate_graphics_options(self):
        # define center coordinates
        center = (self.screen_size[0] / 2, self.screen_size[1] / 2)

        # create surface and apply background color
        background_color = (61, 120, 180)
        background = pygame.Surface(self.screen_size)
        background.fill(background_color)

        self.manager = TitleScreen.init_manager(self.screen_size)

        button_labels = [
            ('Resolution:', ['1920 x 1080',
                             '1280 x 720',
                             '800 x 600',
                             '1600 x 1200']),
            ('Fullscreen:', ['True', 'False']),
            ('Borderless:', ['True', 'False'])
        ]

        # button dimensions
        button_width = self.screen_size[0] // 10 * 5
        button_height = self.screen_size[1] // 10

        self.menu_buttons = []

        # function to add menu buttons to UI manager
        def menu_button(location, text):
            self.menu_buttons.append(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(location, (button_width, button_height)),
                text=text, manager=self.manager,
                object_id='#menu_button_square_back'))

        # create back button
        menu_button((center[0] - button_width // 2, int(8 * self.screen_size[1] / 10) - button_height // 2), 'Back')

        pygame.font.init()
        label_font = pygame.font.Font("../data/fonts/impact.ttf", self.screen_size[1] // 20)
        label_surface = pygame.Surface(self.screen_size, pygame.SRCALPHA)

        option_label_location = (center[0], self.screen_size[1] // (10 / 4))
        option_label_offset = self.screen_size[1] // 10

        padding = self.screen_size[0] // 40

        options_location = (center[0] + padding, self.screen_size[1] // (10 / 4))
        options_offset = self.screen_size[1] // 10
        options_size = (self.screen_size[0] // 5 - padding, self.screen_size[1] // 20)
        temp_size = 100

        # draw option labels
        for index in range(len(button_labels)):
            text = pygame.font.Font.render(label_font, button_labels[index][0], True, (255, 255, 255), None)
            temp_size = text.get_width()
            label_surface.blit(text, (option_label_location[0] - text.get_width(),
                                      option_label_offset * index + option_label_location[1] - text.get_height() // 2))

            # create placeholder
            if index > 0:
                text = pygame.font.Font.render(label_font, "True", True, (255, 255, 255), None)
                label_surface.blit(text, (option_label_location[0] + padding,
                                          option_label_offset * index + option_label_location[
                                              1] - text.get_height() // 2))

        options_size = (temp_size, self.screen_size[1] // 20)

        def get_resolution_string():
            return str(self.resolution[0]) + ' x ' + str(self.resolution[1])

        # 3 settings for font size, annoying but good enough

        if self.screen_size[1] > 600 and self.screen_size[0] > 950:
            size_id = '#drop_down_menu'

        elif self.screen_size[1] > 500 and self.screen_size[0] > 700:
            size_id = '#drop_down_menu_medium'
        else:
            size_id = '#drop_down_menu_small'

        # create drop down list for resolution options
        self.resolution_drop_down = UIDropDownMenu(button_labels[0][1],
                                                   get_resolution_string(),
                                                   pygame.Rect((int(options_location[0]),
                                                                int(options_location[1] - options_size[1] // 2)),
                                                               options_size),
                                                   self.manager,
                                                   object_id=size_id)

        # create title text
        title_text = pygame.font.Font.render(pygame.font.Font(
            "../data/fonts/impact.ttf",
            self.screen_size[1] // 5),
            "Options", True, (255, 255, 255), None)

        if title_text.get_width() > self.screen_size[0]:
            scale = self.screen_size[0] / title_text.get_width()
            title_text = pygame.transform.scale(title_text,
                                                (int(title_text.get_width() * scale),
                                                 int(title_text.get_height() * scale)))

        # create screen sized software surface
        title_surface = pygame.Surface(self.screen_size, pygame.SRCALPHA)

        # apply title to screen sized software surface
        title_surface.blit(title_text,
                           (int(self.screen_size[0] / 2 - title_text.get_width() / 2),
                            int(self.screen_size[1] / 5 - title_text.get_height() / 2)))

        # apply title to background surface
        background.blit(title_surface, (0, 0))
        # apply buttons to background surface
        background.blit(label_surface, (0, 0))

        return background

    def generate_graphics_gameui(self):
        # define center coordinates
        center = (self.screen_size[0] / 2, self.screen_size[1] / 2)

        # create surface and apply background color
        background_color = (61, 120, 180)
        background = pygame.Surface(self.screen_size)
        background.fill(background_color)

        self.manager = TitleScreen.init_manager(self.screen_size)

        def intify(location):
            return int(location[0]), int(location[1])

        def rounded_rectangle_flat_bottom(surface, location, width, height, radius, color):
            circle_centers = [intify((location[0] + radius,
                                      location[1] + radius)),
                              intify((location[0] + width - radius - 1,
                                      location[1] + radius))]
            for points in circle_centers:
                pygame.gfxdraw.filled_circle(surface, points[0], points[1], radius, color)

            pygame.gfxdraw.box(surface, pygame.Rect(
                intify((location[0] + radius, location[1])),
                intify((width - radius * 2, height))
            ), color)

            pygame.gfxdraw.box(surface, pygame.Rect(
                intify((location[0], location[1] + radius)),
                intify((width, height - radius))
            ), color)

        def rounded_rectangle(surface, location, width, height, radius, color):
            circle_x = [location[0] + radius, location[0] + width - radius - 1]
            circle_y = [location[1] + radius, location[1] + height - radius - 1]

            circle_centers = [
                (circle_x[0], circle_y[0]),
                (circle_x[0], circle_y[1]),
                (circle_x[1], circle_y[0]),
                (circle_x[1], circle_y[1])
            ]

            for points in circle_centers:
                pygame.gfxdraw.filled_circle(surface, points[0], points[1], radius, color)

            pygame.gfxdraw.box(surface, pygame.Rect(
                intify((location[0] + radius, location[1])),
                intify((width - radius * 2, height))
            ), color)

            pygame.gfxdraw.box(surface, pygame.Rect(
                intify((location[0], location[1] + radius)),
                intify((width, height - radius * 2))
            ), color)

        bottom_panel = pygame.Surface(self.screen_size, pygame.SRCALPHA)

        # bottom panel
        panel_width = self.screen_size[0] // 2
        panel_height = self.screen_size[1] // 10
        panel_corner_radius = panel_height // 2
        color = (255, 255, 255)

        rounded_rectangle_flat_bottom(bottom_panel,
                                      (center[0] - panel_width / 2, self.screen_size[1] - panel_height),
                                      panel_width, panel_height, panel_corner_radius, color)

        bottom_panel_mask = pygame.mask.from_surface(bottom_panel)
        # bottom_panel_mask.invert()
        wood_panel = pygame.Surface(self.screen_size, flags=pygame.SRCALPHA)
        for x in range(0, wood_panel.get_width() + 1):
            for y in range(0, wood_panel.get_height() + 1):
                wood_panel.blit(self.panel_wood_texture[0], (1000 * x, 1000 * y))

        bottom_panel_texture = bottom_panel_mask.to_surface(wood_panel, unsetcolor=None, unsetsurface=None)

        # resource circles
        circle_height = panel_height // 2
        circle_radius = int(panel_height // 3)
        circle_offset = (panel_width - 2 * panel_corner_radius) / 5
        circle_y = self.screen_size[1] - panel_height + panel_corner_radius
        circle_left = center[0] - panel_width / 2 + panel_corner_radius
        circle_centers = []

        for circle in range(0, 6):
            circle_centers.append(intify((circle_left + circle * circle_offset, circle_y)))

        index = 0
        for textures in self.panel_circle_art:
            self.panel_art_scaled[index] = pygame.transform.scale(textures, (circle_radius * 2, circle_radius * 2))
            index += 1

        index = 0
        for amount_panel in range(0, 5):
            rounded_rectangle(bottom_panel, (circle_centers[index][0], circle_centers[index][1]),
                              circle_radius * 2, circle_radius + 1, circle_radius // 8, (120, 120, 120))
            index += 1

        index = 0
        for center in circle_centers:
            bottom_panel.blit(self.panel_art_scaled[index], (center[0] - circle_radius, center[1] - circle_radius))
            index += 1
            pygame.gfxdraw.circle(bottom_panel, center[0], center[1], circle_radius, (0, 0, 0))

        background.blit(bottom_panel, (0, 0))
        # background.blit(bottom_panel_texture, (0, 0))

        return background

    def generate_graphics_main(self):

        # define center coordinates
        center = (self.screen_size[0] / 2, self.screen_size[1] / 2)

        # create surface and apply background color
        background_color = (61, 120, 180)
        background = pygame.Surface(self.screen_size)
        background.fill(background_color)

        self.manager = TitleScreen.init_manager(self.screen_size)

        # function to add menu buttons to UI manager
        def menu_button(location, text):
            self.menu_buttons.append(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(location, (button_width, button_height)),
                text=text, manager=self.manager,
                object_id='#menu_button_square'))

        # the four buttons text
        button_labels = [
            'Join Game',
            'Options',
            'Exit'
        ]

        # button dimensions
        button_width = self.screen_size[0] // 10 * 5
        button_height = self.screen_size[1] // 10

        self.menu_buttons = []
        pygame.font.init()
        button_font = pygame.font.Font("../data/fonts/impact.ttf", self.screen_size[1] // 25)
        button_surface = pygame.Surface(self.screen_size, pygame.SRCALPHA)

        button_scale = 1
        thickness_0 = self.screen_size[0] // 300
        thickness_1 = self.screen_size[1] // 200
        thickness = max(min(thickness_0, thickness_1), 1)

        # add the four buttons
        for index in range(len(button_labels)):
            position = (int(center[0] - button_width / 2),
                        int((4 + index) * button_height))
            menu_button(position, "")

            # create background button text that works alongside py-game gui
            button_text = pygame.font.Font.render(button_font, button_labels[index], True, (255, 255, 255), None)

            if index == 0 and button_text.get_width() > button_width:
                button_scale = button_text.get_width() / button_width

            if button_scale != 1:
                button_text = pygame.transform.scale(button_text,
                                                     (int(button_text.get_width() / button_scale),
                                                      int(button_text.get_height() / button_scale)))

            button_surface.blit(
                button_text,
                (int(center[0] - button_text.get_width() / 2),
                 int((4.5 + index) * button_height - button_text.get_height() / 2))
            )

            # manually draw button borders
            '''
            for index in range(0, thickness):
                border = pygame.Rect((position[0] + index, position[1] + index),
                                     (button_width - 2 * index, button_height - 2 * index))
                pygame.draw.rect(button_surface, (255, 255, 255), border, width=1)
            '''

        # create title text
        title_text = pygame.font.Font.render(pygame.font.Font(
            "../data/fonts/impact.ttf",
            self.screen_size[1] // 5),
            "Frontiersman", True, (255, 255, 255), None)

        if title_text.get_width() > self.screen_size[0]:
            scale = self.screen_size[0] / title_text.get_width()
            title_text = pygame.transform.scale(title_text,
                                                (int(title_text.get_width() * scale),
                                                 int(title_text.get_height() * scale)))

        # create screen sized software surface
        title_surface = pygame.Surface(self.screen_size, pygame.SRCALPHA)

        # apply title to screen sized software surface
        title_surface.blit(title_text,
                           (int(self.screen_size[0] / 2 - title_text.get_width() / 2),
                            int(self.screen_size[1] / 5 - title_text.get_height() / 2)))

        # apply title to background surface
        background.blit(title_surface, (0, 0))
        # apply buttons to background surface
        background.blit(button_surface, (0, 0))

        return background

    def resize(self):
        WINDOW_WIDTH = pygame.display.get_window_size()[0]
        WINDOW_HEIGHT = pygame.display.get_window_size()[1]
        self.screen_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.graphics = self.generate_graphics()


if __name__ == "__main__":
    TitleScreen()
