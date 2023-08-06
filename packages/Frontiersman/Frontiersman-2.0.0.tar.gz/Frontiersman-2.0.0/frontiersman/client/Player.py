class PlayerResourceHand:
    def __init__(self):
        self.brick = 0
        self.grain = 0
        self.lumber = 0
        self.ore = 0
        self.wool = 0
        self.totalResources = 0


class PlayerDevelopmentHand:
    def __init__(self):
        self.knights = 0
        self.roadBuildings = 0
        self.yearOfPlenty = 0
        self.monopolies = 0
        self.victoryPoints = 0
        self.totalDevelopments = 0

    def add_card(self, card):
        if card == 'knight':
            self.knights += 1
        elif card == 'roadBuilding':
            self.roadBuildings += 1
        elif card == 'yearOfPlenty':
            self.yearOfPlenty += 1
        elif card == 'monopoly':
            self.monopolies += 1
        elif card == 'victoryPoint':
            self.victoryPoints += 1
        self.totalDevelopments += 1

    def remove_card(self, card):
        if card == 'knight':
            self.knights -= 1
        elif card == 'roadBuilding':
            self.roadBuildings -= 1
        elif card == 'yearOfPlenty':
            self.yearOfPlenty -= 1
        elif card == 'monopoly':
            self.monopolies -= 1
        elif card == 'victoryPoint':
            self.victoryPoints -= 1
        self.totalDevelopments -= 1


class TradeRatios:
    def __init__(self):
        self.brick = 4
        self.grain = 4
        self.lumber = 4
        self.ore = 4
        self.wool = 4

    def update(self, resource):
        if resource == "Brick":
            self.brick = 2
        elif resource == "Wheat":
            self.grain = 2
        elif resource == "Wood":
            self.lumber = 2
        elif resource == "Ore":
            self.ore = 2
        elif resource == "Sheep":
            self.wool = 2
        elif resource == "None":
            self.brick = min(self.brick, 3)
            self.grain = min(self.grain, 3)
            self.lumber = min(self.lumber, 3)
            self.ore = min(self.ore, 3)
            self.wool = min(self.wool, 3)


class EnemyPlayer:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.handSize = '0'
        self.developmentSize = '0'
        self.visibleVictoryPoints = '0'
        self.numRoads = '15'
        self.numSettlements = '5'
        self.numCities = '4'
        self.longestRoad = '0'
        self.largestArmy = '0'

    def update_enemy(self, data):
        self.name = data[0]
        self.color = data[1]
        self.handSize = data[2]
        self.developmentSize = data[3]
        self.visibleVictoryPoints = data[4]
        self.numRoads = data[5]
        self.numSettlements = data[6]
        self.numCities = data[7]
        self.longestRoad = data[8]
        self.largestArmy = data[9]


class Player:
    def __init__(self, name, color, screen_num):
        self.color = color
        self.name = name
        self.numRoads = 15
        self.numSettlements = 5
        self.numCities = 4
        self.longestRoad = 0
        self.claimLongestRoad = False
        self.largestArmy = 0
        self.claimLargestArmy = False
        self.victoryPoints = 0
        self.hiddenVictoryPoints = 0
        self.resourceHand = PlayerResourceHand()
        self.developmentHand = PlayerDevelopmentHand()
        self.bankTrading = TradeRatios()
        self.development_card_played = False
        self.ownedRoads = list()
        self.ownedNodes = list()
        self.screen_num = screen_num

    def get_num_resources(self):
        return self.resourceHand.totalResources

    def get_num_development(self):
        return self.developmentHand.totalDevelopments

    def get_sent_to_enemies(self):
        to_send = ','.join([self.name, self.color,
                            str(self.resourceHand.totalResources), str(self.developmentHand.totalDevelopments),
                            str(self.victoryPoints), str(self.numRoads), str(self.numSettlements), str(self.numCities),
                            str(self.longestRoad), str(self.largestArmy)])
        return to_send

    # todo has problem with joining established roads

    def acquire_road(self, road):
        self.ownedRoads.append(road)
        for edge in self.ownedRoads:
            road_stack = list()
            road_stack.append(edge)
            road_checked = list()
            road_checked.append(edge)

            to_check = self.longest_road_value(road_stack, road_checked)
            if self.longestRoad < to_check:
                self.longestRoad = to_check
        self.numRoads -= 1

    def get_longest_road(self, enemy_longest_road):
        if enemy_longest_road < 5 and self.longestRoad >= 5 and not self.claimLongestRoad:
            self.claimLongestRoad = True
            self.victoryPoints += 2
        elif 5 <= enemy_longest_road < self.longestRoad and not self.claimLongestRoad:
            self.claimLongestRoad = True
            self.victoryPoints += 2
            return True
        return False

    def lose_longest_road(self, enemy_longest_road):
        if enemy_longest_road > self.longestRoad and self.claimLongestRoad:
            self.claimLongestRoad = False
            self.victoryPoints -= 2

    def get_largest_army(self, enemy_largest_army):
        if enemy_largest_army < 3 and self.largestArmy >= 3 and not self.claimLargestArmy:
            self.claimLargestArmy = True
            self.victoryPoints += 2
        elif 3 <= enemy_largest_army < self.largestArmy and not self.claimLargestArmy:
            self.claimLargestArmy = True
            self.victoryPoints += 2
            return True
        return False

    def lost_largest_army(self, enemy_largest_army):
        if enemy_largest_army > self.largestArmy and self.claimLargestArmy:
            self.claimLargestArmy = False
            self.victoryPoints -= 2

    def longest_road_value(self, road_stack, road_checked, length=1, prev_corner = None):
        current = road_stack.pop()
        to_return = length
        for corner in current.corners:
            if prev_corner is not None and corner == prev_corner:
                continue

            for edge in corner.edges:
                if edge is not None and (edge not in road_checked) and (edge.color == self.color):
                    road_stack.append(edge)
                    road_checked.append(edge)
                    length_check = self.longest_road_value(road_stack, road_checked, length + 1, corner)

                    if to_return < length_check:
                        to_return = length_check

                    break
        return to_return

    def acquire_node(self, node):
        self.ownedNodes.append(node)
        self.numSettlements -= 1
        self.victoryPoints += 1

    def acquire_city(self):
        self.numCities -= 1
        self.numSettlements += 1
        self.victoryPoints += 1

    def add_resource(self, update_frame):
        self.resourceHand.brick += update_frame[0]
        self.resourceHand.grain += update_frame[1]
        self.resourceHand.lumber += update_frame[2]
        self.resourceHand.ore += update_frame[3]
        self.resourceHand.wool += update_frame[4]

        self.resourceHand.totalResources += sum(update_frame)
