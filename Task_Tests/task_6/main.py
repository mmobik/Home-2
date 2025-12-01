import time
import tracemalloc
import sys
import os
from io import StringIO
from tests.test_cases import generate_test_cases, solve_hash_table_problem


def setup_task_main():
    """Настройка импорта main из решения задачи"""
    # Пробуем разные возможные пути к файлу решения
    possible_paths = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Tasks/task_18/main.py")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Tasks/task_6.py")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../task_6.py")),
    ]

    for task_path in possible_paths:
        if os.path.exists(task_path):
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("task_main", task_path)
                task_main_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(task_main_module)
                print(f"✅ Загружено решение из: {task_path}")
                return task_main_module.main
            except Exception as e:
                print(f"❌ Ошибка загрузки {task_path}: {e}")

    print("❌ Не удалось найти файл решения")
    return None


def progress_bar(current, total, bar_length=40):
    percent = float(current) * 100 / total
    arrow = '█' * int(percent / 100 * bar_length)
    spaces = '░' * (bar_length - len(arrow))
    sys.stdout.write(f'\r│{arrow}{spaces}│ {current}/{total} ({percent:.1f}%)')
    sys.stdout.flush()


def save_test_result(test_number, description, input_data, result, expected, status, time_taken, memory_used):
    """Сохраняет результат теста"""
    result_dir = os.path.join(os.path.dirname(__file__), "tests")
    os.makedirs(result_dir, exist_ok=True)

    large_dir = os.path.join(result_dir, 'large_results')
    os.makedirs(large_dir, exist_ok=True)

    filename = os.path.join(result_dir, 'test_results.txt')
    mode = 'a' if test_number > 1 else 'w'

    with open(filename, mode, encoding='utf-8') as f:
        if test_number == 1:
            f.write("ТЕСТЫ ДЛЯ ЗАДАЧИ 18 (ХЕШ-ТАБЛИЦА)\n")
            f.write("=" * 80 + "\n\n")

        f.write(f"ТЕСТ {test_number}\n")
        f.write("-" * 60 + "\n")
        f.write(f"Описание: {description}\n")
        f.write(f"Статус: {status}\n")
        f.write(f"Время: {time_taken:.6f} сек\n")
        f.write(f"Память: {memory_used:.2f} МБ\n\n")

        f.write("ВХОДНЫЕ ДАННЫЕ:\n")
        if len(input_data) > 10000:
            f.write(f"Количество операций: {input_data.split(chr(10))[0]}\n")
            f.write(f"Размер данных: {len(input_data)} символов\n")
            f.write("Полные данные сохранены в отдельном файле\n\n")

            input_filename = os.path.join(large_dir, f'test_{test_number}_input.txt')
            with open(input_filename, 'w', encoding='utf-8') as input_file:
                input_file.write(input_data)
        else:
            f.write(input_data + "\n")
        f.write("\n")

        f.write("ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:\n")
        if expected in ["max_test", "collision_test"]:
            f.write("ПРОВЕРКА ВЫПОЛНЕНИЯ БЕЗ ОШИБОК\n")
        else:
            f.write(str(expected) + "\n")
        f.write("\n")

        f.write("ФАКТИЧЕСКИЙ РЕЗУЛЬТАТ:\n")
        if result is None:
            f.write("НЕТ ВЫВОДА\n")
        elif len(str(result)) > 10000:
            f.write(f"Размер вывода: {len(str(result))} символов\n")
            result_lines = str(result).split('\n')
            f.write(f"Количество строк: {len(result_lines)}\n")
            f.write("Первые 10 строк:\n")
            f.write('\n'.join(result_lines[:10]) + "\n")
            f.write("...\n")
            f.write("Полный вывод сохранен в отдельном файле\n")
            
            # Сохранение полного вывода в отдельный файл
            output_filename = os.path.join(large_dir, f'test_{test_number}_output.txt')
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                output_file.write(str(result))
        else:
            f.write(str(result) + "\n")
        f.write("\n" + "=" * 60 + "\n\n")

    return filename


def run_tests_simple():
    test_cases = generate_test_cases()
    total_tests = len(test_cases)
    passed_tests = 0

    # Очистка старых результатов
    result_dir = os.path.join(os.path.dirname(__file__), "tests")
    result_file = os.path.join(result_dir, 'test_results.txt')
    large_dir = os.path.join(result_dir, 'large_results')

    os.makedirs(result_dir, exist_ok=True)
    os.makedirs(large_dir, exist_ok=True)

    if os.path.exists(result_file):
        os.remove(result_file)

    # Очистка больших файлов
    for file in os.listdir(large_dir):
        if file.startswith('test_') and (file.endswith('_input.txt') or file.endswith('_output.txt')):
            os.remove(os.path.join(large_dir, file))

    print("Запуск тестов для задачи 18 (Хеш-таблица)...")
    print(f"Всего тестов: {total_tests}")

    # Настройка main функции
    main = setup_task_main()
    if main is None:
        print("❌ Не удалось загрузить решение")
        return 0, total_tests

    for i, case in enumerate(test_cases, 1):
        progress_bar(i, total_tests)
        input_data = case["input"]
        expected = case["expected"]
        description = case.get("description", "")

        time_taken = 0
        memory_used = 0
        status = "❌ НЕ ПРОЙДЕН"
        result = None

        try:
            old_stdin = sys.stdin
            old_stdout = sys.stdout
            sys.stdin = StringIO(input_data)
            captured_output = StringIO()
            sys.stdout = captured_output

            tracemalloc.start()
            start_time = time.perf_counter()

            # Запуск main функции
            main()

            end_time = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            time_taken = end_time - start_time
            memory_used = peak / (1024 * 1024)
            result = captured_output.getvalue().strip()

            # Проверка результата
            if expected in ["max_test", "collision_test"]:
                # Для больших тестов проверяем выполнение без ошибок
                if "ERROR" not in str(result):
                    status = "✅ ПРОЙДЕН"
                    passed_tests += 1
                else:
                    status = "❌ ОШИБКА ВЫПОЛНЕНИЯ"
            else:
                # Для обычных тестов сравниваем с ожидаемым
                expected_result = solve_hash_table_problem(input_data)
                if result == expected_result:
                    status = "✅ ПРОЙДЕН"
                    passed_tests += 1
                else:
                    expected = expected_result

        except Exception as e:
            result = f"ОШИБКА ВЫПОЛНЕНИЯ: {str(e)}"
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout

        save_test_result(i, description, input_data, result, expected, status, time_taken, memory_used)

    print(f"\n\nПройдено {passed_tests} из {total_tests} тестов.")
    return passed_tests, total_tests


if __name__ == "__main__":
    start = time.time()
    passed, total = run_tests_simple()
    end = time.time()

    print(f"\nОбщее время выполнения: {end - start:.2f} сек")
    print(f"Результат: {passed}/{total} ({passed / total * 100:.1f}%)")

    if passed == total:
        print("🎉 Все тесты пройдены успешно!")
    else:
        print("❌ Некоторые тесты не пройдены.")
        print("Проверьте файл tests/test_results.txt")