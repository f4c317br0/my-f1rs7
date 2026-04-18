from functools import reduce

# Чтение входных данных
first_line = input().split()
start_coef = int(first_line[0])
step = int(first_line[1])

numbers = list(map(int, input().split()))

# Генерация коэффициентов: start, start+step, start+2*step, ...
coefficients = [start_coef + i * step for i in range(len(numbers))]

# Использование zip для пар (число, коэффициент) и reduce для суммирования произведений
result = reduce(lambda acc, pair: acc + pair[0] * pair[1], zip(numbers, coefficients), 0)

print(result)
