from lambda1_functions import *
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

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
        a_coord = int(round(round(point[0], int(math.log10(scale)))*scale, 0))
        # a_coord = int(round(point[0]*scale))
        # print('a transfer ===> ', point[0], round(point[0], int(math.log10(scale))), a_coord)
        b_coord = int(round(point[1]*scale))
        color = point[2]
        # print(a_coord, b_coord, height - b_coord, width + a_coord)
        try:
            data[height - b_coord][width + a_coord] = color
            # data[height - b_coord][width + a_coord] = [255, 0, 0]
        except IndexError:
            pass
    return data


# генерация изображения
def create_image(width, height, points, scale, img_name):
    data = create_grid(width, height, scale)

    # mini-lines
    is_exists = True
    try:
        data[:, width + int(round(0.5 * scale))] = [150, 150, 150]
        data[:, width - int(round(0.5 * scale))] = [150, 150, 150]
        data[height + int(round(0.5 * scale)), :] = [150, 150, 150]
        data[height - int(round(0.5 * scale)), :] = [150, 150, 150]
    except:
        is_exists = False
    data = transfer_points_to_canvas(width, height, data, points, scale)
    print('Width, height, scale: ', width, height, scale)
    print('Data array size: ', data.shape)
    print('Paint!')
    from PIL import Image
    img = Image.fromarray(data, mode='RGB')  # replace z with zz and it will just produce a black image
    draw = ImageDraw.Draw(img)
    font_fname = 'fonts/arial.ttf'
    font_size = 20
    font = ImageFont.truetype(font_fname, font_size)
    draw.text((width, height), "0", font=font, fill='rgb(0, 0, 0)')
    if is_exists:
        draw.text((width + scale/2, height), "0.5", font=font, fill='rgb(0, 0, 0)')
        draw.text((width, height - scale / 2), "0.5", font=font, fill='rgb(0, 0, 0)')
    # draw.text((width + scale/2, height), "0.5", font=font, fill='rgb(0, 0, 0)')
    # draw.text((width + scale, height), "1", font=font, fill='rgb(0, 0, 0)')

    iwidth, iheight = img.size
    print('Image size: ', iwidth, iheight)

    img.save(img_name)
    # img.show()