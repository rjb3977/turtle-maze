from dataclasses import dataclass, field
from random import shuffle
from typing import Any

class DisjointSet:
    __slots__ = ['_parent', '_height']

    def __init__(self):
        self._parent = self
        self._height = 0

    def _root(self):
        x = self

        while x._parent is not x:
            x, x._parent = x._parent, x._parent._parent

        return x

    @staticmethod
    def join(x, y):
        x = x._root()
        y = y._root()

        if x._height < y._height:
            x, y = y, x

        y._parent = x._parent

        if x._height == y._height:
            x._height += 1

    def __eq__(self, other):
        return self._root() is other._root()

@dataclass
class Cell:
    e: bool = field(default=True)
    n: bool = field(default=True)
    w: bool = field(default=True)
    s: bool = field(default=True)
    extra: Any = field(default=None)

    all_open = None

    def __getitem__(self, direction):
        if direction in ('e', (1, 0)):
            return self.e
        if direction in ('n', (0, 1)):
            return self.n
        if direction in ('w', (-1, 0)):
            return self.w
        if direction in ('s', (0, -1)):
            return self.s

    def __setitem__(self, direction, value):
        if direction in ('e', (1, 0)):
            self.e = value
        if direction in ('n', (0, 1)):
            self.n = value
        if direction in ('w', (-1, 0)):
            self.w = value
        if direction in ('s', (0, -1)):
            self.s = value

Cell.all_open = Cell(e=False, n=False, w=False, s=False)


class Maze:
    __slots__ = ['_cells', '_width', '_height']

    def __init__(self, width, height):
        self._cells = [Cell() for i in range(width * height)]
        self._width = width
        self._height = height


    def __getitem__(self, index):
        x, y = index

        if x not in range(self._width) or y not in range(self._height):
            return Cell.all_open

        return self._cells[x + self._width * y]

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @staticmethod
    def generate(width, height):
        maze = Maze(width, height)
        choices = []

        for y in range(height):
            for x in range(width):
                if x > 0:
                    choices.append((x, y, x - 1, y))

                if y > 0:
                    choices.append((x, y, x, y - 1))

                maze[y, x].extra = DisjointSet()

        shuffle(choices)

        for x1, y1, x2, y2 in choices:
            if maze[x1, y1].extra == maze[x2, y2].extra:
                continue

            DisjointSet.join(maze[x1, y1].extra, maze[x2, y2].extra)
            maze[x1, y1][x2 - x1, y2 - y1] = False
            maze[x2, y2][x1 - x2, y1 - y2] = False


        for y in range(height):
            for x in range(width):
                maze[x, y].extra = None

        return maze
