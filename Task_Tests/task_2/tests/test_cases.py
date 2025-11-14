import random

def can_split(chapters, k, max_pages):
    """Проверяет, можно ли разбить главы на k томов с максимальной толщиной max_pages"""
    volumes = 1
    current_pages = 0
    
    for pages in chapters:
        if current_pages + pages <= max_pages:
            current_pages += pages
        else:
            volumes += 1
            current_pages = pages
            if volumes > k:
                return False
    return True

def solve_book_problem(input_data):
    """
    Решает задачу с романом в томах и возвращает правильный ответ
    Используется для вычисления ожидаемых значений в больших тестах
    """
    lines = input_data.strip().split('\n')
    n = int(lines[0])
    chapters = list(map(int, lines[1].split()))
    k = int(lines[2])
    
    left = max(chapters)
    right = sum(chapters)
    
    while left < right:
        mid = (left + right) // 2
        if can_split(chapters, k, mid):
            right = mid
        else:
            left = mid + 1
    
    return left

def generate_book_test(n, k=None, min_pages=1, max_pages=100):
    """
    Генерация теста для задачи с романом в томах
    Формат: N (количество глав), затем N чисел через пробел, затем K (количество томов)
    K должно быть в диапазоне 1 ≤ K ≤ N
    """
    if k is None:
        k = random.randint(1, n)
    else:
        # Убеждаемся, что K ≤ N
        k = min(k, n)
    chapters = [str(random.randint(min_pages, max_pages)) for _ in range(n)]
    lines = [str(n), " ".join(chapters), str(k)]
    return "\n".join(lines)

def generate_basic_cases():
    """
    Генерация базовых граничных тестовых случаев
    """
    return [
        {
            "input": "3\n1 2 1\n2",
            "description": "Пример 1: 3 главы, 2 тома",
            "expected": 3
        },
        {
            "input": "4\n1 2 1 1\n3",
            "description": "Пример 2: 4 главы, 3 тома",
            "expected": 2
        },
        {
            "input": "1\n10\n1",
            "description": "Одна глава, один том",
            "expected": 10
        },
        {
            "input": "5\n10 20 30 40 50\n1",
            "description": "Все главы в один том",
            "expected": 150
        },
        {
            "input": "5\n10 20 30 40 50\n5",
            "description": "Каждая глава в отдельный том",
            "expected": 50
        },
        {
            "input": "10\n1 1 1 1 1 1 1 1 1 1\n2",
            "description": "Равномерное распределение",
            "expected": 5
        },
        {
            "input": "10\n1 1 1 1 1 1 1 1 1 1\n3",
            "description": "Равномерное распределение на 3 тома",
            "expected": 4
        },
        {
            "input": "4\n100 1 1 1\n2",
            "description": "Одна большая глава и маленькие",
            "expected": 100
        },
        {
            "input": "6\n1 2 3 4 5 6\n3",
            "description": "Возрастающая последовательность",
            "expected": 9
        },
    ]

def generate_large_cases():
    """
    Генерация нагрузочных тестовых случаев с вычислением правильных ответов
    Все большие тесты используют max_pages=32767 (максимум по условию задачи)
    """
    tests = []
    
    # Тест 1: 50 глав, 10 томов
    test1_input = generate_book_test(50, k=10, max_pages=32767)
    tests.append({
        "input": test1_input,
        "description": "50 глав, 10 томов, до 32767 страниц",
        "expected": solve_book_problem(test1_input)
    })
    
    # Тест 2: 100 глав, 1 том
    test2_input = generate_book_test(100, k=1, max_pages=32767)
    tests.append({
        "input": test2_input,
        "description": "100 глав, 1 том, до 32767 страниц",
        "expected": solve_book_problem(test2_input)
    })
    
    # Тест 3: 100 глав, 100 томов (K = N, каждая глава отдельно)
    test3_input = generate_book_test(100, k=100, max_pages=32767)
    tests.append({
        "input": test3_input,
        "description": "100 глав, 100 томов (каждая глава отдельно), до 32767 страниц",
        "expected": solve_book_problem(test3_input)
    })
    
    # Тест 4: 100 глав, 50 томов
    test4_input = generate_book_test(100, k=50, max_pages=32767)
    tests.append({
        "input": test4_input,
        "description": "100 глав, 50 томов, до 32767 страниц",
        "expected": solve_book_problem(test4_input)
    })
    
    return tests

def generate_test_cases():
    """
    Объединение всех тестовых случаев
    """
    return generate_basic_cases() + generate_large_cases()

