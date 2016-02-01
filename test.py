__author__ = 'sweidman'

import unittest
import mapdata
from game import Game, Slot, Token

class TestTextToken(unittest.TestCase):

    def setUp(self):
        clr = mapdata.BLUE
        self.game = Game()
        self.slot = Slot()
        self.token = Token(self.game.screen, clr, mapdata.HOME[clr][0])

    def test_draw(self):
        assert self.token.draw() == 'B'

    def test_set_slot(self):
        self.slot.token = self.token
        assert self.slot.content == 'B'

    def tearDown(self):
        pass


class TestSlot(unittest.TestCase):

    def setUp(self):
        self.slot = Slot()

    def test_slot_empty(self):
        assert self.slot.is_empty()

    def test_slot_not_empty(self):
        self.slot.content = 'B'
        assert not self.slot.is_empty()

class TestTextMenu(unittest.TestCase):

    def setUp(self):
        test.menu = TextMenu()

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_board_initial_state(self):
        for i in self.game.slots:
            assert i.is_empty()

if __name__ == '__main__':
    unittest.main()
