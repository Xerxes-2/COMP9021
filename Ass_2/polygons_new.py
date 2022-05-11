from collections import namedtuple
from copy import deepcopy
from math import inf
from typing import Any, List, Set, Tuple


# make `diff` test happy
class PolygonsError(Exception):

    @staticmethod
    def input_error():
        return PolygonsError('Incorrect input.')

    @staticmethod
    def no_expected_polygon():
        return PolygonsError('Cannot get polygons as expected.')


class Coord(namedtuple('Coordinate', ['y', 'x'])):
    """
    why (y, x) not (x, y)? \n
    in c:
    ```c
    int foo[Y][X];
    foo[y][x] = 42
    ```
    in python:
    ```python
    Grid([[0, 1], [2, 3], [4, 5]])
    Grid[y, x] = 42
    ```
    """

    def __add__(self, other):
        return Coord(self.y + other.y, self.x + other.x)

    def __sub__(self, other):
        return Coord(self.y - other.y, self.x - other.x)

    def __mul__(self, other) -> int:
        return self.y * other.x - self.x * other.y

    def manhattan_distance(self, other):
        return abs(self.y - other.y) + abs(self.x - other.x)

    def in_range(self, x_dim: int, y_dim: int):
        return (0 <= self.x < x_dim) and (0 <= self.y < y_dim)

    def __slope(self):
        if self.x:
            return self.y / self.x
        return self.y * inf

    def are_parallel(self, other):
        return self.__slope() == other.__slope()

    def max(self, other):
        return Coord(max(self.y, other.y), max(self.x, other.x))

    def min(self, other):
        return Coord(min(self.y, other.y), min(self.x, other.x))

    def near_tdlr(self):
        near = [
            Coord(-1, 0),  # top
            Coord(1, 0),  # down
            Coord(0, -1),  # left
            Coord(0, 1),  # right
        ]
        return list(map(lambda n: n + self, near))

    def near_clock_seq(self):
        near = [
            Coord(-1, -1),  # upper left
            Coord(-1, 0),  # top
            Coord(-1, 1),  # upper right
            Coord(0, 1),  # right
            Coord(1, 1),  # lower right
            Coord(1, 0),  # bottom
            Coord(1, -1),  # lower left
            Coord(0, -1),  # left
        ]
        return list(map(lambda n: n + self, near))


class Grid:
    Shape = namedtuple('Shape', ['y_dim', 'x_dim'])

    _grid: List[List[int]]
    _shape: Shape

    def __init__(self, grid: List[List[int]]) -> None:
        self._grid = grid
        self._shape = self.Shape(len(grid), len(grid[0]))

    def __getitem__(self, index: Tuple[int, int]):
        return self._grid[index[0]][index[1]]

    def __setitem__(self, index: Tuple[int, int], obj: int):
        self._grid[index[0]][index[1]] = obj

    def __iter__(self):
        return iter(self._grid)

    def shape(self):
        return self._shape

    def copy(self):
        return Grid(deepcopy(self._grid))

    @staticmethod
    def zeros(shape: Tuple[int, int]):
        grid: List[Any] = [None] * shape[0]
        for index, _ in enumerate(grid):
            grid[index] = [0] * shape[1]
        return Grid(grid)


class Array(list):
    @staticmethod
    def roll(lst: List[Any], count: int):
        """
        return a copy of list, as same as numpy.roll
        """
        new_lst = lst[-count:]
        new_lst.extend(lst[:-count])
        return new_lst


