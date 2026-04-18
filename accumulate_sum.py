def accumulate_sum(numbers, current_sum=0):
    """
    Рекурсивная функция для вычисления накопительной суммы списка чисел.
    
    Args:
        numbers: список чисел
        current_sum: текущая накопленная сумма (используется для рекурсии)
    
    Returns:
        Новый список с накопительными суммами.
    """
    if not numbers:
        return []
    
    current_sum += numbers[0]
    return [current_sum] + accumulate_sum(numbers[1:], current_sum)
