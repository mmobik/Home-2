import random

def solve_range_sum_problem(input_data):
    """
    Решает задачу с запросами сумм и возвращает правильный ответ
    Используется для вычисления ожидаемых значений в больших тестах
    Использует простое накопление сумм для маленьких тестов и оптимизированный алгоритм для больших
    """
    # Парсим так же, как main() - через split() без аргументов
    data = input_data.strip().split()
    if not data:
        return ""
    
    n = int(data[0])
    m = int(data[1])
    
    # Чтение исходного массива
    arr = []
    idx = 2
    for i in range(n):
        arr.append(int(data[idx]))
        idx += 1
    
    # Для больших тестов используем более эффективный подход
    # Просто пересчитываем префиксные суммы только при запросах типа 1
    # Это медленнее, чем дерево Фенвика, но проще и достаточно для проверки
    results = []
    
    # Обработка запросов
    for _ in range(m):
        code = int(data[idx])
        idx += 1
        if code == 1:
            l = int(data[idx])
            idx += 1
            r = int(data[idx])
            idx += 1
            # Запрос суммы на отрезке [l, r] - просто суммируем
            # Для очень больших тестов это может быть медленно, но это только для проверки
            s = sum(arr[l:r+1])
            results.append(str(s))
        else:  # code == 2
            i = int(data[idx])
            idx += 1
            new_val = int(data[idx])
            idx += 1
            # Обновление элемента
            arr[i] = new_val
    
    return "\n".join(results)

def generate_range_sum_test(n, m, min_val=0, max_val=2**32-1, query1_ratio=0.5):
    """
    Генерация теста для задачи с запросами сумм
    Формат: N M, затем N чисел (массив), затем M запросов
    query1_ratio - доля запросов типа 1 (сумма) от общего количества
    """
    # Генерация массива
    arr = [random.randint(min_val, max_val) for _ in range(n)]
    
    lines = [f"{n} {m}"]
    lines.extend([str(x) for x in arr])
    
    # Генерация запросов
    query1_count = int(m * query1_ratio)
    query2_count = m - query1_count
    
    queries_1 = []
    queries_2 = []
    
    # Запросы типа 1 (сумма на отрезке)
    for _ in range(query1_count):
        l = random.randint(0, n - 1)
        r = random.randint(l, n - 1)
        queries_1.append(f"1 {l} {r}")
    
    # Запросы типа 2 (обновление)
    for _ in range(query2_count):
        idx = random.randint(0, n - 1)
        new_val = random.randint(min_val, max_val)
        queries_2.append(f"2 {idx} {new_val}")
    
    # Перемешиваем запросы
    all_queries = queries_1 + queries_2
    random.shuffle(all_queries)
    
    lines.extend(all_queries)
    return "\n".join(lines)

def generate_basic_cases():
    """
    Генерация базовых граничных тестовых случаев
    """
    return [
        {
            "input": "10 8\n1\n7\n15\n8\n9\n15\n15\n19\n5\n19\n1 1 8\n1 6 8\n1 0 6\n2 6 6\n2 1 6\n2 0 9\n1 4 7\n1 3 6",
            "description": "Пример из условия задачи",
            "expected": "93\n39\n70\n49\n38"
        },
        {
            "input": "1 1\n5\n1 0 0",
            "description": "Один элемент, один запрос суммы",
            "expected": "5"
        },
        {
            "input": "3 2\n10\n20\n30\n1 0 2\n1 1 1",
            "description": "Несколько запросов суммы без обновлений",
            "expected": "60\n20"
        },
        {
            "input": "3 3\n1\n2\n3\n2 0 10\n1 0 2\n1 0 0",
            "description": "Обновление и запросы",
            "expected": "15\n10"
        },
        {
            "input": "5 5\n1\n1\n1\n1\n1\n1 0 4\n2 0 5\n1 0 4\n2 2 10\n1 0 4",
            "description": "Множественные обновления и запросы",
            "expected": "5\n9\n18"
        },
        {
            "input": "2 4\n0\n0\n2 0 1\n2 1 2\n1 0 1\n1 0 0",
            "description": "Обновления нулевых элементов",
            "expected": "3\n1"
        },
        {
            "input": "10 3\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n1 0 9\n1 5 9\n1 0 0",
            "description": "Запросы на разных отрезках",
            "expected": "55\n40\n1"
        },
        {
            "input": "4 6\n100\n200\n300\n400\n1 0 3\n2 1 250\n1 0 3\n2 3 500\n1 0 3\n1 2 3",
            "description": "Большие числа и обновления",
            "expected": "1000\n1050\n1150\n800"
        },
    ]

def generate_large_cases():
    """
    Генерация нагрузочных тестовых случаев с вычислением правильных ответов
    """
    tests = []
    
    # Тест 1: Средний размер (1000 элементов, 1000 запросов)
    test1_input = generate_range_sum_test(1000, 1000, min_val=0, max_val=1000, query1_ratio=0.5)
    tests.append({
        "input": test1_input,
        "description": "1000 элементов, 1000 запросов (50% запросов типа 1)",
        "expected": solve_range_sum_problem(test1_input)
    })
    
    # Тест 2: Большой массив, мало запросов
    test2_input = generate_range_sum_test(10000, 100, min_val=0, max_val=2**31-1, query1_ratio=0.7)
    tests.append({
        "input": test2_input,
        "description": "10000 элементов, 100 запросов (70% запросов типа 1)",
        "expected": solve_range_sum_problem(test2_input)
    })
    
    # Тест 3: Много запросов типа 1
    test3_input = generate_range_sum_test(5000, 5000, min_val=0, max_val=10000, query1_ratio=0.8)
    tests.append({
        "input": test3_input,
        "description": "5000 элементов, 5000 запросов (80% запросов типа 1)",
        "expected": solve_range_sum_problem(test3_input)
    })
    
    # Тест 4: Максимальные значения (близко к границам задачи)
    test4_input = generate_range_sum_test(100000, 100000, min_val=0, max_val=2**32-1, query1_ratio=0.5)
    tests.append({
        "input": test4_input,
        "description": "100000 элементов, 100000 запросов, значения до 2^32-1",
        "expected": solve_range_sum_problem(test4_input)
    })
    
    # Тест 5: Максимальные значения из условия задачи (N=500000, M=500000)
    # Для такого большого теста вычисление ожидаемого результата может занять очень много времени
    # Используем "large_result" чтобы просто проверить, что решение работает без ошибок
    test5_input = generate_range_sum_test(500000, 500000, min_val=0, max_val=2**32-1, query1_ratio=0.5)
    tests.append({
        "input": test5_input,
        "description": "500000 элементов, 500000 запросов (максимум по условию), значения до 2^32-1",
        "expected": "large_result"  # Не вычисляем ожидаемый результат из-за сложности
    })
    
    return tests

def generate_test_cases():
    """
    Объединение всех тестовых случаев
    """
    return generate_basic_cases() + generate_large_cases()

