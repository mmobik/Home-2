"""
Тест-кейсы для задачи 9: Дополнение строки до палиндрома
"""
import random

def solve_reference(s):
    """
    Эталонное (медленное) решение для проверки.
    Проверяет все возможные добавления.
    Условие: добавленная часть S2 должна быть непустой.
    """
    n = len(s)
    if n == 0:
        return ""
    # Пробуем найти палиндромный суффикс, начиная с индекса 1 (чтобы префикс был непустым)
    for i in range(1, n):
        suffix = s[i:]
        if suffix == suffix[::-1]:
            return s + s[:i][::-1]
    # Если не нашли, добавляем всю строку (кроме, возможно, последнего символа? Нет, всю перевернутую)
    # Но подождите, если i доходит до n-1, суффикс - последний символ (палиндром).
    # Если цикл завершился, значит даже последний символ не подошел? 
    # Нет, последний символ всегда палиндром. Цикл всегда найдет решение, если n > 0.
    # Единственный случай, когда цикл не сработает - если n=1.
    if n == 1:
        return s + s
        
    return s + s[:-1][::-1] # На всякий случай, но логика выше должна покрыть

def generate_random_string(length):
    chars = "abcdefghijklmnopqrstuvwxyz"
    return "".join(random.choice(chars) for _ in range(length))

def generate_random_palindrome(length):
    half_len = length // 2
    chars = "abcdefghijklmnopqrstuvwxyz"
    half = "".join(random.choice(chars) for _ in range(half_len))
    if length % 2 == 0:
        return half + half[::-1]
    else:
        mid = random.choice(chars)
        return half + mid + half[::-1]

def generate_test_cases():
    """Генерация тестовых случаев для задачи 9"""
    test_cases = []
    random.seed(42)
    
    # Тест 1: Базовый пример (нет палиндромного суффикса > 1)
    test_cases.append({
        "input": "abcde",
        "description": "Строка без палиндромных суффиксов > 1",
        "expected": "abcdedcba"
    })
    
    # Тест 2: Уже палиндром (S2 должно быть непустым)
    test_cases.append({
        "input": "abacaba",
        "description": "Строка уже является палиндромом (S2 непустое)",
        "expected": "abacabacaba"
    })
    
    # Тест 3: Суффикс-палиндром есть (banana -> anana)
    test_cases.append({
        "input": "banana",
        "description": "Есть длинный палиндромный суффикс (anana)",
        "expected": "bananab"
    })
    
    # Тест 4: Все символы одинаковые (S2 непустое)
    test_cases.append({
        "input": "aaaaa",
        "description": "Все символы одинаковые (S2 непустое)",
        "expected": "aaaaaa"
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
    
    # Тест 7: Один символ (S2 непустое)
    test_cases.append({
        "input": "z",
        "description": "Один символ (S2 непустое)",
        "expected": "zz"
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

    # Тест 10: Случайная строка средней длины
    s_rand_1000 = generate_random_string(1000)
    test_cases.append({
        "input": s_rand_1000,
        "description": "Случайная строка (1000 символов)",
        "expected": solve_reference(s_rand_1000)
    })

    # Тест 11: Длинная строка без палиндромов (1000)
    long_seq = "".join(chr(ord('a') + (i % 26)) for i in range(1000))
    test_cases.append({
        "input": long_seq,
        "description": "Длинная строка без палиндромов (1000)",
        "expected": solve_reference(long_seq)
    })

    # Тест 12: Случайная большая строка (10^5)
    large_len = 100000
    large_s = generate_random_string(large_len)
    
    test_cases.append({
        "input": large_s,
        "description": "Случайная большая строка (10^5)",
        "expected": "" # Не проверяем expected для больших тестов
    })
    
    # Тест 13: Большой случайный палиндром (10^5)
    large_pal = generate_random_palindrome(100000)
    test_cases.append({
        "input": large_pal,
        "description": "Большой случайный палиндром (10^5)",
        "expected": "" 
    })

    # Тест 14: Случайная строка с большим палиндромным суффиксом
    # 50000 случайных + 50000 палиндром
    mixed_s = generate_random_string(50000) + generate_random_palindrome(50000)
    test_cases.append({
        "input": mixed_s,
        "description": "Случайная строка с палиндромным суффиксом (10^5)",
        "expected": ""
    })

    return test_cases
