from django.test import TestCase
import ipdb
from .models import Game, Status, Move, Players
import numpy as np
from .utils import default_coords
import json
from django.core.exceptions import ValidationError


class GameTestCase(TestCase):
    def setUp(self):
        self.game = Game.objects.create()

    def test_game_initial_vals(self):
        self.assertEqual(self.game.status, Status.INCOMPLETE)
        self.assertEqual(self.game.move_set.count(), 0)

    def test_game_grid_props(self):
        self.assertIsInstance(self.game.grid_array, np.ndarray)


class MoveTestCase(TestCase):
    def setUp(self):
        self.game = Game.objects.create()
        self.move = Move.objects.create(game=self.game)

    def test_move_default_props(self):
        self.assertEqual(self.move.game, self.game)
        self.assertEqual(self.move.player, Players.NOUGHTS)
        self.assertEqual(self.move.coords, default_coords())

    def test_move_set_get(self):
        coord_array = np.array([1, 1])
        coord_dict = {"coord": coord_array.tolist()}
        coord_json = json.dumps(coord_dict)
        move = Move.objects.create(game=self.game, coords=coord_json)
        np.testing.assert_array_equal(move.coord_array, coord_array)

    def test_move_illegal_index_validation(self):
        coord_json = Move.coord_array_to_json(np.array([4, 4]))
        move = Move.objects.create(game=self.game, coords=coord_json)
        with self.assertRaises(ValidationError):
            move.full_clean()

    def test_move_occupied_validation(self):
        coord_json = Move.coord_array_to_json(np.array([1, 1]))
        Move.objects.create(
            game=self.game, coords=coord_json, player=Players.NOUGHTS)

        coord_json = Move.coord_array_to_json(np.array([1, 1]))
        self.move = Move.objects.create(
            game=self.game, coords=coord_json, player=Players.CROSSES)

        with self.assertRaises(ValidationError):
            self.move.full_clean()

    def test_move_order_validation(self):
        coord_json = Move.coord_array_to_json(np.array([1, 1]))
        Move.objects.create(
            game=self.game, coords=coord_json, player=Players.NOUGHTS)

        coord_json = Move.coord_array_to_json(np.array([1, 2]))
        self.move = Move.objects.create(
            game=self.game, coords=coord_json, player=Players.NOUGHTS)

        with self.assertRaises(ValidationError):
            self.move.full_clean()
