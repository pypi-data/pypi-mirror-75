import sys, os

import pygame
import pygame.gfxdraw
import pygame_gui
from pygame_gui.core.utility import clipboard_copy

sys.path.insert(0, '../../frontiersman')
from frontiersman.client.ClientGraphics import ClientGraphics
from frontiersman.main.DrawHelper import DrawHelper
from frontiersman.main.PopUp import PopUp
# sys.path.insert(0, '../../frontiersman')
from pygame_gui.elements import UITextEntryLine
from frontiersman.gameboard.Board import *


class GameLobby:
    def create_window(self):
        WINDOW_WIDTH = self.size[0]
        WINDOW_HEIGHT = self.size[1]

        pygame.init()

        pygame.display.set_caption('Startup Menu')
        os.environ['SDL_VIDEODRIVER'] = 'x11'
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        background_color = (61, 120, 180)
        background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        background.fill(background_color)
        self.window.blit(background, (0, 0))
        pygame.display.update()

    def __init__(self, size, host=False, callbacks=None, manager=None):
        self.name = 'Nick'
        self.code = None
        self.font = None
        self.small_font = None
        self.large_font = None
        self.smaller_font = None
        self.state = 'menu'  # menu, join, create
        self.prompt_color = (255, 255, 255)
        self.text_color = (0, 0, 0)
        self.temp_text_color = (127, 127, 127)
        self.size = size
        self.width = self.size[0]
        self.height = self.size[1]
        self.init_pygame()
        self.is_host = host
        self.players = []
        self.loading =False
        # self.is_host = True
        self.notify_window_up = False
        self.notify_windows = []
        self.button_list = []
        self.text_entry_list = []
        self.lobby_status = []
        self.lobby_code = ''
        self.player_code = ''
        self.board = None
        self.leave_lobby = False
        self.quit_gui = False
        self.to_menu = False
        self.run_game = False
        self.host_left = False
        self.player_left= False
        self.client_instance = None
        self.winner=''
        if manager is None:
            self.manager = pygame_gui.UIManager(size, './themes/menu_theme.json')
        else:
            self.manager = manager

        if callbacks is None:
            self.callbacks = []

            def callback_join():
                print('Join callback')

            def callback_quit():
                print('quit callback')

            def callback_create():
                print('create callback')

            def callback_leave():
                print('leave callback')

            self.callbacks.append(callback_join)
            self.callbacks.append(callback_quit)
            self.callbacks.append(callback_create)
            self.callbacks.append(callback_leave)
        else:
            self.callbacks = callbacks

        self.window = pygame.Surface(self.size)

        self.graphics = pygame.Surface(self.size)

        self.create_window()

        self.state = 'menu'

        self.change_state()

        self.animations = []

        self.running = True
        clock = pygame.time.Clock()

        while self.running is True:
            if self.run_game:
                self.state = 'game'
                self.change_state()
                self.run_game = False
            elif self.to_menu:
                self.lobby_code = ''
                self.player_code = ''
                self.name = ''
                self.color = ''
                self.screen_num = ''
                self.players = []
                self.lobby_status = []
                self.state = 'menu'
                self.change_state()
                if self.winner!='':
                    self.create_notification(self.winner+' won!')
                self.to_menu = False
            elif self.host_left:
                self.lobby_code = ''
                self.player_code = ''
                self.name = ''
                self.color = ''
                self.screen_num = ''
                self.players = []
                self.lobby_status = []
                self.state = 'menu'
                self.change_state()
                if not self.is_host:
                    self.create_notification("Host left, lobby terminated")
                self.host_left = False
            elif self.player_left:
                self.lobby_code = ''
                self.player_code = ''
                self.name = ''
                self.color = ''
                self.screen_num = ''
                self.players = []
                self.lobby_status = []
                self.state = 'menu'
                self.change_state()
                #if not self.is_host:
                self.create_notification("A player has left the game")
                self.player_left = False
            if self.state == "game":
                self.client_instance.update_frame()
                if not self.client_instance.running and self.winner=='':
                    break
            else:
                try:
                    time_delta = clock.tick(60) / 1000.0
                    if self.leave_lobby:
                        self.lobby_code = ''
                        self.player_code = ''
                        self.name = ''
                        self.color = ''
                        self.screen_num = ''
                        self.players = []
                        self.lobby_status = []
                        
                        self.state = 'menu'
                        self.change_state()
                        self.leave_lobby = False

                        # pygame.display.quit()
                        # pygame.quit()
                        # break
                    for event in pygame.event.get():
                        # close if X is clicked
                        if event.type == pygame.QUIT:
                            # self.running = False
                            if self.state == 'lobby':
                                self.callbacks[2](self)
                            self.state = 'quit'
                            self.change_state()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.key.key_code('0'):
                                #self.graphics_banner()
                                self.graphics_test()

                        self.manager.process_events(event)
                        if event.type == pygame.USEREVENT:
                            if self.notify_window_up:
                                if event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                                    self.notify_windows.remove(event.ui_element)
                                    if len(self.notify_windows) == 0:
                                        self.notify_window_up = False

                            if self.state == 'create':
                                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                                    # action if client is pressed
                                    if len(self.button_list) != 0:
                                        if event.ui_element == self.button_list[0]:
                                            self.state = 'menu'
                                            self.change_state()
                                        elif event.ui_element == self.button_list[1]:
                                            self.players = []
                                            self.lobby_status = []
                                            self.name = self.text_entry_list[0].get_text()
                                            error_strings = []
                                            error = False
                                            if self.name == '':
                                                error_strings.append('Missing name')
                                                error = True
                                            if error:
                                                self.create_notification(error_strings, True)
                                            else:
                                                if self.callbacks[0](self):
                                                    self.state = 'lobby'
                                                    self.change_state()
                                                else:
                                                    # do nothing I guess
                                                    pass
                            elif self.state == 'lobby':
                                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                                    # action if client is pressed
                                    if len(self.button_list) != 0:
                                        if event.ui_element == self.button_list[0]:
                                            self.leave_lobby = True
                                            self.players = []
                                            self.callbacks[2](self)
                                        elif self.is_host and event.ui_element == self.button_list[1]:
                                            # self.state = 'start_game'
                                            # self.change_state()
                                            self.callbacks[3](self)
                            elif self.state == 'join':
                                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                                    # action if client is pressed
                                    if len(self.button_list) != 0:
                                        if event.ui_element == self.button_list[0]:
                                            self.players = []
                                            self.lobby_status = []
                                            self.name = self.text_entry_list[0].get_text()
                                            self.lobby_code = self.text_entry_list[1].get_text()
                                            error_strings = []
                                            error = False
                                            if self.name == '':
                                                error_strings.append('Missing name')
                                                error = True
                                            if self.lobby_code == '':
                                                error_strings.append('Missing code')
                                                error = True
                                            if error:
                                                self.create_notification(error_strings, True)
                                            else:
                                                res=self.callbacks[1](self)
                                                if res=='success':
                                                    self.state = 'lobby'
                                                    self.change_state()
                                                elif res=='running':
                                                    self.create_notification("Game Already Started")
                                                elif res=='code':
                                                    self.create_notification("Game Not Found")
                                                elif res=='fail':
                                                    self.create_notification("Didn't connect")
                                        elif event.ui_element == self.button_list[1]:
                                            self.state = 'menu'
                                            self.change_state()
                            elif self.state == 'menu':
                                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                                    # action if client is pressed
                                    if len(self.button_list) != 0:
                                        if event.ui_element == self.button_list[0]:
                                            self.state = 'join'
                                            self.is_host = False
                                            self.change_state()
                                        elif event.ui_element == self.button_list[1]:
                                            self.state = 'create'
                                            self.is_host = True
                                            self.change_state()
                                        elif event.ui_element == self.button_list[2]:
                                            self.state = 'quit'
                                            self.change_state()

                    self.manager.update(time_delta)
                    self.window.blit(self.graphics, (0, 0))

                    if len(self.animations) > 0:
                        for animations in self.animations:
                            if animations[1] > 0:
                                self.window.blit(animations[0], (0, 0))
                                animations[0].set_alpha(animations[2])
                                animations[2] -= animations[3]
                                animations[1] -= 1
                            else:
                                self.animations.remove(animations)
                    if self.window is None:
                        self.window=pygame.Surface(self.size)
                    self.manager.draw_ui(self.window)
                    

                    pygame.display.update()
                except AttributeError:
                    print('oof')
        pygame.display.quit()
        pygame.quit()
        sys.exit(0)

    def add_player(self, player):
        self.players.append(player)
        self.lobby_status.append(player.name + ' Joined')
        self.change_state()

    def remove_player(self, player):
        self.players.remove(player)
        self.lobby_status.append(player.name + ' Left')
        self.change_state()

    def set_lobby_code(self, code):
        self.lobby_code = code
        self.change_state()

    def change_state(self):
        background_color = (61, 120, 180)
        background = pygame.Surface(self.size)
        background.fill(background_color)
        self.window.blit(background, (0, 0))

        self.manager.clear_and_reset()
        self.clear_button_list()
        self.clear_text_list()

        flag = False

        if self.state == 'join':
            self.graphics_join()
            flag = True

        if self.state == 'create':
            self.graphics_create()
            flag = True

        if self.state == 'lobby':
            self.graphics_lobby()
            flag = True

        if self.state == 'menu':
            # self.clear_text_list()
            self.graphics_main()
            flag = True

        if self.state == 'game':
            flag = True
            pass
        if self.state == 'game':
            self.winner=''
            self.client_instance.run(self.board)
            flag = True
        if self.state == 'quit':
            self.running = False
            flag = True
        if self.state == 'start':
            self.running = False
            flag = True

        # error handling crash to main menu
        if flag is False:
            print(self.state + ' is not a valid gui state, returning to main menu')
            self.state = 'main'
            self.graphics_main()

        #pygame.display.update()

    def create_10x10(self):
        graphics = pygame.Surface(self.size, flags=pygame.SRCALPHA)

        for x in range(0, 10):
            for y in range(0, 10):
                if (x + y) % 2 == 0:
                    location = (x * 2 + 1, y * 2 + 1)
                    size = (2, 2)
                    DrawHelper.input_box(self.size, graphics, location, size, self.temp_text_color)

        self.window.blit(graphics, (0, 0))
        pygame.display.update()

    def button_list_func(self, insert):
        self.button_list.append(insert)

    def addbackground(self, graphics):
        background_color = (61, 120, 180)
        background = pygame.Surface(self.size)
        background.fill(background_color)
        graphics.blit(background, (0, 0))

    def clear_button_list(self):
        self.button_list = []

    def text_list_func(self, insert):
        self.text_entry_list.append(insert)

    def clear_text_list(self):
        self.text_entry_list = []

    def create_notification(self, text='Wooo.... Error', array=False):
        self.notify_window_up = True

        background_color = (61, 120, 180)
        background = pygame.Surface(self.size)
        background.fill(background_color)
        background.blit(self.graphics, (0, 0))
        self.graphics = background

        popup_size = (400, 300)

        self.notify_windows.append(
            PopUp(
                (self.size[0] // 2 - popup_size[0] // 2,
                 self.size[1] // 2 - popup_size[1] // 2),
                self.manager, text, array, popup_size))

    def ct(self, string):
        if string == 'button':
            return 'button', self.manager, self.button_list_func
        elif string == 'text':
            return 'text', self.manager, self.text_list_func

    def graphics_test(self):
        graphics = ClientGraphics.test_info_cards(self.size, self.small_font, self.smaller_font)
        self.graphics.blit(graphics, (0, 0))

    def graphics_banner(self, text='Cool fading banner wooooo'):
        graphics = pygame.Surface(self.size, flags=pygame.SRCALPHA)

        height = 100
        width = self.size[0]

        #font = pygame.font.Font(self.font, 64)

        transparency = 200
        transparent_step = 2

        shadow_color = (0, 0, 0, transparency)

        element_color = (255, 255, 255, transparency)

        #draw shadow
        location = (0, 6)
        size = (20, 8)
        DrawHelper.rectangle(graphics, location, size[0], size[1], shadow_color)

        #draw center
        location = (0, 8)
        size = (20, 4)
        DrawHelper.rectangle(graphics, location, size[0], size[1], element_color)

        #animation
        self.animations.append([graphics, transparency // transparent_step, transparency, transparent_step])

    def graphics_main(self):
        graphics = pygame.Surface(self.size, flags=pygame.SRCALPHA)

        self.addbackground(graphics)

        # title name text
        location = (10, 4)  # centered
        DrawHelper.big_text('Frontiersman', self.size, graphics, location, self.prompt_color, self.large_font)

        # join game box
        location = (10, 8)
        size = (8, 2)
        DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color, 0, self.ct('button'))
        # join game text
        location = (10, 8)  # centered
        DrawHelper.big_text('Join', self.size, graphics, location, self.text_color, self.font)
        # create game box
        location = (10, 11)
        size = (8, 2)
        DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color, 0, self.ct('button'))
        # create game text
        location = (10, 11)  # centered
        DrawHelper.big_text('Host', self.size, graphics, location, self.text_color, self.font)
        # exit game box
        location = (10, 14)  # centered
        size = (8, 2)
        DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color, 0, self.ct('button'))
        # exit game text
        location = (10, 14)  # centered
        DrawHelper.big_text('Exit', self.size, graphics, location, self.text_color, self.font)

        self.graphics = graphics
        #pygame.display.update()

    def graphics_join(self):

        graphics = pygame.Surface(self.size, flags=pygame.SRCALPHA)

        self.addbackground(graphics)

        # name text
        location = (10, 3)  # centered
        DrawHelper.big_text('Name', self.size, graphics, location, self.prompt_color, self.font)

        # invite text
        location = (10, 9)  # centered
        DrawHelper.big_text('Invite Code', self.size, graphics, location, self.prompt_color, self.font)

        # Name input box
        location = (10, 5)
        size = (8, 2)
        DrawHelper.input_box(
            self.size, graphics, location, size, self.prompt_color, 0, self.ct('text'), name='#name_input')

        # invite code box
        location = (10, 11)
        size = (8, 2)
        DrawHelper.input_box(
            self.size, graphics, location, size, self.prompt_color, 0, self.ct('text'), name='#invite_code')

        padding = 5

        # join button
        location = (12, 15)
        size = (4, 2)
        DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color, padding, self.ct('button'))

        # join button text
        location = (12, 15)
        DrawHelper.big_text('Join', self.size, graphics, location, self.text_color, self.font)

        # back button
        location = (8, 15)
        size = (4, 2)
        DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color, padding, self.ct('button'))

        # back button text
        location = (8, 15)
        DrawHelper.big_text('Back', self.size, graphics, location, self.text_color, self.font)

        # self.window.blit(graphics, (0, 0))
        self.graphics = graphics
        #pygame.display.update()

    def graphics_create(self):

        graphics = pygame.Surface(self.size, flags=pygame.SRCALPHA)

        self.addbackground(graphics)

        # name text
        location = (10, 5)  # centered
        DrawHelper.big_text('Name', self.size, graphics, location, self.prompt_color, self.font)

        # Name input box
        location = (10, 7)
        size = (8, 2)
        DrawHelper.input_box(
            self.size, graphics, location, size, self.prompt_color, 0, self.ct('text'), name='#name_input')

        padding = 5

        # back button
        location = (8, 12)
        size = (4, 2)
        DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color, padding, self.ct('button'))
        # back button text
        location = (8, 12)
        DrawHelper.big_text('Back', self.size, graphics, location, self.text_color, self.font)

        # join button
        location = (12, 12)
        size = (4, 2)
        DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color, padding, self.ct('button'))
        # join button text
        location = (12, 12)
        DrawHelper.big_text('Join', self.size, graphics, location, self.text_color, self.font)

        # self.window.blit(graphics, (0, 0))
        self.graphics = graphics
        #pygame.display.update()

    def graphics_lobby(self):
        graphics = pygame.Surface(self.size, flags=pygame.SRCALPHA)

        self.addbackground(graphics)

        '''
        #text
        location = (10, 3)  # centered
        DrawHelper.big_text('Name', self.size, graphics, location, self.prompt_color, self.font)

        #rectangle
        location = (10, 9)  # centered
        size = (1, 1)
        DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color)
        '''

        # RECTANGLES

        padding = 5

        # top area
        location = (10, 3)
        size = (12, 2)
        DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color, padding)

        # top text
        location = (10, 3)  # centered
        DrawHelper.big_text(
            'Lobby Code: ' + str(self.lobby_code), self.size, graphics, location, self.text_color, self.font)

        # left area

        # left title area
        location = (6, 5)  # centered
        size = (4, 2)
        DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color, padding)

        # left title
        DrawHelper.big_text('Lobby History', self.size, graphics, location, self.text_color,
                            self.small_font)

        # left text area
        location = (6, 11)  # centered
        size = (4, 10)
        DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color, padding)
        # left text
        padding = 1
        count = 0
        location = (6, 7 - 1)
        for message in reversed(self.lobby_status):
            if count < 9:
                location = (location[0], location[1] + padding)
                DrawHelper.big_text(
                    message, self.size, graphics, location, self.text_color, self.small_font, width=size[0])
                count += 1
            else:
                break
        # right area

        padding = 5

        # right title area
        location = (12, 5)  # centered
        size = (8, 2)
        DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color, padding)
        # right title
        location = (12, 5)
        DrawHelper.big_text('Players:  ' + str(len(self.players)) + '/' + '4',
                            self.size, graphics, location, self.text_color, self.font)
        # right text area
        location = (12, 11)  # centered
        size = (8, 10)
        DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color, padding)
        # right text
        index = 1
        count = 0
        location = (12, 7 - 2)
        for player in self.players:
            if count < 5:
                location = (location[0], location[1] + index * 2)
                DrawHelper.big_text(player.name + ' [' + player.color + ']', self.size, graphics, location, self.text_color, self.font, width=size[0])
                count += 1
            else:
                break
        # middle button
        location = (14, 17)  # centered
        size = (4, 2)
        DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color, padding, self.ct('button'))

        # left button (only if host)
        if self.is_host:
            location = (6, 17)  # centered
            size = (4, 2)
            DrawHelper.input_box(self.size, graphics, location, size, self.prompt_color, padding, self.ct('button'))
        # TEXT

        # left area

        # right area

        # left button (only if host)
        if self.is_host:
            location = (6, 17)  # centered
            DrawHelper.big_text('Start', self.size, graphics, location, self.text_color, self.font)
        # middle button
        location = (14, 17)  # centered
        DrawHelper.big_text('Leave', self.size, graphics, location, self.text_color, self.font)

        # self.window.blit(graphics, (0, 0))
        self.graphics = graphics
        #pygame.display.update()

    def init_pygame(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font("./data/fonts/impact.ttf", self.size[1] // 12)
        self.large_font = pygame.font.Font("./data/fonts/impact.ttf", self.size[1] // 6)
        self.small_font = pygame.font.Font("./data/fonts/impact.ttf", self.size[1] // 24)
        self.smaller_font = pygame.font.Font("./data/fonts/impact.ttf", self.size[1] // 36)

if __name__ == "__main__":
    GameLobby((1200, 900))