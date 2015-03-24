import pygame

SLOTS = ('top_left', 'top_right', 'right_upper', 'right_lower',
         'bottom_right', 'bottom_left', 'left_lower', 'left_upper',
         'center',)

SLOT_IDX = dict(top_left=0, top_right=1, right_upper=2, right_lower=3, bottom_right=4, bottom_left=5, left_lower=6,
                left_upper=7, center=8)

SLOT_MAP = [(str(idx), 'Unoccupied') for idx, i in enumerate(SLOT_IDX)]
LEGEND = dict(SLOT_MAP)
LEGEND['B'] = 'Blue'
LEGEND['G'] = 'Green'

GRID = """+--------------------------------+
|                                |
|         1         2            |
|          *        *            |
|                                |
|    8 *                * 3      |
|                                |
|              0                 |
|                                |
|    7 *                * 4      |
|                                |
|           *       *            |
|         6          5           |
|                                |
+--------------------------------+"""

BOARD = []
for idx, i in enumerate(SLOTS):
    BOARD.append([i, str(idx)])

# Slot location on an array of strings, like pixels
ASCII_GRID = [(4, 12), (4, 21), (6, 25), (10, 25), (12, 21), (12, 13), (10, 8), (6, 8), (8, 16)]

VALID_MOVES = {'top_left': (1, 7, 8),
               'top_right': (0, 2, 8),
               'right_upper': (1, 3, 8),
               'right_lower': (2, 4, 8),
               'bottom_right': (3, 5, 8),
               'bottom_left': (4, 6, 8),
               'left_lower': (5, 7, 8),
               'left_upper': (6, 1, 8),
               'center': (0, 1, 2, 3, 4, 5, 6, 7),
               }

STATE = {
    'blue_select': 1,
    'blue_move': 2,
    'green_select': 3,
    'green_move': 4,
}

GREEN = pygame.color.THECOLORS['green']
BLUE = pygame.color.THECOLORS['blue']
WHITE = pygame.color.THECOLORS['white']
BLACK = pygame.color.THECOLORS['black']

COLOR_NAME = {
    GREEN: 'green',
    BLUE: 'blue',
}

COLOR_VALUE = {
    'green': GREEN,
    'blue': BLUE,
}

TXT_COLOR = {
    BLUE: 'B',
    GREEN: 'G',
}

stars = dict(center=(345, 355),
             top_left=(20, 217),
             top_right=(213, 19),
             right_upper=(483, 22),
             right_lower=(666, 217),
             bottom_right=(666, 493),
             bottom_left=(474, 684),
             left_lower=(205, 681),
             left_upper=(18, 491),
            )

winners = [(stars['top_left'], stars['center'], stars['bottom_right']),
           (stars['top_right'], stars['center'], stars['bottom_left']),
           (stars['right_upper'], stars['center'], stars['left_lower']),
           (stars['right_lower'], stars['center'], stars['left_upper']),
           ]

ring = SLOTS[:-1]

ring_pos = [stars[i] for i in ring]

tokens = [
    ('blue', (35, 40)),
    ('blue', (35, 100)),
    ('blue', (35, 160)),
    ('green', (660, 40)),
    ('green', (660, 100)),
    ('green', (660, 160)),
]

HOME = {
    BLUE: ((35, 40),
           (35, 100),
           (35, 160),),
    GREEN: ((660, 40),
            (660, 100),
            (660, 160),),
}

