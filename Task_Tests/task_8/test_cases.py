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

def generate_test_cases():
    """Генерация тестовых случаев для задачи 8"""
    test_cases = []
    
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
    # 2[a]2[ab] -> aaabab
    # 3[a]2[r2[t]] -> aaarttrtt
    # a2[aa3[b]] -> aaabbbaabbb
    # Общий префикс: aaa
    test_cases.append({
        "input": "3\n2[a]2[ab]\n3[a]2[r2[t]]\na2[aa3[b]]",
        "description": "Пример 1 из условия",
        "expected": "aaa"
    })
    
    # Тест 4: Пример 2 из условия
    # abacabaca
    # 2[abac]a -> abacabaca
    # 3[aba] -> abaabaaba
    # Общий префикс: aba
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
    # 2[a]2[b] -> aabb
    # aabb -> aabb
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
    # 100[a]
    # 50[a]
    # Общий: 50[a]
    test_cases.append({
        "input": "2\n100[a]\n50[a]",
        "description": "Большие числа повторений",
        "expected": "a" * 50
    })

    # Тест 10: Сложная вложенность
    # 2[2[2[a]]] -> aaaaaaaa (8 a)
    # 8[a] -> aaaaaaaa
    test_cases.append({
        "input": "2\n2[2[2[a]]]\n8[a]",
        "description": "Сложная вложенность",
        "expected": "aaaaaaaa"
    })
    
    # Тест 11: Длинный префикс
    long_prefix = "a" * 1000
    test_cases.append({
        "input": f"2\n1000[a]b\n1000[a]c",
        "description": "Длинный префикс (1000 символов)",
        "expected": long_prefix
    })

    # Тест 12: Граничное значение N=1000 (максимальное число строк)
    # 1000 строк вида "a", "aa", "aaa" ...
    # Общий префикс: "a"
    max_lines = 1000
    lines = ["a" * i for i in range(1, max_lines + 1)]
    input_str_12 = f"{max_lines}\n" + "\n".join(lines)
    test_cases.append({
        "input": input_str_12,
        "description": "Граничное значение N=1000 строк",
        "expected": "a"
    })
    
    # Тест 13: Граничное значение длины 10^5
    # Две строки длиной 100000, отличающиеся последним символом
    # 1000[100[a]] -> 100000 'a'
    max_len = 100000
    # Строка 1: 100000 'a' + 'b'
    # Строка 2: 100000 'a' + 'c'
    # Общий префикс: 100000 'a'
    input_str_13 = f"2\n1000[100[a]]b\n1000[100[a]]c"
    test_cases.append({
        "input": input_str_13,
        "description": "Граничное значение длины 10^5",
        "expected": "a" * max_len
    })

    return test_cases

if __name__ == "__main__":
    cases = generate_test_cases()
    print(f"Сгенерировано {len(cases)} тест-кейсов")
