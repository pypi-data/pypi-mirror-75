import math
import os

import pygame
import pygame.gfxdraw


class RoadHardwareArt:
    @staticmethod
    def generate_road_art(radius, color, angle=0):
        # accepts angle in degrees

        tan_color = (230, 196, 129)

        # create surface to build shape on
        canvas = pygame.Surface((int(radius), int(radius)), pygame.SRCALPHA)
        center = (radius / 2, radius / 2)

        length = radius
        width = radius / 10
        # tip_length = math.tan(math.pi / 6) * width / 2
        tip_length = width * 0.288675135
        # tip_length = 10
        tip_width = width // 2

        '''
        #apply rect body
        body = pygame.Rect(int(center[0] - width / 2),
                           int(center[1] - length / 2 + tip_length),
                           int(width / 2 * 2),
                           int(length - 2 * tip_length + 1))
        pygame.gfxdraw.box(canvas, body, color)

        #apply top trigon
        point = (radius / 2, 0)
        left = (radius / 2 - tip_width, tip_length)
        right = (radius / 2 + tip_width, tip_length)
        pygame.gfxdraw.filled_polygon(canvas, [point, left, right], color)

        #apply bottom trigon
        point = (radius / 2, radius)
        left = (radius / 2 - tip_width, radius - tip_length)
        right = (radius / 2 + tip_width, radius - tip_length)
        pygame.gfxdraw.filled_polygon(canvas, [point, left, right], color)

        '''
        # apply full hex

        # apply top trigon
        top_point = (radius / 2, 0)
        top_left = (radius / 2 - tip_width, tip_length)
        top_right = (radius / 2 + tip_width, tip_length)

        # apply bottom trigon
        bottom_point = (radius / 2, radius)
        bottom_left = (radius / 2 - tip_width, radius - tip_length)
        bottom_right = (radius / 2 + tip_width, radius - tip_length)

        # color shape
        pygame.gfxdraw.filled_polygon(canvas,
                                      [top_left, top_point, top_right, bottom_right, bottom_point, bottom_left],
                                      color)
        # black outline
        pygame.gfxdraw.aapolygon(canvas,
                                 [top_left, top_point, top_right, bottom_right, bottom_point, bottom_left],
                                 tan_color)

        # apply rotate
        canvas = pygame.transform.rotate(canvas, angle)

        return canvas

    @staticmethod
    def generate_road_polygons(road_length, road_ratio):
        # create 3 types of roads, |, /, \
        road_points = []
        road_width = road_length * road_ratio

        road_points.append([
            [-road_width, road_length],
            [road_width, road_length],
            [road_width, -road_length],
            [-road_width, -road_length]
        ])

        angle = math.pi * 5 / 6
        half_angle = math.pi / 2
        end_points = [[road_length * math.cos(angle), road_length * math.sin(angle)],
                      [-1 * road_length * math.cos(angle), -1 * road_length * math.sin(angle)]]
        road_points.append([])

        road_points[1].append([end_points[0][0] - road_width * math.cos(angle + half_angle),
                               end_points[0][1] - road_width * math.sin(angle + half_angle)])
        road_points[1].append([end_points[0][0] - road_width * math.cos(angle - half_angle),
                               end_points[0][1] - road_width * math.sin(angle - half_angle)])
        road_points[1].append([end_points[1][0] - road_width * math.cos(angle - half_angle),
                               end_points[1][1] - road_width * math.sin(angle - half_angle)])
        road_points[1].append([end_points[1][0] - road_width * math.cos(angle + half_angle),
                               end_points[1][1] - road_width * math.sin(angle + half_angle)])

        angle = math.pi / 6
        end_points = [[road_length * math.cos(angle), road_length * math.sin(angle)],
                      [-1 * road_length * math.cos(angle), -1 * road_length * math.sin(angle)]]
        road_points.append([])

        road_points[2].append([end_points[0][0] - road_width * math.cos(angle + half_angle),
                               end_points[0][1] - road_width * math.sin(angle + half_angle)])
        road_points[2].append([end_points[0][0] - road_width * math.cos(angle - half_angle),
                               end_points[0][1] - road_width * math.sin(angle - half_angle)])
        road_points[2].append([end_points[1][0] - road_width * math.cos(angle - half_angle),
                               end_points[1][1] - road_width * math.sin(angle - half_angle)])
        road_points[2].append([end_points[1][0] - road_width * math.cos(angle + half_angle),
                               end_points[1][1] - road_width * math.sin(angle + half_angle)])

        return road_points


