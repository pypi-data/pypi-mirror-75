class Bank:
    def __init__(self):
        self.brick = 19
        self.grain = 19
        self.lumber = 19
        self.ore = 19
        self.wool = 19
        self.totalResources = 95
        self.totalDevelopment = 20
        '''
        self.knight = 14
        self.roadBuilding = 2
        self.yearOfPlenty = 2
        self.monopoly = 2
        self.victoryPoint = 5
        '''

    def get_dev_card(self):
        self.totalDevelopment -= 1

    def update(self, update_frame):
        self.brick += update_frame[0]
        self.grain += update_frame[1]
        self.lumber += update_frame[2]
        self.ore += update_frame[3]
        self.wool += update_frame[4]
        self.totalResources = self.brick + self.grain + self.lumber + self.ore + self.wool
