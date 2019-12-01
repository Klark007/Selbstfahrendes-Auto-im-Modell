"""
    Priority Queue: https://www.youtube.com/watch?v=wptevk0bshY
    A*: https://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/
"""
import heapq


class Cell(object):
    def __init__(self, x, y, walkable):
        """
        :param x: x coordinate
        :param y: y coordinate
        :param walkable: true if floor (0), false if wall (1)
        """
        self.x = x
        self.y = y
        self.walkable = walkable

        self.parent = None

        """
        :param g: distant from start to cell (self)
        :param h: distant from cell to end point
        :param f: g+h (value of cell)
        """
        self.g = 0
        self.h = 0
        self.f = 0
        pass


class AStar(object):
    def __init__(self, grid):
        # List of reachable but not yet explored cells
        self.opened = []
        heapq.heapify(self.opened)

        # set: Datatype like a list, without duplicates... https://www.youtube.com/watch?v=r3R3h5ly_8g
        # List of already explored cells
        self.closed = set()

        self.cells = []

        self.grid_width = None
        self.grid_height = None

        self.start = None
        self.end = None

        dim = grid.shape
        self.init_grid(dim[1], dim[0], grid)

        self.path = None
        pass

    def init_grid(self, width, height, grid):
        """
        :param width: width of the grid
        :param height: width of the grid
        :param grid: grid with walls
        """
        self.grid_width = width
        self.grid_height = height

        # Goes trough grid and adds cells to the cells list
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                tile = grid[y][x]
                if tile == 1:
                    walkable = False
                else:
                    walkable = True

                self.cells.append(Cell(x, y, walkable))

                # if current tile is the start/end tile, it saves the last added cell
                if tile == 2:
                    self.start = self.cells[-1]
                elif tile == 3:
                    self.end = self.cells[-1]
        pass

    def get_heuristic(self, cell):
        """
        :param cell: cell to be evaluated
        :return: heuristic value h
        """
        return 10 * (abs(cell.x - self.end.y) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        """
        :param x: cells x coordinate
        :param y: cells y coordinate
        :return: cell at that position
        """
        return self.cells[y * self.grid_width + x]

    def get_adjacent_cells(self, cell):
        """
        Returns adjacent/neighbouring cells
        Has to check if they aren't out of bonds
        From the right cell clockwise

        :param cell: cell from which to look
        :return: list of the neighbouring cells
        """
        cells = []

        if cell.x < self.grid_width - 1:
            cells.append(self.get_cell(cell.x + 1, cell.y))
        if cell.y < self.grid_height - 1:
            cells.append(self.get_cell(cell.x, cell.y + 1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x - 1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y - 1))

        return cells

    def get_path(self):
        """
        :return: the reversed path from the end node to the start trough
                looking up there parent and using them as the next node
        """
        cell = self.end
        path = [(cell.x, cell.y)]

        while cell.parent is not self.start:
            cell = cell.parent
            path.append((cell.x, cell.y))

        path.append((self.start.x, self.start.y))
        path.reverse()

        self.path = path
        return path

    def get_directions(self):
        """
        :return: list of directions to follow
        """
        directions = []

        for n in range(1, len(self.path)):
            delta_x = self.path[n][0] - self.path[n - 1][0]
            delta_y = self.path[n][1] - self.path[n - 1][1]
            directions.append((delta_x, delta_y))

        return directions

    def update_cell(self, adj, cell):
        """
        Updates adjacent cell if the current way is better than her own
        (Lower g value: shorter path)

        :param adj: adjacent cell being reevaluated
        :param cell: current cell
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell

        adj.f = adj.g + adj.h
        pass

    def solve(self):
        """ Solves the mazes and returns the path (list of positions)

        :return: path or None if no path is found
        """

        # add the starting cell to the opened list
        heapq.heappush(self.opened, (self.start.f, (self.start.x, self.start.y)))

        # loops as long as there are unexplored cells which are reachable
        while len(self.opened):
            # pop cell from heap queue (gets lowest current f)
            f, pos = heapq.heappop(self.opened)
            cell = self.get_cell(pos[0], pos[1])

            # add to the closed list so it won't be processed multiple times
            self.closed.add(cell)

            # if tending cell than return the path
            if cell is self.end:
                return self.get_path()

            # get adjacent cells (scan)
            adj_cells = self.get_adjacent_cells(cell)

            for adj_cell in adj_cells:
                if adj_cell.walkable and adj_cell not in self.closed:
                    if (adj_cell.f, (adj_cell.x, adj_cell.y)) in self.opened:
                        """
                            if adj_cell in open_list and adj_cell.g is higher
                            (longer path) then update adj_cell (path from current cell to
                            adj cell)
                        """
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # adds adj_cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, (adj_cell.x, adj_cell.y)))
