# Written by Shupeng Xue for COMP9021
import numpy as np


def display(*grid):
    for e in grid:
        print(*e)


def neighbours(point, height, width):
    output = []
    i, j = point
    offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for offset in offsets:
        if 0 <= i + offset[0] < height and 0 <= j + offset[1] < width:
            output.append((i + offset[0], j + offset[1]))
    return output


def display_leftmost_topmost_boundary(*grid):
    width = len(grid[0])
    height = len(grid)
    dic = {' ': 0, '*': 1}
    graph_in = [[dic[char] for char in row] for row in grid]
    graph_1 = np.zeros((height, width), dtype=int)
    graph_2 = graph_1.copy()
    re_dic = {v: k for k, v in dic.items()}
    found = 0
    visited = set()
    for i, row in enumerate(graph_in):
        for j, char in enumerate(row):
            if char:
                found = 1
                queue = list()
                queue.append((i, j))
                while queue:
                    point = queue.pop(0)
                    if point in visited:
                        continue
                    visited.add(point)
                    x, y = point
                    graph_1[x][y] = 1
                    for p in neighbours(point, height, width):
                        if graph_in[p[0]][p[1]] and (p not in visited):
                            queue.append(p)
                break
        if found:
            break
    for i, row in enumerate(graph_1):
        for j, char in enumerate(row):
            if char:
                pro = 1
                for p in neighbours((i, j), height, width):
                    pro = pro * graph_1[p[0]][p[1]]
                graph_2[i][j] = not pro
    grid_out = (''.join([re_dic[_] for _ in row]) for row in graph_2)
    display(*grid_out)
