import pygame
from pygame.locals import *

RED = pygame.color.THECOLORS['red']
GREEN = pygame.color.THECOLORS['green']
BLUE = pygame.color.THECOLORS['blue']
YELLOW = pygame.color.THECOLORS['yellow']

COLOR_NAME = {
    RED:  'red',
    GREEN: 'green',
    BLUE:  'blue',
    YELLOW: 'yellow',
}

COLOR_VALUE = {
    'red':   RED,
    'green': GREEN,
    'blue':  BLUE,
    'yellow':YELLOW,
}
    
HOME = {
    BLUE: ((116, 108),
           (134, 78),
           (159, 51),
           (192, 31),),
    GREEN: ((473, 34),
            (502, 57),
            (527, 81),
            (544, 113),),
    YELLOW:((541, 389),
            (522, 420),
            (496, 445),
            (465, 464),),
    RED:   ((192, 464),
            (160, 442),
            (134, 418),
            (117, 387),),
}
    
FINISH = {
    BLUE:  ((189, 108),
            (217, 135),
            (243, 159),
            (271, 185),),
    GREEN: ((473, 110),
            (446, 138),
            (420, 163),
            (395, 189),),
    YELLOW:((472, 390),
            (444, 366),
            (422, 342),
            (393, 316),),
    RED:   ((190, 390),
            (217, 364),
            (242, 340),
            (267, 316),),
}

PATH = (
    (191, 71),
    (235, 45),
    (281, 38),
    (334, 41),
    (382, 41),
    (427, 51),
    (472, 74),
    (507, 115),
    (533, 158),
    (543, 200),
    (537, 254),
    (539, 300),
    (524, 344),
    (502, 390),
    (466, 427),
    (423, 448),
    (378, 458),
    (327, 457),
    (282, 456),
    (231, 447),
    (191, 426),
    (155, 387),
    (132, 344),
    (121, 297),
    (122, 250),
    (122, 198),
    (130, 151),
    (153, 109),
)

COURSE = {
    BLUE:    PATH[0:28] + FINISH[BLUE],
    GREEN:   PATH[7:28] + PATH[0:7] + FINISH[GREEN],
    YELLOW:  PATH[14:28] + PATH[0:14] + FINISH[YELLOW],
    RED:     PATH[21:28] + PATH[0:21] + FINISH[RED],
}
