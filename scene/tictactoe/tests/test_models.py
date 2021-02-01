from django.test import TestCase
from ..models import Game, Status, Move
import numpy as np
from ..utils import empty_game_grid


class GameTestCase(TestCase):
    def setUp(self):
        self.game = Game.objects.create()

    def test_type(self):
        self.assertIsInstance(self.game, Game)

    def test_game_initial_vals(self):
        self.assertEqual(self.game.status, Status.INCOMPLETE)
        self.assertEqual(self.game.moves.count(), 0)
        self.assertEqual(self.game.grid, empty_game_grid())


class MoveTestCase(TestCase):
    def setUp(self):
        self.game = Game.objects.create()
        self.move = Move.objects.create(game=self.game)

    def test_type(self):
        self.assertIsInstance(self.move, Move)
