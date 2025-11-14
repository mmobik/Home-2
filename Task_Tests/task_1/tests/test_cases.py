import random

def generate_wire_test(n, k=None, min_length=1, max_length=10**6):
    """
    Генерация теста для задачи с проводами
    """
    if k is None:
        k = random.randint(1, n * 10)
    wires = [str(random.randint(min_length, max_length)) for _ in range(n)]
    lines = [f"{n} {k}"] + wires
    return "\n".join(lines)

def generate_basic_cases():
    """
    Генерация базовых граничных тестовых случаев
    """
    return [
        {"input": "1 1\n1", "description": "Один провод, один кусок", "expected": 1},
        {"input": "2 2\n2\n2", "description": "Два провода, два куска", "expected": 2},
        {"input": "3 5\n10\n15\n20", "description": "Три провода, пять кусков (правильный ответ: 7)", "expected": 7},
        {"input": "2 5\n4\n5", "description": "Провода впритык (правильный ответ: 1)", "expected": 1},
        {"input": "5 1\n100\n200\n300\n400\n500", "description": "Максимально длинный кусок", "expected": 500},
        {"input": "5 15\n10\n10\n10\n10\n10", "description": "Много маленьких кусков", "expected": 3},
        {"input": "5 100\n100\n100\n100\n100\n100", "description": "Много кусков, большие провода (правильный ответ: 5)", "expected": 5},
        {"input": "10 50\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10", "description": "Распределение длин разное (правильный ответ: 1)", "expected": 1},
        {"input": "2 4\n1\n100000", "description": "Очень небольшой и очень большой провод", "expected": 25000},
    ]

def generate_large_cases():
    """
    Генерация нагрузочных тестовых случаев
    """
    tests = [
        {
            "input": generate_wire_test(20000, max_length=10**9),
            "description": "20 000 проводов, длины до 10^9",
            "expected": "large_result"
        },
        {
            "input": generate_wire_test(10000, max_length=10000),
            "description": "10 000 проводов, длины до 10 000",
            "expected": "large_result"
        },
    ]
    # Новый большой тест на 100 000 проводов, длины до 10^9, минимум 100 000 кусочков
    tests.append({
        "input": generate_wire_test(100000, k=100000, min_length=1, max_length=10**9),
        "description": "100 000 проводов, длины до 10^9, минимум 100 000 кусочков",
        "expected": "large_result"
    })
    return tests

def generate_test_cases():
    """
    Объединение всех тестовых случаев
    """
    return generate_basic_cases() + generate_large_cases()
