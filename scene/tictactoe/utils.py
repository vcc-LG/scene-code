import numpy as np
import json


def empty_game_grid(rows=3, cols=3):
    grid_array = np.zeros((rows, cols), dtype=int)
    grid_dict = {"grid": grid_array.tolist()}
    return json.dumps(grid_dict)


def default_coords(x=1,y=1):
    coord_array = np.array([x, y])
    coord_dict = {"coord": coord_array.tolist()}
    return json.dumps(coord_dict)
