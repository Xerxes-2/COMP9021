from enum import Enum

import numpy as np


class PolygonsError(Exception):
    class ErrorType(Enum):
        InputError = 'Incorrect input.'
        NoExpectedPolygon = 'Cannot get polygons as expected.'

    class PolygonsErrorBuilder:

        def __init__(self):
            self.type = None

        def input_error(self):
            self.type = PolygonsError.ErrorType.InputError
            return self

        def no_expected_polygon(self):
            self.type = PolygonsError.ErrorType.NoExpectedPolygon
            return self

        def build(self):
            if not self.type:
                raise Exception('Not Enough Argument.')
            else:
                return PolygonsError(self.type.value)

    @staticmethod
    def error_builder():
        return PolygonsError.PolygonsErrorBuilder()


class Polygons:
    class Polygon:
        INTERVAL = 0.4

        def __init__(self, coord, found: np.ndarray, depth_map):
            self._start = coord
            self.depth = depth_map[coord]
            self._depth_map = depth_map.copy()
            self._yDim, self.xDim = found.shape
            self.new_found = found.copy()
            self._banned = set()
            self._circle = self.__dfs([], coord)
            if not self._circle:
                raise PolygonsError.error_builder().no_expected_polygon().build()
            for p in self._circle:
                self.new_found[p] = 1
            self.vertex = self.__vertex()
            self._nb_ver = len(self.vertex)
            self._perimeter = self.__perimeter()
            self.area = self.__area()
            self._convex = self.__convex()
            self._rotations = self.__rotations()

        def __vertex(self):
            ver = [self._start, self._circle[1]]
            for i, (y2, x2) in enumerate(self._circle[2:]):
                y0, x0 = ver[- 2]
                y1, x1 = ver[- 1]
                if (y2 - y0) * (x1 - x0) == (y1 - y0) * (x2 - x0):
                    ver[- 1] = y2, x2
                else:
                    ver.append((y2, x2))
            y2, x2 = self._start
            y0, x0 = ver[- 2]
            y1, x1 = ver[- 1]
            if (y2 - y0) * (x1 - x0) == (y1 - y0) * (x2 - x0):
                ver.pop()
            return ver

        def __clock(self, coord, from_coord):
            clock_list = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)] * 2
            next_list = [(coord[0] + c[0], coord[1] + c[1]) for c in clock_list]
            start = next_list.index(from_coord) + 1
            next_list = next_list[start:start + 7]
            next_list = [(y, x) for (y, x) in next_list if
                         -1 < y < self._yDim and -1 < x < self.xDim and self.depth == self._depth_map[y, x] and (
                             y, x) not in self._banned and not self.new_found[y, x]]
            return next_list

        def __dfs(self, circle: list, coord):
            if coord == self._start and circle:
                return circle
            if coord in circle:
                return []
            if not circle:
                prev = coord[0] - 1, coord[1] + 1
            else:
                prev = circle[-1]
            my_circle = circle.copy()
            my_circle.append(coord)
            clock_list = self.__clock(coord, prev)
            for next_coord in clock_list:
                result = self.__dfs(my_circle, next_coord)
                if result:
                    return result
            self._banned.add(coord)
            return []

        def __perimeter(self):
            result = [0, 0]
            for i, (y, x) in enumerate(self._circle):
                y0, x0 = self._circle[i - 1]
                offset = abs(y - y0) + abs(x - x0)
                if offset == 1:
                    result[0] += 1
                else:
                    result[1] += 1
            string = ''
            if result[0]:
                string += f'{self.INTERVAL * result[0]:.1f}'
            if result[0] and result[1]:
                string += ' + '
            if result[1]:
                string += f'{result[1]}*sqrt(.32)'
            return string

        def __area(self):
            coords = np.asarray(self.vertex)
            y, x = coords[:, 0], coords[:, 1]
            y1, x1 = np.roll(y, 1), np.roll(x, 1)
            result = 0
            for i in range(0, self._nb_ver):
                result += y[i] * x1[i] - x[i] * y1[i]
            return (abs(result) / 2) * self.INTERVAL ** 2

        def __convex(self):
            for i, (y1, x1) in enumerate(self.vertex):
                y0, x0 = self.vertex[i - 1]
                if i == self._nb_ver - 1:
                    y2, x2 = self.vertex[0]
                else:
                    y2, x2 = self.vertex[i + 1]
                v01 = y1 - y0, x1 - x0
                v02 = y2 - y0, x2 - x0
                if v02[0] * v01[1] - v02[1] * v01[0] < 0:
                    return False
            return True

        def __rotations(self):
            max_y, max_x = 0, 0
            min_y, min_x = 114514, 114514
            for y, x in self.vertex:
                max_y, max_x = max(y, max_y), max(x, max_x)
                min_y, min_x = min(y, min_y), min(x, min_x)
            width = max_x - min_x
            height = max_y - min_y
            vertex = [(max_y - y, max_x - x) for y, x in self.vertex]
            vertex_4 = [(x, -y) for y, x in vertex]
            for y, x in vertex:
                if (y, x - width) not in vertex_4:
                    break
            else:
                return 4
            vertex_2 = [(-y, -x) for y, x in vertex]
            for y, x in vertex:
                if (y - height, x - width) not in vertex_2:
                    break
            else:
                return 2
            return 1

        def show(self):
            print('    Perimeter: ' + self._perimeter)
            print(f'    Area: {self.area:.2f}')
            print('    Convex: ' + self._convex * 'yes' + (not self._convex) * 'no')
            print(f'    Nb of invariant rotations: {self._rotations}')
            print(f'    Depth: {self.depth}')

    def __init__(self, filename: str):
        def near_4(coord):
            near_list = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            result = list()
            y, x = coord
            for os in near_list:
                if -1 < x + os[0] < self.xDim and -1 < y + os[1] < self.yDim:
                    result.append((y + os[1], x + os[0]))
            return result

        def new_depth(coord, cur_depth):
            nears = near_4(coord)
            new_boundary = np.array([depth[p] < cur_depth for p in nears])
            if new_boundary.any() or len(nears) != 4:
                return cur_depth
            else:
                return 114514

        def bfs(search_map, cur_depth, coord):
            queue = [coord]
            while queue:
                current = queue.pop(0)
                if search_map[current] or (depth[current] > cur_depth and raw[current]):
                    continue
                if not raw[current]:
                    depth[current] = -1
                search_map[current] = 1
                for p in near_4(current):
                    queue.append(p)

        def search_from_edge(cur_depth):
            search_map = np.zeros(raw.shape)
            for x in range(0, self.xDim):
                bfs(search_map, cur_depth, (0, x))
                bfs(search_map, cur_depth, (self.yDim - 1, x))
            for y in range(1, self.yDim - 1):
                bfs(search_map, cur_depth, (y, 0))
                bfs(search_map, cur_depth, (y, self.xDim - 1))

        self.name = filename.rstrip('txt')
        with open(filename) as file:
            reader = file.readlines()
        for i, row in enumerate(reader):
            reader[i] = row.rstrip('\n').replace(' ', '')
        while True:
            try:
                reader.remove('')
            except ValueError:
                break
        self.xDim = len(reader[0])
        self.yDim = len(reader)
        for row in reader:
            if len(row) != self.xDim or row.count('1') + row.count('0') != self.xDim:
                raise PolygonsError.error_builder().input_error().build()
        if not (1 < self.xDim < 51 and 1 < self.yDim < 51):
            raise PolygonsError.error_builder().input_error().build()
        self.poly_list = []
        raw = np.asarray([[int(char) for char in row] for row in reader])
        shape = raw.shape
        depth = np.asarray([[114514 for _ in row] for row in raw])
        current_depth = -1
        finished = 0
        while not finished:
            search_from_edge(current_depth)
            current_depth += 1
            finished = 1
            for i, row in enumerate(raw):
                for j, digit in enumerate(row):
                    if depth[i, j] == 114514 and digit:
                        finished = 0
                        depth[i, j] = new_depth((i, j), current_depth)
        self.max_depth = current_depth - 1
        found = np.zeros(shape)
        for i, row in enumerate(depth):
            for j, dep in enumerate(row):
                if not found[i, j] and depth[i, j] > -1:
                    self.poly_list.append(self.Polygon((i, j), found, depth))
                    found = self.poly_list[-1].new_found
        for i in range(0, self.yDim):
            for j in range(0, self.yDim):
                if not found[i, j] and raw[i, j]:
                    raise PolygonsError.error_builder().no_expected_polygon().build()

    def analyse(self):
        for i, p in enumerate(self.poly_list):
            print(f'Polygon {i + 1}:')
            p.show()

    def display(self):
        max_area = 0
        min_area = 2500
        for p in self.poly_list:
            max_area = max(max_area, p.area)
            min_area = min(min_area, p.area)
        ran = max_area - min_area
        with open(self.name + 'tex', 'w') as f:
            f.write('\\documentclass[10pt]{article}\n'
                    '\\usepackage{tikz}\n'
                    '\\usepackage[margin=0cm]{geometry}\n'
                    '\\pagestyle{empty}\n'
                    '\n'
                    '\\begin{document}\n'
                    '\n'
                    '\\vspace*{\\fill}\n'
                    '\\begin{center}\n'
                    '\\begin{tikzpicture}[x=0.4cm, y=-0.4cm, thick, brown]\n'
                    f'\\draw[ultra thick] (0, 0) -- ({self.xDim - 1}, 0) -- ({self.xDim - 1}, '
                    f'{self.yDim - 1}) -- (0, {self.yDim - 1}) -- cycle;\n')
            for depth in range(0, self.max_depth + 1):
                f.write(f'\n% Depth {depth}')
                for p in self.poly_list:
                    if p.depth == depth:
                        if ran == 0:
                            f.write('\n\\filldraw[fill=orange!0!yellow] ')
                        else:
                            f.write(f'\n\\filldraw[fill=orange!{round((max_area - p.area) / ran * 100)}!yellow] ')
                        for y, x in p.vertex:
                            f.write(f'({x}, {y}) -- ')
                        f.write('cycle;')
            f.write('\n\\end{tikzpicture}\n'
                    '\\end{center}\n'
                    '\\vspace*{\\fill}\n'
                    '\n'
                    '\\end{document}\n')
