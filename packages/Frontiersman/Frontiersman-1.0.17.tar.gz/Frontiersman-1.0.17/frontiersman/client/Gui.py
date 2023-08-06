# import ctypes
# ctypes.windll.user32.SetProcessDPIAware()
import os
import sys
import requests

os.environ['SDL_AUDIODRIVER'] = 'dsp'
# sys.path.insert(0, '../frontiersman')

import random
import pygame.gfxdraw
import pygame_gui as pg_g
from frontiersman.gameboard.NodeRoads import *
from frontiersman.gameboard.SettlementButtons import *
from frontiersman.client.Bank import *
from frontiersman.client import ClientHelper
from frontiersman.client import Actions
from frontiersman.client.CardPickerGui import CardPickerGui
from frontiersman.client.TextDialog import TextDialog
from frontiersman.client.TraderGui import TraderGui
from frontiersman.client.PlayerSelector import PlayerSelector
from frontiersman.client.CardDiscarder import CardDiscarder
from frontiersman.client.TradePrompt import TradePrompt
from frontiersman.client.HelpWindow import HelpWindow
from frontiersman.client.GuiConstants import *
from frontiersman.client.PlayerInfo import PlayerInfo

COLORS = {
    'red': (127, 0, 0),
    'cyan': (0, 255, 255),
    'orange': (255, 106, 0),
    'blue': (0, 38, 255),
    'green': (0, 153, 15),
    'pink': (255, 0, 110),
    'yellow': (255, 216, 0)
}
INSTRUCTION_TEXT = {
    'display': '',
    'turn': '',
    'road': 'Choose Location for Road',
    'roadfree': 'Choose Location for Road',
    'initialroad': 'Choose Location for Road',
    'set': 'Choose Location for Settlement',
    'initialsettlement': 'Choose Location for Settlement',
    'city': 'Choose Settlement to Upgrade',
    "robber": 'Choose Tile for Robber',
    "thieftarget": 'Choose a Player to Rob',
    'discard': 'discard half your hand',
    'awaitingtrade': 'waiting for other players to respond',
    'tradeoffer': '',
    'tradepartner': ''
}
DEVELOPMENT_TEXT = {
    'knight': "Move the Robber",
    'roadBuilding': "build 2 free roads",
    'yearOfPlenty': "get 2 of any resource from the bank",
    'monopoly': "Take the resource of your choice from other players",
    'victoryPoint': 'Hidden Victory Point'
}

CARD_IMAGES = ClientHelper.TextureScale.scale_cards(CARD_SIZE)
PORT_TEXTURES = ClientHelper.TextureScale.scale_port_tiles(HEX_SIZE)
TILE_TEXTURES = ClientHelper.TextureScale.scale_resource_tiles(HEX_SIZE)
ROAD_POINTS = ClientHelper.RoadHardwareArt.generate_road_polygons(HEX_SIZE / 4, 1 / 10)


