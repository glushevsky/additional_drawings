import numpy as np
import math
import datetime


def get_a_null_case(b, w, f, T):
    a = w*(1.0 - b*T)/(math.sin(f) - math.sin(f - w*T))
    return a


def get_b_null_case(a, w, f, T):
    b = (w - a*(math.sin(f) - math.sin(f - w*T)))/(w*T)
    return b


def get_utility_m_case(w, f, T):
    w_sin = w*math.sin(f)
    cos = math.cos(f)
    w_big_sin = w*math.sin(f - w*T)
    big_cos = math.cos(f - w*T)
    return w_sin, cos, w_big_sin, big_cos



def get_parts_m_case(T, m, w_sin, cos, w_big_sin, big_cos):
    first_part = w_sin - w_big_sin*math.cos(m*T) - m*big_cos*math.sin(m*T)
    second_part = w_big_sin*math.sin(m*T) + m*(cos - big_cos*math.cos(m*T))
    return first_part, second_part


def get_b_m_case(T, m, first_part, second_part):
    b = m*(second_part - m*first_part)/((1.0 - math.cos(m*T))*first_part + math.sin(m*T)*second_part)
    return b


def get_a_m_case(b, w, T, m, first_part):
    a = (w**2 - m**2)*(1.0 - b*math.sin(m*T)/m)/first_part
    return a


def get_parts_w_case(w, f, T):
    first_part = (math.cos(f)*math.sin(2.0*w*T) + math.sin(f)*(1.0 - math.cos(2.0*w*T)))/(4.0*w) + T*math.cos(f)/2.0
    second_part = ( math.sin(f)*math.sin(2.0*w*T) - math.cos(f)*(1.0 - math.cos(2.0*w*T)))/(4.0*w) - T*math.cos(f)/2.0
    return first_part, second_part


def get_b_w_case(T, w, first_part, second_part):
    b = w*(first_part - w*second_part)/(first_part*(1.0 - math.cos(w*T)) + second_part*math.sin(w*T))
    return b


def get_a_w_case(b, w, T, first_part):
    a = (1.0 - b*math.sin(w*T)/w)/first_part
    return a


def update_chunk(points, left_edge, right_edge, chunk, m_step, width, height, scale, T, w, w_sin, cos, w_big_sin, big_cos):
    for m in np.arange(left_edge + 3.0 * chunk, right_edge + 3.0 * chunk, m_step):
        first_part, second_part = get_parts_m_case(T, m, w_sin, cos, w_big_sin, big_cos)
        b = get_b_m_case(T, m, first_part, second_part)
        a = get_a_m_case(b, w, T, m, first_part)
        a2 = a*T/30.0
        # if abs(b) < 0.0001 and abs(a2) < 10.0:
        #     print('-->', a2, a * 50.0 / 3.0, ' -- ', b)
        if abs(a2) <= width / scale and abs(b) <= height / scale:
            points.append((a2, b, [255, 0, 0]))
    return points


def get_common_points(w, f, T, error, width, height, step, scale, m_step):
    points = []
    # m_step = 0.000001
    # zero case
    for a in np.arange(-width / scale, width / scale, step):
        a2 = a*T/30.0
        points.append((a2, get_b_null_case(a, w, f, T), [0, 255, 0]))
    # m case
    w_sin, cos, w_big_sin, big_cos = get_utility_m_case(w, f, T)
    for chunk in range(0, 5):
        print('chunk: ', chunk + 1)
        chunk_time = datetime.datetime.now()
        points = update_chunk(points, 0.001, 1.001, chunk, m_step, width, height, scale, T, w, w_sin, cos, w_big_sin,
                     big_cos)
        print('---1')
        points = update_chunk(points, 1.001, 2.001, chunk, m_step, width, height, scale, T, w, w_sin, cos, w_big_sin,
                              big_cos)
        print('---2')
        points = update_chunk(points, 2.001, 3.001, chunk, m_step, width, height, scale, T, w, w_sin, cos, w_big_sin,
                              big_cos)
        print('---3')
        # for m in np.arange(0.001 + 3.0*chunk, 1.501 + 3.0*chunk, m_step):
        #     first_part, second_part = get_parts_m_case(T, m, w_sin, cos, w_big_sin, big_cos)
        #     b = get_b_m_case(T, m, first_part, second_part)
        #     a = get_a_m_case(b, w, T, m, first_part)
        #     if abs(a) <= width / scale and abs(b) <= height / scale:
        #         points.append((a, b, [255, 0, 0]))
        # for m in np.arange(1.501 + 3.0*chunk, 3.001 + 3.0*chunk, m_step):
        #     first_part, second_part = get_parts_m_case(T, m, w_sin, cos, w_big_sin, big_cos)
        #     b = get_b_m_case(T, m, first_part, second_part)
        #     a = get_a_m_case(b, w, T, m, first_part)
        #     if abs(a) <= width / scale and abs(b) <= height / scale:
        #         points.append((a, b, [255, 0, 0]))
        print(datetime.datetime.now() - chunk_time)
    # w case
    first_part, second_part = get_parts_w_case(w, f, T)
    b = get_b_w_case(T, w, first_part, second_part)
    a = get_a_w_case(b, w, T, first_part)
    a2 = a*T/30.0
    if abs(a2) <= width / scale and abs(b) <= height / scale:
        points.append((a2, b, [0, 0, 255]))
    return points