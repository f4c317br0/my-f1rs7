def convert(number, base):
    """
    Рекурсивная функция для перевода числа из десятичной системы счисления
    в любую другую (кроме унарной).
    
    Возвращает список "цифр" числа в правильном порядке (от старших к младшим).
    """
    if number < base:
        return [number]
    else:
        return convert(number // base, base) + [number % base]
