from common_functions import *


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


# получение всех точек кривых с цветом
def get_line_points(w, f, T, error, width, height, step, scale):
    # w = 12.0
    # f = 0.0
    # T = 162.07963
    # error = 0.0001
    theta = get_theta(w*T)
    print('theta ', theta)
    points = []
    f_cos = open('cos_error.txt', 'w')
    print('-------', height/scale, width*3.0 / scale)
    ttt = 0
    for b in np.arange(-height/scale, height/scale, step):
        is_A_exists, A_value = calculate_A(b, w, f, T, error)
        if is_A_exists:
            is_cos_exists, omega_cos = get_cos_omega(b, w, f, T, A_value, error)
            if is_cos_exists:
                if abs(omega_cos) <= 1.0:
                    omega = math.acos(omega_cos)
                    for period in range(0, 12 + 12*round(T/60)):  # прохождение 10*2 шагов периодичности по Omega
                        a1 = (theta + omega + period*2*np.pi)*A_value
                        # a2 = 50.0*a1/T
                        # print(a1/3.0, width/scale)
                        a1 = a1/3.0
                        if abs(a1) < width*3.0 / scale:
                            ttt += 1
                            # if abs(b) < 0.0001:
                            # print('===>', a1, ' == ', b)
                            points.append((a1/3.0, b, [255, 0, 0], theta, omega + period*2*np.pi))
                        a1 = (theta + omega - period * 2 * np.pi) * A_value
                        a1 = a1/3.0
                        # a2 = 50.0*a1/T
                        if abs(a1) < width*3.0 / scale:
                            ttt += 1
                            # if abs(b) < 0.0001:
                            # print('===>', a1, ' == ', b)
                            points.append((a1, b, [255, 0, 0], theta, omega - period*2*np.pi))
                else:
                    f_cos.write(str(b) + ' ' + str(omega_cos) + '\n')
                    # print('Incorrect value for omega cos: ', omega_cos)
            else:
                print('Omega cos_denominator is below error: ', omega_cos)
        else:
            print('A_denominator is below error: ', A_value)
    print('>>>>>>> ', ttt)
    f_cos.close()
    return points
