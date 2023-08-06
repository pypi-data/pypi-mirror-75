import pygame
import pygame_gui as pg_g

from frontiersman.client import ClientHelper
from frontiersman.client.GuiConstants import INFO_WIDTH, SPACING, PLAYER_SECTION_SIZE, PLAYER_HEIGHT, BANK_SECTION_SIZE, BANK_HEIGHT

INFO_LOGOS = ClientHelper.TextureScale.scale_logos((PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE))
BANK_IMAGES = ClientHelper.TextureScale.scale_bank((BANK_SECTION_SIZE, BANK_SECTION_SIZE))
BANK_LOGO = ClientHelper.TextureScale.scale_bank_logo((BANK_SECTION_SIZE * 2, BANK_SECTION_SIZE * 2))


class PlayerInfo(pg_g.elements.UIPanel):
    def __init__(self, relative_rect, starting_layer_height, manager, font_size, anchors=None):
        super().__init__(relative_rect, starting_layer_height, manager, anchors=anchors)
        self.manager = manager
        self.font = pygame.font.SysFont('Comic Sans MS', font_size)

        self.bank_element = pg_g.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, INFO_WIDTH, BANK_HEIGHT),
            container=self,
            starting_layer_height=1,
            manager=self.manager)

        self.player_elements = []

    def render_text(self, text, size, gold_bg=False):
        if gold_bg:
            small_surface = self.font.render(text, True, (0,0,0))
        else:
            small_surface = self.font.render(text, True, (187, 187, 187))
        big_surface = pygame.Surface(size, pygame.SRCALPHA)

        text_pos = (big_surface.get_width() - small_surface.get_width()) / 2, (
                big_surface.get_height() - small_surface.get_height()) / 2
        bg_size = [small_surface.get_width() + 4 * SPACING, small_surface.get_height() + 4 * SPACING]
        bg_size[0] = max(bg_size[0], bg_size[1])

        bg_pos = text_pos[0] - (bg_size[0] - small_surface.get_width()) / 2, text_pos[1] - (
                bg_size[1] - small_surface.get_height()) / 2
        bg_rect = pygame.Rect(bg_pos, bg_size)

        
        if gold_bg:
            pygame.draw.rect(big_surface, (218,165,32), bg_rect)
        else:
            pygame.draw.rect(big_surface, (33, 40, 45), bg_rect)
        pygame.draw.rect(big_surface, (92, 96, 98), bg_rect, width=1)
        big_surface.blit(small_surface, text_pos)
        return big_surface

    def add_player_element(self, index, player, turn):
        curr_player_info = pg_g.elements.UIPanel(
            relative_rect=pygame.Rect(0, (PLAYER_HEIGHT + SPACING) * index + BANK_HEIGHT + SPACING,
                                      INFO_WIDTH - 2 * SPACING, PLAYER_HEIGHT + 2 * SPACING),
            container=self,
            starting_layer_height=1,
            manager=self.manager,
            object_id="#" + player['color']
        )

        name = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(0, 0, 2 * PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE),
            container=curr_player_info,
            image_surface=self.render_text(player['name'], (2 * PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE), turn),
            manager=self.manager,
        )

        vp_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(name.relative_rect.right, name.relative_rect.top, PLAYER_SECTION_SIZE,
                                      PLAYER_SECTION_SIZE),
            container=curr_player_info,
            image_surface=INFO_LOGOS['star'],
            manager=self.manager,
        )
        vp_value = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(vp_logo.relative_rect.right, vp_logo.relative_rect.top, PLAYER_SECTION_SIZE,
                                      PLAYER_SECTION_SIZE),
            container=curr_player_info,
            image_surface=self.render_text(player['vp'], (PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE)),
            manager=self.manager,
        )

        longest_road_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(vp_value.relative_rect.right, vp_value.relative_rect.top, PLAYER_SECTION_SIZE,
                                      PLAYER_SECTION_SIZE),
            container=curr_player_info,
            image_surface=INFO_LOGOS['road'],
            manager=self.manager,
        )
        longest_road_value = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(longest_road_logo.relative_rect.right, longest_road_logo.relative_rect.top,
                                      PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE),
            container=curr_player_info,
            image_surface=self.render_text(player['lr'], (PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE)),
            manager=self.manager,
        )

        largest_army_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(longest_road_value.relative_rect.right, longest_road_value.relative_rect.top,
                                      PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE),
            image_surface=INFO_LOGOS['army'],
            container=curr_player_info,
            manager=self.manager,
        )
        largest_army_value = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(largest_army_logo.relative_rect.right, largest_army_logo.relative_rect.top,
                                      PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE),
            container=curr_player_info,
            image_surface=self.render_text(player['la'], (PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE)),
            manager=self.manager,
        )

        hand_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(name.relative_rect.left, name.relative_rect.bottom, PLAYER_SECTION_SIZE,
                                      PLAYER_SECTION_SIZE),
            container=curr_player_info,
            image_surface=INFO_LOGOS['cards'],
            manager=self.manager,
        )
        hand_value = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(hand_logo.relative_rect.right, hand_logo.relative_rect.top,
                                      PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE),
            container=curr_player_info,
            image_surface=self.render_text(player['hand'], (PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE)),
            manager=self.manager,
        )

        roads_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(hand_value.relative_rect.right, hand_value.relative_rect.top, PLAYER_SECTION_SIZE,
                                      PLAYER_SECTION_SIZE),
            container=curr_player_info,
            image_surface=INFO_LOGOS['num_roads'],
            manager=self.manager,
        )
        roads_value = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(roads_logo.relative_rect.right, roads_logo.relative_rect.top, PLAYER_SECTION_SIZE,
                                      PLAYER_SECTION_SIZE),
            container=curr_player_info,
            image_surface=self.render_text(player['roads'], (PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE)),
            manager=self.manager,
        )

        settlements_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(roads_value.relative_rect.right, roads_value.relative_rect.top,
                                      PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE),
            container=curr_player_info,
            image_surface=INFO_LOGOS['settlement'],
            manager=self.manager,
        )
        settlements_value = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(settlements_logo.relative_rect.right, roads_value.relative_rect.top,
                                      PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE),
            container=curr_player_info,
            image_surface=self.render_text(player['settlements'], (PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE)),
            manager=self.manager,
        )

        cities_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(settlements_value.relative_rect.right, settlements_value.relative_rect.top,
                                      PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE),
            container=curr_player_info,
            image_surface=INFO_LOGOS['city'],
            manager=self.manager,
        )
        cities_value = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(cities_logo.relative_rect.right, cities_logo.relative_rect.top,
                                      PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE),
            container=curr_player_info,
            image_surface=self.render_text(player['city'], (PLAYER_SECTION_SIZE, PLAYER_SECTION_SIZE)),
            manager=self.manager,
        )

        self.player_elements.append(curr_player_info)

    def set_player_info(self, current_player, enemy_players, turn_color):
        for player_element in self.player_elements:
            player_element.kill()
        if current_player.color==turn_color:
            turn=True
        else:
            turn=False
        curr_player = {
            'color': current_player.color.capitalize(),
            'name': current_player.name,
            'vp': str(current_player.victoryPoints) + (
                '' if current_player.hiddenVictoryPoints == 0 else ' (' + str(
                    current_player.hiddenVictoryPoints + current_player.victoryPoints) + ')'),
            'lr': str(current_player.longestRoad),
            'la': str(current_player.largestArmy),
            'hand': str(current_player.resourceHand.totalResources),
            'roads': str(current_player.numRoads),
            'settlements': str(current_player.numSettlements),
            'city': str(current_player.numCities),
        }
        self.add_player_element(0, curr_player,turn)

        for i, enemy in enumerate(enemy_players):
            if enemy.color==turn_color:
                turn=True
            else:
                turn=False
            player = {
                'color': enemy.color.capitalize(),
                'name': enemy.name,
                'vp': str(enemy.visibleVictoryPoints),
                'lr': str(enemy.longestRoad),
                'la': str(enemy.largestArmy),
                'hand': str(enemy.handSize),
                'roads': str(enemy.numRoads),
                'settlements': str(enemy.numSettlements),
                'city': str(enemy.numCities),
            }
            self.add_player_element(i + 1, player, turn)

    def set_bank_info(self, bank):
        self.bank_element.kill()
        self.bank_element = pg_g.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, INFO_WIDTH, BANK_HEIGHT + 2 * SPACING),
            container=self,
            starting_layer_height=1,
            manager=self.manager)

        bank_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(0, 0, BANK_SECTION_SIZE * 2, BANK_SECTION_SIZE * 2),
            container=self.bank_element,
            manager=self.manager,
            image_surface=BANK_LOGO,
        )

        wood_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(bank_logo.relative_rect.right, bank_logo.relative_rect.top, BANK_SECTION_SIZE,
                                      BANK_SECTION_SIZE),
            image_surface=BANK_IMAGES["Wood"],
            manager=self.manager,
            container=self.bank_element)

        brick_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(wood_logo.relative_rect.right, wood_logo.relative_rect.top, BANK_SECTION_SIZE,
                                      BANK_SECTION_SIZE),
            image_surface=BANK_IMAGES["Brick"],
            manager=self.manager,
            container=self.bank_element)

        sheep_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(brick_logo.relative_rect.right, brick_logo.relative_rect.top, BANK_SECTION_SIZE,
                                      BANK_SECTION_SIZE),
            image_surface=BANK_IMAGES["Sheep"],
            manager=self.manager,
            container=self.bank_element)

        wheat_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(sheep_logo.relative_rect.right, sheep_logo.relative_rect.top, BANK_SECTION_SIZE,
                                      BANK_SECTION_SIZE),
            image_surface=BANK_IMAGES["Wheat"],
            manager=self.manager,
            container=self.bank_element)

        ore_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(wheat_logo.relative_rect.right, wheat_logo.relative_rect.top, BANK_SECTION_SIZE,
                                      BANK_SECTION_SIZE),
            image_surface=BANK_IMAGES["Ore"],
            manager=self.manager,
            container=self.bank_element)

        dev_logo = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(ore_logo.relative_rect.right, ore_logo.relative_rect.top, BANK_SECTION_SIZE,
                                      BANK_SECTION_SIZE),
            image_surface=BANK_IMAGES["Dev"],
            manager=self.manager,
            container=self.bank_element)

        wood_text = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(wood_logo.relative_rect.left, wood_logo.relative_rect.bottom, BANK_SECTION_SIZE,
                                      BANK_SECTION_SIZE),
            image_surface=self.render_text(str(bank.lumber), (BANK_SECTION_SIZE, BANK_SECTION_SIZE)),
            manager=self.manager,
            container=self.bank_element,
        )

        brick_text = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(brick_logo.relative_rect.left, brick_logo.relative_rect.bottom, BANK_SECTION_SIZE,
                                      BANK_SECTION_SIZE),
            image_surface=self.render_text(str(bank.brick), (BANK_SECTION_SIZE, BANK_SECTION_SIZE)),
            manager=self.manager,
            container=self.bank_element,
        )

        sheep_text = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(sheep_logo.relative_rect.left, sheep_logo.relative_rect.bottom, BANK_SECTION_SIZE,
                                      BANK_SECTION_SIZE),
            image_surface=self.render_text(str(bank.wool), (BANK_SECTION_SIZE, BANK_SECTION_SIZE)),
            manager=self.manager,
            container=self.bank_element,
        )

        wheat_text = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(wheat_logo.relative_rect.left, wheat_logo.relative_rect.bottom, BANK_SECTION_SIZE,
                                      BANK_SECTION_SIZE),
            image_surface=self.render_text(str(bank.grain), (BANK_SECTION_SIZE, BANK_SECTION_SIZE)),
            manager=self.manager,
            container=self.bank_element,
        )

        ore_text = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(ore_logo.relative_rect.left, ore_logo.relative_rect.bottom, BANK_SECTION_SIZE,
                                      BANK_SECTION_SIZE),
            image_surface=self.render_text(str(bank.ore), (BANK_SECTION_SIZE, BANK_SECTION_SIZE)),
            manager=self.manager,
            container=self.bank_element,
        )

        dev_text = pg_g.elements.UIImage(
            relative_rect=pygame.Rect(dev_logo.relative_rect.left, dev_logo.relative_rect.bottom, BANK_SECTION_SIZE,
                                      BANK_SECTION_SIZE),
            image_surface=self.render_text(str(bank.totalDevelopment), (BANK_SECTION_SIZE, BANK_SECTION_SIZE)),
            manager=self.manager,
            container=self.bank_element,
        )
