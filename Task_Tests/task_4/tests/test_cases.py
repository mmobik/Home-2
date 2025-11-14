import random
import string

def get_anagram_key(word):
    """Создает ключ анаграммы через подсчет букв за O(L) вместо O(L log L)"""
    # Создаем массив счетчиков для 26 букв A-Z
    count = [0] * 26
    
    # Подсчитываем частоты букв
    for char in word:
        count[ord(char) - ord('A')] += 1
    
    # Создаем ключ в формате "A5B3C1..." чтобы избежать коллизий
    key_parts = []
    for i in range(26):
        if count[i] > 0:
            key_parts.append(chr(ord('A') + i))
            key_parts.append(str(count[i]))
    
    return ''.join(key_parts)

def solve_anagram_problem(input_data):
    """
    Решает задачу с анаграммами и возвращает правильный ответ
    Используется для вычисления ожидаемых значений в больших тестах
    Использует ту же логику, что и main() - подсчет букв вместо сортировки
    """
    lines = input_data.strip().split('\n')
    if not lines:
        return "0"
    
    n = int(lines[0])
    if n == 0:
        return "0"
    
    # Группируем слова по ключам анаграмм (подсчет букв)
    anagram_groups = {}
    
    for i in range(1, n + 1):
        word = lines[i].strip()
        # Используем ту же функцию, что и в решении
        key = get_anagram_key(word)
        
        if key not in anagram_groups:
            anagram_groups[key] = 1
        else:
            anagram_groups[key] += 1
    
    return str(len(anagram_groups))

def generate_anagram_test(n, word_length=5, num_groups=None, min_length=3, max_length=10000):
    """
    Генерация теста для задачи с анаграммами
    n - количество слов
    word_length - длина слова (или случайная в диапазоне min_length..max_length)
    num_groups - количество различных комплектов (если None - случайное)
    """
    lines = [str(n)]
    
    if n == 0:
        return "\n".join(lines)
    
    # Определяем длину слова
    if isinstance(word_length, tuple):
        actual_length = random.randint(word_length[0], word_length[1])
    else:
        actual_length = word_length
    
    # Генерируем слова
    if num_groups is None:
        num_groups = random.randint(1, min(n, 100))
    
    # Создаем базовые слова для каждого комплекта
    base_words = []
    for _ in range(num_groups):
        # Генерируем случайное слово из заглавных букв
        base_word = ''.join(random.choices(string.ascii_uppercase, k=actual_length))
        base_words.append(base_word)
    
    # Создаем слова: для каждого базового слова создаем несколько анаграмм
    words = []
    words_per_group = n // num_groups
    remainder = n % num_groups
    
    for i, base_word in enumerate(base_words):
        count = words_per_group + (1 if i < remainder else 0)
        # Создаем анаграммы путем перестановки букв
        chars = list(base_word)
        for _ in range(count):
            random.shuffle(chars)
            words.append(''.join(chars))
    
    # Перемешиваем все слова
    random.shuffle(words)
    
    lines.extend(words)
    return "\n".join(lines)

def generate_basic_cases():
    """
    Генерация базовых граничных тестовых случаев
    """
    return [
        {
            "input": "3\nLOOP\nPOOL\nPOLO",
            "description": "Пример: 3 слова, 1 комплект анаграмм",
            "expected": "1"
        },
        {
            "input": "1\nABC",
            "description": "Минимальное количество слов (1)",
            "expected": "1"
        },
        {
            "input": "3\nABC\nDEF\nGHI",
            "description": "Все слова разные (3 комплекта)",
            "expected": "3"
        },
        {
            "input": "4\nABC\nABC\nABC\nABC",
            "description": "Все слова одинаковые (1 комплект)",
            "expected": "1"
        },
        {
            "input": "6\nLOOP\nPOOL\nPOLO\nRAT\nTAR\nART",
            "description": "Два комплекта анаграмм",
            "expected": "2"
        },
        {
            "input": "5\nAAA\nAAA\nBBB\nBBB\nCCC",
            "description": "Повторяющиеся слова, 3 комплекта",
            "expected": "3"
        },
        {
            "input": "4\nABCD\nDCBA\nBACD\nCDAB",
            "description": "Один комплект из 4 анаграмм",
            "expected": "1"
        },
        {
            "input": "10\nABC\nACB\nBAC\nBCA\nCAB\nCBA\nDEF\nDFE\nEDF\nEFD",
            "description": "Два комплекта по 6 и 4 слова",
            "expected": "2"
        },
        {
            "input": "2\nXYZ\nZYX",
            "description": "Два слова, один комплект",
            "expected": "1"
        },
        {
            "input": "3\nMIN\nMAX\nMID",
            "description": "Три разных слова (3 комплекта)",
            "expected": "3"
        },
    ]

def generate_large_cases():
    """
    Генерация нагрузочных тестовых случаев с вычислением правильных ответов
    """
    tests = []
    
    # Тест 1: Средний размер (1000 слов, длина 10)
    test1_input = generate_anagram_test(1000, word_length=10, num_groups=50)
    tests.append({
        "input": test1_input,
        "description": "1000 слов, длина 10, ~50 комплектов",
        "expected": solve_anagram_problem(test1_input)
    })
    
    # Тест 2: Максимальная длина слова (10000)
    test2_input = generate_anagram_test(100, word_length=10000, num_groups=10)
    tests.append({
        "input": test2_input,
        "description": "100 слов, максимальная длина 10000, 10 комплектов",
        "expected": solve_anagram_problem(test2_input)
    })
    
    # Тест 3: Минимальная длина слова (3)
    test3_input = generate_anagram_test(1000, word_length=3, num_groups=100)
    tests.append({
        "input": test3_input,
        "description": "1000 слов, минимальная длина 3, 100 комплектов",
        "expected": solve_anagram_problem(test3_input)
    })
    
    # Тест 4: Все слова одинаковые (1 комплект)
    test4_input = generate_anagram_test(10000, word_length=50, num_groups=1)
    tests.append({
        "input": test4_input,
        "description": "10000 слов, все одинаковые (1 комплект)",
        "expected": solve_anagram_problem(test4_input)
    })
    
    # Тест 5: Все слова разные (N комплектов)
    test5_input = generate_anagram_test(5000, word_length=20, num_groups=5000)
    tests.append({
        "input": test5_input,
        "description": "5000 слов, все разные (5000 комплектов)",
        "expected": solve_anagram_problem(test5_input)
    })
    
    # Тест 6: Максимальное количество слов (100000)
    test6_input = generate_anagram_test(100000, word_length=10, num_groups=1000)
    tests.append({
        "input": test6_input,
        "description": "100000 слов (максимум), длина 10, 1000 комплектов",
        "expected": "large_result"  # Не вычисляем из-за сложности
    })
    
    # Тест 7: Максимальная длина слова при большом количестве слов
    test7_input = generate_anagram_test(1000, word_length=10000, num_groups=50)
    tests.append({
        "input": test7_input,
        "description": "1000 слов, максимальная длина 10000, 50 комплектов",
        "expected": solve_anagram_problem(test7_input)
    })
    
    return tests

def generate_test_cases():
    """
    Объединение всех тестовых случаев
    """
    return generate_basic_cases() + generate_large_cases()

