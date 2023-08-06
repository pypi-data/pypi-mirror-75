import pygame
from pygame_gui.elements import UIWindow, UIImage


# todo resize properly

class Notification:
    def __init__(self, ui_manager, size, text, array=False):
        self.size = (size[0], size[1])
        self.background = pygame.Surface(self.size, flags=pygame.SRCALPHA)
        self.background.fill((255, 255, 255))
        self.manager = ui_manager
        self.background = self.background.convert()

        self.square = (size[0] - 32, size[1] - 59)

        self.text = []

        if not array:
            self.text.append(text)
        else:
            self.text = text

        self.text_surface = pygame.Surface(self.square, flags=pygame.SRCALPHA)

        pygame.font.init()
        self.font = pygame.font.Font("./data/fonts/impact.ttf", 24)
        self.text_height = 24
        self.line_padding = 24

        num_lines = len(self.text)
        center_x = self.square[0] // 2
        center_y = self.square[1] // 2

        if num_lines % 2 == 0:
            start_y = int(
                center_y - (num_lines // 2 + 1) * self.text_height - (num_lines // 2 - 0.5 * self.line_padding))
        else:
            start_y = int(center_y - ((num_lines // 2) + 0.5) * self.text_height - (num_lines // 2 * self.line_padding))
        for index in range(0, num_lines):
            text_line = pygame.font.Font.render(self.font, self.text[index], True, (0, 0, 0), None)
            self.text_surface.blit(
                text_line,
                (int(center_x - text_line.get_width() // 2),
                 int(start_y + index * (self.text_height + self.line_padding))))

        self.background.blit(
            self.text_surface, (
                int(self.square[0] // 2 - self.text_surface.get_width() // 2),
                int(self.square[1] // 2 - self.text_surface.get_height() // 2))
        )

    def draw(self, surface):
        surface.blit(self.background, (0, 0))


class PopUp(UIWindow):
    def __init__(self, position, ui_manager, text, array=False, size=(300, 100)):
        self.size = size
        super().__init__(pygame.Rect(position, self.size), ui_manager,
                         window_display_title='Notification',
                         object_id='#help_window')

        surface_size = self.get_container().get_size()
        self.surface_element = UIImage(pygame.Rect((0, 0),
                                                   surface_size),
                                       pygame.Surface(surface_size).convert(),
                                       manager=ui_manager,
                                       container=self,
                                       parent_element=self)

        self.text_image = Notification(ui_manager, self.size, text, array)

        self.is_active = False

        self.set_blocking(True)

    def update(self, time_delta):
        super().update(time_delta)

        self.text_image.draw(self.surface_element.image)
