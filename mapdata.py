import pygame

LEGEND = {'*': 'Unoccupied',
          'B': 'Blue',
          'G': 'Green'}
SLOTS = ('top_left', 'top_right', 'right_upper', 'right_lower',
         'bottom_right', 'bottom_left', 'left_lower', 'left_upper',
         'center',)

GRID = """+-----------------+
|     *     *     |
|                 |
| *             * |
|        *        |
| *             * |
|                 |
|     *     *     |
+-----------------+"""

BOARD = []
for i in SLOTS:
    BOARD.append([i,'*'])

SLOT_IDX = dict(top_left=0, top_right=1, right_upper=2, right_lower=3, bottom_right=4, bottom_left=5, left_lower=6,
                left_upper=7, center=8)

# Slot location on 9 x 9 ascii grid separated by spaces and newlines
ASCII_GRID = [(1, 6),(1, 12),(3, 2),(3, 16),(4, 9),(5, 2),(5, 16),(7, 6),(7, 12),]

VALID_MOVES = {'top_left':    (1, 7, 8),
               'top_right':   (0, 2, 8),
               'right_upper': (1, 3, 8),
               'right_lower': (2, 4, 8),
               'bottom_right':(3, 5, 8),
               'bottom_left': (4, 6, 8),
               'left_lower':  (5, 7, 8),
               'left_upper':  (6, 1, 8),
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
    BLUE:  'blue',
}

COLOR_VALUE = {
    'green': GREEN,
    'blue':  BLUE,
}

stars = {
    'center': (345, 355),
    'one':    ( 20, 217),
    'two':    (213,  19),
    'three':  (483,  22),
    'four':   (666, 217),
    'five':   (666, 493),
    'six':    (474, 684),
    'seven':  (205, 681),
    'eight':  ( 18, 491),
}

winners = [(stars['one'], stars['center'], stars['five']),
           (stars['two'], stars['center'], stars['six']),
           (stars['three'], stars['center'], stars['seven']),
           (stars['four'], stars['center'], stars['eight']),
           ]

ring = 'one two three four five six seven eight'.split()

ring_pos =[(20, 217), 
          (213, 19), 
          (483, 22), 
          (666, 217),
          (666, 493),
          (474, 684),
          (205, 681),
          ( 18, 491),]

tokens = [
    ('blue', (35,40)),
    ('blue', (35, 100)),
    ('blue', (35, 160)),
    ('green',(660, 40)),
    ('green',(660, 100)),
    ('green',(660, 160)),
    ]

HOME = {
    BLUE: ((35, 40),
           (35, 100),
           (35, 160),),
    GREEN: ((660, 40),
            (660, 100),
            (660, 160),),
}

