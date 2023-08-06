from typing import Union

import pygame
from pygame_gui.core import UIElement, IContainerLikeInterface
from pygame_gui.elements import UIWindow, UIImage, UIVerticalScrollBar

IMAGE_SIZE = (624, 804)


class HelpImage(UIVerticalScrollBar):
    def __init__(self, ui_manager,
                 container: Union[IContainerLikeInterface, None] = None,
                 parent_element: UIElement = None, ):
        super().__init__(relative_rect=pygame.Rect((IMAGE_SIZE[0] - 32 - 2, 0 - 2), (32 + 2, 346)),
                         visible_percentage=.62,
                         manager=ui_manager,
                         container=container,
                         parent_element=parent_element)
        self.HELP_IMAGE = pygame.image.load('./assets/help.png')
        self.size = self.HELP_IMAGE.get_size()
        self.background = pygame.Surface(self.size)
        self.background.fill((0, 0, 0))
        self.visible_percentage = .5
        self.manager = ui_manager
        self.background = pygame.Surface(self.size)
        self.background = self.background.convert()

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.HELP_IMAGE, (0, 0 - int(self.scroll_position * 4)))


class HelpWindow(UIWindow):
    def __init__(self, position, ui_manager):
        self.size = (IMAGE_SIZE[0] + 28, 400)
        super().__init__(pygame.Rect(position, self.size), ui_manager,
                         window_display_title='Help Window',
                         object_id='#help_window')

        surface_size = self.get_container().get_size()
        self.surface_element = UIImage(pygame.Rect((0, 0),
                                                   surface_size),
                                       pygame.Surface(surface_size).convert(),
                                       manager=ui_manager,
                                       container=self,
                                       parent_element=self)

        self.help_image = HelpImage(ui_manager, container=self, parent_element=self)

        self.is_active = False

        self.set_blocking(True)

    def update(self, time_delta):
        super().update(time_delta)

        self.help_image.draw(self.surface_element.image)
