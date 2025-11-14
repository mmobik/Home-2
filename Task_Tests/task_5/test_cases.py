import random
import string

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