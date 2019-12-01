"""
    Finds the exit of the labyrinth
    Current solution: Find the spaces on the ouside not occupied by an obstacle
    Then look which one is reachable
"""
import Pathfinding.A_Star as A_Star
import numpy as np


def scan(grid):
    exits = []

    # loops trough the outer frame of the grid an looks for free spaces
    for y in range(len(grid)):
        if grid[y][0] == 0:
            exits.append((0, y))
        if grid[y][grid.shape[1]-1] == 0:
            exits.append((grid.shape[1]-1, y))

    for x in range(grid.shape[1]):
        if grid[0][x] == 0:
            exits.append((x, 0))
        if grid[grid.shape[0]-1][x] == 0:
            exits.append((x, grid.shape[0]-1))

    # solves the path to the possible exits
    paths = []
    for pos in exits:
        current_grid = grid
        current_grid[pos[1]][pos[0]] = 3

        a_star_algorithm = A_Star.AStar(grid)
        path = a_star_algorithm.solve()
        if path:
            paths.append(a_star_algorithm.get_directions())

    # Takes the shortest one by comparing to the current path
    # (Beginning Value: longest path on a empty grid)
    shortest_path = np.zeros(shape=(grid.shape[0] * grid.shape[1], 1))
    for path in paths:
        shortest_path = path if len(path) < len(shortest_path) else shortest_path

    return shortest_path
