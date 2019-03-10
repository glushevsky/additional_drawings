from a1_functions import *


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