from PIL import Image

# Открываем исходное изображение
img = Image.open('roses.png')
width, height = img.size

# Создаем новое изображение шириной в 2 раза больше исходного
# Высота остается той же
new_width = width * 2
mirror_img = Image.new('RGB', (new_width, height))

# Вставляем исходное изображение слева
mirror_img.paste(img, (0, 0))

# Создаем отраженную копию (отражение по вертикальной оси)
flipped_img = img.transpose(Image.FLIP_LEFT_RIGHT)

# Вставляем отраженное изображение справа
mirror_img.paste(flipped_img, (width, 0))

# Сохраняем результат
mirror_img.save('mirror.png')