class Polygon:
    INTERVAL = 0.4

    all_points: List[Coord]
    dead_loop: Set[Coord]
    vertex: List[Coord]
    origin: Coord
    new_found_points: Grid
    depth: int
    x_dim: int
    y_dim: int
    nb_vertex: int
    perimeter: str
    area: float
    convex: str
    rotations: int

    def __init__(self, coord: Coord, found_points: Grid, depth_map: Grid):
        self.depth = depth_map[coord]
        self.origin = coord
        self.depth_map = depth_map.copy()
        self.y_dim, self.x_dim = depth_map.shape()
        self.new_found_points = found_points.copy()
        self.dead_loop = set()
        self.all_points = self.__search_boundary([], coord)
        if not self.all_points:
            raise PolygonsError.no_expected_polygon()
        for p in self.all_points:
            self.new_found_points[p] = 1
        for p in self.all_points:
            self.depth_map[p] = self.depth
        self.vertex = self.__find_vertex()
        self.nb_vertex = len(self.vertex)
        self.perimeter = self.__find_perimeter()
        self.area = self.__find_area()
        self.convex = self.__find_convex()
        self.rotations = self.__find_rotations()

    def __find_vertex(self) -> List[Coord]:
        v = [self.origin, self.all_points[1]]
        for p in self.all_points[2:]:
            if (p - v[-2]).are_parallel(p - v[-1]):
                v[-1] = p
            else:
                v.append(p)
        if (v[-1] - v[-2]).are_parallel(v[0] - v[-2]):
            v.pop()
        return v

    def __find_by_clock(self, coord: Coord, from_coord: Coord) -> List[Coord]:
        next_list = coord.near_clock_seq()
        next_list = Array.roll(next_list, - (next_list.index(from_coord) + 1))
        next_list = next_list[:7]

        next_list = [c for c in next_list
                     if c.in_range(self.x_dim, self.y_dim)
                     and self.depth == self.depth_map[c]
                     and c not in self.dead_loop
                     and not self.new_found_points[c]
                     ]
        return next_list

    def __search_boundary(self, points: List[Coord], p: Coord) -> List[Coord]:
        match not points, p == self.origin, p in points:
            case True, True, False:
                prev = p + Coord(-1, 1)
            case False, True, True:
                return points
            case False, False, False:
                prev = points[-1]
            case _:
                return []

        new_points = points.copy()
        new_points.append(p)
        for next_coord in self.__find_by_clock(p, prev):
            result = self.__search_boundary(new_points, next_coord)
            if result:
                return result
        self.dead_loop.add(p)
        return []

    def __find_perimeter(self):
        p = [0, 0]
        for i, c in enumerate(self.all_points):
            c0 = self.all_points[i - 1]
            offset = c.manhattan_distance(c0)
            p[offset - 1] += 1
        return \
            (p[0] > 0) * f'{self.INTERVAL * p[0]:.1f}' + \
            (p[0] * p[1] > 0) * ' + ' + \
            (p[1] > 0) * f'{p[1]}*sqrt(.32)'

    def __find_area(self):
        y = Array([yy[0] for yy in self.vertex])
        x = Array([xx[1] for xx in self.vertex])
        y1 = Array.roll(y, 1)
        x1 = Array.roll(x, 1)
        result = 0
        for i in range(0, self.nb_vertex):
            result += y[i] * x1[i] - x[i] * y1[i]
        return (abs(result) / 2) * self.INTERVAL ** 2

    def __find_convex(self) -> str:
        for i, c1 in enumerate(self.vertex):
            c0 = self.vertex[i - 1]
            c2 = self.vertex[(i + 1) % self.nb_vertex]
            if (c2 - c0) * (c1 - c0) < 0:
                return 'no'
        # output format required
        return 'yes'

    def __find_rotations(self):
        furthest = Coord(0, 0)
        nearest = Coord(99, 99)
        for c in self.vertex:
            furthest = c.max(furthest)
            nearest = c.min(nearest)
        (height, width) = furthest - nearest
        vertex = [furthest - c for c in self.vertex]
        vertex_4 = [Coord(x, -y) for y, x in vertex]
        for c in vertex:
            if (c.y, c.x - width) not in vertex_4:
                break
        else:
            return 4
        vertex_2 = [Coord(-c.y, -c.x) for c in vertex]
        for c in vertex:
            if Coord(c.y - height, c.x - width) not in vertex_2:
                break
        else:
            return 2
        return 1

    def __str__(self):
        s = f'''    Perimeter: {self.perimeter}
    Area: {self.area:.2f}
    Convex: {self.convex}
    Nb of invariant rotations: {self.rotations}
    Depth: {self.depth}'''
        return s


