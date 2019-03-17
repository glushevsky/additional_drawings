from a1_functions import *


def calculate_A_Re1(w, f, T, theta, omega, a1, b):
    t_o_sum = theta + omega
    omega_cos= math.cos(omega)
    omega_sin = math.sin(omega)
    f_cos = math.cos(f)
    A_Re1 = t_o_sum**2 * (-5*w**2 - b + b*omega_cos) + t_o_sum*(-2*w*a1*f_cos+omega_cos*2*w*a1*math.cos(f - w*T) - omega_sin*w**2 *a1*math.sin(f - w*T))
    return A_Re1


def calculate_B_Re1(w, f, T, theta, omega, a1, b):
    B_Re1 = -2*w**2+math.cos(omega)*(w**2*a1*math.cos(f-w*T) + 2*w*b*(theta+omega)) - math.sin(omega)*w**2*a1*math.sin(f-w*T)
    return B_Re1


def calculate_A_Im1(w, f, T, theta, omega, a1, b):
    A_Im1 = (omega + theta)**2*(3*w -b*math.sin(omega))+(omega + theta)*(w*a1*math.sin(f) -2*math.sin(omega)*w*a1*math.cos(f-w*T) - math.cos(omega)*w**2*a1*math.sin(f - w*T))
    return A_Im1


def calculate_B_Im1(w, f, T, theta, omega, a1, b):
    B_Im1 = -2*w**2 - 2*w*b-math.sin(omega)*(w**2*a1*math.cos(f-w*T)+2*w*b*(theta+omega)) -math.cos(omega)*w**2*a1*math.sin(f - w*T)
    return B_Im1


def get_sign(w, f, T, theta, omega, a1, b):
    A_Re1 = calculate_A_Re1(w, f, T, theta, omega, a1, b)
    B_Re1 = calculate_B_Re1(w, f, T, theta, omega, a1, b)
    A_Im1 = calculate_A_Im1(w, f, T, theta, omega, a1, b)
    B_Im1 = calculate_B_Im1(w, f, T, theta, omega, a1, b)
    result = A_Re1*B_Re1 + A_Im1*B_Im1
    if result > 0:
        return 1
    elif result < 0:
        return -1
    else:
        return 0


def modify_points_by_sign(w, f, T, points):
    for point in points:
        sign = get_sign(w, f, T, point[3], point[4], point[0]*T, point[1])
        if sign == 1:
            point[2][0] = 255
            point[2][1] = 0
            point[2][2] = 0
        elif sign == -1:
            point[2][0] = 0
            point[2][1] = 255
            point[2][2] = 0
        else:
            point[2][0] = 0
            point[2][1] = 0
            point[2][2] = 0
    return points
