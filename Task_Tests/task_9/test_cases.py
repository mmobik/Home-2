"""
Тест-кейсы для задачи 9: Дополнение строки до палиндрома
"""
import random

def solve_reference(s):
    """
    Эталонное (медленное) решение для проверки.
    Проверяет все возможные добавления.
    """
    n = len(s)
    if n == 0:
        return ""
    # Пробуем добавить i символов с начала строки (в обратном порядке)
    for i in range(n):
        # Суффикс s[i:] должен быть палиндромом
        suffix = s[i:]
        if suffix == suffix[::-1]:
            return s + s[:i][::-1]
    return s + s[::-1] # В худшем случае (хотя цикл выше покроет это)

def generate_random_string(length):
    chars = "abcdefghijklmnopqrstuvwxyz"
    return "".join(random.choice(chars) for _ in range(length))

def generate_test_cases():
    """Генерация тестовых случаев для задачи 9"""
    test_cases = []
    
    # Тест 1: Базовый пример (нет палиндромного суффикса > 1)
    test_cases.append({
        "input": "abcde",
        "description": "Строка без палиндромных суффиксов > 1",
        "expected": "abcdedcba"
    })
    
    # Тест 2: Уже палиндром
    test_cases.append({
        "input": "abacaba",
        "description": "Строка уже является палиндромом",
        "expected": "abacaba"
    })
    
    # Тест 3: Суффикс-палиндром есть (banana -> anana)
    test_cases.append({
        "input": "banana",
        "description": "Есть длинный палиндромный суффикс (anana)",
        "expected": "bananab"
    })
    
    # Тест 4: Все символы одинаковые
    test_cases.append({
        "input": "aaaaa",
        "description": "Все символы одинаковые",
        "expected": "aaaaa"
    })
    
    # Тест 5: Почти палиндром, но лишний символ в начале
    test_cases.append({
        "input": "xabacaba",
        "description": "Лишний символ в начале палиндрома",
        "expected": "xabacabax"
    })
    
    # Тест 6: Пустая строка
    test_cases.append({
        "input": "",
        "description": "Пустая строка",
        "expected": ""
    })
    
    # Тест 7: Один символ
    test_cases.append({
        "input": "z",
        "description": "Один символ",
        "expected": "z"
    })
    
    # Тест 8: Два разных символа
    test_cases.append({
        "input": "ab",
        "description": "Два разных символа",
        "expected": "aba"
    })

    # Тест 9: Случайная короткая строка
    s_rand_small = "aabac"
    test_cases.append({
        "input": s_rand_small,
        "description": "Короткая строка aabac",
        "expected": solve_reference(s_rand_small)
    })

    # Тест 10: Длинная строка из одинаковых символов (проверка переполнения хешей)
    long_a = "a" * 1000
    test_cases.append({
        "input": long_a,
        "description": "Длинная строка из 'a' (1000)",
        "expected": long_a
    })

    # Тест 11: Длинная строка, где палиндром только последний символ
    # abcde...z -> abcde...z...edcba
    long_seq = "".join(chr(ord('a') + (i % 26)) for i in range(1000))
    # Сделаем так, чтобы суффиксов-палиндромов не было (или были очень короткие)
    # Для простоты возьмем эталонное решение, оно справится с 1000
    test_cases.append({
        "input": long_seq,
        "description": "Длинная строка без палиндромов (1000)",
        "expected": solve_reference(long_seq)
    })

    # Тест 12: Большой тест (10^5 символов) - случайная строка
    # Ожидаемый результат не сохраняем для экономии места в коде, 
    # но в main.py он не будет проверяться для больших тестов.
    # Однако для генерации expected нам нужно что-то.
    # Для больших тестов expected можно оставить пустым или сгенерировать reference (но это долго).
    # В main.py логика: если тест большой, expected игнорируется.
    
    random.seed(42)
    large_len = 100000
    large_s = generate_random_string(large_len)
    
    test_cases.append({
        "input": large_s,
        "description": "Случайная большая строка (10^5)",
        "expected": "" # Не проверяем expected для больших тестов
    })
    
    # Тест 13: Большой тест - почти палиндром (худший случай для хешей?)
    # a...ab...b (много a, потом много b)
    # Нет, худший случай для хешей - коллизии, но здесь полиномиальный хеш.
    # Худший случай для алгоритма - когда палиндромный суффикс очень короткий.
    worst_case = "a" * 50000 + "b" + "a" * 49999
    # Суффикс "a"*49999 - палиндром.
    # Нужно добавить "a"*50000 + "b" в обратном порядке? Нет.
    # Строка: A...AB A...A
    # Суффикс A...A (49999) - палиндром.
    # Префикс A...AB (50001). Его перевернем: BA...A
    # Результат: A...AB A...A BA...A
    
    test_cases.append({
        "input": worst_case,
        "description": "Большая строка 'почти палиндром' (10^5)",
        "expected": "" # Не проверяем
    })

    return test_cases
