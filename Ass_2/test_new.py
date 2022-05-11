from polygons_new import *
from sys import argv

try:
    p = Polygons(argv[1])
    p.analyse()
except PolygonsError as e:
    print(f'PolygonsError: {e}')