class TextureScale:
    @staticmethod
    def scale_resource_tiles(hex_size):

        base_path = os.path.dirname(__file__)

        texture_dictionary = {
            'Desert': pygame.image.load(os.path.join(base_path, '../assets/hexes/desert.png')),
            'Ocean': pygame.image.load(os.path.join(base_path, '../assets/hexes/ocean.png')),
            'Wheat': pygame.image.load(os.path.join(base_path, '../assets/hexes/wheat.png')),
            'Brick': pygame.image.load(os.path.join(base_path, '../assets/hexes/quarry.png')),
            'Ore': pygame.image.load(os.path.join(base_path, '../assets/hexes/mountain.png')),
            'Sheep': pygame.image.load(os.path.join(base_path, '../assets/hexes/plains.png')),
            'Wood': pygame.image.load(os.path.join(base_path, '../assets/hexes/forest.png')),

            'Wheat1': pygame.image.load(os.path.join(base_path, '../assets/hexes/Wheat/one.png')),
            'Wheat2': pygame.image.load(os.path.join(base_path, '../assets/hexes/Wheat/two.png')),
            'Wheat3': pygame.image.load(os.path.join(base_path, '../assets/hexes/Wheat/three.png')),
            'Wheat4': pygame.image.load(os.path.join(base_path, '../assets/hexes/Wheat/four.png')),
            'Wheat5': pygame.image.load(os.path.join(base_path, '../assets/hexes/Wheat/five.png')),

            'Brick1': pygame.image.load(os.path.join(base_path, '../assets/hexes/Quarry/one.png')),
            'Brick2': pygame.image.load(os.path.join(base_path, '../assets/hexes/Quarry/two.png')),
            'Brick3': pygame.image.load(os.path.join(base_path, '../assets/hexes/Quarry/three.png')),
            'Brick4': pygame.image.load(os.path.join(base_path, '../assets/hexes/Quarry/four.png')),
            'Brick5': pygame.image.load(os.path.join(base_path, '../assets/hexes/Quarry/five.png')),

            'Ore1': pygame.image.load(os.path.join(base_path, '../assets/hexes/Mountain/one.png')),
            'Ore2': pygame.image.load(os.path.join(base_path, '../assets/hexes/Mountain/two.png')),
            'Ore3': pygame.image.load(os.path.join(base_path, '../assets/hexes/Mountain/three.png')),
            'Ore4': pygame.image.load(os.path.join(base_path, '../assets/hexes/Mountain/four.png')),
            'Ore5': pygame.image.load(os.path.join(base_path, '../assets/hexes/Mountain/five.png')),

            'Sheep1': pygame.image.load(os.path.join(base_path, '../assets/hexes/Plains/one.png')),
            'Sheep2': pygame.image.load(os.path.join(base_path, '../assets/hexes/Plains/two.png')),
            'Sheep3': pygame.image.load(os.path.join(base_path, '../assets/hexes/Plains/three.png')),
            'Sheep4': pygame.image.load(os.path.join(base_path, '../assets/hexes/Plains/four.png')),
            'Sheep5': pygame.image.load(os.path.join(base_path, '../assets/hexes/Plains/five.png')),

            'Wood1': pygame.image.load(os.path.join(base_path, '../assets/hexes/Forest/one.png')),
            'Wood2': pygame.image.load(os.path.join(base_path, '../assets/hexes/Forest/two.png')),
            'Wood3': pygame.image.load(os.path.join(base_path, '../assets/hexes/Forest/three.png')),
            'Wood4': pygame.image.load(os.path.join(base_path, '../assets/hexes/Forest/four.png')),
            'Wood5': pygame.image.load(os.path.join(base_path, '../assets/hexes/Forest/five.png')),
        }

        for key in texture_dictionary:
            picture = texture_dictionary.get(key)
            texture_dictionary[key] = pygame.transform.scale(picture, (int(hex_size), int(hex_size)))

        return texture_dictionary

    @staticmethod
    def scale_port_tiles(hex_size):

        base_path = os.path.dirname(__file__)

        port_textures = {
            'None': pygame.image.load(os.path.join(base_path, '../assets/default_port.png')),
            'Wheat': pygame.image.load(os.path.join(base_path, '../assets/wheat_port.png')),
            'Brick': pygame.image.load(os.path.join(base_path, '../assets/brick_port.png')),
            'Ore': pygame.image.load(os.path.join(base_path, '../assets/ore_port.png')),
            'Sheep': pygame.image.load(os.path.join(base_path, '../assets/sheep_port.png')),
            'Wood': pygame.image.load(os.path.join(base_path, '../assets/wood_port.png')),
        }

        for key in port_textures:
            picture = port_textures.get(key)
            port_textures[key] = pygame.transform.scale(picture, (int(hex_size), int(hex_size)))

        return port_textures

    @staticmethod
    def scale_cards(card_size):

        base_path = os.path.dirname(__file__)

        card_images = {
            'knight': pygame.image.load(os.path.join(base_path, '../assets/cards/dev/Knight.png')),
            'monopoly': pygame.image.load(os.path.join(base_path, '../assets/cards/dev/Monopoly.png')),
            'roadBuilding': pygame.image.load(os.path.join(base_path, '../assets/cards/dev/Road_Building.png')),
            'yearOfPlenty': pygame.image.load(os.path.join(base_path, '../assets/cards/dev/Year_Of_Plenty.png')),
            'victoryPoint': pygame.image.load(os.path.join(base_path, '../assets/cards/dev/Victory_Point.png')),
            'Brick': pygame.image.load(os.path.join(base_path, '../assets/cards/res/bricks.png')),
            'Ore': pygame.image.load(os.path.join(base_path, '../assets/cards/res/ore.png')),
            'Sheep': pygame.image.load(os.path.join(base_path, '../assets/cards/res/sheep.png')),
            'Wheat': pygame.image.load(os.path.join(base_path, '../assets/cards/res/wheat.png')),
            'Wood': pygame.image.load(os.path.join(base_path, '../assets/cards/res/wood.png'))
        }

        for key in card_images:
            picture = card_images.get(key)
            card_images[key] = pygame.transform.scale(picture, card_size)

        return card_images

    @staticmethod
    def scale_bank(card_size):

        base_path = os.path.dirname(__file__)

        card_images = {
            'Brick': pygame.image.load(os.path.join(base_path, '../assets/cards/res/bricks.png')),
            'Ore': pygame.image.load(os.path.join(base_path, '../assets/cards/res/ore.png')),
            'Sheep': pygame.image.load(os.path.join(base_path, '../assets/cards/res/sheep.png')),
            'Wheat': pygame.image.load(os.path.join(base_path, '../assets/cards/res/wheat.png')),
            'Wood': pygame.image.load(os.path.join(base_path, '../assets/cards/res/wood.png')),
            'Dev': pygame.image.load(os.path.join(base_path, '../assets/cards/res/resource_card_bank_square.png')),
        }

        for key in card_images:
            picture = card_images.get(key)
            card_images[key] = pygame.transform.scale(picture, card_size)

        return card_images

    @staticmethod
    def scale_logos(logo_size):
        base_path = os.path.dirname(__file__)
        logo_images = {
            'army': pygame.image.load(os.path.join(base_path, '../assets/army.png')),
            'city': pygame.image.load(os.path.join(base_path, '../assets/city.png')),
            'num_roads': pygame.image.load(os.path.join(base_path, '../assets/num_roads.png')),
            'settlement': pygame.image.load(os.path.join(base_path, '../assets/settlement.png')),
            'road': pygame.image.load(os.path.join(base_path, '../assets/road.png')),
            'cards': pygame.image.load(os.path.join(base_path, '../assets/cards.png')),
            'star': pygame.image.load(os.path.join(base_path, '../assets/star.png')),
        }

        for key in logo_images:
            picture = logo_images[key]
            logo_images[key] = pygame.transform.scale(picture, logo_size)

        return logo_images

    @staticmethod
    def scale_bank_logo(logo_size):
        base_path = os.path.dirname(__file__)
        image = pygame.image.load(os.path.join(base_path, '../assets/bank.png'))
        image = pygame.transform.scale(image, logo_size)
        return image


class ButtonResources:
    @staticmethod
    def save_scaled_cards(scaled_cards):
        base_path = os.path.dirname(__file__)

        for key in scaled_cards.keys():
            card = scaled_cards[key]
            pygame.image.save(card, os.path.join(base_path, '../assets/scaled/' + key + '.png'))

            darkened_amount = 10
            darkened_card = card.copy()
            dark = pygame.Surface((card.get_width(), card.get_height()), flags=pygame.SRCALPHA)
            dark.fill((darkened_amount, darkened_amount, darkened_amount, 0))
            darkened_card.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            pygame.image.save(darkened_card, os.path.join(base_path, '../assets/scaled/' + key + '_disabled.png'))

            lightened_amount = 10
            lightened_card = card.copy()
            light = pygame.Surface((card.get_width(), card.get_height()), flags=pygame.SRCALPHA)
            light.fill((lightened_amount, lightened_amount, lightened_amount, 0))
            lightened_card.blit(light, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            pygame.image.save(lightened_card, os.path.join(base_path, '../assets/scaled/' + key + '_hovered.png'))
