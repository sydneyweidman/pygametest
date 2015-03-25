import optparse
import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN
from pygame.locals import K_n, K_q, K_r, K_p
from pygame.locals import K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8
from mapdata import stars, ring, tokens, winners, BLUE, GREEN, BLACK, WHITE, COLOR_VALUE, STATE, ASCII_GRID
from mapdata import LEGEND, SLOTS, BOARD, SLOT_IDX, VALID_MOVES, GRID, TXT_COLOR, COLOR_NAME

class IllegalMove(Exception):
    pass

USAGE="""%(prog)s [OPTIONS]

Play the Stars strategy game
"""

parser = optparse.OptionParser(usage=USAGE)
parser.add_option('-m', '--mode', help="Run game in MODE", default='text')

H = 800
W = 690
H_BGND = 710
H_MSG = 9

TOKEN_SIZE = 40
TOKEN_COUNT = 3
SLOT_SIZE = 20
FONT_SIZE = 32

NUMKEYS = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8]

class BaseSlot(object):

    def __init__(self, top=0, left=0, index=-1, content='*', width=SLOT_SIZE, height=SLOT_SIZE,
                 nextslot=None, prevslot=None, ctrslot=None, token=None, name=None):
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.name = name
        self.index = index
        self.content = content
        self.nextslot = nextslot
        self.prevslot = prevslot
        self.ctrslot = ctrslot
        self._token = token

    def __str__(self):
        return self.content

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token
        self.content = "%s%s" % (TXT_COLOR[token.color], self.index)

    def is_empty(self):
        if self.content not in ['B', 'G']:
            return True
        else:
            return False

    def valid_content(self):
        if self.content in LEGEND:
            return True
        else:
            return False

    @property
    def token(self):
        return self._token


    @token.setter
    def token(self, token):
        self._token = token
        self.content = TXT_COLOR[token.color]


    def is_empty(self):
        if self.content not in ['B', 'G']:
            return True
        else:
            return False


    def valid_content(self):
        if self.content in LEGEND:
            return True
        else:
            return False


class Slot(pygame.Rect, BaseSlot):

    def __init__(self, top=0, left=0, index=-1, content='*', width=SLOT_SIZE, height=SLOT_SIZE,
                 nextslot=None, prevslot=None, ctrslot=None, token=None):
        pygame.Rect.__init__(self, top, left, width, height)
        BaseSlot.__init__(self, top, left, index, content, width, height, nextslot, prevslot,
                          ctrslot, token)

class Board(object):
    """a collection of spaces through which a token can move"""

    def __init__(self):
        self.slots = []
        self._setup_slots()
        self.array = []
        for v in GRID.splitlines():
            row = list(v)
            self.array.append(row)

    def get_text_cell(self, cell):
        return self.array[cell[0]][cell[1]]

    def set_text_cell(self, cell, value):
        # if value not in LEGEND:
        #     raise ValueError("Wrong value for text cell")
        self.array[cell[0]][cell[1]] = value

    def display_text(self):
        tmp = []
        s = ''
        for l in self.array:
            c = s.join(l)
            tmp.append(c)
        self.msg('\n'.join(tmp))

    def _setup_slots(self):
        center = Slot(*stars['center'],
                      index=SLOT_IDX['center'],
                      content=str(SLOT_IDX['center']))
        self.slots.append(center)
        for s in ring:
            self.slots.append(Slot(*stars[s], index=SLOT_IDX[s], content=str(SLOT_IDX[s])))
        for idx, slot in enumerate(self.slots):
            slot.nextslot = self.slots[(idx + 1) % len(self.slots)]
            slot.prevslot = self.slots[(idx - 1) % len(self.slots)]
            slot.ctrslot = center

class TextMenuItem(object):

    def __init__(self, label, accel, callback):
        self.label = label
        self.accel = accel
        self.callable = callback

    def activate(self, *args, **kwargs):
        self.callback(*args, **kwargs)

    def display(self):
        print "%s: %s" % (self.accel, self.label,)

class TextMenu(object):

    def __init__(self, title, menu_items):
        self.title = title
        self.do = {}
        self.menu_items = menu_items
        for mi in self.menu_items:
            self.do[mi.accel.upper()] = mi.callable

    def display(self):
        print self.title
        for mi in self.menu_items:
            mi.display()
        choice = raw_input("Choice? ").upper()
        if choice not in [mi.accel for mi in self.menu_items]:
            print "Invalid choice"
        else:
            return choice


class BaseToken(object):

    def __init__(self, color, slot=None, name=None):
        self.color = color
        self.slot = slot
        self.name = name
        self.selectable = False
        self._selected = False

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

    def move(self, to_slot):
        """Move the peg to a new position.
        """
        self.pos = to_slot
        self.rect = to_slot
        self.slot = to_slot

    def draw(self):
        return TXT_COLOR[self.color]

