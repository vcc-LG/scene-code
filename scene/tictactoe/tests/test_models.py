from django.test import TestCase
from ..models import Game, Status, Move, Players
import numpy as np
from ..utils import empty_game_grid, default_coords
import json
from django.core.exceptions import ValidationError


class GameTestCase(TestCase):
    def setUp(self):
        self.game = Game.objects.create()

    def test_type(self):
        self.assertIsInstance(self.game, Game)

    def test_game_initial_vals(self):
        self.assertEqual(self.game.status, Status.INCOMPLETE)
        self.assertEqual(self.game.moves.count(), 0)
        self.assertEqual(self.game.grid, empty_game_grid())

    # def test_game_grid_props(self):
    #     self.assertIsInstance(self.game.grid_array, np.ndarray)

    # def test_game_grid_updated_after_move(self):
    #     move_coords = [1, 1]
    #     coord_json = Move.coord_array_to_json(np.array(move_coords))
    #     move = Move.objects.create(
    #         game=self.game, coords=coord_json, player=Players.NOUGHTS)
    #     move.full_clean()
        # with self.assertEqual(self.game.grid_array[move_coords].any(), 'o'):
        #     move.full_clean()

    # def test_game_status_win(self):
    #     coord_json = Move.coord_array_to_json(np.array([1, 1]))
    #     Move.objects.create(game=self.game, coords=coord_json)
    #     coord_json = Move.coord_array_to_json(np.array([1, 2]))
    #     Move.objects.create(game=self.game, coords=coord_json)
    #     coord_json = Move.coord_array_to_json(np.array([1, 3]))
    #     Move.objects.create(game=self.game, coords=coord_json)
    #     self.assertEqual(self.game.status, Status.WIN)


class MoveTestCase(TestCase):
    def setUp(self):
        self.game = Game.objects.create()
        self.move = Move.objects.create(game=self.game)

    def test_type(self):
        self.assertIsInstance(self.move, Move)

#     def test_move_default_props(self):
#         self.assertEqual(self.move.game, self.game)
#         self.assertEqual(self.move.player, Players.NOUGHTS)
#         self.assertEqual(self.move.coords, default_coords())

#     def test_move_set_get(self):
#         coord_array = np.array([4, 4])
#         coord_json = Move.coord_array_to_json(coord_array)
#         move = Move.objects.create(game=self.game, coords=coord_json)
#         np.testing.assert_array_equal(move.coord_array, coord_array)

#     def test_move_illegal_index_validation(self):
#         coord_json = Move.coord_array_to_json(np.array([4, 4]))
#         move = Move.objects.create(game=self.game, coords=coord_json)
#         with self.assertRaises(ValidationError):
#             move.full_clean()

#     def test_move_occupied_validation(self):
#         coord_json = Move.coord_array_to_json(np.array([1, 2]))
#         Move.objects.create(
#             game=self.game, coords=coord_json, player=Players.NOUGHTS)

#         coord_json = Move.coord_array_to_json(np.array([1, 2]))
#         self.move = Move.objects.create(
#             game=self.game, coords=coord_json, player=Players.CROSSES)

#         with self.assertRaises(ValidationError):
#             self.move.full_clean()

#     def test_move_order_validation_ok(self):
#         coord_json = Move.coord_array_to_json(np.array([1, 2]))
#         Move.objects.create(
#             game=self.game, coords=coord_json, player=Players.NOUGHTS)

#         coord_json = Move.coord_array_to_json(np.array([1, 3]))
#         self.move = Move.objects.create(
#             game=self.game, coords=coord_json, player=Players.CROSSES)

#         self.assertEqual(self.game.move_set.count(), 3)

#     def test_move_order_validation_error(self):
#         coord_json = Move.coord_array_to_json(np.array([1, 2]))
#         Move.objects.create(
#             game=self.game, coords=coord_json, player=Players.NOUGHTS)

#         coord_json = Move.coord_array_to_json(np.array([1, 3]))
#         self.move = Move.objects.create(
#             game=self.game, coords=coord_json, player=Players.NOUGHTS)

#         with self.assertRaises(ValidationError):
#             self.move.full_clean()
