import numpy as np

def empty_game_grid(rows=3, cols=3):
    grid_array = np.chararray((rows, cols),unicode=True)
    return grid_array.tolist()


def default_coords(x=0,y=0):
    coord_array = np.array([x, y])
    return coord_array.tolist()


def coord_array_from_string(coord_string):
    return [int(item) for item in list(coord_string[1:-1].split(','))]