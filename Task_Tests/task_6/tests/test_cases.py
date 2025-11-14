import random


def generate_test_cases():
    """Генерация тестовых случаев для задачи 18"""
    test_cases = []

    # Базовые тесты из условия
    test_cases.extend(generate_basic_cases())

    # Граничные тесты
    test_cases.extend(generate_edge_cases())

    # Максимальные тесты
    test_cases.extend(generate_max_cases())

    # Тесты на коллизии
    test_cases.extend(generate_collision_cases())

    return test_cases


def generate_basic_cases():
    """Базовые тесты из условия"""
    return [
        {
            "input": """10
get 1
put 1 10
put 2 4
get 1
get 2
delete 2
get 2
put 1 5
get 1
delete 2""",
            "description": "Пример из условия",
            "expected": "None\n10\n4\n4\nNone\n5\nNone"
        },
        {
            "input": """8
get 9
delete 9
put 9 1
get 9
put 9 2
get 9
put 9 3
get 9""",
            "description": "Второй пример из условия",
            "expected": "None\nNone\n1\n2\n3"
        }
    ]


def generate_edge_cases():
    """Граничные тесты"""
    return [
        {
            "input": """1
get 1""",
            "description": "Минимальный тест - запрос несуществующего ключа",
            "expected": "None"
        },
        {
            "input": """3
put 1 100
get 1
delete 1""",
            "description": "Добавление, чтение, удаление",
            "expected": "100\n100"
        },
        {
            "input": """4
put 1 10
put 1 20
get 1
delete 1""",
            "description": "Обновление значения",
            "expected": "20\n20"
        },
        {
            "input": """3
delete 1
get 1
put 1 100""",
            "description": "Удаление и чтение несуществующего ключа",
            "expected": "None\nNone"
        }
    ]


def generate_max_cases():
    """Тесты с максимальными значениями"""
    tests = []

    # Тест 1: Максимальное количество операций (10^6)
    test1_commands = []
    n = 1000000

    # Генерируем 10^6 операций
    operations = ['put', 'get', 'delete']

    for i in range(n):
        op_type = random.choice(operations)
        key = random.randint(0, 10 ** 9)

        if op_type == 'put':
            value = random.randint(0, 10 ** 9)
            test1_commands.append(f"put {key} {value}")
        else:
            test1_commands.append(f"{op_type} {key}")

    test1_input = f"{n}\n" + "\n".join(test1_commands)

    tests.append({
        "input": test1_input,
        "description": "Максимальное количество операций (1,000,000)",
        "expected": "max_test"
    })

    # Тест 2: Максимальные значения ключей и данных
    test2_commands = []
    n = 100000

    for i in range(n):
        if i < 50000:
            # PUT с максимальными значениями
            key = 10 ** 9 - i  # Максимальные ключи
            value = 10 ** 9 - i * 2  # Максимальные значения
            test2_commands.append(f"put {key} {value}")
        else:
            # GET и DELETE
            key = random.randint(10 ** 9 - 50000, 10 ** 9)
            op_type = random.choice(['get', 'delete'])
            test2_commands.append(f"{op_type} {key}")

    test2_input = f"{n}\n" + "\n".join(test2_commands)

    tests.append({
        "input": test2_input,
        "description": "Максимальные значения ключей и данных (10^9)",
        "expected": "max_test"
    })

    # Тест 3: Много уникальных ключей (близко к 10^5)
    test3_commands = []
    n = 200000  # 100K PUT + 100K операций

    # 100000 уникальных PUT
    for i in range(100000):
        key = i
        value = i * 10
        test3_commands.append(f"put {key} {value}")

    # 100000 GET случайных ключей
    for i in range(100000):
        key = random.randint(0, 150000)  # Часть ключей не существует
        test3_commands.append(f"get {key}")

    test3_input = f"{n}\n" + "\n".join(test3_commands)

    tests.append({
        "input": test3_input,
        "description": "100,000 уникальных ключей + 100,000 операций чтения",
        "expected": "max_test"
    })

    return tests


def generate_collision_cases():
    """Тесты на коллизии хешей"""
    tests = []

    # Тест 1: Ключи с одинаковыми хешами (если capacity=100000)
    test1_commands = []
    n = 1000

    # Ключи, которые дают одинаковые хеши при capacity=100000
    base_key = 100000
    for i in range(n):
        key = base_key + i * 100000  # Все дают одинаковый хеш
        if i < 500:
            test1_commands.append(f"put {key} {i}")
        else:
            test1_commands.append(f"get {key}")

    test1_input = f"{n}\n" + "\n".join(test1_commands)

    tests.append({
        "input": test1_input,
        "description": "Тест на коллизии хешей",
        "expected": "collision_test"
    })

    return tests


def solve_hash_table_problem(input_data):
    """
    Эталонное решение для вычисления ожидаемых результатов
    """
    lines = input_data.strip().split('\n')
    if not lines:
        return ""

    try:
        n = int(lines[0])
    except:
        return "ERROR: Invalid input"

    # Используем обычный dict как эталон (только для проверки!)
    database = {}
    output_lines = []

    for i in range(1, n + 1):
        if i >= len(lines):
            break

        line = lines[i].strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) == 0:
            continue

        command = parts[0]

        if command == "put":
            if len(parts) < 3:
                continue
            key, value = int(parts[1]), int(parts[2])
            database[key] = value

        elif command == "get":
            if len(parts) < 2:
                output_lines.append("None")
                continue
            key = int(parts[1])
            output_lines.append(str(database.get(key, "None")))

        elif command == "delete":
            if len(parts) < 2:
                output_lines.append("None")
                continue
            key = int(parts[1])
            if key in database:
                output_lines.append(str(database[key]))
                del database[key]
            else:
                output_lines.append("None")

    return "\n".join(output_lines)