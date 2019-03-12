# import sys
# import matplotlib.pyplot as plt
import datetime
# import scipy.misc as smp

from image_functions import *


def main(scale, w, f, T, error, width, height, step):
    time_start = datetime.datetime.now()
    points = get_line_points(w, f, T, error, width, height, step, scale)
    create_image(width, height, points, scale)
    print('create img in ', datetime.datetime.now() - time_start)
    print(len(points))


if __name__ == "__main__":
    scale = 100  # масштаб
    w = 12.0  # параметр омега-малое
    f = 0.0  # параметр фи
    T = 5 + 50*math.pi  # запаздывание
    error = 0.0001  # величина погрешности от нуля (лучше задавать равной шагу)
    main(scale, w, f, T, error, 500, 250, 0.0001)
