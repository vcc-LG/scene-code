from django.db import models
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
    NOUGHTS = 'OS', 'Noughts'
    CROSSES = 'XS', 'Crosses'


class Game(models.Model):
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.INCOMPLETE,
    )
    grid = models.JSONField(default=empty_game_grid)

    def grid_coord_legal(self, coords):
        try:
            if self.grid_array[coords] == 0:
                return True
            else:
                return False
        except IndexError:
            return False

    @property
    def grid_array(self):
        grid_list = json.loads(self.grid)['grid']
        return np.array(grid_list)


class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.CharField(
        max_length=2,
        choices=Players.choices,
        default=Players.NOUGHTS,
    )
    coords = models.JSONField(default=default_coords)

    def coord_array_to_json(coord_array):
        coord_dict = {"coord": coord_array.tolist()}
        return json.dumps(coord_dict)

    def clean(self):
        if not self.game.grid_coord_legal(self.coords):
            raise ValidationError({'coords': _(
                'Invalid coordinates')})
        if not self.game.next_player == self.player:
            raise ValidationError({'player': _(
                'Incorrect player order')})

    @property
    def coord_array(self):
        coord_list = json.loads(self.coords)['coord']
        return np.array(coord_list)
