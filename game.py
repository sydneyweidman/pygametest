import optparse
import random
import sys

import pygame
from pygame import Rect
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, K_n, K_q, K_s

import mapdata

parser = optparse.OptionParser()
parser.add_option('-n', '--name', default=[], action='append')
parser.add_option('-c', '--color', default=[], action='append')

class Player(object):

    def __init__(self, screen, name, color):
        """Create a player
        
        Arguments:
        - `name`: The player's name'
        - `color`: The player's color'
        """
        self.screen = screen
        self.name = name
        self.color = color
        self.pegs = []
        for p in mapdata.HOME[color]:
            self.pegs.append(GamePeg(color, p))

    def nextpeg(self):
        for p in self.pegs:
            yield p

    def roll(self):
        """Roll the die
        """
        return random.randint(1,6)

    def move(self, peg, value):
        peg.move(value)
    
class GameBoard(object):
    """A game board
    """
    bubble = Rect(290,200,100,100)

    max_players = 4

    def __init__(self, mode=(640,480)):
        """Create and initialize the game board
        """
        self.screen = pygame.display.set_mode(mode)
        self.background = pygame.image.load('images/bgnd.bmp').convert()
        self.started = False
        self.players = []
        self.player_count = 0
        self.whose_turn = 0
        self.colors_in_use = []
        self.number_rolled = None
        
    def take_turn(self):
        """Process a player's turn
        """
        if not self.started:
            self.started = True
        self.whose_turn += 1
        if self.whose_turn >= self.player_count:
            self.whose_turn = 0
        player = self.players[self.whose_turn]
        self.number_rolled = player.roll()
        return self.number_rolled
    
    def add_player(self, name, color):
        """Add a player to the game
        
        Arguments:
        - `name`: Player's name'
        - `color`: One of mapdata.RED, mapdata.BLUE, mapdata.GREEN, mapdata.YELLOW
        """
        # Check that name and color are unique
        for p in self.players:
            if name == p.name:
                raise ValueError("The name %s is already in use" % (name,))
            if color == p.color:
                raise ValueError("The color %s is already taken by %s" % (mapdata.COLOR_NAME[color], p.name))
        if len(self.players) >= self.max_players:
            raise ValueError("No more than %s players can join" % self.max_players)
        player = Player(self.screen, name, color)
        self.players.append(player)
        self.player_count += 1
        return player

class GamePeg(pygame.sprite.Sprite):
    """A peg in the board. There can be 0 - 4 in play at any given time.
    """
    radius = 10
    
    def __init__(self, color, pos):
        """
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((24,24))
        self.pos = pos
        self.color = color
        self.image.fill(self.color)
        self.rect = pygame.draw.circle(self.image, self.color, self.pos, self.radius, 0)
        
    def draw(self, screen):
        screen.blit(self.image,(0,0))
        self.rect = pygame.draw.circle(screen, self.color, self.pos, self.radius, 0)

    def update(self, screen):
        screen.blit(self.image, (0,0))
        self.rect = pygame.draw.circle(self.image, self.color, self.pos, self.radius, 0)
        
    def move(self, newpos):
        """Move the peg to a new position.
        """
        self.pos = newpos
        
def main(*args, **kwargs):
    """Start the main loop
    
    Arguments:
    - `*args`:
    - `**kwargs`:
    """
    print kwargs
    pygame.init()
    game = GameBoard()
    screen = game.screen
    screen.blit(game.background, (0,0))
    if 'name' in kwargs:
        for idx, n in enumerate(kwargs['name']):
            color = mapdata.COLOR_VALUE[kwargs['color'][idx]]
            game.add_player(n,color)
    pegpos = 0
    pegobj = GamePeg(color, mapdata.HOME[color][0])
    allpegs = pygame.sprite.Group(pegobj)
    for p in game.players:
        for pg in p.pegs:
            allpegs.add(pg)
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_s:
                print "Starting game"
                for player in game.players:
                    print "%s is %s" % (player.name, mapdata.COLOR_NAME[player.color],)
                print "It is %s's turn" % (game.players[game.whose_turn].name,)
                print "Click the bubble to start your turn"
                continue
            if event.type == KEYDOWN and event.key == K_n:
                screen.blit(game.background, (0,0))
                try:
                    peg = mapdata.COURSE[color][pegpos]
                except IndexError:
                    pegpos = 0
                    peg = mapdata.COURSE[color][pegpos]
                print peg
                pegobj.move(peg)
                pegpos += 1
                continue
            if event.type == MOUSEBUTTONDOWN:
                print event.pos
                if game.bubble.collidepoint(event.pos):
                    roll = game.take_turn()
                    player = game.players[game.whose_turn]
                    print "%s rolled %s" % (player.name, roll,)
                    if roll == 6:
                        p = player.nextpeg().next()
                        p.move(mapdata.COURSE[player.color][0])
                        print "Click again, %s" % (player.name,)
                    else:
                        pass
                continue
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                sys.exit()
        allpegs.clear(game.screen, game.background)
        allpegs.draw(game.screen)
        allpegs.update(game.screen)
        pygame.display.update()
        pygame.time.delay(100)

if __name__ == '__main__':
    (opts, args) = parser.parse_args()
    sys.exit(main(*args, **opts.__dict__))
