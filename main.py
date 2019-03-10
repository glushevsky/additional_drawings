import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import scipy.misc as smp


def formula(x):
    return x**2


def calculate(f, half_width, half_height):
    # Create a 1024x1024x3 array of 8 bit unsigned integers
    data = np.full((2*half_width, 2*half_height, 3), fill_value=[255,255,255], dtype=np.uint8 )
    vertical_edge = abs(half_height)
    for x in np.arange(-half_width, half_width):
        y = formula(x)
        if y <= vertical_edge:
            data[-y + half_width, half_height + x] = [254,0,0]
            f.write(str(x) + ' ' + str(y) + '\n')
    return data


# получение значения А
def calculate_A(b, w, f, T, error):
    a1_denominator = (w**2.0 + b)*math.cos(f) + w*math.sin(f) - b*math.cos(f - w*T)
    if abs(a1_denominator) >= error:
        a1_numerator = -w**3 - (2.0*b + 1.0)*w
        return True, a1_numerator/a1_denominator
    else:
        return False, a1_denominator


# получение значения theta
def get_theta(wT):
    return 2.0*math.pi - wT%(2.0*math.pi)


# получение значения омега
def get_cos_omega(b, w, f, T, A, error):
    delay_cos = math.cos(f - w*T)
    delay_sin = math.sin(f - w*T)
    theta_denominator = (2.0*b + w*A*delay_cos)**2 + (w*A*delay_sin)**2
    if abs(theta_denominator) >= error:
        f_cos = math.cos(f)
        f_sin = math.sin(f)
        theta_numerator = (2.0*(w**2 + b) + w*A*f_cos)*(2.0*b + w*A*delay_cos) + w*(2.0 + A*f_sin)*w*A*delay_sin
        return True, theta_numerator/theta_denominator
    else:
        return False, theta_denominator


# получение всех точек кривых
def get_line_points(width, height, step, scale):
    w = 12.0
    f = 0.0
    T = 162.07963
    error = 0.0001
    theta = get_theta(w*T)
    points = []
    f_cos = open('cos_error.txt', 'w')
    for b in np.arange(-height/scale, height/scale, step):
        is_A_exists, A_value = calculate_A(b, w, f, T, error)
        if is_A_exists:
            is_cos_exists, omega_cos = get_cos_omega(b, w, f, T, A_value, error)
            if is_cos_exists:
                if abs(omega_cos) <= 1.0:
                    omega = math.acos(omega_cos)
                    for period in range(0, 12):  # прохождение 10*2 шагов периодичности по Omega
                        a1 = (theta + omega + period*2*np.pi)*A_value
                        a = a1/T
                        if abs(a) < width/scale:
                            points.append((a, b))
                        a1 = (theta + omega - period * 2 * np.pi) * A_value
                        a = a1 / T
                        if abs(a) < width / scale:
                            print('hi', end='\r')
                            points.append((a, b))
                else:
                    f_cos.write(str(b) + ' ' + str(omega_cos) + '\n')
                    # print('Incorrect value for omega cos: ', omega_cos)
            else:
                print('Omega cos_denominator is below error: ', omega_cos)
        else:
            print('A_denominator is below error: ', A_value)
    f_cos.close()
    return points


def get_status(count, len_points):
    return str(count/len_points*100) + '%'


# создание сетки
def create_grid(width, height, scale):
    data = np.full((2 * height + 1, 2 * width + 1, 3), fill_value=[255, 255, 255], dtype=np.uint8)
    for i in range(0, width, scale):
        data[:, width + i] = [150, 150, 150]
        data[:, width - i] = [150, 150, 150]
    for i in range(0, height, scale):
        data[height + i] = [150, 150, 150]
        data[height - i] = [150, 150, 150]
    data[height] = [0, 0, 0]
    data[:, width] = [0, 0, 0]
    return data


# масштабирование точек на изображение
def transfer_points_to_canvas(width, height, data, points, scale):
    for point in points:
        a_coord = int(round(point[0]*scale))
        b_coord = int(round(point[1]*scale))
        # print(a_coord, b_coord, height - b_coord, width + a_coord)
        try:
            data[height - b_coord][width + a_coord] = [255, 0, 0]
            # data[height - b_coord][width + a_coord] = [255, 0, 0]
        except IndexError:
            pass
    return data


# генерация изображения
def create_image(width, height, points, scale):
    data = create_grid(width, height, scale)
    data = transfer_points_to_canvas(width, height, data, points, scale)
    img = smp.toimage(data)  # Create a PIL image
    img.show()


def main(width, height, step):
    scale = 100  # масштаб
    points = get_line_points(width, height, step, scale)
    create_image(width, height, points, scale)
    # unzipped_data = zip(*points)
    # first_list = list(list(unzipped_data)[0])
    # second_list = list(list(unzipped_data)[1])
    # print(len(first_list), len(second_list))
    # print(list(list(unzipped_data))[0])
    print(len(points))
    print('Paint!')
    # for ee in second_list:
    #     print(ee)
    # print('hi!', end='\r')
    # count = 0
    # len_points = len(points)
    # for el in points:
    #     count += 1
    #     print(get_status(count, len_points))
    #     plt.plot(el[0], el[1], 'ro')
    # plt.axis([0, 6, 0, 20])
    # plt.show()
    ##############################################
    # figure_object = plt.figure()  # creating Figure object
    # plt.axis([-10.0, 10.0, -10.0, 10.0])  # setting the rendering area
    # plt.title('graph for dewpdd')  # creating header
    # plt.grid()  # grid display
    # count = 0
    # len_points = len(points)
    # for el in points:
    #     count += 1
    #     print(get_status(count, len_points), type(el[0]), type(el[1]))
        # plt.scatter(el[0], el[1], s=1, marker='.', c=0)
    # for line in file0:
    #     tmp = line.split(' ')
    #     print "%.2f" % (float(tmp[2]) / iter * 100), '%'
    #     plt.scatter(float(tmp[0]), float(tmp[1]), s=1, marker='.', c=0)
    # plt.show()
    # print('Done!')
    ##############################################
    # f = open('tgdata.dat', 'a')
    # data = calculate(f, 200, 200)
    # f.close()
    # create_image(width, height, points, scale)
    # data = create_grid(width, height)
    # data = np.full((2 * width + 1, 2 * height + 1, 3), fill_value=[255, 255, 255], dtype=np.uint8)
    # print(data[0])
    # data[512,512] = [254,0,0]       # Makes the middle pixel red
    # data[512,513] = [0,0,255]       # Makes the next pixel blue
    # print('__________________')
    # print(data[:,0])
    # img = smp.toimage(data)       # Create a PIL image
    # img.show()                      # View in default viewer
    # print(len(points))
if __name__ == "__main__":
    main(500, 250, 0.0001)
