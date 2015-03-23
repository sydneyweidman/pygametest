__author__ = 'sweidman'

import unittest
import mapdata
from game import Game, Slot, BaseToken

class TestTextToken(unittest.TestCase):

    def setUp(self):
        self.slot = Slot(index=9)
        self.token = BaseToken(mapdata.BLUE)

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

    def test_set_text_cell(self):
        self.game.set_text_cell((1,6),'B')
        assert self.game.array[1][6] == 'B'

    def test_ascii_grid(self):
        for cell in mapdata.ASCII_GRID:
            assert self.game.get_text_cell(cell) in mapdata.LEGEND

if __name__ == '__main__':
    unittest.main()
