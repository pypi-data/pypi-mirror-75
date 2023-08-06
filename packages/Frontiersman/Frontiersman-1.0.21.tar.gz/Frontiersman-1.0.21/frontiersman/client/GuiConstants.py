# Configurable options:
# Configurable options:
resolution_selection = ''
CIRCLE_TILES=False
try:
    file1 = open('config.txt', 'r')
    Lines = file1.readlines()
    count = 0
    for line in Lines:
        setting = line[:-1].split('=')
        if setting[0] == 'circle_tiles':
            CIRCLE_TILES = (setting[1] == 'True' or setting[1] == 1)
        if setting[0] == 'resolution_selection':
            if setting[1] in ['A', 'B', 'C', 'D', 'E']:
                resolution_selection = setting[1]
            else:
                resolution_selection = 'C'
    file1.close()
except FileNotFoundError:
    try:
        file1 = open('../config.txt', 'r')
        Lines = file1.readlines()
        count = 0
        for line in Lines:
            setting = line[:-1].split('=')
            if setting[0] == 'circle_tiles':
                CIRCLE_TILES = (setting[1] == 'True' or setting[1] == 1)
            if setting[0] == 'resolution_selection':
                if setting[1] in ['A', 'B', 'C', 'D', 'E']:
                    resolution_selection = setting[1]
                else:
                    resolution_selection = 'C'
        file1.close()
    except FileNotFoundError:
        pass

if resolution_selection == '':
    resolution_selection = 'C'

# resolution_selection = 'C'

# Constants

RES_SCALE_DICT = {
    'A': ((1920, 1080), 1),
    'B': ((1200, 800), 75 / 100),
    'C': ((1600, 900), 83 / 100),
    'D': ((960, 540), 50 / 100),
    'E': ((1280, 720), 69 / 100)
}
FRAME_RATE = 60
RESOLUTION, PROTOTYPE_SCALE = RES_SCALE_DICT[resolution_selection]
SPACING = 3
FULLSCREEN = False
SCALE = 5 / 16
HEX_SIZE = 600 * SCALE * PROTOTYPE_SCALE
ACTION_SIZE = 70, 98
CARD_SIZE = 70, 98
WINDOW_CENTER = (RESOLUTION[0] / 2, RESOLUTION[1] / 2)

ACTION_WIDTH = ACTION_SIZE[0] * 6 + 7 * SPACING
INFO_WIDTH = 400 * PROTOTYPE_SCALE
DIALOG_SIZE = ACTION_WIDTH, 300 * PROTOTYPE_SCALE - 6 * SPACING
INFO_HEIGHT = RESOLUTION[1] - ACTION_SIZE[1] - DIALOG_SIZE[1] - 4 * SPACING

PLAYER_HEIGHT = int(INFO_WIDTH / 4)
PLAYER_SECTION_WIDTH = int((INFO_WIDTH - 4 * SPACING) / 5)
PLAYER_QUARTER_HEIGHT = int((PLAYER_HEIGHT - 2 * SPACING) / 4)
PLAYER_SECTION_SIZE = int((INFO_WIDTH - 3 * SPACING) / 8)

BANK_SECTION_SIZE = int((INFO_WIDTH - SPACING) / 8)
BANK_HEIGHT = BANK_SECTION_SIZE * 2
