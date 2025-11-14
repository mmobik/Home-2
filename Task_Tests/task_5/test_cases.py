import random
import string


def generate_huge_cases():
    """Очень большие тесты (300К операций)"""
    tests = []

    # Тест 1: 300000 операций согласно условию (первые N/2 - ADD)
    test1_commands = []
    n = 300000

    # Первые 150000 команд - ADD (половина от 300000)
    print("Генерация 150000 команд ADD...")
    for i in range(150000):
        # Генерируем ключ и значение длиной до 4096 символов
        key_length = random.randint(10, 100)  # До 100 символов для ключа
        value_length = random.randint(10, 200)  # До 200 символов для значения

        key = f"KEY_{i:08d}_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=key_length - 15))
        value = f"VAL_{i:08d}_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=value_length - 15))

        test1_commands.append(f"ADD {key} {value}")

        if i % 10000 == 0:
            print(f"Сгенерировано {i} команд ADD")

    # Остальные 150000 команд - смешанные операции
    print("Генерация 150000 смешанных команд...")
    operations = ['PRINT', 'UPDATE', 'DELETE', 'ADD']
    weights = [0.4, 0.2, 0.2, 0.2]  # Вероятности операций

    for i in range(150000):
        op_type = random.choices(operations, weights=weights)[0]

        if op_type == 'ADD':
            # Добавляем новый уникальный ключ
            key = f"NEW_KEY_{i:08d}_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=50))
            value = f"NEW_VAL_{i:08d}_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))
            test1_commands.append(f"ADD {key} {value}")

        elif op_type == 'PRINT':
            # Берем случайный существующий ключ (первые 150000)
            key_idx = random.randint(0, 149999)
            key = f"KEY_{key_idx:08d}_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=50))
            test1_commands.append(f"PRINT {key}")

        elif op_type == 'UPDATE':
            # Обновляем случайный существующий ключ
            key_idx = random.randint(0, 149999)
            key = f"KEY_{key_idx:08d}_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=50))
            new_value = f"UPD_VAL_{i:08d}_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=100))
            test1_commands.append(f"UPDATE {key} {new_value}")

        elif op_type == 'DELETE':
            # Удаляем случайный существующий ключ
            key_idx = random.randint(0, 149999)
            key = f"KEY_{key_idx:08d}_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=50))
            test1_commands.append(f"DELETE {key}")

        if i % 10000 == 0:
            print(f"Сгенерировано {i} смешанных команд")

    test1_input = f"{n}\n" + "\n".join(test1_commands)

    tests.append({
        "input": test1_input,
        "description": "300000 операций (150000 ADD + 150000 смешанных), ключи и значения до 4096 символов",
        "expected": "huge_test"  # Специальная метка для огромных тестов
    })

    # Тест 2: Максимальная длина ключей и значений
    test2_commands = []
    n = 10000  # Меньше операций, но с максимальной длиной

    print("Генерация теста с максимальной длиной...")
    for i in range(n):
        if i < n // 2:
            # ADD с максимальной длиной
            key = 'K' + str(i).zfill(6) + 'X' * 4089  # Всего 4096 символов
            value = 'V' + str(i).zfill(6) + 'Y' * 4089  # Всего 4096 символов
            test2_commands.append(f"ADD {key} {value}")
        else:
            # PRINT существующих ключей
            key_idx = random.randint(0, n // 2 - 1)
            key = 'K' + str(key_idx).zfill(6) + 'X' * 4089
            test2_commands.append(f"PRINT {key}")

    test2_input = f"{n}\n" + "\n".join(test2_commands)

    tests.append({
        "input": test2_input,
        "description": "10000 операций с ключами и значениями максимальной длины (4096 символов)",
        "expected": "huge_test"
    })

    return tests


def generate_test_cases():
    """
    Генерация тестовых случаев для задачи с базой данных
    """
    test_cases = []

    # Базовые тесты
    test_cases.extend(generate_basic_cases())

    # Граничные тесты
    test_cases.extend(generate_edge_cases())

    # Нагрузочные тесты
    test_cases.extend(generate_stress_cases())

    # Тесты, требующие внешней памяти
    test_cases.extend(generate_external_memory_cases())

    return test_cases


def generate_basic_cases():
    """Базовые тесты"""
    return [
        {
            "input": """10
ADD KEY1 VAL1
ADD KEY2 VAL2
ADD KEY3 VAL3
PRINT KEY1
UPDATE KEY2 NEWVAL2
PRINT KEY2
DELETE KEY3
PRINT KEY3
ADD KEY4 VAL4
PRINT KEY4""",
            "description": "Базовые операции: ADD, UPDATE, DELETE, PRINT",
            "expected": "KEY1 VAL1\nKEY2 NEWVAL2\nERROR\nKEY4 VAL4"
        },
        {
            "input": """8
ADD K1 V1
ADD K2 V2
ADD K3 V3
DELETE K2
PRINT K1
PRINT K2
ADD K4 V4
PRINT K4""",
            "description": "Добавление, удаление и чтение разных ключей",
            "expected": "K1 V1\nERROR\nK4 V4"
        }
    ]


def generate_edge_cases():
    """Граничные тесты"""
    return [
        {
            "input": """1
PRINT KEY""",
            "description": "Запрос несуществующего ключа",
            "expected": "ERROR"
        },
        {
            "input": """1
ADD KEY VALUE""",
            "description": "Одна команда ADD",
            "expected": ""
        },
        {
            "input": """2
ADD KEY VALUE
PRINT KEY""",
            "description": "Добавление и чтение",
            "expected": "KEY VALUE"
        },
        {
            "input": """3
ADD KEY VALUE
DELETE KEY
PRINT KEY""",
            "description": "Добавление, удаление и чтение",
            "expected": "ERROR"
        },
        {
            "input": """3
ADD KEY VALUE
UPDATE KEY NEWVALUE
PRINT KEY""",
            "description": "Добавление, обновление и чтение",
            "expected": "KEY NEWVALUE"
        },
        {
            "input": """2
ADD KEY VALUE
ADD KEY VALUE""",
            "description": "Добавление дубликата",
            "expected": "ERROR"
        },
        {
            "input": """2
DELETE KEY
PRINT KEY""",
            "description": "Удаление несуществующего ключа",
            "expected": "ERROR\nERROR"
        },
        {
            "input": """2
UPDATE KEY VALUE
PRINT KEY""",
            "description": "Обновление несуществующего ключа",
            "expected": "ERROR\nERROR"
        },
        {
            "input": """4
ADD K1 V1
UPDATE K1 V2
DELETE K1
PRINT K1""",
            "description": "ADD → UPDATE → DELETE → PRINT",
            "expected": "ERROR"
        },
        {
            "input": """5
ADD A 1
ADD B 2
PRINT A
UPDATE A 10
PRINT A""",
            "description": "Работа с разными ключами",
            "expected": "A 1\nA 10"
        }
    ]


def generate_stress_cases():
    """Нагрузочные тесты"""
    tests = []

    # Тест 1: 1000 операций ADD + PRINT
    test1_commands = []
    n = 1000
    expected_output = []

    # Первые 500 команд - ADD
    for i in range(500):
        key = f"KEY{i:04d}"
        value = f"VALUE{i:04d}"
        test1_commands.append(f"ADD {key} {value}")

    # Следующие 500 команд - PRINT (все должны существовать)
    for i in range(500):
        key = f"KEY{i:04d}"
        test1_commands.append(f"PRINT {key}")
        expected_output.append(f"{key} VALUE{i:04d}")

    test1_input = f"{n}\n" + "\n".join(test1_commands)

    tests.append({
        "input": test1_input,
        "description": "1000 операций: 500 ADD + 500 PRINT существующих ключей",
        "expected": "\n".join(expected_output)
    })

    # Тест 2: 2000 операций с ошибками
    test2_commands = []
    n = 2000
    expected_output = []

    # 1000 ADD дубликатов (500 успешных + 500 ошибок)
    for i in range(1000):
        key = f"K{i % 500:04d}"
        value = f"V{i:04d}"
        test2_commands.append(f"ADD {key} {value}")
        if i >= 500:
            expected_output.append("ERROR")

    # 1000 UPDATE несуществующих ключей
    for i in range(1000):
        key = f"NONEXISTENT{i:04d}"
        value = f"VAL{i:04d}"
        test2_commands.append(f"UPDATE {key} {value}")
        expected_output.append("ERROR")

    test2_input = f"{n}\n" + "\n".join(test2_commands)

    tests.append({
        "input": test2_input,
        "description": "2000 операций с ошибками",
        "expected": "\n".join(expected_output)
    })

    # Тест 3: 5000 смешанных операций
    test3_commands = []
    n = 5000
    expected_output = []

    # Создаем 1000 ключей для работы
    keys = [f"KEY{i:04d}" for i in range(1000)]

    for i in range(n):
        op_type = i % 6
        key_idx = i % len(keys)
        key = keys[key_idx]

        if op_type == 0:
            # ADD - первые 1000 успешны, остальные ошибки
            value = f"VAL{i:05d}"
            test3_commands.append(f"ADD {key} {value}")
            if i < 1000:
                # Первые 1000 ADD успешны
                pass
            else:
                expected_output.append("ERROR")

        elif op_type == 1:
            # UPDATE - успешно для существующих ключей
            value = f"NEWVAL{i:05d}"
            test3_commands.append(f"UPDATE {key} {value}")
            if i >= 1000:  # Ключ существует после первых 1000 ADD
                pass
            else:
                expected_output.append("ERROR")

        elif op_type == 2:
            # DELETE - успешно для существующих ключей
            test3_commands.append(f"DELETE {key}")
            if i >= 1000:
                pass
            else:
                expected_output.append("ERROR")

        elif op_type == 3:
            # PRINT - проверяем состояние
            test3_commands.append(f"PRINT {key}")
            if i >= 1000 and (i - 1000) % 6 != 2:  # Если не был удален
                expected_output.append(f"{key} NEWVAL{i:05d}")
            else:
                expected_output.append("ERROR")

        elif op_type == 4:
            # ADD нового уникального ключа
            unique_key = f"UNIQUE{i:05d}"
            value = f"UVAL{i:05d}"
            test3_commands.append(f"ADD {unique_key} {value}")
            # Всегда успешно, т.к. ключи уникальные

        elif op_type == 5:
            # PRINT уникального ключа
            unique_key = f"UNIQUE{i:05d}"
            test3_commands.append(f"PRINT {unique_key}")
            expected_output.append(f"{unique_key} UVAL{i:05d}")

    test3_input = f"{n}\n" + "\n".join(test3_commands)

    tests.append({
        "input": test3_input,
        "description": "5000 смешанных операций",
        "expected": "\n".join(expected_output)
    })

    # Тест 4: Длинные ключи и значения
    test4_commands = []
    n = 100
    expected_output = []

    # Генерация длинных строк (почти максимальная длина)
    key_length = 4000
    value_length = 4000

    for i in range(n // 2):
        key = f"K{i:03d}" + "X" * (key_length - 5)
        value = f"V{i:03d}" + "Y" * (value_length - 5)
        test4_commands.append(f"ADD {key} {value}")

    for i in range(n // 2):
        key = f"K{i:03d}" + "X" * (key_length - 5)
        test4_commands.append(f"PRINT {key}")
        expected_output.append(f"{key} V{i:03d}" + "Y" * (value_length - 5))

    test4_input = f"{n}\n" + "\n".join(test4_commands)

    tests.append({
        "input": test4_input,
        "description": "100 операций с длинными ключами и значениями (~4000 символов)",
        "expected": "\n".join(expected_output)
    })

    # Тест 5: Только успешные ADD (10000 операций)
    test5_commands = []
    n = 10000

    for i in range(n):
        key = f"SUCCESS_KEY_{i:08d}"
        value = f"SUCCESS_VAL_{i:08d}"
        test5_commands.append(f"ADD {key} {value}")

    test5_input = f"{n}\n" + "\n".join(test5_commands)

    tests.append({
        "input": test5_input,
        "description": f"{n} успешных операций ADD",
        "expected": ""
    })

    return tests


def generate_external_memory_cases():
    """Тесты, проверяющие использование внешней памяти"""
    tests = []

    # Тест 1: 300000 операций с контролем памяти
    test1_commands = []
    n = 300000

    print("Генерация 300000 операций для теста внешней памяти...")

    # Первые 150000 команд - ADD (половина от 300000)
    for i in range(150000):
        key = f"KEY{i:06d}"
        value = f"VALUE{i:06d}"
        test1_commands.append(f"ADD {key} {value}")

    # Остальные 150000 команд - смешанные операции
    operations = ['PRINT', 'UPDATE', 'DELETE']

    for i in range(150000):
        op_type = random.choice(operations)

        if op_type == 'PRINT':
            key_idx = random.randint(0, 149999)
            test1_commands.append(f"PRINT KEY{key_idx:06d}")

        elif op_type == 'UPDATE':
            key_idx = random.randint(0, 149999)
            test1_commands.append(f"UPDATE KEY{key_idx:06d} NEWVAL{i:06d}")

        elif op_type == 'DELETE':
            key_idx = random.randint(0, 149999)
            test1_commands.append(f"DELETE KEY{key_idx:06d}")

    test1_input = f"{n}\n" + "\n".join(test1_commands)

    tests.append({
        "input": test1_input,
        "description": "300000 операций (требует внешней памяти, максимум 4МБ ОЗУ)",
        "expected": "external_memory_required"
    })

    # Тест 2: Длинные ключи и значения (но много операций)
    test2_commands = []
    n = 50000  # Меньше операций, но длинные данные

    print("Генерация теста с длинными данными...")

    for i in range(n // 2):
        # Ключи и значения по 1000 символов
        key = f"LONG_KEY_{i:05d}_" + 'X' * 950
        value = f"LONG_VAL_{i:05d}_" + 'Y' * 950
        test2_commands.append(f"ADD {key} {value}")

    for i in range(n // 2):
        key_idx = random.randint(0, n // 2 - 1)
        key = f"LONG_KEY_{key_idx:05d}_" + 'X' * 950
        test2_commands.append(f"PRINT {key}")

    test2_input = f"{n}\n" + "\n".join(test2_commands)

    tests.append({
        "input": test2_input,
        "description": "50000 операций с длинными ключами/значениями (требует внешней памяти)",
        "expected": "external_memory_required"
    })

    return tests