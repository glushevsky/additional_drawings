from lambda1_functions import *
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

# создание сетки
def create_grid(width, height, scale):
    data = np.full((2 * height + 1, 2 * width + 1, 3), fill_value=[255, 255, 255], dtype=np.uint8)
    scale_fit = int(scale/3.0)
    for i in range(0, width, scale_fit):
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
    is_exists_05 = True
    is_exists_001 = True
    is_exists = []
    scale_fit = int(scale/3.0)
    gr_step_fit = int(round(0.1 * scale_fit))
    while gr_step_fit < width:
        data[:, width + gr_step_fit] = [150, 150, 150]
        data[:, width - gr_step_fit] = [150, 150, 150]
        gr_step_fit = gr_step_fit + int(round(0.1 * scale_fit))
    gr_step = int(round(0.1 * scale))
    while gr_step < height:
        data[height + gr_step, :] = [150, 150, 150]
        data[height - gr_step, :] = [150, 150, 150]
        gr_step = gr_step + int(round(0.1 * scale))
    # try:
    #     data[:, width + int(round(0.5 * scale))] = [150, 150, 150]
    #     data[:, width - int(round(0.5 * scale))] = [150, 150, 150]
    #     data[height + int(round(0.5 * scale)), :] = [150, 150, 150]
    #     data[height - int(round(0.5 * scale)), :] = [150, 150, 150]
    # except:
    #     is_exists_05 = False
    # try:
    #     data[:, width + int(round(0.01 * scale))] = [150, 150, 150]
    #     data[:, width - int(round(0.01 * scale))] = [150, 150, 150]
    #     data[height + int(round(0.01 * scale)), :] = [150, 150, 150]
    #     data[height - int(round(0.01 * scale)), :] = [150, 150, 150]
    # except:
    #     is_exists_001 = False
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
    # if is_exists_05:
    #     draw.text((width + scale/2, height), "0.5", font=font, fill='rgb(0, 0, 0)')
    #     draw.text((width, height - scale / 2), "0.5", font=font, fill='rgb(0, 0, 0)')
    # if is_exists_001:
    draw.text((width + scale_fit/10, height), "0.1", font=font, fill='rgb(0, 0, 0)')
    draw.text((width, height - scale / 10), "0.1", font=font, fill='rgb(0, 0, 0)')
    # draw.text((width + scale/2, height), "0.5", font=font, fill='rgb(0, 0, 0)')
    # draw.text((width + scale, height), "1", font=font, fill='rgb(0, 0, 0)')

    iwidth, iheight = img.size
    print('Image size: ', iwidth, iheight)
    print(img_name)
    img.save(img_name)
    # img.show()