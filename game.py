import pygame
import sys
import mapdata
import optparse

parser = optparse.OptionParser()
parser.add_option('-n', '--name')
parser.add_option('-c', '--color')

from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, K_a, K_n, K_q

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
            self.pegs.append(GamePeg(self.screen, color, p))
        pygame.display.update()

    def do_move(self, ):
        """Process a player's turn: Roll the dice, wait for move selection'
        """
        pass

class GameBoard(object):
    """A game board
    """

    max_players = 4

    def __init__(self, mode=(640,480)):
        """Create and initialize the game board
        """
        self.screen = pygame.display.set_mode(mode)
        self.background = pygame.image.load('bgnd.bmp').convert()
        self.started = False
        self.players = []
        self.player_count = 0
        self.whose_turn = 0
        self.colors_in_use = []

    def take_turn(self):
        """Process a player's turn
        """
        if not self.started:
            self.started = True
        try:
            player = self.players[self.whose_turn]
            player.do_move()
        except IndexError:
            self.whose_turn = 0
        self.whose_turn += 1
        
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
        self.players.append(Player(self.screen, name, color))
        self.colors_in_use.append(color)
        self.player_count += 1

class GamePeg(object):
    """A peg in the board. There can be 0 - 4 in play at any given time.
    """
    radius = 14
    def __init__(self, screen, color, startpos):
        """
        """
        self.screen = screen
        self.color = color
        self.pos = startpos
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius)
        pygame.display.update()
        
    def move(self, newpos):
        """Move the peg to a new position.
        """
        self.pos = newpos
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius)

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
        name = kwargs['name']
    else:
        name = 'Player 1'
    try:
        color = mapdata.COLOR_VALUE[kwargs['color']]
    except KeyError:
        color = mapdata.BLUE
    pegpos = 0
    pegobj = GamePeg(screen, color, mapdata.HOME[color][0])
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_a:
                # add a player
                name = raw_input('Name: ')
                colorname = raw_input('Choose color (red, yellow, blue, or green): ')
                color = mapdata.COLOR_VALUE[colorname]
                game.add_player(name, color)
                pegobj = GamePeg(screen, color, mapdata.HOME[color][0])
                continue
            if event.type == KEYDOWN and event.key == K_n:
                if not game.players:
                    print "Please add a player first"
                    continue
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
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                sys.exit()
        pygame.display.update()
        pygame.time.delay(100)

if __name__ == '__main__':
    (opts, args) = parser.parse_args()
    sys.exit(main(*args, **opts.__dict__))