class Polygons:
    plist: List[Polygon]
    x_dim: int
    y_dim: int

    def __init__(self, polys_input_file: str):

        # input
        self.name = polys_input_file.rstrip('txt')
        with open(polys_input_file) as file:
            tmp_list = map(lambda row: row.rstrip(
                '\n').replace(' ', ''), file.readlines())
            raw_polygon_text = list(filter(lambda row: row != '', tmp_list))

        '''The input is expected to consist of ydim lines of xdim 0’s and 1’s, where xdim and ydim are at
        least equal to 2 and at most equal to 50, with possibly lines consisting of spaces only that will be ignored and
        with possibly spaces anywhere on the lines with digits. If n is the x
        th digit of the y
        th line with digits, with
        0 ≤ x < xdim and 0 ≤ y < ydim , then n is to be associated with a point situated x × 0.4 cm to the right and
        y × 0.4 cm below an origin.
        '''
        self.y_dim = len(raw_polygon_text)
        if self.y_dim < 2 or self.y_dim > 50:
            raise PolygonsError.input_error()
        self.x_dim = len(raw_polygon_text[0])
        if self.x_dim < 2 or self.x_dim > 50:
            raise PolygonsError.input_error()

        for line in raw_polygon_text:
            # check each line
            if self.x_dim != len(line):
                raise PolygonsError.input_error()
            if not all(map(lambda ch: ch == '0' or ch == '1', line)):
                raise PolygonsError.input_error()

        # end.

        def new_depth(coord: Coord, cur_depth):
            nears = list(filter(lambda n: n.in_range(
                self.x_dim, self.y_dim), coord.near_tdlr()))
            new_boundary = [depth[p] < cur_depth for p in nears]
            if any(new_boundary) or len(nears) != 4:
                return cur_depth
            else:
                return 99

        def bfs(searched: Grid, depth_now: int, coord: Coord):
            queue = [coord]
            while queue:
                current = queue.pop(0)
                if searched[current] or (depth[current] > depth_now and grid[current]):
                    continue
                if not grid[current]:
                    depth[current] = -1
                searched[current] = 1
                for p in filter(lambda n: (n.in_range(self.x_dim, self.y_dim)), current.near_tdlr()):
                    queue.append(p)

        def search_from_edge(depth_now: int):
            searched = Grid.zeros(grid.shape())
            for xx in range(0, self.x_dim):
                bfs(searched, depth_now, Coord(0, xx))
                bfs(searched, depth_now, Coord(self.y_dim - 1, xx))
            for yy in range(0, self.y_dim):
                bfs(searched, depth_now, Coord(yy, 0))
                bfs(searched, depth_now, Coord(yy, self.x_dim - 1))

        self.plist = []
        grid: Grid = Grid([[int(char) for char in row]
                           for row in raw_polygon_text])
        depth: Grid = Grid([[int(99) for _ in row] for row in grid])
        current_depth = -1
        finished = False
        while not finished:
            search_from_edge(current_depth)
            current_depth += 1
            finished = True
            for y in range(grid.shape().y_dim):
                for x in range(grid.shape().x_dim):
                    if depth[y, x] == 99 and grid[y, x]:
                        finished = False
                        depth[y, x] = new_depth(
                            Coord(y, x), current_depth)
        self.max_depth = current_depth - 1
        found = Grid.zeros(grid.shape())
        for y, row in enumerate(depth):
            for x, dep in enumerate(row):
                if not found[y, x] and depth[y, x] > -1:
                    self.plist.append(Polygon(Coord(y, x), found, depth))
                    found = self.plist[-1].new_found_points
        for y in range(0, self.y_dim):
            for x in range(0, self.y_dim):
                if not found[y, x] and grid[y, x]:
                    raise PolygonsError.no_expected_polygon()

    def analyse(self):
        for i, p in enumerate(self.plist):
            print(f'Polygon {i + 1}:')
            print(p)

    def display(self):
        def outline():
            return f'\\draw[ultra thick] (0, 0) -- ({self.x_dim - 1}, 0) -- ({self.x_dim - 1}, ' \
                   + f'{self.y_dim - 1}) -- (0, {self.y_dim - 1}) -- cycle;'

        def polys(gap):
            string = ''
            for depth in range(0, self.max_depth + 1):
                string += f'\n% Depth {depth}'
                for poly in self.plist:
                    if poly.depth == depth:
                        if gap:
                            color = round((max_area - poly.area) / gap * 100)
                        else:
                            color = 0
                        string += f'\n\\filldraw[fill=orange!{color}!yellow] '
                        for y, x in poly.vertex:
                            string += f'({x}, {y}) -- '
                        string += 'cycle;'
            return string

        areas = [p.area for p in self.plist]
        max_area = max(areas)
        min_area = min(areas)
        ranging = max_area - min_area
        with open(self.name + 'tex', 'w') as file:
            file.write(
                f'''\\documentclass[10pt]{{article}}
\\usepackage{{tikz}}
\\usepackage[margin=0cm]{{geometry}}
\\pagestyle{{empty}}

\\begin{{document}}

\\vspace*{{\\fill}}
\\begin{{center}}
\\begin{{tikzpicture}}[x=0.4cm, y=-0.4cm, thick, brown]
{outline()}
{polys(ranging)}
\\end{{tikzpicture}}
\\end{{center}}
\\vspace*{{\\fill}}

\\end{{document}}
''')


Polygons('polys_1.txt').display()
