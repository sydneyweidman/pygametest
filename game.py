import time
import optparse
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN
from pygame.locals import K_n, K_q, K_r, K_p
from pygame.locals import K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8
from mapdata import stars, ring, tokens, winners, BLUE, GREEN, BLACK, WHITE, COLOR_VALUE, STATE

parser = optparse.OptionParser()

H = 800
W = 690
H_BGND = 710
H_MSG = 9

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
        self.selectable = False
        self._selected = False
        self.rect = pygame.draw.circle(self.screen, self.color, self.pos, self.radius, 0)
        self.screen.blit(self.image, self.rect)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        if type(value) == bool:
            self._selected = value
        else:
            raise ValueError("The selected property must be True or False")
        if self.selectable and value == True:
            self._selected = True

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


class MessageArea(pygame.Surface):

    def __init__(self, top, left, height, width, initial_text=None, margin=10,
                 duration=5, fg_color=BLACK, bg_color=WHITE, font_size=FONT_SIZE,
                 font=None):
        self.height = height
        self.top = top
        self.left = left
        self.width = width
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.font_size = font_size
        self.initial_text = initial_text
        self.margin = margin
        self.duration = duration
        self.font = font
        super(MessageArea, self).__init__((self.width, self.height))
        self._setup_messagebar()

    def _setup_messagebar(self):
        self.fill(self.bg_color)
        self.msgsrc = pygame.font.SysFont(self.font, self.font_size)
        self.surf = self.msgsrc.render(self.initial_text, True, self.fg_color)
        self.blit(self.surf, (self.margin, self.left))

    def display(self, text):
        print text
        self.fill(self.bg_color)
        self.surf = self.msgsrc.render(text, True, self.fg_color)
        self.blit(self.surf, (self.margin, self.left))

    def clear(self):
        self.surf.fill(self.bg_color)
        self.fill(self.bg_color)
        self.blit(self.surf, (self.margin, self.left))

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
        self.state = STATE['blue_select']
        self.messages = MessageArea(H_BGND, 0, 90, W, "BLUE'S TURN")
        self.msg = self.messages.display
        self.screen.blit(self.messages, (0, self.messages.top))
        pygame.display.flip()
        self.tokens = pygame.sprite.LayeredUpdates()
        self.current_color = BLUE
        self._setup_tokens()
        self.active_token = self.tokens.get_sprite(0)
        self.current_slot = self.board.slots[0]
        self.active_token.selected = True

    def _setup_tokens(self):
        # set up tokens
        for t in tokens:
            token = Token(self.screen, COLOR_VALUE[t[0]], t[1])
            if token.color == self.current_color:
                token.selectable = True
            else:
                token.selectable = False
            self.tokens.add(token)

    def homes_empty(self):
        for t in self.tokens:
            if t.pos in [i[1] for i in tokens]:
                return False
        return True

    def select_token(self, token):
        """Put token in the selected state"""
        if (self.state == STATE['blue_select'] and token.color == BLUE) or \
            (self.state == STATE['green_select'] and token.color == GREEN):
            token.selected = True
            self.active_token = token
        else:
            self.msg("Wrong token. Try again")

    def check_win(self):
        "Check for a winner. Returns current color if winner is found or None"
        green = [t.pos for t in self.tokens if t.color == GREEN]
        blue = [t.pos for t in self.tokens if t.color == BLUE]
        for trio in winners:
            if set(trio) == set(green):
                return "GREEN"
            elif set(trio) == set(blue):
                return "BLUE"
        return None

    def switch_turn(self):
        winner = self.check_win()
        if winner:
            self.msg("%s WINS!" % (winner,))
            return
        if self.current_color == BLUE:
            self.current_color = GREEN
            c = 'GREEN'
            self.state = STATE['green_select']
        else:
            c = 'BLUE'
            self.current_color = BLUE
            self.state = STATE['blue_select']
        for token in self.tokens:
            token.selected = False
            self.active_token = None
            if token.color == self.current_color:
                self.selectable = True
            else:
                self.selectable = False
        self.msg("%s'S TURN" % (c,))

    # noinspection PyUnreachableCode
    def on_key_down(self, event):
        """Handle keyboard events"""
        if event.key == K_r:
            self.msg("Restarting")
            self.__init__()
            self.screen.blit(self.background, (0,0))
        if event.key in NUMKEYS:
            print "Not implemented"
            return
            to_slot = self.board.slots[NUMKEYS.index(event.key)]
            tlist = [i for i in self.tokens.sprites() if i.color == self.current_color]
            if to_slot.collidelist(tlist) != -1:
                self.msg("That space is occupied")
                return
            self.active_token.move((to_slot.x, to_slot.y))
            self.active_token.draw()
            self.switch_turn()
            return
        if event.key == K_n:
            print "Not implemented"
            return
            if self.current_slot.nextslot.token:
                self.msg("That space is occupied")
                return
            self.current_slot = self.current_slot.nextslot
            self.screen.blit(self.background, (0, 0))
            self.active_token.move((self.current_slot.x, self.current_slot.y))
            self.active_token.draw()
            return
        if event.key == K_p:
            print "Not implemented"
            return
            if self.current_slot.prevslot.token:
                self.msg("That space is occupied")
                return
            self.current_slot = self.current_slot.prevslot
            self.screen.blit(self.background, (0, 0))
            self.active_token.move((self.current_slot.x, self.current_slot.y))
            self.active_token.draw()
            return
        if event.key == K_q:
            self.on_quit()

    def on_mousebutton_down(self, event):
        """Handle mouse events"""
        print "Click: %s" % (event.pos,)
        # MOVE TOKEN
        # if a token has been selected previously, move it to the destination of the click
        # as long as the spot is not occupied
        hits = self.tokens.get_sprites_at(event.pos)
        if len(hits) == 1 and self.active_token is None:
            if not self.homes_empty() and hits[0].rect.collidelist(self.board.slots) != -1:
                self.msg("You must move all of your tokens out of home first")
                return
            self.select_token(hits[0])
            return
        # SELECT TOKEN
        if self.active_token is None:
            self.msg("Please select a token")
            return
        if self.active_token.selected:
            if len(hits) == 1:
                # if we have clicked on the active token
                if hits[0] is self.active_token:
                    return
                else:
                    self.msg("That space is occupied")
                    return
            elif len(hits) == 0:
                # a token is selected and the player must choose a destination
                s = pygame.Rect((event.pos[0], event.pos[1], 20, 20))
                hit = s.collidelist(self.board.slots)
                if hit != -1:
                    self.active_token.selected = False
                    self.active_token.move((self.board.slots[hit].x, self.board.slots[hit].y))
                    self.switch_turn()
        return

    def on_quit(self):
        pygame.quit()
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
        game.screen.blit(game.messages, (0, game.messages.top))
        pygame.display.flip()
        pygame.time.delay(100)


if __name__ == '__main__':
    (opts, cli_args) = parser.parse_args()
    sys.exit(main(*cli_args, **opts.__dict__))
