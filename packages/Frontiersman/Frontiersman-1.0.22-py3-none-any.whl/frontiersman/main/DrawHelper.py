import pygame
import pygame.gfxdraw
import pygame_gui
from pygame_gui.elements import UITextEntryLine


class DrawHelper:
    @staticmethod
    def x_centered(size, location):
        return location[0] - size[0] // 2, location[1]

    @staticmethod
    def y_centered(size, location):
        return location[0], location[1] - size[1] // 2

    @staticmethod
    def xy_centered(size, location):
        return location[0] - size[0] // 2, location[1] - size[1] // 2

    @staticmethod
    def input_box(screen_size, surface, location, size, color, padding=0, function=None, name=None, radius=10):
        # tired of copy pasting, function is [string (type of function), ui manager, callback for adding it]
        h_scale = screen_size[0] // 20
        v_scale = screen_size[1] // 20
        size = (size[0] * h_scale - padding, size[1] * v_scale - padding)
        location = (location[0] * h_scale, location[1] * v_scale)
        location = DrawHelper.xy_centered(size, location)
        if function is not None:
            if function[0] == 'button':
                function[2](
                    pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect(location, size),
                        text='', manager=function[1],
                        object_id='#menu_button_rounded')
                )
                DrawHelper.rounded_rectangle(
                    surface, location, size[0],
                    size[1], radius, color)
            if function[0] == 'text':
                text_entry = UITextEntryLine(
                    relative_rect=pygame.Rect(location, size),
                    manager=function[1],
                    object_id=name)
                text_entry.set_forbidden_characters([',', '|', '&', '\\', '#'])
                function[2](text_entry)
                DrawHelper.rounded_rectangle(
                    surface, location, size[0],
                    size[1], radius, (61, 120, 180))
        else:
            DrawHelper.rounded_rectangle(
                surface, location, size[0],
                size[1], radius, color)

    @staticmethod
    def big_text(text, screen_size, surface, location, color, font, width=None):
        text_surface = pygame.font.Font.render(font, text, True, color, None)
        if width is None:
            pass
        else:
            h_scale = screen_size[0] // 20
            max_width = width * h_scale - h_scale * 0.5
            text_surface = pygame.font.Font.render(font, text, True, color, None)
            if text_surface.get_width() >= max_width:
                new_ratio = text_surface.get_width() / max_width
                new_height = int(text_surface.get_height() / new_ratio)
                new_width = int(text_surface.get_width() / new_ratio)
                text_surface = pygame.transform.scale(text_surface, (new_width, new_height))
        position = (int(screen_size[0] // 20 * location[0] - text_surface.get_width() / 2),
                    int(screen_size[1] // 20 * location[1] - text_surface.get_height() / 2))
        surface.blit(text_surface, position)

    @staticmethod
    def left_text(text, screen_size, surface, location, color, font, padding):
        text = pygame.font.Font.render(font, text, True, color, None)
        position = (int(screen_size[0] // 20 * location[0] + padding),
                    int(screen_size[1] // 20 * location[1]) - text.get_height() / 2)
        surface.blit(text, position)

    @staticmethod
    def intify(float_tuple):
        return int(float_tuple[0]), int(float_tuple[1])

    @staticmethod
    def rounded_rectangle(surface, location, width, height, radius, color):
        circle_x = DrawHelper.intify((location[0] + radius, location[0] + width - radius - 1))
        circle_y = DrawHelper.intify((location[1] + radius, location[1] + height - radius - 1))

        circle_centers = [
            (circle_x[0], circle_y[0]),
            (circle_x[0], circle_y[1]),
            (circle_x[1], circle_y[0]),
            (circle_x[1], circle_y[1])
        ]

        for points in circle_centers:
            pygame.gfxdraw.filled_circle(surface, points[0], points[1], radius, color)

        pygame.gfxdraw.box(surface, pygame.Rect(
            DrawHelper.intify((location[0] + radius, location[1])),
            DrawHelper.intify((width - radius * 2, height))
        ), color)

        pygame.gfxdraw.box(surface, pygame.Rect(
            DrawHelper.intify((location[0], location[1] + radius)),
            DrawHelper.intify((width, height - radius * 2))
        ), color)

    @staticmethod
    def rectangle(surface, location, width, height, color):

        h_scale = surface.get_width() // 20
        v_scale = surface.get_height() // 20

        location = DrawHelper.intify((h_scale * location[0], v_scale * location[1]))
        size = DrawHelper.intify((h_scale * width, v_scale * height))

        pygame.gfxdraw.box(surface, pygame.Rect(
            DrawHelper.intify(location),
            DrawHelper.intify(size)
        ), color)
