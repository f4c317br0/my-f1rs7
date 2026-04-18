# ==============================================================================
# СБОРНИК РЕШЕНИЙ ИЗ ТЕКУЩЕЙ СЕССИИ
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Проверка степени числа (рекурсия)
# ------------------------------------------------------------------------------
def power(number, base):
    """Проверяет, является ли number степенью base."""
    if number == 1:
        return True
    if number < base or base == 1:
        return False
    if number % base != 0:
        return False
    return power(number // base, base)


# ------------------------------------------------------------------------------
# 2. Проверка палиндрома (рекурсия)
# ------------------------------------------------------------------------------
def is_palindrome(text):
    """Проверяет, является ли строка палиндромом (игнорируя регистр и небуквенные символы)."""
    # Фильтруем строку: оставляем только буквы и приводим к нижнему регистру
    filtered = [char.lower() for char in text if char.isalpha()]
    
    def check(left, right):
        if left >= right:
            return True
        if filtered[left] != filtered[right]:
            return False
        return check(left + 1, right - 1)
    
    return check(0, len(filtered) - 1)


# ------------------------------------------------------------------------------
# 3. Перевод в другую систему счисления (рекурсия)
# ------------------------------------------------------------------------------
def convert(number, base):
    """Переводит число из десятичной системы в другую. Возвращает список цифр."""
    if number == 0:
        return [0]
    
    def helper(n):
        if n == 0:
            return []
        return helper(n // base) + [n % base]
    
    return helper(number)


# ------------------------------------------------------------------------------
# 4. Фрактал из пузырьков (рекурсия, PIL)
# ------------------------------------------------------------------------------
def bubbles(draw, side_length, radius, color, iterations, x=0, y=0):
    """Рисует фрактал из пузырьков."""
    # Рисуем текущий круг
    draw.ellipse(
        (x - radius, y - radius, x + radius, y + radius),
        outline=color,
        width=3
    )

    if iterations <= 0:
        return

    # Координаты вершин ромба: верх, низ, лево, право
    centers = [
        (x, y - side_length),
        (x, y + side_length),
        (x - side_length, y),
        (x + side_length, y)
    ]

    for cx, cy in centers:
        bubbles(draw, side_length / 3, radius / 2, color, iterations - 1, cx, cy)


# ------------------------------------------------------------------------------
# 5. Количество путей в Королевстве чисел (рекурсия с мемоизацией)
# ------------------------------------------------------------------------------
def paths(a, b):
    """Считает количество путей от a до b по правилам: +1, +3, *2."""
    memo = {}

    def helper(current):
        if current == b:
            return 1
        if current > b:
            return 0
        if current in memo:
            return memo[current]

        count = (
            helper(current + 1) +
            helper(current + 3) +
            helper(current * 2)
        )
        memo[current] = count
        return count

    return helper(a)


# ------------------------------------------------------------------------------
# 6. Накопительная сумма (рекурсия)
# ------------------------------------------------------------------------------
def accumulate_sum(numbers):
    """Возвращает список накопительных сумм."""
    if not numbers:
        return []
    
    def helper(index, current_sum):
        if index == len(numbers):
            return []
        new_sum = current_sum + numbers[index]
        return [new_sum] + helper(index + 1, new_sum)
    
    return helper(0, 0)


# ------------------------------------------------------------------------------
# 7. Судоку (рекурсивный backtracking)
# ------------------------------------------------------------------------------
# Глобальная переменная board предполагается определенной во внешней области видимости
def sudoku():
    """Заполняет глобальную доску board буквами."""
    n = len(board)
    letters = [chr(ord('A') + i) for i in range(n)]

    def is_valid(r, c, letter):
        if letter in board[r]:
            return False
        for i in range(n):
            if board[i][c] == letter:
                return False
        return True

    def solve():
        for r in range(n):
            for c in range(n):
                if board[r][c] == '':
                    for letter in letters:
                        if is_valid(r, c, letter):
                            board[r][c] = letter
                            if solve():
                                return True
                            board[r][c] = ''
                    return False
        return True

    solve()


# ------------------------------------------------------------------------------
# 8. Фрактал из квадратов (рекурсия, PIL)
# ------------------------------------------------------------------------------
def corners(draw, size, color, iterations, x=0, y=0):
    """Рисует вложенные квадраты в углах."""
    if iterations <= 0:
        return

    inset = 10
    new_size = size // 2

    if new_size <= inset * 2:
        return

    # Верхний левый квадрат
    tl_x = x + inset
    tl_y = y + inset
    tl_size = new_size - 2 * inset
    
    # Нижний правый квадрат
    br_x = x + new_size + inset
    br_y = y + new_size + inset
    br_size = new_size - 2 * inset

    draw.rectangle((tl_x, tl_y, tl_x + tl_size, tl_y + tl_size), outline=color, width=3)
    draw.rectangle((br_x, br_y, br_x + br_size, br_y + br_size), outline=color, width=3)

    corners(draw, new_size, color, iterations - 1, x, y)
    corners(draw, new_size, color, iterations - 1, x + new_size, y + new_size)


# ------------------------------------------------------------------------------
# 9. Оформление заказа (декоратор)
# ------------------------------------------------------------------------------
def format_decorator(func):
    """Декоратор для добавления заголовка и разделителя к заказу."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        result.insert(0, "Ваш заказ:")
        result.append("-" * 20)
        return result
    return wrapper

@format_decorator
def order(data):
    """Формирует список строк заказа."""
    sorted_items = sorted(data.items())
    result = []
    total = 0
    for dish, price in sorted_items:
        result.append(f"{dish} - {price}")
        total += price
    result.append(f"Итого: {total}")
    return result


# ------------------------------------------------------------------------------
# 10. Сумма цифр в восьмеричном представлении
# ------------------------------------------------------------------------------
def oct_sum(*numbers):
    """Группирует числа по сумме цифр их восьмеричного представления."""
    result = {}
    for num in numbers:
        oct_repr = oct(num)[2:]
        digit_sum = sum(int(digit) for digit in oct_repr)
        result[digit_sum] = result.get(digit_sum, 0) + 1
    return result


# ------------------------------------------------------------------------------
# 11. Раскраска фигурок (cycle, zip)
# ------------------------------------------------------------------------------
from itertools import cycle

def coloring(colors, figures):
    """Возвращает список кортежей (цвет, фигура) с циклическим повторением цветов."""
    return list(zip(cycle(colors), figures))


# ------------------------------------------------------------------------------
# 12. Группировка людей по возрасту (groupby)
# ------------------------------------------------------------------------------
# Этот код предполагается запускать как отдельный скрипт с чтением из stdin
"""
import sys
from itertools import groupby

lines = sys.stdin.read().strip().split('\n')
data = []
for line in lines:
    parts = line.split()
    age = int(parts[-1])
    name = " ".join(parts[:-1])
    data.append((name, age))

data.sort(key=lambda x: (-x[1], x[0]))

for age, group in groupby(data, key=lambda x: x[1]):
    print(age)
    for person in group:
        print(person[0])
"""


# ------------------------------------------------------------------------------
# 13. Декораторы square и minus для функции multiples
# ------------------------------------------------------------------------------
def square(func):
    def wrapper(*args, **kwargs):
        return [x ** 2 for x in func(*args, **kwargs)]
    return wrapper

def minus(func):
    def wrapper(*args, **kwargs):
        return [x - 1 for x in func(*args, **kwargs)]
    return wrapper

@square
@minus
def multiples(*numbers, key):
    """Возвращает числа, кратные key, после применения декораторов (вычитание 1, затем квадрат)."""
    return [num for num in numbers if num % key == 0]


# ------------------------------------------------------------------------------
# 14. Расстояние между многомерными векторами
# ------------------------------------------------------------------------------
import math

def distance(vector1, vector2):
    """Вычисляет евклидово расстояние между двумя векторами."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vector1, vector2)))


# ------------------------------------------------------------------------------
# 15. Группировка студентов по баллам из CSV (groupby)
# ------------------------------------------------------------------------------
# Этот код предполагается запускать как отдельный скрипт с файлом marks.csv
"""
import csv
from itertools import groupby

students = []
with open('marks.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        name = row[1]
        scores = [int(x) for x in row[2:]]
        total = sum(scores)
        students.append((total, name))

students.sort(key=lambda x: -x[0])

count = 0
for score, group in groupby(students, key=lambda x: x[0]):
    if count >= 3:
        break
    print(score)
    for student in group:
        print(student[1])
    count += 1
"""
