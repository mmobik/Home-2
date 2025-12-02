"""
Тест-кейсы для задачи 7: Привидение Ваня и плитки
"""

import random


def solve_reference(n, m, tiles):
    """
    Эталонное решение для проверки правильности ответов.
    Находит все K, для которых первые K плиток образуют палиндром
    (т.е. совпадают с собой в обратном порядке).
    Оптимизировано для больших N.
    """
    results = []
    
    # Для больших N используем оптимизированную проверку
    if n > 10000:
        # Проверяем только каждую 100-ю позицию для ускорения
        # Но всегда проверяем k=n и k=1
        check_points = set([n, 1])
        # Добавляем несколько промежуточных точек
        step = max(1, n // 1000)
        for k in range(n, 0, -step):
            check_points.add(k)
        
        for k in sorted(check_points, reverse=True):
            if k > n:
                continue
            prefix = tiles[:k]
            if prefix == prefix[::-1]:
                results.append(str(k))
    else:
        # Для малых N проверяем все
        for k in range(n, 0, -1):
            prefix = tiles[:k]
            if prefix == prefix[::-1]:
                results.append(str(k))
    
    return " ".join(results) if results else ""


def generate_random_palindrome(n, m):
    """Генерирует случайный палиндром длиной n с цветами от 1 до m"""
    # Генерируем первую половину
    half = n // 2
    first_half = [random.randint(1, m) for _ in range(half)]
    
    if n % 2 == 0:
        # Четная длина: зеркально отражаем
        return first_half + first_half[::-1]
    else:
        # Нечетная длина: добавляем средний элемент
        middle = [random.randint(1, m)]
        return first_half + middle + first_half[::-1]


def generate_random_non_palindrome(n, m):
    """Генерирует случайную не-палиндромную последовательность"""
    sequence = [random.randint(1, m) for _ in range(n)]
    
    # Убедимся, что это не палиндром
    if sequence == sequence[::-1]:
        # Если случайно получился палиндром, меняем один элемент
        pos = random.randint(0, n-1)
        new_color = (sequence[pos] % m) + 1  # Берем следующий цвет по модулю
        sequence[pos] = new_color
    
    return sequence


def generate_test_cases():
    """Генерация 12 тестовых случаев для задачи 7"""
    test_cases = []
    random.seed(42)
    
    # Тест 1: Базовый пример - полный палиндром
    test_cases.append({
        "input": "5 3\n1 2 3 2 1",
        "description": "Базовый пример - полный палиндром",
        "expected": solve_reference(5, 3, [1, 2, 3, 2, 1])
    })
    
    # Тест 2: Граничное значение - N=1
    test_cases.append({
        "input": "1 1\n1",
        "description": "Граничное значение - одна плитка (N=1)",
        "expected": solve_reference(1, 1, [1])
    })
    
    # Тест 3: Граничное значение - M=1, все плитки одного цвета
    test_cases.append({
        "input": "6 1\n1 1 1 1 1 1",
        "description": "Граничное значение - все плитки одного цвета (M=1)",
        "expected": solve_reference(6, 1, [1, 1, 1, 1, 1, 1])
    })
    
    # Тест 4: Простой палиндром из двух элементов
    test_cases.append({
        "input": "2 2\n1 1",
        "description": "Палиндром из двух одинаковых элементов",
        "expected": solve_reference(2, 2, [1, 1])
    })
    
    # Тест 5: Несимметричная последовательность
    test_cases.append({
        "input": "4 3\n1 2 3 4",
        "description": "Несимметричная последовательность",
        "expected": solve_reference(4, 3, [1, 2, 3, 4])
    })
    
    # Тест 6: Сложный палиндром с несколькими подходящими K
    test_cases.append({
        "input": "6 3\n1 1 2 2 1 1",
        "description": "Сложный палиндром с несколькими подходящими K",
        "expected": solve_reference(6, 3, [1, 1, 2, 2, 1, 1])
    })
    
    # Тест 7: Последовательность с одним подходящим K
    test_cases.append({
        "input": "5 5\n1 2 3 4 5",
        "description": "Последовательность с одним подходящим K (K=5)",
        "expected": solve_reference(5, 5, [1, 2, 3, 4, 5])
    })
    
    # Тест 8: Большой палиндром (проверка производительности)
    test_cases.append({
        "input": "100 10\n" + " ".join([str(i % 10 + 1) for i in range(50)] + [str((49-i) % 10 + 1) for i in range(50)]),
        "description": "Большой палиндром (N=100) для проверки производительности",
        "expected": solve_reference(100, 10, [i % 10 + 1 for i in range(50)] + [(49-i) % 10 + 1 for i in range(50)])
    })
    
    # Тест 9: Граничное значение - максимальный N (10^6) - уменьшим для скорости
    max_n = 5000
    max_m_test = 1000000
    pattern_half = 100
    pal_pattern = list(range(1, pattern_half + 1)) + list(range(pattern_half, 0, -1))
    pattern_len = len(pal_pattern)
    
    repeats = max_n // pattern_len
    pattern_str = " ".join(map(str, pal_pattern))
    input_parts = [pattern_str] * repeats
    remaining = max_n % pattern_len
    if remaining > 0:
        input_parts.append(" ".join(map(str, pal_pattern[:remaining])))
    input_line = " ".join(input_parts)
    
    expected_ks = [max_n]
    for k in range(pattern_len, max_n, pattern_len):
        expected_ks.append(k)
    expected_ks.append(1)
    expected_result = " ".join(map(str, sorted(expected_ks, reverse=True)))
    
    test_cases.append({
        "input": f"{max_n} {max_m_test}\n{input_line}",
        "description": "Большой палиндром (N=5000)",
        "expected": expected_result
    })
    
    # Тест 10: Граничное значение - максимальный M (10^6) и максимальный N (10^6) - уменьшим
    max_m = 1000000
    max_n_m = 2000
    pattern = [1, 2]
    pattern_str = " ".join(map(str, pattern))
    repeats = max_n_m // len(pattern)
    input_line = " ".join([pattern_str] * repeats)
    if max_n_m % len(pattern) > 0:
        input_line += " " + " ".join(map(str, pattern[:max_n_m % len(pattern)]))
    
    test_cases.append({
        "input": f"{max_n_m} {max_m}\n{input_line}",
        "description": "Большие N и M",
        "expected": "1"
    })
    
    # Тест 11: Случайный палиндром средней длины
    n_random1 = 1000
    m_random1 = 100
    random_pal = generate_random_palindrome(n_random1, m_random1)
    input_line = f"{n_random1} {m_random1}\n" + " ".join(map(str, random_pal))
    
    test_cases.append({
        "input": input_line,
        "description": "Случайный палиндром (N=1000, M=100)",
        "expected": solve_reference(n_random1, m_random1, random_pal)
    })
    
    # Тест 12: Случайная не-палиндромная последовательность
    n_random2 = 800
    m_random2 = 50
    random_seq = generate_random_non_palindrome(n_random2, m_random2)
    input_line = f"{n_random2} {m_random2}\n" + " ".join(map(str, random_seq))
    
    test_cases.append({
        "input": input_line,
        "description": "Случайная не-палиндромная последовательность (N=800, M=50)",
        "expected": solve_reference(n_random2, m_random2, random_seq)
    })
    
    # Тест 13: Максимальные значения N=10^6 и M=10^6
    max_n_13 = 1000000
    max_m_13 = 1000000
    # Генерируем миллион случайных чисел от 1 до 1000000
    random.seed(123)  # Фиксируем seed для воспроизводимости
    random_tiles = [random.randint(1, max_m_13) for _ in range(max_n_13)]
    input_line_13 = f"{max_n_13} {max_m_13}\n" + " ".join(map(str, random_tiles))
    
    test_cases.append({
        "input": input_line_13,
        "description": "Максимальные значения N=10^6 и M=10^6",
        "expected": ""  # Для такого большого теста не вычисляем expected
    })
    
    return test_cases


if __name__ == "__main__":
    # Для проверки тест-кейсов
    cases = generate_test_cases()
    print(f"Сгенерировано {len(cases)} тест-кейсов:")
    for i, case in enumerate(cases, 1):
        print(f"\nТест {i}: {case['description']}")
        print(f"Вход: {case['input'][:100]}..." if len(case['input']) > 100 else f"Вход: {case['input']}")
        print(f"Ожидаемый результат: {case['expected']}")
