from django.db import models
import ipdb
from model_utils.fields import StatusField
from model_utils import Choices
from django.utils.translation import gettext_lazy as _
from .utils import empty_game_grid, default_coords
import json
import numpy as np
from django.core.exceptions import ValidationError


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


    # def grid_coord_legal(self, coords):
    #     try:
    #         return True if not self.grid_array[coords[0]][coords[1]] else False
    #     except IndexError:
    #         return False

    def previous_player(self):
        moves = self.move_set.all()
        if len(moves)>1:
            return moves[-2].player
        else:
            return None

    # def update_grid(self, move):
    #     coord_array = move.coord_array
    #     self.grid_array[coord_array[0]][coord_array[1]] = move.player.value

    # @property
    # def grid_array(self):
    #     grid_list = json.loads(self.grid)['grid']
    #     return np.array(grid_list)


class Move(models.Model):
    game = models.ForeignKey(Game, related_name='moves', on_delete=models.CASCADE)
    player = models.CharField(
        max_length=2,
        choices=Players.choices,
        default=Players.NOUGHTS,
    )
    coords = models.CharField(max_length=100)

    # def coord_array_to_json(coord_array):
    #     coord_dict = {"coord": coord_array.tolist()}
    #     return json.dumps(coord_dict)

    # def clean(self):
    #     if not self.game.grid_coord_legal(self.coord_array):
    #         raise ValidationError({'coords': _(
    #             'Invalid coordinates')})
    #     elif self.game.previous_player() == self.player:
    #         raise ValidationError({'player': _(
    #             'Incorrect player order')})
    #     else:
    #         self.game.update_grid(self)
    #         # self.game.update_status()

    # @property
    # def coord_array(self):
    #     coord_list = json.loads(self.coords)['coord']
    #     return np.array(coord_list)
