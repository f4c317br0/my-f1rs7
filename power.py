def power(number, base):
    """
    Рекурсивная функция для проверки, является ли число степенью заданного основания.
    
    :param number: число для проверки
    :param base: основание степени
    :return: True или False
    """
    # Базовый случай: если число равно 1, это степень (base^0 = 1)
    if number == 1:
        return True
    
    # Если число меньше основания или не делится нацело, это не степень
    if number < base or number % base != 0:
        return False
    
    # Рекурсивный вызов для частного
    return power(number // base, base)


# Примеры использования
if __name__ == "__main__":
    print(power(81, 3))  # True (3^4 = 81)
    print(power(30, 2))  # False
