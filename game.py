import optparse
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN
from pygame.locals import K_n, K_q, K_s, K_p
from mapdata import HOME, stars, BLUE, GREEN

parser = optparse.OptionParser()

WINDOW = pygame.Rect(0, 0, 690, 710)

class Slot(pygame.Rect):

    def __init__(self, stype, top, left, width=40, height=40, nextslot=None, prevslot=None, ctrslot=None, token=None):
        super(Slot, self).__init__((top, left, width, height))
        self.stype = stype
        self.nextslot = nextslot
        self.prevslot = prevslot
        self.ctrslot = ctrslot
        self.token = token

class GameBoard(object):
    """A game board
    """

    def __init__(self, mode=(690,710)):
        """Create and initialize the game board
        """
        self.screen = pygame.display.set_mode(mode)
        self.background = pygame.image.load('images/board.png').convert()
        self.slots = []
        self.tokens = {}
        self._setup_slots()
        self._setup_tokens()
        self.current_color = BLUE
        self.active_token = self.tokens[self.current_color].sprites()[0]
        self.active_token.selected = True
        self.current_slot = self.slots[0]
        
    def _setup_slots(self):
        for s in stars:
            if s != 'center':
                self.slots.append(Slot('ring', *stars[s][0]))
            else:
                self.slots.append(Slot('center', *stars['center'][0]))
        for idx, slot in enumerate(self.slots):
            slot.nextslot = self.slots[(idx + 1) % 8]
            slot.prevslot = self.slots[(idx - 1) % 8]

    def _setup_tokens(self):
        # set up tokens
        for color in HOME:
            self.tokens[color] = pygame.sprite.Group()
            for tokenpos in HOME[color]:
                token = Token(self.screen, color, tokenpos)
                self.tokens[color].add(token)

    def onKeyDown(self, event):
        """Handle keyboard events"""
        if event.key == K_s:
            print "Starting game"
            return
        if event.key == K_n:
            if self.current_slot.nextslot.token:
                print "That space is occupied"
                return
            self.current_slot = self.current_slot.nextslot
            self.screen.blit(self.background, (0,0))
            self.active_token.move((self.current_slot.x, self.current_slot.y))
            self.active_token.draw()
            return
        if event.key == K_p:
            if self.current_slot.prevslot.token:
                print "That space is occupied"
                return
            self.current_slot = self.current_slot.prevslot
            self.screen.blit(self.background, (0,0))
            self.active_token.move((self.current_slot.x, self.current_slot.y))
            self.active_token.draw()
            return
        if event.key == K_q:
            self.onQuit(event)
            
    def onMouseButtonDown(self, event):
        """Handle mouse events"""
        print "Click: %s" % (event.pos,)
        # if a token has been selected previously, move it to the destination of the click
        # as long as the spot is not occupied
        if self.active_token:
            if self.active_token.selected:
                self.active_token.selected = False
            for slot in self.slots:
                print "Slot %s" % slot
                if slot.collidepoint(event.pos):
                    print "Hit slot"
                    if slot.token:
                        print "That space is occupied"
                        return
                    self.active_token.move((slot.x, slot.y))
                    slot.token = self.active_token
                    self.active_token.selected = False
                    self.active_token = None
                    break
        else:
            for color in HOME:
                for token in self.tokens[color]:
                    if token.rect.collidepoint(event.pos):
                        print "hit"
                        self.active_token = token
                        token.selected = True
        return

    def onQuit(self, event):
        sys.exit()
        
class Token(pygame.sprite.Sprite):
    """A peg in the board. 3 Tokens are placed on the board at the beginning of the game.
    """
    radius = 20

    def __init__(self, screen, color, pos):
        """
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.screen = screen
        self.pos = pos
        self.color = color
        self.selected = False
        self.rect = pygame.draw.circle(self.screen, self.color, self.pos, self.radius, 0)
        self.image.fill((255,255,255,255))

    def _draw(self):
        self.rect = pygame.draw.circle(self.screen, self.color, self.pos, self.radius, 0)
        if self.selected:
            self.image.fill((0, 0, 0, 0))
        else:
            self.image.fill((255, 255, 255, 255))

    def draw(self):
        self._draw()

    def update(self):
        self._draw()

    def move(self, to_slot):
        """Move the peg to a new position.
        """
        self.pos = to_slot
        self.rect = to_slot


def main(*args, **kwargs):
    """Start the main loop

    Arguments:
    - `*args`:
    - `**kwargs`:
    """
    print kwargs
    pygame.init()
    game = GameBoard()
    active_token = None
    screen = game.screen
    screen.blit(game.background, (0,0))
    slot = game.slots[0]
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                game.onKeyDown(event)
            if event.type == MOUSEBUTTONDOWN:
                game.onMouseButtonDown(event)
            if event.type == QUIT:
                game.onQuit(event)
        for color in HOME:
            game.tokens[color].clear(game.screen, game.background)
            game.tokens[color].draw(game.screen)
            game.tokens[color].update()
        pygame.display.update()
        pygame.time.delay(100)

if __name__ == '__main__':
    (opts, args) = parser.parse_args()
    sys.exit(main(*args, **opts.__dict__))
