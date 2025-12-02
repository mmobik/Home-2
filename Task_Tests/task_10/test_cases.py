"""
Тест-кейсы для задачи 10: Слово с забора (разбиение на префиксы)
"""
import random

def generate_test_cases():
    """Генерация тестовых случаев для задачи 10"""
    test_cases = []
    random.seed(42)
    
    # Тест 1: Полное совпадение
    # s2 является префиксом s1
    test_cases.append({
        "input": "abcde\nabc",
        "description": "Вторая строка является префиксом первой",
        "expected": "No\nabc"
    })
    
    # Тест 2: Невозможно составить
    test_cases.append({
        "input": "abc\nd",
        "description": "Невозможно составить (нет нужных символов)",
        "expected": "Yes"
    })
    
    # Тест 3: Простая конкатенация двух префиксов
    # s1 = abacaba
    # s2 = aba + abac = abaabac
    test_cases.append({
        "input": "abacaba\nabaabac",
        "description": "Конкатенация двух префиксов",
        "expected": "No\naba abac"
    })
    
    # Тест 4: Перекрытие префиксов
    # s1 = aba
    # s2 = ababa
    # Вариант: ab (префикс) + aba (префикс) = ababa
    test_cases.append({
        "input": "aba\nababa",
        "description": "Перекрытие префиксов",
        "expected": "No\nab aba"
    })
    
    # Тест 5: Повторение одного префикса
    test_cases.append({
        "input": "abc\nabcabc",
        "description": "Повторение префикса",
        "expected": "No\nabc abc"
    })
    
    # Тест 6: Невозможно из-за суффикса
    test_cases.append({
        "input": "abc\nabcx",
        "description": "Невозможно из-за последнего символа",
        "expected": "Yes"
    })
    
    # Тест 7: Однобуквенные строки (валидный)
    test_cases.append({
        "input": "a\naaaaa",
        "description": "Однобуквенные строки (валидный)",
        "expected": "No\na a a a a"
    })
    
    # Тест 8: Однобуквенные строки (невалидный)
    test_cases.append({
        "input": "a\naaaab",
        "description": "Однобуквенные строки (невалидный)",
        "expected": "Yes"
    })
    
    # Тест 9: Большой валидный тест (много 'a')
    # s1 = 100 'a'
    # s2 = 1000 'a'
    # Ожидаем "No" и какое-то разбиение
    test_cases.append({
        "input": ("a" * 100) + "\n" + ("a" * 1000),
        "description": "Большой валидный тест (много 'a')",
        "expected": "No" # Проверка будет через валидатор
    })
    
    # Тест 10: Большой невалидный тест
    test_cases.append({
        "input": ("a" * 100) + "\n" + ("a" * 999) + "b",
        "description": "Большой невалидный тест",
        "expected": "Yes"
    })
    
    # Тест 11: Случайный валидный тест
    # Генерируем s1, затем составляем s2 из префиксов s1
    s1_rand = "".join(random.choice("abc") for _ in range(50))
    parts = []
    s2_rand = ""
    for _ in range(20):
        # Берем случайный префикс s1
        plen = random.randint(1, len(s1_rand))
        prefix = s1_rand[:plen]
        parts.append(prefix)
        s2_rand += prefix
        
    test_cases.append({
        "input": f"{s1_rand}\n{s2_rand}",
        "description": "Случайный валидный тест (составлен из префиксов)",
        "expected": "No" # Проверка валидатором
    })

    # Тест 12: Большой случайный тест (скорее всего Yes)
    # 1000 символов
    s1_large = "".join(random.choice("abc") for _ in range(1000))
    s2_large = "".join(random.choice("abc") for _ in range(1000))
    test_cases.append({
        "input": f"{s1_large}\n{s2_large}",
        "description": "Большой случайный тест (вероятно Yes)",
        "expected": "N/A" # Не знаем точно, но скорее всего Yes
    })
    
    # Тест 13: Максимальный валидный тест (по условию задачи 75000)
    # Простой случай: s1 и s2 из одинаковых символов
    max_len = 75000
    s1_max_simple = "a" * max_len
    s2_max_simple = "a" * max_len
    test_cases.append({
        "input": f"{s1_max_simple}\n{s2_max_simple}",
        "description": "Граничный тест: 75000 символов 'a'",
        "expected": "No"
    })

    # Тест 14: Граничный сложный тест (75000 символов)
    # s1 - случайная строка
    # s2 - составлена из префиксов s1
    s1_max_complex = "".join(random.choice("abc") for _ in range(max_len))
    s2_max_complex = ""
    
    # Собираем s2 из префиксов s1, пока не достигнем 75000
    current_len = 0
    while current_len < max_len:
        # Берем случайный префикс, но не длиннее оставшегося места
        remaining = max_len - current_len
        # Ограничим длину префикса, чтобы было много частей (нагрузка на DP)
        part_len = random.randint(1, min(remaining, 1000)) 
        
        prefix = s1_max_complex[:part_len]
        s2_max_complex += prefix
        current_len += part_len
        
    test_cases.append({
        "input": f"{s1_max_complex}\n{s2_max_complex}",
        "description": "Граничный сложный тест: 75000 случайных символов",
        "expected": "No"
    })

    return test_cases