class Token(pygame.sprite.Sprite, BaseToken):
    """A peg in the board. 3 Tokens are placed on the board at the beginning of the game.
    """
    radius = int(TOKEN_SIZE / 2.0)

    def __init__(self, screen, color, pos):
        """
        """
        pygame.sprite.Sprite.__init__(self)
        BaseToken.__init__(self, color, pos)
        self.image = pygame.Surface((TOKEN_SIZE, TOKEN_SIZE))
        self.screen = screen
        self.pos = pos
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
        pygame.font.init()
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


class BaseGame(Board):

    def __init__(self, mode=(W, H)):
        super(BaseGame, self).__init__()
        self.tokens = {}
        self.current_color = BLUE
        self.tokens[GREEN] = [BaseToken(GREEN) for i in range(TOKEN_COUNT)]
        self.tokens[BLUE] = [BaseToken(BLUE) for i in range(TOKEN_COUNT)]
        self.state = STATE['blue_select']
        self.active_token = None
        self.msg = __builtins__['print']

    def homes_empty(self):
        for t in self.tokens:
            if t.pos in [i[1] for i in tokens]:
                return False
        return True

    def select_token(self, idx=None):
        """Put token in the selected state"""
        if self.active_token:
            self.msg("You have already selected a token. Press M to move")
            return
        token = self.get_token_at(idx)
        if not token:
            token = self.tokens[self.current_color].pop()
        if (self.state == STATE['blue_select'] and token.color == BLUE) or \
                (self.state == STATE['green_select'] and token.color == GREEN):
            token.selected = True
            self.active_token = token
        else:
            self.msg("Wrong token. Try again. It is %s's turn" % (COLOR_NAME[self.current_color].upper(),))

    def get_token_at(self, idx):
        for s in self.slots:
            if s.index == idx:
                return s.token
        return None

    def move_token(self, slot=None):
        self.display_text()
        while not slot:
            idx = raw_input('To which location? ')
            try:
                slot = self.slots[int(idx)]
            except (IndexError, ValueError):
                self.msg("You can't move to that space.")

        if self.active_token:
            src = getattr(self.active_token, 'slot', 'home')
            self.msg("Moving from %s to %s " % (src, slot))
            self.active_token.move(slot)
            self.active_token.slot = slot
            self.set_text_cell(slot, self.active_token.name)
            slot.token = self.active_token
            self.active_token = None
            self.switch_turn()
        else:
            self.msg("Please select a token first")

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


class Game(BaseGame):
    """A game board
    """

    def __init__(self, mode=(W, H)):
        """Create and initialize the game board
        """
        super(Game, self).__init__()
        self.screen = pygame.display.set_mode(mode)
        self.background = pygame.image.load('images/board.png').convert()
        self.messages = MessageArea(H_BGND, 0, 90, W, "BLUE'S TURN")
        self.msg = self.messages.display
        self.screen.blit(self.messages, (0, self.messages.top))
        pygame.display.flip()
        self.tokens = pygame.sprite.LayeredUpdates()
        self.current_color = BLUE
        self._setup_tokens()
        self.active_token = self.tokens.get_sprite(0)
        self.current_slot = self.slots[0]
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

    def select_token(self, token):
        """Put token in the selected state"""
        if (self.state == STATE['blue_select'] and token.color == BLUE) or \
                (self.state == STATE['green_select'] and token.color == GREEN):
            token.selected = True
            self.active_token = token
        else:
            self.msg("Wrong token. Try again. It is %s's turn" % (COLOR_NAME[self.current_color].upper(),))

    def on_key_down(self, event):
        """Handle keyboard events"""
        if event.key == K_r:
            self.msg("Restarting")
            self.__init__()
            self.screen.blit(self.background, (0,0))
        if event.key in NUMKEYS:
            print "Not implemented"
            return
        if event.key == K_n:
            print "Not implemented"
            return
        if event.key == K_p:
            print "Not implemented"
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
            if not self.homes_empty() and hits[0].rect.collidelist(self.slots) != -1:
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
                hit = s.collidelist(self.slots)
                if hit != -1:
                    self.active_token.selected = False
                    self.active_token.move((self.slots[hit].x, self.slots[hit].y))
                    self.switch_turn()
        return

    def on_quit(self):
        pygame.quit()
        sys.exit()

def text_main_loop():

    game = BaseGame()
    move = TextMenuItem('Move', 'M', game.move_token)
    select = TextMenuItem('Select', 'S', game.select_token)
    display = TextMenuItem('Display board', 'D', game.display_text)
    quit = TextMenuItem('Quit', 'Q', sys.exit)
    main_menu = TextMenu("Stars Main Menu", [display, select, move, quit])
    while True:
        choice = main_menu.display()
        game.msg("Chose %s" % (choice,))
        try:
            main_menu.do[choice]()
        except KeyError:
            game.msg("Invalid choice. Try again.")

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
    if opts.mode == 'text':
        text_main_loop()
    sys.exit(main(*cli_args, **opts.__dict__))