class Client:
    # for mapping hexagon tiles to x,y
    @staticmethod
    def translate_hex_to_xy(location, origin, radius):
        if location == (0, 0, 0):
            return origin
        x_off = 0
        y_off = 3 / 2 * radius * location[2]
        x_constant = .5 * radius * (3 ** 0.5)
        x_factor = location[0] - location[1]
        x_off = x_factor * x_constant

        y_diff = (1 + 3 ** 0.5) / 2 * radius
        x_diff = (3 ** 0.5) / 2 * radius

        return int(origin[0] + x_off), int(origin[1] + y_off)

    @staticmethod
    def quit():
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    @staticmethod
    def add_event(event):
        pygame.event.post(event)

    def __init__(self, board_input, post_url, game_window):
        self.board_input = board_input
        self.board_action = "display"
        self.last_board_action = "display"
        self.board_updated = False
        self.board_input = board_input
        self.settlementButtons = []
        self.property_list = []
        self.road_list = []
        self.manual_card_list = []
        self.card_hand = []
        self.bank = Bank()
        self.running = False
        self.is_rolling = False
        self.directions_text = 'Temporary Text'
        self.trade_prompt = None
        self.trade_cost = []
        self.trade_offer = []
        self.trade_list = []
        self.post_url = post_url
        # todo initialize the rest of these
        self.card_keys = []
        self.cards_updated = False
        self.card_element_list = []
        self.player_element_list = []
        self.dice_image = None
        self.dice_button = None
        self.player = None
        self.enemy_list = []
        self.game_board = None
        self.building_locations = None
        self.font = None
        self.manager = None
        self.clock = None
        self.house_points = None
        self.object_textures = None
        self.board_center = None
        self.resource_hexes = None
        self.port_hexes = None
        self.game_window = game_window
        self.action_panel = None
        self.grid_size = None
        self.set_butts = None
        self.card_panel = None
        self.info_panel = None
        self.road_butts = None
        self.trade_button = None
        self.road_button = None
        self.settlement_button = None
        self.city_button = None
        self.development_button = None
        self.end_turn_button = None
        self.card_picker = None
        self.card_trader = None
        self.help_button = None
        self.help_window = None
        self.player_selector = None
        self.card_discarder = None
        self.text_dialog = None
        self.turn_start = False

        # constants translated to the previously used instance variables
        self.hex_size = HEX_SIZE
        self.port_textures = PORT_TEXTURES
        self.texture_dictionary = TILE_TEXTURES
        self.scale = SCALE * PROTOTYPE_SCALE
        self.card_images = CARD_IMAGES
        self.road_points = ROAD_POINTS

    def set_player(self, player):
        self.player = player

    def board_setup_coordinates_display(self, data):
        self.board_input.put(','.join(data))
        self.board_action = self.last_board_action

    def initial_settlement_buttons(self):
        settlement_buttons = []
        for j in range(0, self.building_locations.settleRowLength):
            for i in range(0, self.building_locations.settleColLength):
                if self.building_locations.settlements[i][j].available:
                    settlement_buttons.append(
                        CircleButton((125, 125, 255), (255, 255, 255), (int(40 * PROTOTYPE_SCALE), int(40 * PROTOTYPE_SCALE)),
                                     CornerNode.translate_settlement((i, j), self.board_center, int(self.hex_size / 2)),
                                     "center", self.board_setup_coordinates_display,
                                     [str(i), str(j)]))
        return settlement_buttons

    def initial_road_buttons(self, prop):
        road_buttons = []
        for edge in prop.edges:
            if edge is not None:
                if edge.real:
                    road_buttons.append(
                        CircleButton((125, 125, 255), (255, 255, 255),
                                     (int(40 * PROTOTYPE_SCALE), int(40 * PROTOTYPE_SCALE)),
                                     EdgeNode.translate_road((edge.cord1, edge.cord2), self.board_center,
                                                             int(self.hex_size / 2)), "center",
                                     self.board_setup_coordinates_display,
                                     [str(edge.cord1), str(edge.cord2)]))
        return road_buttons

    def get_settlement_buttons(self):
        settlement_buttons = []
        list_o_setts = Actions.build_settlement_available(self.player)
        for settle in list_o_setts:
            settlement_buttons.append(
                CircleButton((125, 125, 255), (255, 255, 255), (40, 40),
                             CornerNode.translate_settlement((settle.cord1, settle.cord2), self.board_center,
                                                             int(self.hex_size / 2)),
                             "center", self.board_setup_coordinates_display,
                             ["set", str(settle.cord1), str(settle.cord2)]))
        return settlement_buttons

    def get_city_buttons(self):
        settlement_buttons = []
        list_o_setts = Actions.build_city_available(self.player)
        for settle in list_o_setts:
            settlement_buttons.append(
                CircleButton((125, 125, 255), (255, 255, 255), (40, 40),
                             CornerNode.translate_settlement((settle.cord1, settle.cord2), self.board_center,
                                                             int(self.hex_size / 2)),
                             "center", self.board_setup_coordinates_display,
                             ["city", str(settle.cord1), str(settle.cord2)]))
        return settlement_buttons

    def get_road_buttons(self, free=False):
        road_buttons = []
        list_o_roads = Actions.build_road_available(self.player, free)
        for edge in list_o_roads:
            road_buttons.append(
                CircleButton((125, 125, 255), (255, 255, 255), (40, 40),
                             EdgeNode.translate_road((edge.cord1, edge.cord2), self.board_center,
                                                     int(self.hex_size / 2)), "center",
                             self.board_setup_coordinates_display,
                             ["road", str(edge.cord1), str(edge.cord2)]))
        return road_buttons

    def get_robber_buttons(self):
        road_buttons = []
        for tile in self.resource_hexes:
            if not tile.get_robber():
                loc = self.translate_hex_to_xy(tile.location, self.board_center, int(self.hex_size / 2))
                (loc[0] + int(self.hex_size / 3), loc[1] + int(self.hex_size / 3))
                road_buttons.append(
                    CircleButton((125, 125, 255), (255, 255, 255), (40, 40),
                                 (loc[0] + int(self.hex_size / 3), loc[1] + int(self.hex_size / 3)), "center",
                                 self.board_setup_coordinates_display,
                                 ["robber", str(tile.location[0]), str(tile.location[1])]))
        return road_buttons

    def set_cards(self, card_keys):
        self.card_keys = card_keys
        self.cards_updated = True

    def update_cards(self):
        for card in self.card_element_list:
            card.kill()

        self.card_element_list = []
        if len(self.card_keys) > 0:
            area_width = self.card_panel.relative_rect.width - CARD_SIZE[0] - 8
            if len(self.card_keys) == 1:
                offset = 0
            else:
                offset = min(area_width / (len(self.card_keys) - 1), CARD_SIZE[0] + SPACING)

            start = (area_width - offset * (len(self.card_keys) - 1)) / 2
            self.card_keys.sort()
            for i, key in enumerate(self.card_keys):
                if key in DEVELOPMENT_TEXT.keys():
                    self.card_element_list.append(pg_g.elements.UIButton(
                        relative_rect=pygame.Rect((start + i * offset, 0), CARD_SIZE),
                        text="",
                        manager=self.manager,
                        tool_tip_text=DEVELOPMENT_TEXT[key],
                        container=self.card_panel,
                        object_id='#' + key,
                    ))
                else:
                    self.card_element_list.append(pg_g.elements.UIButton(
                        relative_rect=pygame.Rect((start + i * offset, 0), CARD_SIZE),
                        text="",
                        manager=self.manager,
                        container=self.card_panel,
                        object_id='#' + key,
                    ))

    @staticmethod
    def translate_from_3d_tile(coordinates):
        center = [5, 2.5]
        y = coordinates[2]
        x = coordinates[0] - coordinates[1]
        array = [[center[0] + x, int(center[1] + y + .5)], [center[0] + x - 1, int(center[1] + y + .5)],
                 [center[0] + x + 1, int(center[1] + y + .5)], [center[0] + x, int(center[1] + y - .5)],
                 [center[0] + x - 1, int(center[1] + y - .5)], [center[0] + x + 1, int(center[1] + y - .5)]]
        return array

    @staticmethod
    def translate_from_2d_tile(coordinates):
        center = [5, 2.5]
        y = 1 - coordinates[0] - coordinates[1]
        x = coordinates[0] - coordinates[1]
        array = [[center[0] + x, int(center[1] + y + .5)], [center[0] + x - 1, int(center[1] + y + .5)],
                 [center[0] + x + 1, int(center[1] + y + .5)], [center[0] + x, int(center[1] + y - .5)],
                 [center[0] + x - 1, int(center[1] + y - .5)], [center[0] + x + 1, int(center[1] + y - .5)]]
        return array

    @staticmethod
    def get_tiles_from_vertex(coordinates):
        x = coordinates[0]
        y = coordinates[1]

        tile_array = []

        location_list = [
            [0, 2, -2],
            [1, 1, -2],
            [2, 0, -2],
            [-1, 2, -1],
            [0, 1, -1],
            [1, 0, -1],
            [2, -1, -1],
            [-2, 2, 0],
            [-1, 1, 0],
            [0, 0, 0],
            [1, -1, 0],
            [2, -2, 0],
            [-2, 1, 1],
            [-1, 0, 1],
            [0, -1, 1],
            [1, -2, 1],
            [-2, 0, 2],
            [-1, -1, 2],
            [0, -2, 2]
        ]
        translate_list = []
        for tile in location_list:
            for point in Client.translate_from_3d_tile(tile):
                if point == [x, y]:
                    tile_array.append(tile)

        return tile_array

    def process_dice(self, roll):
        cards_to_get = []
        if roll == 7:
            pass  # todo remove cards
        else:
            for prop in self.player.ownedNodes:
                for tile_coordinate in Client.get_tiles_from_vertex([prop.cord1, prop.cord2]):
                    tile = self.game_board.get_tile(tile_coordinate)
                    if tile.number == roll and not tile.get_robber():
                        if prop.city:
                            if (tile.resource == 'Wheat' and self.bank.grain > 0) or (tile.resource == 'Sheep' and self.bank.wool > 0) or (
                                    tile.resource == 'Wood' and self.bank.lumber > 0) or (tile.resource == 'Ore' and self.bank.ore > 0) or (tile.resource == 'Brick' and self.bank.brick > 0):
                                cards_to_get.append(tile.resource)
                            if (tile.resource == 'Wheat' and self.bank.grain > 0) or (tile.resource == 'Sheep' and self.bank.wool > 0) or (
                                    tile.resource == 'Wood' and self.bank.lumber > 0) or (tile.resource == 'Ore' and self.bank.ore > 0) or (tile.resource == 'Brick' and self.bank.brick > 0):
                                cards_to_get.append(tile.resource)
                        else:
                            if (tile.resource == 'Wheat' and self.bank.grain > 0) or (tile.resource == 'Sheep' and self.bank.wool > 0) or (
                                    tile.resource == 'Wood' and self.bank.lumber > 0) or (tile.resource == 'Ore' and self.bank.ore > 0) or (tile.resource == 'Brick' and self.bank.brick > 0):
                                cards_to_get.append(tile.get_resource())
        self.get_cards(cards_to_get)

    def get_adjacent_nodes(self, tile_location):

        to_return = list()

        tile = self.game_board.get_tile(tile_location)
        location_list = [
            [0, 2, -2],
            [1, 1, -2],
            [2, 0, -2],
            [-1, 2, -1],
            [0, 1, -1],
            [1, 0, -1],
            [2, -1, -1],
            [-2, 2, 0],
            [-1, 1, 0],
            [0, 0, 0],
            [1, -1, 0],
            [2, -2, 0],
            [-2, 1, 1],
            [-1, 0, 1],
            [0, -1, 1],
            [1, -2, 1],
            [-2, 0, 2],
            [-1, -1, 2],
            [0, -2, 2]
        ]

        for prop in self.building_locations.settlements:
            for tile_coordinate in Client.get_tiles_from_vertex([prop.cord1, prop.cord2]):
                check_tile = self.game_board.get_tile(tile_coordinate)
                if check_tile.location == tile.location:
                    to_return.append(prop)
                    break

        return to_return

    def get_adjacent_owners(self, robber_tile):
        adj_color = list()
        steal_from = list()
        for prop in self.property_list:
            for tile_coordinate in Client.get_tiles_from_vertex([prop.cord1, prop.cord2]):
                if robber_tile.location[0] == tile_coordinate[0] and robber_tile.location[1] == tile_coordinate[1]:
                    if (prop.color is not None) and (prop.color not in adj_color):
                        adj_color.append(prop.color)
        for player in self.enemy_list:
            if player.color in adj_color:
                steal_from.append(player)
        return steal_from

    def stolen_card(self):
        if len(self.card_hand) == 0:
            return "none"
        card_to_steal = random.choice(self.card_hand)
        self.card_hand.remove(card_to_steal)
        self.set_cards(self.card_hand)
        array1 = [0, 0, 0, 0, 0]
        if card_to_steal == 'Brick':
            array1[0] -= 1
        elif card_to_steal == 'Wheat':
            array1[1] -= 1
        elif card_to_steal == 'Wood':
            array1[2] -= 1
        elif card_to_steal == 'Ore':
            array1[3] -= 1
        elif card_to_steal == 'Sheep':
            array1[4] -= 1
        self.player.add_resource(array1)
        self.set_board_updated(True)
        return card_to_steal

    def steal_card(self, card):
        self.card_hand.append(card)
        self.set_cards(self.card_hand)
        array1 = [0, 0, 0, 0, 0]
        if card == 'Brick':
            array1[0] += 1
        elif card == 'Wheat':
            array1[1] += 1
        elif card == 'Wood':
            array1[2] += 1
        elif card == 'Ore':
            array1[3] += 1
        elif card == 'Sheep':
            array1[4] += 1
        self.player.add_resource(array1)
        self.set_board_updated(True)

    def card_list_to_arr(self, res_list):
        array1 = [0, 0, 0, 0, 0]
        for r in res_list:
            if r == 'Brick':
                array1[0] += 1
            elif r == 'Wheat':
                array1[1] += 1
            elif r == 'Wood':
                array1[2] += 1
            elif r == 'Ore':
                array1[3] += 1
            elif r == 'Sheep':
                array1[4] += 1
        return array1

    def pay_cards(self, res):
        for r in range(0, res[0]):
            self.card_hand.remove('Brick')
        for r in range(0, res[1]):
            self.card_hand.remove('Wheat')
        for r in range(0, res[2]):
            self.card_hand.remove('Wood')
        for r in range(0, res[3]):
            self.card_hand.remove('Ore')
        for r in range(0, res[4]):
            self.card_hand.remove('Sheep')
        self.set_cards(self.card_hand)
        self.bank.update(res)
        array2 = [0 - x for x in res]
        self.player.add_resource(array2)
        self.set_board_updated(True)
        self.board_input.put('bank,' + ','.join([str(x) for x in res]))

    def trade_cards_with_player(self, trade, get):
        arr = [0, 0, 0, 0, 0]
        for r in range(0, trade[0]):
            self.card_hand.remove('Brick')
            arr[0] -= 1
        for r in range(0, trade[1]):
            self.card_hand.remove('Wheat')
            arr[1] -= 1
        for r in range(0, trade[2]):
            self.card_hand.remove('Wood')
            arr[2] -= 1
        for r in range(0, trade[3]):
            self.card_hand.remove('Ore')
            arr[3] -= 1
        for r in range(0, trade[4]):
            self.card_hand.remove('Sheep')
            arr[4] -= 1
        for r in range(0, get[0]):
            self.card_hand.append('Brick')
            arr[0] += 1
        for r in range(0, get[1]):
            self.card_hand.append('Wheat')
            arr[1] += 1
        for r in range(0, get[2]):
            self.card_hand.append('Wood')
            arr[2] += 1
        for r in range(0, get[3]):
            self.card_hand.append('Ore')
            arr[3] += 1
        for r in range(0, get[4]):
            self.card_hand.append('Sheep')
            arr[4] += 1
        self.set_cards(self.card_hand)
        self.player.add_resource(arr)
        self.set_board_updated(True)

    def trade_cards(self, trade, get):
        array1 = [0, 0, 0, 0, 0]
        for r in trade:
            if r == 'Brick':
                array1[0] -= 1
                self.card_hand.remove('Brick')
            elif r == 'Wheat':
                array1[1] -= 1
                self.card_hand.remove('Wheat')
            elif r == 'Wood':
                array1[2] -= 1
                self.card_hand.remove('Wood')
            elif r == 'Ore':
                array1[3] -= 1
                self.card_hand.remove('Ore')
            elif r == 'Sheep':
                array1[4] -= 1
                self.card_hand.remove('Sheep')
        for r in get:
            if r == 'Brick':
                array1[0] += 1
                self.card_hand.append('Brick')
            elif r == 'Wheat':
                array1[1] += 1
                self.card_hand.append('Wheat')
            elif r == 'Wood':
                array1[2] += 1
                self.card_hand.append('Wood')
            elif r == 'Ore':
                array1[3] += 1
                self.card_hand.append('Ore')
            elif r == 'Sheep':
                array1[4] += 1
                self.card_hand.append('Sheep')
        self.set_cards(self.card_hand)
        self.player.add_resource(array1)
        array2 = [0 - x for x in array1]
        self.bank.update(array2)
        self.set_board_updated(True)
        self.board_input.put('bank,' + ','.join([str(x) for x in array2]))

    def get_dev_card(self, card):
        self.bank.get_dev_card()
        self.player.developmentHand.add_card(card)
        self.card_hand.append(card)
        self.set_cards(self.card_hand)
        self.set_board_updated(True)

    def get_cards(self, res):
        array1 = [0, 0, 0, 0, 0]
        for r in res:
            if r == 'Brick':
                array1[0] += 1
            elif r == 'Wheat':
                array1[1] += 1
            elif r == 'Wood':
                array1[2] += 1
            elif r == 'Ore':
                array1[3] += 1
            elif r == 'Sheep':
                array1[4] += 1
        self.card_hand += res
        self.set_cards(self.card_hand)
        self.player.add_resource(array1)
        array2 = [0 - x for x in array1]
        self.bank.update(array2)
        self.set_board_updated(True)
        self.board_input.put('bank,' + ','.join([str(x) for x in array2]))

    def get_monopoly(self, r):
        res = []
        array1 = [0, 0, 0, 0, 0]
        if r == 'Brick':
            for x in range(0, 19 - self.bank.brick - self.player.resourceHand.brick):
                res.append(r)
                array1[0] += 1
        elif r == 'Wheat':
            for x in range(0, 19 - self.bank.grain - self.player.resourceHand.grain):
                res.append(r)
                array1[1] += 1
        elif r == 'Wood':
            for x in range(0, 19 - self.bank.lumber - self.player.resourceHand.lumber):
                res.append(r)
                array1[2] += 1
        elif r == 'Ore':
            for x in range(0, 19 - self.bank.ore - self.player.resourceHand.ore):
                res.append(r)
                array1[3] += 1
        elif r == 'Sheep':
            for x in range(0, 19 - self.bank.wool - self.player.resourceHand.wool):
                res.append(r)
                array1[4] += 1
        self.card_hand += res
        self.set_cards(self.card_hand)
        self.player.add_resource(array1)
        self.set_board_updated(True)
        self.board_input.put('monopoly,' + r)

    def pay_monopoly(self, r):
        res = []
        array1 = [0, 0, 0, 0, 0]
        if r == 'Brick':
            for x in range(0, self.player.resourceHand.brick):
                self.card_hand.remove(r)
                array1[0] -= 1
        elif r == 'Wheat':
            for x in range(0, self.player.resourceHand.grain):
                self.card_hand.remove(r)
                self.card_hand.remove(r)
                array1[1] -= 1
        elif r == 'Wood':
            for x in range(0, self.player.resourceHand.lumber):
                self.card_hand.remove(r)
                array1[2] -= 1
        elif r == 'Ore':
            for x in range(0, self.player.resourceHand.ore):
                self.card_hand.remove(r)
                array1[3] -= 1
        elif r == 'Sheep':
            for x in range(0, self.player.resourceHand.wool):
                self.card_hand.remove(r)
                array1[4] -= 1
        self.set_cards(self.card_hand)
        self.player.add_resource(array1)
        self.set_board_updated(True)

    def start_resources(self):
        last = self.player.ownedNodes[-1]
        array = Client.get_tiles_from_vertex([last.cord1, last.cord2])
        res = []
        for h in array:
            if self.game_board.get_tile(h).get_resource() != 'Desert':
                res.append(self.game_board.get_tile(h).get_resource())
        self.get_cards(res)

    def set_board_action(self, bool1, last_action=None):
        if self.board_action != bool1:
            self.board_updated = True
        if last_action is None:
            self.last_board_action = self.board_action
        else:
            self.last_board_action = last_action
        self.board_action = bool1

    def set_board_updated(self, bool1):
        self.board_updated = bool1

    def render_dice(self, rolls):
        size = int(80 * PROTOTYPE_SCALE)
        width = len(rolls) * (2 * SPACING + size) - 2 * SPACING
        height = size

        dice_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        dice_surface.fill((0, 0, 0, 0))

        for i, roll in enumerate(rolls):
            x = i * (2 * SPACING + size) - 2 * SPACING
            y = 0
            pygame.draw.rect(dice_surface, (255, 255, 255), pygame.Rect(x, y, size, size))
            text_surface = self.font.render(str(roll), True, (0, 0, 0))
            dice_surface.blit(text_surface,
                              (x + (size - text_surface.get_width()) / 2, y + (size - text_surface.get_height()) / 2))

        return dice_surface

    def display_dice(self, rolls):
        if self.dice_image:
            self.dice_image.kill()

        dice_render = self.render_dice(rolls)
        dice_rect = pygame.Rect(self.info_panel.relative_rect.left - dice_render.get_width() - SPACING,
                                self.action_panel.relative_rect.top - dice_render.get_height() - SPACING,
                                dice_render.get_width(),
                                dice_render.get_height())

        if self.dice_button is None:
            self.dice_button = pg_g.elements.UIButton(
                relative_rect=dice_rect,
                manager=self.manager,
                text="",
                anchors={'left': 'right',
                         'right': 'right',
                         'top': 'bottom',
                         'bottom': 'bottom'},
            )

        self.dice_image = pg_g.elements.UIImage(
            relative_rect=dice_rect,
            manager=self.manager,
            image_surface=dice_render,
            anchors={'left': 'right',
                     'right': 'right',
                     'top': 'bottom',
                     'bottom': 'bottom'}
        )

    def initialize_gui(self):
        pygame.init()
        pygame.display.set_caption('Client')
        # print(os.path.abspath(__file__))
        # os.chdir(os.path.dirname(__file__))
        font_size = int(45 * PROTOTYPE_SCALE)
        self.font = pygame.font.SysFont('Comic Sans MS', font_size)

        font_size = int(45 * PROTOTYPE_SCALE)
        self.font_bank = pygame.font.SysFont('Comic Sans MS', font_size)

        # print(self.player.screen_num)
        #screen_string = "localhost:0." + self.player.screen_num
        #os.putenv("DISPLAY", screen_string)
        os.environ['SDL_VIDEODRIVER'] = 'x11'
        '''
        if FULLSCREEN:
            self.game_window = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
        else:
            self.game_window = pygame.display.set_mode(RESOLUTION)
        '''
        cursor = pygame.cursors.arrow
        pygame.mouse.set_cursor(*cursor)

        self.manager = pg_g.UIManager(RESOLUTION, './themes/total_theme.json')
        self.clock = pygame.time.Clock()

        # creates settlement polygon
        house_width = 120 * self.scale / 2
        house_height = -135 * self.scale / 2
        self.house_width = 120 * self.scale / 2
        self.house_height = -135 * self.scale / 2
        self.house_points = [
            [-house_width, -house_height],
            [-house_width, 0],
            [0, house_height],
            [house_width, 0],
            [house_width, -house_height]
        ]

        # creates city polygon
        city_width = 120 * self.scale / 2
        city_height = -120 * self.scale / 2

        self.city_width = 120 * self.scale / 2
        self.city_height = -120 * self.scale / 2
        difference = -5

        self.city_points = [
            [-city_width, city_height],
            [-city_width / 2, city_height * 5 / 4],
            [0, city_height],
            [0, 0 + difference],
            [city_width, 0 + difference],
            [city_width, -city_height],
            [-city_width, -city_height]
        ]

        base_path = os.path.dirname(__file__)
        self.object_textures = {
            'Board': pygame.image.load('./assets/gameboard_grid_v6.png')
        }

        self.board_center = (
            RESOLUTION[0] / 2 - int(self.hex_size / 2), RESOLUTION[1] / 2 - int(self.hex_size / 2) - CARD_SIZE[1] / 2)
        # prototype
        self.board_center = (
            int(RESOLUTION[0] / 2 - int(self.hex_size / 2) - 150),
            int(RESOLUTION[1] / 2 - int(self.hex_size / 2) - CARD_SIZE[1] / 2))

        self.resource_hexes = self.game_board.land_list
        self.port_hexes = self.game_board.port_list

        # game grid
        self.object_textures['Board'] = pygame.transform.scale(self.object_textures.get('Board'),
                                                               (int(3600 * self.scale), int(3600 * self.scale)))
        self.grid_size = self.object_textures.get('Board').get_size()
        self.set_butts = self.initial_settlement_buttons()
        self.road_butts = []

        action_panel_layout = pygame.Rect(0, 0, INFO_WIDTH, ACTION_SIZE[1] + 2 * SPACING)
        action_panel_layout.bottomright = (-SPACING, -SPACING)
        self.action_panel = pg_g.elements.UIPanel(relative_rect=action_panel_layout,
                                                  starting_layer_height=1,
                                                  manager=self.manager,
                                                  anchors={'left': 'right',
                                                           'right': 'right',
                                                           'top': 'bottom',
                                                           'bottom': 'bottom'}
                                                  )

        self.trade_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((0 * ACTION_SIZE[0] + 0 * SPACING, 0), ACTION_SIZE),
            container=self.action_panel,
            manager=self.manager,
            text="TRADE",
            tool_tip_text="Trade resources with the bank")

        self.road_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((1 * ACTION_SIZE[0] + 1 * SPACING, 0), ACTION_SIZE),
            container=self.action_panel,
            manager=self.manager,
            text="ROAD")

        self.settlement_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((2 * ACTION_SIZE[0] + 2 * SPACING, 0), ACTION_SIZE),
            container=self.action_panel,
            manager=self.manager,
            text="SETTLE")

        self.city_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((3 * ACTION_SIZE[0] + 3 * SPACING, 0), ACTION_SIZE),
            container=self.action_panel,
            manager=self.manager,
            text="CITY")

        self.development_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((4 * ACTION_SIZE[0] + 4 * SPACING, 0), ACTION_SIZE),
            container=self.action_panel,
            manager=self.manager,
            text="DEV CARD")

        self.end_turn_button = pg_g.elements.UIButton(
            relative_rect=pygame.Rect((5 * ACTION_SIZE[0] + 5 * SPACING, 0), ACTION_SIZE),
            container=self.action_panel,
            manager=self.manager,
            text="END",
        )

        card_panel_layout = pygame.Rect(0, 0, RESOLUTION[0] - action_panel_layout.width - 2 * SPACING,
                                        CARD_SIZE[1] + 2 * SPACING)
        card_panel_layout.bottomleft = (SPACING, -SPACING)
        self.card_panel = pg_g.elements.UIPanel(relative_rect=card_panel_layout,
                                                starting_layer_height=1,
                                                manager=self.manager,
                                                anchors={'left': 'left',
                                                         'right': 'right',
                                                         'top': 'bottom',
                                                         'bottom': 'bottom'}
                                                )

        info_panel_layout = pygame.Rect(0, 0, INFO_WIDTH, RESOLUTION[1] - action_panel_layout.height - 2 * SPACING)
        info_panel_layout.topright = (-SPACING, SPACING)
        self.info_panel = PlayerInfo(relative_rect=info_panel_layout,
                                     starting_layer_height=1,
                                     manager=self.manager,
                                     anchors={'left': 'right',
                                              'right': 'right',
                                              'top': 'top',
                                              'bottom': 'top'}
                                     )

        self.help_button = pg_g.elements.UIButton(
            text="Help",
            manager=self.manager,
            relative_rect=pygame.Rect(self.card_panel.relative_rect.left + SPACING, self.card_panel.relative_rect.top - SPACING - 50, 50, 50),
            anchors={'left': 'left',
                     'right': 'left',
                     'top': 'bottom',
                     'bottom': 'bottom'}
        )

        self.text_dialog = TextDialog(pygame.Rect(SPACING, SPACING, INFO_WIDTH, INFO_WIDTH / 2), self.manager)
        self.text_dialog.add_line("<b>Welcome to Frontiersman!</b>")

        self.end_turn_button.disable()
        self.development_button.disable()
        self.city_button.disable()
        self.settlement_button.disable()
        self.road_button.disable()
        self.trade_button.disable()
        self.card_hand = []
        self.set_cards(self.card_hand)

    def accept_trade(self):
        self.board_input.put('accept,' + self.player.color)
        self.board_action = self.last_board_action
        self.board_updated = True

    def deny_trade(self):
        self.board_input.put('deny,' + self.player.color)
        self.board_action = self.last_board_action
        self.board_updated = True

    def player_selector_callback(self, enemy_player):
        self.board_input.put('steal,' + enemy_player.color)
        self.player_selector.kill()
        self.player_selector = None
        self.board_action = self.last_board_action
        self.board_updated = True

    def trade_selector_callback(self, enemy_player):
        self.board_input.put('trade,' + enemy_player.color)
        self.player_selector.kill()
        self.player_selector = None
        self.board_action = self.last_board_action
        self.board_updated = True

    def trade_selector_cancel_callback(self):
        self.board_input.put('tradecancel')
        self.player_selector.kill()
        self.player_selector = None
        self.board_action = self.last_board_action
        self.board_updated = True

    def card_discarder_callback(self, cards_to_discard):
        self.board_input.put(','.join(cards_to_discard))
        self.card_discarder.kill()
        self.card_discarder = None
        self.board_action = self.last_board_action
        self.board_updated = True

    def handle_board_actions(self):
        if self.board_updated and self.board_action == "initialsettlement":
            self.set_butts = self.initial_settlement_buttons()
            self.add_text("Place settlement.")
            self.board_updated = False
        if self.board_updated and self.board_action == "road":
            self.add_text("Place road.")
            self.road_butts = self.get_road_buttons()
            self.board_updated = False
        if self.board_updated and self.board_action == "roadfree":
            self.add_text("Place road.")
            self.road_butts = self.get_road_buttons(True)
            self.board_updated = False
        if self.board_updated and self.board_action == "thieftarget":
            self.add_text("Choose who to steal from.")
            listy = self.get_adjacent_owners(self.game_board.get_robber())
            if len(listy) == 0:
                self.board_action = self.last_board_action
                self.board_update = True
            else:
                self.player_selector = PlayerSelector((100, 100), listy, self.manager, "sample text", self.player_selector_callback)
                self.board_updated = False
        if self.board_updated and self.board_action == "tradepartner":
            self.add_text("Choose who to trade with.")
            self.player_selector = PlayerSelector((100, 100), self.trade_list, self.manager, "sample text", self.trade_selector_callback, self.trade_selector_cancel_callback)
            self.board_updated = False
        if self.board_updated and self.board_action == "tradeoffer":
            self.add_text("Do you want to accept this trade?.")
            self.trade_prompt = TradePrompt(self.manager, self.trade_offer, self.trade_cost, self.card_list_to_arr(self.card_hand), self.accept_trade, self.deny_trade)
            self.board_updated = False
        if self.board_updated and self.board_action == "discard":
            self.add_text("You have to discard cards.")
            self.card_discarder = CardDiscarder(self.card_panel.rect, self.card_hand, self.manager, self.card_discarder_callback, 100)
            self.board_updated = False

        if self.board_updated and self.board_action == "robber":
            self.add_text("Move the robber.")
            self.robber_butts = self.get_robber_buttons()  # todo why is this uninitialized
            self.board_updated = False
        if self.board_updated and self.board_action == "set":
            self.add_text("Place a settlement.")
            self.set_butts = self.get_settlement_buttons()
            self.board_updated = False
        if self.board_updated and self.board_action == "city":
            self.add_text("Upgrade a settlement.")
            self.set_butts = self.get_city_buttons()
            self.board_updated = False
        if self.board_updated and self.board_action == "initialroad":
            self.add_text("Place a road.")
            self.road_butts = self.initial_road_buttons(self.property_list[-1])
            self.board_updated = False
        if self.board_action != "turn":
            self.end_turn_button.disable()
            self.development_button.disable()
            self.city_button.disable()
            self.settlement_button.disable()
            self.road_button.disable()
            self.trade_button.disable()
        elif self.board_action == "turn" and self.board_updated:
            self.end_turn_button.enable()
            if Actions.buy_development_check(self.player):
                self.development_button.enable()
            else:
                self.development_button.disable()
            if len(Actions.build_city_available(self.player)) != 0:
                self.city_button.enable()
            else:
                self.city_button.disable()
            if len(Actions.build_settlement_available(self.player)) != 0:
                self.settlement_button.enable()
            else:
                self.settlement_button.disable()
            if Actions.build_road_check(self.player):
                self.road_button.enable()
            else:
                self.road_button.disable()
            self.trade_button.enable()
            self.board_updated = False

    def handle_mouse_motion(self, event):
        if self.board_action == "initialsettlement" or self.board_action == "set" or self.board_action == "city":
            for butt in self.set_butts:
                butt.on_mousemotion(event)
        elif self.board_action == "initialroad" or self.board_action == "road" or self.board_action == "roadfree":
            for butt in self.road_butts:
                butt.on_mousemotion(event)
        elif self.board_action == "robber":
            for butt in self.robber_butts:
                butt.on_mousemotion(event)

    def handle_mouse_button_down(self, event):
        if self.board_action == "initialsettlement" or self.board_action == "set" or self.board_action == "city":
            for butt in self.set_butts:
                butt.on_mousebuttondown(event)
        elif self.board_action == "initialroad" or self.board_action == "road" or self.board_action == "roadfree":
            for butt in self.road_butts:
                butt.on_mousebuttondown(event)
        elif self.board_action == "robber":
            for butt in self.robber_butts:
                butt.on_mousebuttondown(event)

    def handle_user_event(self, event):
        if event.user_type == pg_g.UI_BUTTON_PRESSED:
            if self.card_picker is not None:
                self.card_picker.handle_ui_button_pressed(event)
            if self.card_trader is not None:
                self.card_trader.handle_ui_button_pressed(event)
            if self.player_selector is not None:
                self.player_selector.handle_ui_button_pressed(event)
            if self.card_discarder is not None:
                self.card_discarder.handle_ui_button_pressed(event)
            if self.trade_prompt is not None:
                self.trade_prompt.handle_events(event)
            if event.ui_element == self.help_button:
                if self.help_window is None:
                    self.help_window = HelpWindow((10, 10), self.manager)
                else:
                    if not self.help_window.alive():
                        self.help_window.kill()
                        self.help_window = None
                        self.help_window = HelpWindow((10, 10), self.manager)
                    else:
                        self.help_window.kill()
                        self.help_window = None
            elif event.ui_element == self.trade_button:
                if self.card_trader is None:
                    def callback(trade_with, give_cards, take_cards):
                        # todo check trade_with to implement player trading
                        if trade_with == "tradebank":
                            self.trade_cards(give_cards, take_cards)
                            self.card_trader.kill()
                            self.card_trader = None
                        else:
                            offer = ','.join([str(i) for i in self.card_list_to_arr(give_cards)])
                            cost = ','.join([str(i) for i in self.card_list_to_arr(take_cards)])
                            self.board_input.put("tradeoffer|" + self.player.color + '|' + offer + '|' + cost)
                            self.card_trader.kill()
                            self.card_trader = None

                    self.card_trader = TraderGui((50, 100), self.player.resourceHand, self.player.bankTrading, self.manager, callback)
                else:
                    self.card_trader.kill()
                    self.card_trader = None
            elif event.ui_element == self.end_turn_button:
                self.board_input.put("end")
            elif event.ui_element == self.road_button:
                self.set_board_action("road", 'turn')
            elif event.ui_element == self.settlement_button:
                self.set_board_action("set", 'turn')
            elif event.ui_element == self.city_button:
                self.set_board_action("city", 'turn')
            elif event.ui_element == self.development_button:
                self.board_input.put("dev")
            elif event.ui_element == self.dice_button:
                self.is_rolling = not self.is_rolling
            elif '#knight' in event.ui_element.object_ids and not self.player.development_card_played and self.board_action == "turn":
                self.player.development_card_played = True
                self.card_hand.remove('knight')
                self.player.developmentHand.remove_card('knight')
                self.set_cards(self.card_hand)
                self.set_board_action("robber", 'turn')
                self.player.largestArmy += 1
            elif '#roadBuilding' in event.ui_element.object_ids and not self.player.development_card_played and self.board_action == "turn":
                self.player.development_card_played = True
                self.card_hand.remove('roadBuilding')
                self.player.developmentHand.remove_card('roadBuilding')
                self.set_cards(self.card_hand)
                self.board_input.put('roadroad')
            elif '#yearOfPlenty' in event.ui_element.object_ids and not self.player.development_card_played and self.board_action == "turn":
                self.player.development_card_played = True
                if self.card_picker is None:
                    def callback(card_type):
                        self.card_picker.kill()
                        self.card_picker = None
                        if (card_type == 'Wheat' and self.bank.grain > 1) or (card_type == 'Sheep' and self.bank.wool > 1) or (card_type == 'Wood' and self.bank.lumber > 1) or (
                                card_type == 'Ore' and self.bank.ore > 1) or (card_type == 'Brick' and self.bank.brick > 1):
                            self.get_cards([card_type, card_type])
                        elif (card_type == 'Wheat' and self.bank.grain > 0) or (card_type == 'Sheep' and self.bank.wool > 0) or (card_type == 'Wood' and self.bank.lumber > 0) or (
                                card_type == 'Ore' and self.bank.ore > 0) or (card_type == 'Brick' and self.bank.brick > 0):
                            self.get_cards([card_type, card_type])
                        self.card_hand.remove('yearOfPlenty')
                        self.player.developmentHand.remove_card('yearOfPlenty')
                        self.set_cards(self.card_hand)

                    self.card_picker = CardPickerGui((50, 200), self.manager, callback)
            elif '#monopoly' in event.ui_element.object_ids and not self.player.development_card_played and self.board_action == "turn":
                self.player.development_card_played = True
                if self.card_picker is None:
                    def callback(card_type):
                        self.card_picker.kill()
                        self.card_picker = None
                        self.card_hand.remove('monopoly')
                        self.player.developmentHand.remove_card('monopoly')
                        self.get_monopoly(card_type)

                    self.card_picker = CardPickerGui((50, 200), self.manager, callback)
            elif '#victoryPoint' in event.ui_element.object_ids and not self.player.development_card_played and self.board_action == "turn":
                pass

    def run(self, board):
        self.game_board = board
        self.game_board.translate_to_3d()
        self.building_locations = StructureBoard(3, self.game_board.get_array())
        self.initialize_gui()
        self.set_cards(self.card_hand)
        pygame.display.flip()  # todo consider removing
        self.running = True
        self.robber_butts = []
        self.display_dice([random.randint(1, 6), random.randint(1, 6)])
        # while True:
        # self.update_frame()

    def add_text(self, text):
        if self.text_dialog is not None:
            self.text_dialog.add_line(text)

    def turn_banner(self):
        pass # todo brian do this please !!!!!

    def update_frame(self):
        time_delta = self.clock.tick(30) / 1000.0
        if self.board_updated:
            self.info_panel.set_bank_info(self.bank)
            self.info_panel.set_player_info(self.player, self.enemy_list)
        if self.cards_updated:
            self.update_cards()
            self.cards_updated = False
        if self.turn_start:
            self.turn_banner()
            self.turn_start = False

        self.handle_board_actions()

        for event in pygame.event.get():
            self.manager.process_events(event)
            if event.type == pygame.QUIT:
                print(event)
                ses = requests.Session()
                ses.post(self.post_url, data={'msg': "quit"})
                self.board_input.put('quit')
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_button_down(event)
            elif event.type == pygame.USEREVENT:
                self.handle_user_event(event)

        self.manager.update(time_delta)

        self.draw_board()
        if self.is_rolling:
            self.display_dice([random.randint(1, 6), random.randint(1, 6)])
        self.manager.draw_ui(self.game_window)

        pygame.display.flip()

    def draw_board(self):


        # paint background
        self.game_window.fill((61, 120, 180))
        # draw hexes
        for tile in self.resource_hexes:
            self.game_window.blit(self.texture_dictionary.get(tile.resource),
                                  self.translate_hex_to_xy(tile.location, self.board_center, int(self.hex_size / 2)))

        # draw Board
        self.game_window.blit(self.object_textures.get('Board'),
                              (int(self.board_center[0] - self.grid_size[0] / 2 + self.hex_size / 2),
                               int(self.board_center[1] - self.grid_size[1] / 2 + self.hex_size / 2) - 1))
        # draw resource numbers
        for tile in self.resource_hexes:
            if tile.resource == 'Desert':
                pass
            else:
                text_surface = self.font.render(str(tile.number), False, (0, 0, 0))
                coord = self.translate_hex_to_xy(tile.location, self.board_center, int(self.hex_size / 2))
                self.game_window.blit(text_surface, (coord[0] + self.hex_size / 2 - text_surface.get_width() / 2,
                                                     coord[1] + self.hex_size / 2 - text_surface.get_height() / 2))
        # draw ports
        for port in self.port_hexes:
            self.game_window.blit(self.port_textures.get(port.resource),
                                  self.translate_hex_to_xy(port.location, self.board_center, int(self.hex_size / 2)))

        # draw roads
        for properties in self.road_list:
            location = EdgeNode.translate_road((properties.cord1, properties.cord2), self.board_center,
                                               self.hex_size / 2)

            if properties.cord2 % 2 == 1:
                variation = 0
                angle = 0
            elif (properties.cord2 + properties.cord1) % 4 == 1:
                variation = 1
                angle = 120
            else:
                variation = 2
                angle = 60

            offset = self.hex_size / 4

            road_shape = ClientHelper.RoadHardwareArt.generate_road_art(self.hex_size / 2,
                                                                        COLORS[properties.color], angle)

            self.game_window.blit(road_shape, (int(location[0] - road_shape.get_width() / 2),
                                               int(location[1] - road_shape.get_height() / 2)))

            '''
            shifted_points = []
            # variation 0, 1, 2 = |, /, \

            self.road_length = self.hex_size / 4
            self.road_width = self.road_length / 15

            offset = [
                [0, 0],
                [0, 0],
                [0, 0]
            ]

            for points in self.road_points[variation]:
                shifted_points.append((location[0] + points[0] + offset[variation][0],
                                       location[1] + points[1] + offset[variation][1]))

            pygame.gfxdraw.filled_polygon(self.game_window, shifted_points, COLORS[properties.color])
            '''

        # draw settlements
        for properties in self.property_list:
            shifted_points = []
            location = CornerNode.translate_settlement((properties.cord1, properties.cord2), self.board_center,
                                                       int(self.hex_size / 2))
            if properties.city:
                for points in self.city_points:
                    # shifted_points.append((location[0] + points[0] - self.city_width / 2,
                    #                       location[1] + points[1] + self.city_height))
                    shifted_points.append((location[0] + points[0],
                                           location[1] + points[1]))

                pygame.gfxdraw.filled_polygon(self.game_window, shifted_points, COLORS[properties.color])
            else:
                for points in self.house_points:
                    # shifted_points.append((location[0] + points[0] - self.house_width / 2,
                    #                       location[1] + points[1] + self.house_height))
                    shifted_points.append((location[0] + points[0],
                                           location[1] + points[1]))

                pygame.gfxdraw.filled_polygon(self.game_window, shifted_points, COLORS[properties.color])

        loc = self.translate_hex_to_xy(self.game_board.get_robber().location, self.board_center, int(self.hex_size / 2))
        pygame.draw.circle(self.game_window, (50, 50, 50),
                           (loc[0] + int(self.hex_size / 3), loc[1] + int(self.hex_size / 3)), int(30 * PROTOTYPE_SCALE))

        if self.board_action == "initialsettlement" or self.board_action == "set" or self.board_action == "city":
            for butt in self.set_butts:
                butt.draw(self.game_window)
        if self.board_action == "initialroad" or self.board_action == "road" or self.board_action == "roadfree":
            for butt in self.road_butts:
                butt.draw(self.game_window)
        if self.board_action == "robber":
            for butt in self.robber_butts:
                butt.draw(self.game_window)
