import subprocess
import sys

import pygame
import pygame_gui
from frontiersman.gameboard.Board import *
from pygame_gui.elements import UITextEntryLine

sys.path.insert(0, '../src')


# os.environ['SDL_AUDIODRIVER'] = 'dsp'
# os.putenv("DISPLAY", "localhost:0")
# os.environ['SDL_AUDIODRIVER'] = 'x11'


class startup:

    def __init__(self):
        self.children = []
        self.startup()

    def open_client(self):
        exec(open('client.py').read())

    def open_server(self):
        exec(open('server.py').read())

    def startup(self):
        WINDOW_WIDTH = 300
        WINDOW_HEIGHT = 200

        pygame.init()

        pygame.display.set_caption('Startup Menu')
        center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), './themes/button_theme.json')
        clock = pygame.time.Clock()

        background_color = (61, 120, 180)
        background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        background.fill(background_color)

        # button dimensions
        button_width = 240
        button_height = 40
        padding = 10

        # text box dimensions
        entry_width = 240
        entry_height = 40
        padding = 10

        position = (int(center[0] - button_width / 2),
                    int(center[1] - button_height - padding - entry_height + 25))
        server_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (button_width, button_height)),
                                                     text='Host', manager=manager, object_id='#standard_button')

        position = (int(center[0] - button_width / 2),
                    int(center[1] + padding / 2 + 25))
        client_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (button_width, button_height)),
                                                     text='Connect', manager=manager, object_id='#standard_button')

        position = (int(center[0] - button_width / 2),
                    int(center[1] - padding / 2 - entry_height / 2 + 25))

        ip_entry = UITextEntryLine(relative_rect=pygame.Rect(position, (button_width - 80, button_height)),
                                   manager=manager, object_id='#text_entry')

        position = (int(center[0] - button_width / 2 + button_width - 80 + padding),
                    int(center[1] - padding / 2 - entry_height / 2 + 25))

        port_entry = UITextEntryLine(relative_rect=pygame.Rect(position, (80 - padding, button_height)),
                                     manager=manager, object_id='#text_entry')

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

                # close if ESC is pressed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        # action if client is pressed
                        if event.ui_element == client_button:
                            client_flag = True
                            # print('Client created')
                        # action if server is pressed
                        if event.ui_element == server_button:
                            server_flag = True

                manager.process_events(event)

            manager.update(time_delta)

            window.blit(background, (0, 0))
            manager.draw_ui(window)

            pygame.display.update()

            if client_flag:
                client_flag = False
                self.children.append(subprocess.Popen([sys.executable, './ClientMain.py']))

            if server_flag:
                server_flag = False
                self.children.append(subprocess.Popen([sys.executable, './server.py']))


test = startup()
