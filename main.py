import numpy as np
import math
# import sys
# import matplotlib.pyplot as plt
import datetime
# import scipy.misc as smp


# def formula(x):
#     return x**2


# def calculate(f, half_width, half_height):
#     # Create a 1024x1024x3 array of 8 bit unsigned integers
#     data = np.full((2*half_width, 2*half_height, 3), fill_value=[255,255,255], dtype=np.uint8 )
#     vertical_edge = abs(half_height)
#     for x in np.arange(-half_width, half_width):
#         y = formula(x)
#         if y <= vertical_edge:
#             data[-y + half_width, half_height + x] = [254,0,0]
#             f.write(str(x) + ' ' + str(y) + '\n')
#     return data


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


# def get_status(count, len_points):
#     return str(count/len_points*100) + '%'


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
    # img = smp.toimage(data)  # Create a PIL image
    print('Paint!')
    from PIL import Image
    img = Image.fromarray(data, mode='RGB')  # replace z with zz and it will just produce a black image
    img.save('result.png')
    img.show()


def main(width, height, step):
    scale = 100  # масштаб
    time_start = datetime.datetime.now()
    points = get_line_points(width, height, step, scale)
    create_image(width, height, points, scale)
    print('create img in ', datetime.datetime.now() - time_start)
    print(len(points))


if __name__ == "__main__":
    main(500, 250, 0.0001)
