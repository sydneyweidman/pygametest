import pygame

STATE = {'start':  0,
         'setup':  1,
         'battle': 2,
         'end':    3,
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

