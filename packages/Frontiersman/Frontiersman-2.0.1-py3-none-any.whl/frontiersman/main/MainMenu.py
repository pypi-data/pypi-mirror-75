import sys

import pygame
import pygame_gui

sys.path.insert(0, '../frontiersman')


# os.environ['SDL_AUDIODRIVER'] = 'dsp'
# os.putenv("DISPLAY", "localhost:0")
# os.environ['SDL_AUDIODRIVER'] = 'x11'


class MultiplayerMenu:
    def __init__(self):
        pass


class MainMenu:

    def resize(self, window, manager):
        WINDOW_WIDTH = pygame.display.get_window_size()[0]
        WINDOW_HEIGHT = pygame.display.get_window_size()[1]

        Colors = {
            'Red': (127, 0, 0),
            'Cyan': (0, 255, 255),
            'Orange': (255, 106, 0),
            'Blue': (0, 38, 255),
            'Green': (0, 153, 15),
            'Pink': (255, 0, 110),
            'Yellow': (255, 216, 0)
        }

        pygame.init()

        pygame.display.set_caption('Frontiersman Menu')
        center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        clock = pygame.time.Clock()

        background_color = (61, 120, 180)
        background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        background.fill(background_color)

        # function to add menu buttons to UI manager
        manager.clear_and_reset()

        def menu_button(location, text):
            menu_buttons.append(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(location, (button_width, button_height)),
                text=text, manager=manager,
                object_id='#menu_button_square'))

            # the four buttons text

        button_labels = [
            'Singleplayer',
            'Multiplayer',
            'Options',
            'Exit'
        ]
        # button dimensions
        button_width = WINDOW_HEIGHT // 10 * 5
        button_height = WINDOW_HEIGHT // 10
        padding = 0

        menu_buttons = []
        menu_title = []
        pygame.font.init()
        button_font = pygame.font.Font("../data/fonts/impact.ttf", WINDOW_HEIGHT // 30)
        button_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        # add the four buttons
        for index in (0, 1, 2, 3):
            position = (int(center[0] - button_width / 2),
                        int((4 + index) * button_height))
            # menu_button(position, button_labels[index])
            menu_button(position, "")
            # create background button text so its more easily scaled
            button_text = pygame.font.Font.render(button_font, button_labels[index], True, (255, 255, 255), None)
            button_surface.blit(
                button_text,
                (int(center[0] - button_text.get_width() / 2),
                 int((4.5 + index) * button_height - button_text.get_height() / 2))
            )

        # title dimensions
        entry_width = WINDOW_WIDTH // 4 * 3
        entry_height = WINDOW_HEIGHT // 5
        padding = 0

        title_font = pygame.font.Font("../data/fonts/impact.ttf", WINDOW_HEIGHT // 5)

        title_text = pygame.font.Font.render(title_font, "Frontiersman", True, (255, 255, 255), None)

        title_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        title_surface.blit(title_text, (int(WINDOW_WIDTH / 2 - title_text.get_width() / 2),
                                        int(WINDOW_HEIGHT / 5 - title_text.get_height() / 2)))

        # update screen
        pygame.display.flip()
        return window, title_surface, button_surface

    def __init__(self):
        self.children = []
        self.user_interface()

    def open_client(self):
        exec(open('client.py').read())

    def user_interface(self):
        RESOLUTION = "720p"
        RESOLUTION_DICT = {
            "1080p": (1920, 1080),
            "720p": (1280, 720)
        }

        WINDOW_WIDTH = RESOLUTION_DICT.get(RESOLUTION)[0]
        WINDOW_HEIGHT = RESOLUTION_DICT.get(RESOLUTION)[1]

        test_string = "Awesome"

        pygame.init()

        pygame.display.set_caption('Frontiersman Menu')
        center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.RESIZABLE)
        manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), '../themes/button_theme.json')
        clock = pygame.time.Clock()

        background_color = (61, 120, 180)
        background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        background.fill(background_color)

        # function to add menu buttons to UI manager
        def menu_button(location, text):
            menu_buttons.append(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(location, (button_width, button_height)),
                text=text, manager=manager,
                object_id='#menu_button_square'))

        # the four buttons text
        button_labels = [
            'Singleplayer',
            'Multiplayer',
            'Options',
            'Exit'
        ]
        # button dimensions
        button_width = WINDOW_HEIGHT // 10 * 5
        button_height = WINDOW_HEIGHT // 10
        padding = 0

        menu_buttons = []
        menu_title = []
        pygame.font.init()
        button_font = pygame.font.Font("../data/fonts/impact.ttf", WINDOW_HEIGHT // 30)
        button_surface = pygame.Surface(RESOLUTION_DICT.get(RESOLUTION), pygame.SRCALPHA)

        # add the four buttons
        for index in (0, 1, 2, 3):
            position = (int(center[0] - button_width / 2),
                        int((4 + index) * button_height))
            # menu_button(position, button_labels[index])
            menu_button(position, "")
            # create background button text so its more easily scaled
            button_text = pygame.font.Font.render(button_font, button_labels[index], True, (255, 255, 255), None)
            button_surface.blit(
                button_text,
                (int(center[0] - button_text.get_width() / 2),
                 int((4.5 + index) * button_height - button_text.get_height() / 2))
            )

        # title dimensions
        entry_width = WINDOW_WIDTH // 4 * 3
        entry_height = WINDOW_HEIGHT // 5
        padding = 0

        title_font = pygame.font.Font("../data/fonts/impact.ttf", WINDOW_HEIGHT // 5)

        title_text = pygame.font.Font.render(title_font, "Frontiersman", True, (255, 255, 255), None)

        title_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

        title_surface.blit(title_text, (int(WINDOW_WIDTH / 2 - title_text.get_width() / 2),
                                        int(WINDOW_HEIGHT / 5 - title_text.get_height() / 2)))

        # update screen
        pygame.display.flip()

        running = True
        client_flag = False
        server_flag = False

        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                # close if X is clicked
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.VIDEORESIZE:
                    # initialize_gui()
                    pass
                # close if ESC is pressed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        # action if client is pressed
                        if event.ui_element == menu_buttons[3]:
                            client_flag = True
                            # print('Client created')

                manager.process_events(event)

            manager.update(time_delta)

            window.blit(background, (0, 0))
            window.blit(button_surface, (0, 0))
            window.blit(title_surface, (0, 0))
            manager.draw_ui(window)

            pygame.display.update()

            if client_flag:
                running = False
                client_flag = False
                # self.children.append(subprocess.Popen([sys.executable, './ClientMain.py']))
                pygame.quit()
                # start_instance = client(ip_entry.text, port_entry.text, name_entry.text)


if __name__ == "__main__":
    MainMenu()
