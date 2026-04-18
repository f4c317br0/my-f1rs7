from PIL import Image, ImageDraw


def bubbles(draw, side_length, radius, color, iterations, x=0, y=0):
    """
    Рекурсивная функция для рисования фрактала из пузырьков по вершинам ромба.

    Args:
        draw: объект ImageDraw для рисования
        side_length: длина стороны ромба
        radius: радиус текущего круга
        color: цвет линии
        iterations: количество оставшихся итераций
        x, y: координаты центра текущего круга
    """
    # Рисуем текущий круг
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=color, width=3)

    # Если есть оставшиеся итерации, рисуем подфракталы
    if iterations > 0:
        # Координаты вершин ромба
        top = (x, y - side_length)
        bottom = (x, y + side_length)
        left = (x - side_length, y)
        right = (x + side_length, y)

        # Рекурсивно вызываем для каждой вершины
        for cx, cy in [top, bottom, left, right]:
            bubbles(draw, side_length / 3, radius / 2, color, iterations - 1, cx, cy)


# Функция для создания полного изображения
def create_bubbles_fractal(image_size, side_length, center_radius, color, iterations, filename="bubbles_fractal.png"):
    """
    Создаёт изображение с фракталом из пузырьков.

    Args:
        image_size: размер изображения (ширина и высота)
        side_length: длина стороны ромба
        center_radius: радиус самого первого круга
        color: цвет линии
        iterations: количество итераций
    """
    # Создаём новое изображение
    img = Image.new('RGB', (image_size, image_size), 'white')
    draw = ImageDraw.Draw(img)

    # Вычисляем центр изображения
    center_x = image_size // 2
    center_y = image_size // 2

    # Запускаем рекурсивное рисование из центра
    bubbles(draw, side_length, center_radius, color, iterations, center_x, center_y)

    return img


if __name__ == "__main__":
    create_bubbles_fractal(
        image_size=900,
        side_length=390,
        center_radius=80,
        color="crimson",
        iterations=4
    ).save("example.png")
