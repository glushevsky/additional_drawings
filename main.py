# import sys
# import matplotlib.pyplot as plt
# import scipy.misc as smp

from image_functions import *


def main(scale, w, f, T, error, width, height, step, m_step):
    time_start = datetime.datetime.now()
    name_part = 'T' + str(round(T)) + '_w' + str(round(w)) + '_f' + str(round(f)) + '_x' + str(scale)
    a1_line_points = get_line_points(w, f, T, error, width, height, step, scale)
    print(len(a1_line_points))
    img_path = 'a_images/' + 'vertical_' + name_part + '.png'
    create_image(width, height, a1_line_points, scale, img_path)
    print('create img in ', datetime.datetime.now() - time_start)
    # time_start = datetime.datetime.now()
    # a1_line_sign_points = modify_points_by_sign(w, f, T, a1_line_points)
    # print(len(a1_line_sign_points))
    # create_image(width, height, a1_line_sign_points, scale, 'a_sign_' + name_part + '.png')
    # print('create img in ', datetime.datetime.now() - time_start)
    # time_start = datetime.datetime.now()
    common_points = get_common_points(w, f, T, error, width, height, step, scale, m_step)
    print(len(common_points))
    img_path = 'common_images/' + 'common_' + name_part + '.png'
    create_image(width, height, common_points, scale, img_path)
    print('create img in ', datetime.datetime.now() - time_start)


if __name__ == "__main__":
    scale = 2000  # масштаб
    w = 1.0  # параметр омега-малое
    f = 0.0  # параметр фи
    T = 1000.0 + 3.0*math.pi/2.0  # запаздывание
    error = 0.0001  # величина погрешности от нуля (лучше задавать равной шагу)
    width = 1200  # половина ширины картинки
    height = 1200  # половина высоты картинки
    step = 0.0001  # шаг
    m_step = 0.000001  # шаг (для мю)
    print('масштаб x', scale)
    print('w ', w)
    print('f ', f)
    print('T ', T)
    main(scale, w, f, T, error, width, height, step, m_step)
