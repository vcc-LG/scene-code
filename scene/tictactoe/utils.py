import numpy as np
import json


def empty_game_grid(rows=3, cols=3):
    grid_array = np.chararray((rows, cols),unicode=True)
    return grid_array.tolist()


def default_coords(x=0,y=0):
    coord_array = np.array([x, y])
    return coord_array.tolist()
