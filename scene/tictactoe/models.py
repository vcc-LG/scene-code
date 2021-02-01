from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import empty_game_grid, coord_array_from_string
import numpy as np
import ast
import json


class Status(models.TextChoices):
    INCOMPLETE = 'IN', 'Incomplete'
    WIN = 'WN', 'Win'
    DRAW = 'DR', 'Draw'


class Players(models.TextChoices):
    NOUGHTS = 'O', 'Noughts'
    CROSSES = 'X', 'Crosses'


class Game(models.Model):
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.INCOMPLETE,
    )
    grid = models.CharField(max_length=100, default=empty_game_grid)

    def previous_player(self):
        previous_move = self.moves.last()
        if previous_move:
            return previous_move.player
        else:
            return None

    def update_grid(self):
        move = self.moves.last()
        coord_array = coord_array_from_string(move.coords)
        grid_array = self.grid_array
        grid_array[coord_array[0]][coord_array[1]] = move.player
        self.grid = grid_array.tolist()
        self.save()

    def update_status(self):
        target_count = 3
        for player in ['o', 'x']:
            for axis in [0, 1]:
                if np.isin(target_count, np.sum(self.grid_array == player, where=[True], axis=axis)):
                    self.status = Status.WIN
                    self.save()
            if np.isin(3, np.sum(np.diag(self.grid_array) == player, where=[True])):
                self.status = Status.WIN
                self.save()
            if np.isin(3, np.sum(np.diag(np.fliplr(self.grid_array)) == player, where=[True])):
                self.status = Status.WIN
                self.save()

    @property
    def grid_array(self):
        try:
            return np.array(ast.literal_eval(self.grid), dtype=str)
        except:
            return np.array(self.grid, dtype=str)


class Move(models.Model):
    game = models.ForeignKey(Game, related_name='moves',
                             on_delete=models.CASCADE)
    player = models.CharField(
        max_length=2,
        choices=Players.choices,
        default=Players.NOUGHTS,
    )
    coords = models.CharField(max_length=100)

    def coord_array_to_json(coord_array):
        coord_dict = {"coord": coord_array.tolist()}
        return json.dumps(coord_dict)
