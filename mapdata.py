import pygame

SLOTS = ('top_left', 'top_right', 'right_upper', 'right_lower',
         'bottom_right', 'bottom_left', 'left_lower', 'left_upper',
         'center',)

SLOT_IDX = dict(top_left=0, top_right=1, right_upper=2, right_lower=3, bottom_right=4, bottom_left=5, left_lower=6,
                left_upper=7, center=8)

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

HOME = {
    BLUE: ((35, 40),
           (35, 100),
           (35, 160),),
    GREEN: ((660, 40),
            (660, 100),
            (660, 160),),
}

COLOR_NAME = {
    GREEN: 'green',
    BLUE: 'blue',
}

COLOR_VALUE = {
    'green': GREEN,
    'blue': BLUE,
}

COLOR_CHAR = {
    BLUE: 'B',
    GREEN: 'G',
}

