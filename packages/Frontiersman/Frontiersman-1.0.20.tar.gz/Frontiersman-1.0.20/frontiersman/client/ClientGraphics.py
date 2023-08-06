import os
import sys

import pygame
import pygame.gfxdraw

sys.path.insert(0, '../../frontiersman')
from frontiersman.main.DrawHelper import DrawHelper


class ClientGraphics:
    @staticmethod
    def top_and_bottom_bar(screen_size, small_font):
        graphics = pygame.Surface(screen_size, flags=pygame.SRCALPHA)

        color = (255, 255, 255)

        # bottom bar
        location = (10, 19)
        size = (20, 2)
        DrawHelper.input_box(screen_size, graphics, location, size, color, padding=0, radius=0)

        # top bar
        location = (10, 0.5)
        size = (20, 1)
        DrawHelper.input_box(screen_size, graphics, location, size, color, padding=0, radius=0)

        color = (0, 0, 0)

        # help button
        location = (1.5, 0.5)
        DrawHelper.big_text('Help', screen_size, graphics, location, color, small_font)

        # exit button
        location = (0.5, 0.5)
        DrawHelper.big_text('Exit', screen_size, graphics, location, color, small_font)

        return graphics

    @staticmethod
    def hand_area(screen_size, small_font, smaller_font):
        graphics = pygame.Surface(screen_size, flags=pygame.SRCALPHA)

        location = (10, 18.5)
        size = (8, 3)
        position = (6, 17)
        color = (255, 255, 255)
        DrawHelper.input_box(screen_size, graphics, location, size, color, padding=0, radius=10)

        return graphics

    @staticmethod
    def action_buttons(screen_size, small_font, smaller_font, action=True):
        # def big_text(text, screen_size, surface, location, color, font, width=None):
        graphics = pygame.Surface(screen_size, flags=pygame.SRCALPHA)

        # end turn
        location = (18, 19)
        size = (4, 2)
        position = (16, 18)
        color = (255, 255, 255)
        DrawHelper.input_box(screen_size, graphics, location, size, color, padding=0, radius=0)

        color = (0, 0, 0)

        DrawHelper.big_text('End Turn', screen_size, graphics, location, color, small_font)

        # Actions
        location = (15, 19)
        size = (2, 2)
        color = (255, 255, 255)
        DrawHelper.input_box(screen_size, graphics, location, size, color, padding=0, radius=0)

        color = (0, 0, 0)

        DrawHelper.big_text('Actions', screen_size, graphics, location, color, small_font)

        if action:
            # Trade
            location = (15, 17)
            size = (2, 2)
            color = (255, 255, 255)
            DrawHelper.input_box(screen_size, graphics, location, size, color, padding=0, radius=0)

            color = (0, 0, 0)

            DrawHelper.big_text('Trade', screen_size, graphics, location, color, small_font)

            # Buy
            location = (15, 15)
            size = (2, 2)
            color = (255, 255, 255)
            DrawHelper.input_box(screen_size, graphics, location, size, color, padding=0, radius=0)

            color = (0, 0, 0)

            DrawHelper.big_text('Buy', screen_size, graphics, location, color, small_font)

            # Play dev card
            location = (15, 13)
            size = (2, 2)
            color = (255, 255, 255)
            DrawHelper.input_box(screen_size, graphics, location, size, color, padding=0, radius=0)

            color = (0, 0, 0)

            DrawHelper.big_text('Dev Card', screen_size, graphics, location, color, small_font)

        return graphics

    @staticmethod
    def test_info_cards(size, small_font, smaller_font):
        graphics = pygame.Surface(size, flags=pygame.SRCALPHA)

        graphics.blit(ClientGraphics.top_and_bottom_bar(size, smaller_font), (0, 0))

        graphics.blit(ClientGraphics.bank_info_card(size, smaller_font), (0, 0))

        graphics.blit(ClientGraphics.hand_area(size, small_font, smaller_font), (0, 0))

        graphics.blit(ClientGraphics.action_buttons(size, small_font, smaller_font), (0, 0))

        for player_number in range(0, 2):
            graphics.blit(ClientGraphics.player_info_card(size, small_font, smaller_font,
                                                          player=player_number,
                                                          name='Player ' + str(player_number),
                                                          num_cards=5,
                                                          inventory=(4, 6, 2, 15, 12, 5)),
                          (0, 0))
        return graphics

    @staticmethod
    def bank_info_card(screen_size, small_font, cards=None):
        bank_surface = pygame.Surface(screen_size, flags=pygame.SRCALPHA)

        h_scale = screen_size[0] // 20
        v_scale = screen_size[1] // 20

        position = (15, 0)
        location = (17.5, 1)

        bank_image_size = (80, 80)
        try:
            base_path = os.path.dirname(__file__)
            bank_image_load = pygame.image.load(os.path.join(base_path, '../assets/bank/bank_outlined_80x80.png'))
            bank_image = pygame.transform.scale(bank_image_load, bank_image_size)
        except:
            print('Failed to load bank image')
            bank_image = pygame.Surface(screen_size, flags=pygame.SRCALPHA)
            pygame.draw.rect(bank_image, pygame.Rect(DrawHelper.intify((position[0] * h_scale, position[1] * v_scale)),
                                                     bank_image_size))

        image_size = (45, 45)
        inventory_icons = ClientGraphics.scale_bank(image_size)

        if cards is None:
            card_list = [19, 19, 19, 19, 19, 20]
        else:
            card_list = cards

        # bank area
        color = (255, 255, 255)
        # color = (100, 100, 100)
        size = (5, 2)
        # bank area art
        color = (0, 0, 0, 120)
        DrawHelper.input_box(screen_size, bank_surface, location, size, color, padding=0, radius=5)
        color = (255, 255, 255)
        DrawHelper.input_box(screen_size, bank_surface, location, size, color, padding=2, radius=5)

        # maths
        pixel_position = (position[0] * h_scale, position[1] * v_scale)
        player_info_card_size = (screen_size[0] // 5, screen_size[1] // 10)
        player_info_card_center = (
            pixel_position[0] + player_info_card_size[0] // 2,
            pixel_position[1] + player_info_card_size[1] // 2)

        bank_image_area_center = (int(pixel_position[0] + h_scale - bank_image_size[0]),
                                  int(pixel_position[1] + v_scale - bank_image_size[1] // 2))

        # draw bank symbol
        bank_surface.blit(bank_image, bank_image_area_center)

        # draw icons
        icon_top_padding = 5
        icon_side_padding = 20
        icon_width = image_size[0]
        icon_tray_max_width = player_info_card_size[0] - 2 * icon_side_padding
        icon_padding = (icon_tray_max_width - 6 * icon_width) / 5

        index = 0
        for image in inventory_icons:
            bank_surface.blit(
                image, (int(pixel_position[0] + icon_side_padding + index * (icon_padding + icon_width) + h_scale),
                        int(player_info_card_center[1] - player_info_card_size[
                            1] // 4 - icon_width // 2 + icon_top_padding)))
            index += 1

        color = (0, 0, 0)

        # draw numbers for icons
        index = 0
        for number in card_list:
            text_surface = pygame.font.Font.render(small_font, str(number), True, color, None)
            bank_surface.blit(
                text_surface,
                (int(pixel_position[0] + icon_side_padding + index * (
                        icon_padding + icon_width) + icon_width // 2 - text_surface.get_width() // 2 + h_scale),
                 int(player_info_card_center[1] + player_info_card_size[1] // 4 - text_surface.get_height() // 2)))
            index += 1

        return bank_surface

    @staticmethod
    def player_info_card(screen_size, font, small_font, name='Zander', num_cards=0, inventory=None, player=0,
                         team_color=(120, 0, 0)):

        if inventory is None:
            player_thing_list = (5, 11, 3, 15, 7, 4)
        else:
            player_thing_list = inventory

        image_surface = pygame.Surface(screen_size, pygame.SRCALPHA)

        h_scale = screen_size[0] // 20
        v_scale = screen_size[1] // 20

        position = (16, 14 - player * 4)
        location = (18, 16 - player * 4)
        pixel_position = (position[0] * h_scale, position[1] * v_scale)
        player_info_card_size = (screen_size[0] // 5, screen_size[1] // 5)
        player_info_card_center = (
            pixel_position[0] + player_info_card_size[0] // 2,
            pixel_position[1] + player_info_card_size[1] // 2)

        image_size = (35, 35)
        inventory_icons = ClientGraphics.scale_logos(image_size)

        # card placeholder art
        card_width = 20
        card_height = 38
        card_side_padding = 10
        card_padding = 10
        max_width = player_info_card_size[0] - card_side_padding * 2
        card_art_thickness = 2
        card_art = pygame.Surface((card_width, card_height))
        card_art_face = pygame.Surface((card_width - card_art_thickness * 2, card_height - card_art_thickness * 2))
        card_art_face.fill((255, 255, 255))
        card_art.blit(card_art_face, (card_art_thickness, card_art_thickness))

        # first player
        size = (4, 4)
        color = (0, 0, 0, 120)
        DrawHelper.input_box(screen_size, image_surface, location, size, color, padding=1)
        color = (255, 255, 255)
        DrawHelper.input_box(screen_size, image_surface, location, size, color, padding=5)
        # player name
        location = (location[0], location[1] - 1.5)
        color = (0, 0, 0)
        DrawHelper.big_text(name, screen_size, image_surface, location, color, font)
        # player hand

        # make padding smaller so cards fit in box
        if num_cards * card_width + (num_cards - 1) * card_padding > max_width:
            card_padding = (max_width - card_side_padding * 2 - card_width * num_cards) / (num_cards - 1)

        # origin to draw cards from
        start_x = pixel_position[0] + card_side_padding \
                  + (max_width - (num_cards * card_width) - (num_cards - 1) * card_padding) // 2
        start_y = player_info_card_center[1] - player_info_card_size[1] // 8 - card_height // 2

        # draw cards
        for index in range(0, num_cards):
            image_surface.blit(card_art, (int(start_x + index * (card_width + card_padding)), int(start_y)))

        # draw icons
        icon_side_padding = 20
        icon_width = 35
        icon_tray_max_width = player_info_card_size[0] - 2 * icon_side_padding
        icon_padding = (icon_tray_max_width - 6 * icon_width) / 5

        bit_masks = ClientGraphics.scale_masks(image_size)
        for mask in bit_masks:
            mask.set_colorkey((255, 255, 255))

        index = 0
        for image in inventory_icons:
            if index in (3, 4, 5):
                color_surface = pygame.Surface(image_size, flags=pygame.SRCALPHA)
                color_surface.fill(team_color)
                color_surface.blit(bit_masks[index - 3], (0, 0))
                color_surface.set_colorkey((0, 0, 0))
                image_surface.blit(
                    color_surface, (int(pixel_position[0] + icon_side_padding + index * (icon_padding + icon_width)),
                                    int(player_info_card_center[1] + player_info_card_size[1] // 8 - icon_width // 2)))
            image_surface.blit(
                image, (int(pixel_position[0] + icon_side_padding + index * (icon_padding + icon_width)),
                        int(player_info_card_center[1] + player_info_card_size[1] // 8 - icon_width // 2)))
            index += 1

        # draw numbers for icons
        index = 0
        for number in player_thing_list:
            text_surface = pygame.font.Font.render(small_font, str(number), True, color, None)
            image_surface.blit(
                text_surface,
                (int(pixel_position[0] + icon_side_padding + index * (
                        icon_padding + icon_width) + icon_width // 2 - text_surface.get_width() // 2),
                 int(player_info_card_center[1] + 3 * player_info_card_size[1] // 8 - text_surface.get_height() // 2)))
            index += 1

        return image_surface

    @staticmethod
    def scale_logos(logo_size):
        base_path = os.path.dirname(__file__)
        logo_images = [
            pygame.image.load(os.path.join(base_path, '../assets/player/star.png')),
            pygame.image.load(os.path.join(base_path, '../assets/player/road.png')),
            pygame.image.load(os.path.join(base_path, '../assets/player/army.png')),
            pygame.image.load(os.path.join(base_path, '../assets/player/num_roads.png')),
            pygame.image.load(os.path.join(base_path, '../assets/player/settlement.png')),
            pygame.image.load(os.path.join(base_path, '../assets/player/city.png'))
        ]

        scaled = []

        for image in logo_images:
            scaled.append(pygame.transform.scale(image, logo_size))

        return scaled

    @staticmethod
    def scale_masks(logo_size):
        base_path = os.path.dirname(__file__)
        logo_images = [
            None,
            None,
            None,
            pygame.image.load(os.path.join(base_path, '../assets/player/road_mask.png')),
            pygame.image.load(os.path.join(base_path, '../assets/player/settlement_mask.png')),
            pygame.image.load(os.path.join(base_path, '../assets/player/city_mask.png'))
        ]

        scaled = []

        for image in logo_images:
            if image is not None:
                scaled.append(pygame.transform.scale(image, logo_size))

        return scaled

    @staticmethod
    def scale_bank(card_size):

        base_path = os.path.dirname(__file__)

        '''
        card_images = {
            'Wood': pygame.image.load(os.path.join(base_path, '../assets/bank/wood_circle.png')),
            'Brick': pygame.image.load(os.path.join(base_path, '../assets/bank/brick_circle.png')),
            'Sheep': pygame.image.load(os.path.join(base_path, '../assets/bank/sheep_circle.png')),
            'Wheat': pygame.image.load(os.path.join(base_path, '../assets/bank/wheat_circle.png')),
            'Ore': pygame.image.load(os.path.join(base_path, '../assets/bank/ore_circle.png')),
            'Dev': pygame.image.load(os.path.join(base_path, '../assets/bank/card_back_square.png')),
        }
        '''

        card_images = {
            'Wood': pygame.image.load(os.path.join(base_path, '../assets/bank/wood_square.png')),
            'Brick': pygame.image.load(os.path.join(base_path, '../assets/bank/brick_square.png')),
            'Sheep': pygame.image.load(os.path.join(base_path, '../assets/bank/sheep_square.png')),
            'Wheat': pygame.image.load(os.path.join(base_path, '../assets/bank/wheat_square.png')),
            'Ore': pygame.image.load(os.path.join(base_path, '../assets/bank/ore_square.png')),
            'Dev': pygame.image.load(os.path.join(base_path, '../assets/bank/card_back_square.png')),
        }

        scaled = []

        for key in card_images:
            picture = card_images.get(key)
            scaled.append(pygame.transform.scale(picture, card_size))

        return scaled
