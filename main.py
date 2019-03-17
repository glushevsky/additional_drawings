# import sys
# import matplotlib.pyplot as plt
# import scipy.misc as smp

from image_functions import *


def main(scale, w, f, T, error, width, height, step, m_step):
    time_start = datetime.datetime.now()
    a1_line_points = get_line_points(w, f, T, error, width, height, step, scale)
    print(len(a1_line_points))
    create_image(width, height, a1_line_points, scale, 'a1_lines.png')
    print('create img in ', datetime.datetime.now() - time_start)
    time_start = datetime.datetime.now()
    a1_line_sign_points = modify_points_by_sign(w, f, T, a1_line_points)
    print(len(a1_line_sign_points))
    create_image(width, height, a1_line_sign_points, scale, 'a1_lines_with_sign.png')
    print('create img in ', datetime.datetime.now() - time_start)
    time_start = datetime.datetime.now()
    common_points = get_common_points(w, f, T, error, width, height, step, scale, m_step)
    print(len(common_points))
    create_image(width, height, common_points, scale, 'common.png')
    print('create img in ', datetime.datetime.now() - time_start)


if __name__ == "__main__":
    scale = 200  # масштаб
    w = 12.0  # параметр омега-малое
    f = 0.0  # параметр фи
    T = 5 + 50*math.pi  # запаздывание
    error = 0.0001  # величина погрешности от нуля (лучше задавать равной шагу)
    width = 500  # половина ширины картинки
    height = 250  # половина высоты картинки
    step = 0.0001  # шаг
    m_step = 0.0000001  # шаг (для мю)
    main(scale, w, f, T, error, width, height, step, m_step)
