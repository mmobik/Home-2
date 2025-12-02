"""
Тест-кейсы для задачи 8: Общий префикс распакованных строк
"""

def unpack(s):
    """Эталонная распаковка строки для проверки"""
    stack = []
    result = []
    i = 0
    while i < len(s):
        if s[i].isdigit():
            num = 0
            while i < len(s) and s[i].isdigit():
                num = num * 10 + int(s[i])
                i += 1
            if i < len(s) and s[i] == '[':
                i += 1
                stack.append((result, num))
                result = []
            else:
                result.append(str(num))
        elif s[i] == ']':
            if stack:
                prev_result, repeat = stack.pop()
                result = prev_result + result * repeat
            i += 1
        else:
            result.append(s[i])
            i += 1
    return "".join(result)

def get_common_prefix(strings):
    """Эталонный поиск общего префикса"""
    if not strings:
        return ""
    unpacked = [unpack(s) for s in strings]
    if not unpacked:
        return ""
    
    prefix = unpacked[0]
    for s in unpacked[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix

import random

def generate_random_packed_string(target_length, depth=0):
    """
    Генерирует случайную запакованную строку, которая распаковывается 
    в строку примерной длины target_length.
    """
    if target_length <= 5 or depth > 3:
        # Базовый случай: просто случайные символы
        chars = "abcdefghijklmnopqrstuvwxyz"
        return "".join(random.choice(chars) for _ in range(target_length))
    
    # Решаем, будем ли использовать упаковку
    if random.random() < 0.7:  # 70% вероятность упаковки
        # Выбираем множитель от 2 до 9
        k = random.randint(2, 9)
        inner_len = target_length // k
        if inner_len == 0:
            inner_len = 1
        
        inner_str = generate_random_packed_string(inner_len, depth + 1)
        
        # Иногда добавляем суффикс или префикс
        remainder = target_length - (len(unpack(inner_str)) * k)
        prefix = ""
        suffix = ""
        
        if remainder > 0:
            if random.random() < 0.5:
                suffix = generate_random_packed_string(remainder, depth + 1)
            else:
                prefix = generate_random_packed_string(remainder, depth + 1)
                
        return f"{prefix}{k}[{inner_str}]{suffix}"
    else:
        # Просто делим на части
        split = random.randint(1, target_length - 1)
        part1 = generate_random_packed_string(split, depth + 1)
        part2 = generate_random_packed_string(target_length - split, depth + 1)
        return part1 + part2

def generate_test_cases():
    """Генерация тестовых случаев для задачи 8"""
    test_cases = []
    random.seed(42) # Для воспроизводимости
    
    # Тест 1: Базовый пример из условия (если был бы)
    # 3
    # 2[a]b
    # 2[a]c
    # 2[a]d
    # -> aa
    test_cases.append({
        "input": "3\n2[a]b\n2[a]c\n2[a]d",
        "description": "Базовый пример: общий префикс 'aa'",
        "expected": "aa"
    })
    
    # Тест 2: Нет общего префикса
    test_cases.append({
        "input": "2\na\nb",
        "description": "Нет общего префикса",
        "expected": ""
    })
    
    # Тест 3: Пример 1 из условия
    test_cases.append({
        "input": "3\n2[a]2[ab]\n3[a]2[r2[t]]\na2[aa3[b]]",
        "description": "Пример 1 из условия",
        "expected": "aaa"
    })
    
    # Тест 4: Пример 2 из условия
    test_cases.append({
        "input": "3\nabacabaca\n2[abac]a\n3[aba]",
        "description": "Пример 2 из условия",
        "expected": "aba"
    })
    
    # Тест 5: Одна строка префикс другой
    test_cases.append({
        "input": "2\n2[a]\n2[a]b",
        "description": "Одна строка является префиксом другой",
        "expected": "aa"
    })
    
    # Тест 6: Разная запись одной строки
    test_cases.append({
        "input": "2\n2[a]2[b]\naabb",
        "description": "Разная запись одной строки",
        "expected": "aabb"
    })

    # Тест 7: Пустой ввод
    test_cases.append({
        "input": "0",
        "description": "Пустой ввод (N=0)",
        "expected": ""
    })
    
    # Тест 8: Одна строка
    test_cases.append({
        "input": "1\n3[a]",
        "description": "Одна строка",
        "expected": "aaa"
    })

    # Тест 9: Большие числа повторений
    test_cases.append({
        "input": "2\n100[a]\n50[a]",
        "description": "Большие числа повторений",
        "expected": "a" * 50
    })

    # Тест 10: Сложная вложенность
    test_cases.append({
        "input": "2\n2[2[2[a]]]\n8[a]",
        "description": "Сложная вложенность",
        "expected": "aaaaaaaa"
    })
    
    # Тест 11: Случайные сложные строки (длина ~1000)
    target_len_11 = 1000
    s1 = generate_random_packed_string(target_len_11)
    s2 = generate_random_packed_string(target_len_11)
    # Чтобы был общий префикс, принудительно сделаем начало одинаковым
    common_part = "2[abc]" # abcabc
    s1 = common_part + s1
    s2 = common_part + s2
    
    # Вычисляем ожидаемый результат эталонной функцией
    expected_11 = get_common_prefix([s1, s2])
    
    test_cases.append({
        "input": f"2\n{s1}\n{s2}",
        "description": "Случайные сложные строки (длина ~1000)",
        "expected": expected_11
    })

    # Тест 12: Граничное значение N=1000 строк (короткие)
    max_lines = 1000
    lines = ["a" * i for i in range(1, max_lines + 1)]
    input_str_12 = f"{max_lines}\n" + "\n".join(lines)
    test_cases.append({
        "input": input_str_12,
        "description": "Граничное значение N=1000 строк",
        "expected": "a"
    })
    
    # Тест 13: Случайные сложные строки максимальной длины (10^5)
    target_len_13 = 100000
    # Генерируем одну сложную структуру
    base_structure = generate_random_packed_string(target_len_13)
    
    # Создаем две строки, которые отличаются только в самом конце
    # Распаковываем, чтобы точно знать длину и контент
    unpacked_base = unpack(base_structure)
    
    # Если строка получилась короче (из-за рандома), добьем 'a'
    if len(unpacked_base) < target_len_13:
        diff = target_len_13 - len(unpacked_base)
        base_structure += f"{diff}[a]"
        unpacked_base += "a" * diff
        
    # Строка 1: base + 'x'
    # Строка 2: base + 'y'
    s13_1 = base_structure + "x"
    s13_2 = base_structure + "y"
    
    test_cases.append({
        "input": f"2\n{s13_1}\n{s13_2}",
        "description": "Случайные сложные строки (длина 10^5)",
        "expected": unpacked_base
    })
    
    # Тест 14: КОМБО - 1000 строк по 10^5 символов
    # Это максимальная нагрузка по всем параметрам
    max_lines_14 = 1000
    target_len_14 = 100000
    
    # Генерируем сложную базу чуть меньшей длины, чтобы добавить вариативность в конце
    base_len = 99900
    base_struct_14 = generate_random_packed_string(base_len)
    unpacked_base_14 = unpack(base_struct_14)
    
    # Добиваем до 99900 если рандом выдал меньше
    if len(unpacked_base_14) < base_len:
        diff = base_len - len(unpacked_base_14)
        base_struct_14 += f"{diff}[a]"
        unpacked_base_14 += "a" * diff
        
    # Генерируем 1000 строк: База + уникальный хвост
    # Хвост делаем простым, чтобы не тратить время на генерацию 1000 сложных хвостов
    lines_14 = []
    for i in range(max_lines_14):
        # Добавляем уникальный хвост длиной 100
        suffix = f"100[{chr(ord('a') + (i % 26))}]"
        lines_14.append(base_struct_14 + suffix)
        
    input_str_14 = f"{max_lines_14}\n" + "\n".join(lines_14)
    
    test_cases.append({
        "input": input_str_14,
        "description": "КОМБО: 1000 сложных строк длиной 10^5",
        "expected": unpacked_base_14
    })

    return test_cases

if __name__ == "__main__":
    cases = generate_test_cases()
    print(f"Сгенерировано {len(cases)} тест-кейсов")
