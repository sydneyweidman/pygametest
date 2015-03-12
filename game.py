import optparse
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN
from pygame.locals import K_n, K_q, K_r, K_s, K_p, K_ESCAPE
from pygame.locals import K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8
from mapdata import stars, ring, tokens, BLUE, GREEN, BLACK, WHITE, COLOR_VALUE, STATE

parser = optparse.OptionParser()

H = 800
W = 690
H_BGND = 710
H_MSG = 90

TOKEN_SIZE = 40
SLOT_SIZE = 20
FONT_SIZE = 32

NUMKEYS = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8]


class Slot(pygame.Rect):
    def __init__(self, top, left, width=SLOT_SIZE, height=SLOT_SIZE,
                 nextslot=None, prevslot=None, ctrslot=None, token=None):
        super(Slot, self).__init__((top, left, width, height))
        self.nextslot = nextslot
        self.prevslot = prevslot
        self.ctrslot = ctrslot
        self.token = token


class Board(object):
    """a collection of spaces through which a token can move"""

    def __init__(self):
        self.slots = []
        self._setup_slots()

    def _setup_slots(self):
        center = Slot(*stars['center'])
        self.slots.append(center)
        for s in ring:
            self.slots.append(Slot(*stars[s]))
        for idx, slot in enumerate(self.slots):
            slot.nextslot = self.slots[(idx + 1) % len(self.slots)]
            slot.prevslot = self.slots[(idx - 1) % len(self.slots)]
            slot.ctrslot = center


class Token(pygame.sprite.Sprite):
    """A peg in the board. 3 Tokens are placed on the board at the beginning of the game.
    """
    radius = int(TOKEN_SIZE / 2.0)

    def __init__(self, screen, color, pos):
        """
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TOKEN_SIZE, TOKEN_SIZE))
        self.screen = screen
        self.pos = pos
        self.color = color
        self.selected = False
        self.rect = pygame.draw.circle(self.screen, self.color, self.pos, self.radius, 0)
        self.screen.blit(self.image, self.rect)

    def _draw(self):
        if self.selected:
            self.image.fill(BLACK)
        else:
            self.image.fill(WHITE)
        self.rect = pygame.draw.circle(self.screen, self.color, self.pos, self.radius, 0)

    def draw(self):
        self._draw()

    def update(self):
        self._draw()

    def move(self, to_slot):
        """Move the peg to a new position.
        """
        self.pos = to_slot
        self.rect = to_slot


class Game(object):
    """A game board
    """

    def __init__(self, mode=(W, H)):
        """Create and initialize the game board
        """
        self.screen = pygame.display.set_mode(mode)
        self.background = pygame.image.load('images/board.png').convert()
        self.tokens = {}
        self.board = Board()
        self.state = STATE['start']
        self._setup_messagebar()
        self.tokens = pygame.sprite.LayeredUpdates()
        self._setup_tokens()
        self.active_token = self.tokens.get_sprite(0)
        self.current_slot = self.board.slots[0]
        self.current_color = BLUE
        self.active_token.selected = True

    def _setup_messagebar(self):
        self.msgsrc = pygame.font.SysFont(None, FONT_SIZE)
        self.msgdest = pygame.Surface((W, H_MSG))
        self.msgdest.fill(WHITE)
        self.surf = self.msgsrc.render("START", True, BLACK)
        self.msgdest.blit(self.surf, (10, 0))
        self.screen.blit(self.msgdest, (0, H_BGND))

    def _setup_tokens(self):
        # set up tokens
        for t in tokens:
            token = Token(self.screen, COLOR_VALUE[t[0]], t[1])
            self.tokens.add(token)

    def msg(self, text):
        print text
        self.msgdest.fill(WHITE)
        s = self.msgsrc.render(text, True, BLACK)
        self.msgdest.blit(s, (0, 0))
        self.screen.blit(self.msgdest, (0, H_BGND))
        pygame.display.flip()

    def token_select(self, token):
        """Put token in the selected state"""
        token.selected = True

    def token_move(self, token, to_slot):
        """Move token to to_slot"""
        token.move(to_slot)

    def on_key_down(self, event):
        """Handle keyboard events"""
        if event.key == K_r:
            self.msg("Restarting")
            self.__init__()

        if event.key == K_s:
            self.msg("Starting game")
            return
        if event.key in NUMKEYS:
            to_slot = self.board.slots[NUMKEYS.index(event.key)]
            tlist = [i for i in self.tokens.sprites() if i.color == self.current_color]
            if to_slot.collidelist(tlist) != -1:
                self.msg("That space is occupied")
                return
            self.active_token.move((to_slot.x, to_slot.y))
            self.active_token.draw()
            return
        if event.key == K_n:
            if self.current_slot.nextslot.token:
                self.msg("That space is occupied")
                return
            self.current_slot = self.current_slot.nextslot
            self.screen.blit(self.background, (0, 0))
            self.active_token.move((self.current_slot.x, self.current_slot.y))
            self.active_token.draw()
            return
        if event.key == K_p:
            if self.current_slot.prevslot.token:
                self.msg("That space is occupied")
                return
            self.current_slot = self.current_slot.prevslot
            self.screen.blit(self.background, (0, 0))
            self.active_token.move((self.current_slot.x, self.current_slot.y))
            self.active_token.draw()
            return
        if event.key == K_ESCAPE:
            self.active_token.selected = False
        if event.key == K_q:
            self.on_quit()

    def on_mousebutton_down(self, event):
        """Handle mouse events"""
        print "Click: %s" % (event.pos,)
        # if a token has been selected previously, move it to the destination of the click
        # as long as the spot is not occupied
        hits = self.tokens.get_sprites_at(event.pos)
        if self.active_token.selected:
            if len(hits) == 1:
                if hits[0] is self.active_token:
                    self.msg("To deselect a token, press the ESCAPE key")
                    return
                else:
                    self.msg("That space is occupied")
                    return
            elif len(hits) == 0:
                s = pygame.Rect((event.pos[0], event.pos[1], 20, 20))
                hit = s.collidelist(self.board.slots)
                if hit != -1:
                    self.active_token.selected = False
                    self.active_token.move((self.board.slots[hit].x, self.board.slots[hit].y))
                    if self.current_color == BLUE:
                        self.current_color = GREEN
                    else:
                        self.current_color = BLUE
        else:
            if len(hits) == 1:
                self.active_token = hits[0]
                self.active_token.selected = True
        return

    def on_quit(self):
        sys.exit()


def main(*args, **kwargs):
    """Start the main loop

    Arguments:
    - `*args`:
    - `**kwargs`:
    """
    pygame.init()
    game = Game()
    screen = game.screen
    screen.blit(game.background, (0, 0))
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                game.on_key_down(event)
            if event.type == MOUSEBUTTONDOWN:
                game.on_mousebutton_down(event)
            if event.type == QUIT:
                game.on_quit()
        game.tokens.clear(game.screen, game.background)
        game.tokens.draw(game.screen)
        game.tokens.update()
        pygame.display.flip()
        pygame.time.delay(100)


if __name__ == '__main__':
    (opts, cli_args) = parser.parse_args()
    sys.exit(main(*cli_args, **opts.__dict__))
