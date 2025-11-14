import time
import tracemalloc
import sys
import os
from io import StringIO
from test_cases import generate_test_cases
from test_utils import solve_database_problem, setup_task_main, is_small_test, progress_bar


def save_test_result(test_number, description, input_data, result, expected, status, time_taken, memory_used, is_small):
    """Сохраняет результат теста"""
    result_dir = os.path.join(os.path.dirname(__file__), "tests")
    os.makedirs(result_dir, exist_ok=True)

    # Создаем large_dir заранее
    large_dir = os.path.join(result_dir, 'large_results')
    os.makedirs(large_dir, exist_ok=True)

    if is_small:
        filename = os.path.join(result_dir, 'results_small.txt')
        mode = 'a' if test_number > 1 else 'w'
    else:
        filename = os.path.join(large_dir, f'test_{test_number}_result.txt')
        mode = 'w'

    with open(filename, mode, encoding='utf-8') as f:
        if is_small and test_number == 1:
            f.write("ЛЕГКИЕ ТЕСТЫ\n")
            f.write("=" * 80 + "\n\n")

        f.write(f"ТЕСТ {test_number}\n")
        f.write("-" * 60 + "\n")
        f.write(f"Описание: {description}\n")
        f.write(f"Статус: {status}\n")
        f.write(f"Время: {time_taken:.6f} сек\n")
        f.write(f"Память: {memory_used:.2f} МБ")

        # Добавляем предупреждение о превышении памяти
        if memory_used > 4.0:
            f.write(" ❌ ПРЕВЫШЕНИЕ ЛИМИТА ПАМЯТИ (4 МБ)")
        f.write("\n\n")

        # Краткая версия для больших тестов
        if expected in ["external_memory_required", "huge_test"] or len(input_data) > 100000:
            f.write("ВХОДНЫЕ ДАННЫЕ: (сокращенно)\n")
            f.write(f"Количество операций: {input_data.split(chr(10))[0]}\n")
            f.write(f"Размер данных: {len(input_data)} символов\n")
            f.write("Полные данные в отдельном файле\n\n")

            # Сохраняем полные данные
            input_filename = os.path.join(large_dir, f'test_{test_number}_input.txt')
            with open(input_filename, 'w', encoding='utf-8') as input_file:
                input_file.write(input_data)
        else:
            f.write("ВХОДНЫЕ ДАННЫЕ:\n")
            f.write(input_data + "\n")
        f.write("\n")

        f.write("ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:\n")
        if expected == "external_memory_required":
            f.write("РЕШЕНИЕ ДОЛЖНО ИСПОЛЬЗОВАТЬ ВНЕШНЮЮ ПАМЯТЬ (макс. 4МБ ОЗУ)\n")
        else:
            f.write(str(expected) + "\n")
        f.write("\n")

        f.write("ФАКТИЧЕСКИЙ РЕЗУЛЬТАТ:\n")
        if result is None:
            f.write("НЕТ ВЫВОДА\n")
        else:
            f.write(str(result) + "\n")
        f.write("\n" + "=" * 60 + "\n\n")

    return filename


def check_memory_usage(memory_used_mb, test_description):
    """Проверяет, что решение использует не более 4МБ ОЗУ"""
    max_allowed_mb = 4.0  # 4 МБ по условию задачи

    if memory_used_mb > max_allowed_mb:
        print(f"❌ ПРЕВЫШЕНИЕ ПАМЯТИ: {memory_used_mb:.2f} МБ > {max_allowed_mb} МБ")
        print(f"   Тест: {test_description}")
        print("   Решение ДОЛЖНО использовать внешнюю память (файлы), а не ОЗУ!")
        return False
    else:
        print(f"✅ Память в норме: {memory_used_mb:.2f} МБ ≤ {max_allowed_mb} МБ")
        return True


def run_tests_simple():
    test_cases = generate_test_cases()
    total_tests = len(test_cases)
    passed_tests = 0
    memory_violations = 0

    # Очистка старых результатов
    result_dir = os.path.join(os.path.dirname(__file__), "tests")
    small_file = os.path.join(result_dir, 'results_small.txt')
    large_dir = os.path.join(result_dir, 'large_results')

    # Создаем папки заранее
    os.makedirs(result_dir, exist_ok=True)
    os.makedirs(large_dir, exist_ok=True)

    # Безопасная очистка файлов
    def safe_remove_files():
        try:
            if os.path.exists(small_file):
                os.remove(small_file)
        except PermissionError:
            print(f"⚠️ Не удалось удалить {small_file}, файл занят")

        try:
            for file in os.listdir(large_dir):
                file_path = os.path.join(large_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except PermissionError:
            print(f"⚠️ Не удалось очистить {large_dir}, некоторые файлы заняты")

    safe_remove_files()

    print("Запуск тестов для задачи с базой данных...")
    print(f"Всего тестов: {total_tests}")
    print("ВАЖНО: Решение должно использовать ВНЕШНЮЮ ПАМЯТЬ (максимум 4МБ ОЗУ)\n")

    # Настройка main функции
    main = setup_task_main()

    for i, case in enumerate(test_cases, 1):
        # Пропускаем уже выполненные тесты чтобы не генерировать заново
        progress_bar(i, total_tests)
        input_data = case["input"]
        expected = case["expected"]
        description = case.get("description", "")

        time_taken = 0
        memory_used = 0
        status = "❌ НЕ ПРОЙДЕН"
        result = None
        memory_ok = True

        try:
            # Для тестов внешней памяти выводим предупреждение
            if expected == "external_memory_required":
                print(f"\n⚡ Тест {i}: Проверка использования внешней памяти")
                print(f"   {description}")

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

            # Проверяем использование памяти для соответствующих тестов
            if expected == "external_memory_required":
                memory_ok = check_memory_usage(memory_used, description)
                if not memory_ok:
                    memory_violations += 1
                    status = "❌ ПРЕВЫШЕНИЕ ПАМЯТИ"
                else:
                    status = "✅ ПРОЙДЕН (память в норме)"
                    passed_tests += 1
            else:
                # Для обычных тестов сравниваем с ожидаемым
                expected_result = solve_database_problem(input_data)
                if result == expected_result:
                    status = "✅ ПРОЙДЕН"
                    passed_tests += 1
                else:
                    # Обновляем expected для сохранения в файл
                    expected = expected_result

        except Exception as e:
            result = f"ОШИБКА ВЫПОЛНЕНИЯ: {str(e)}"
            import traceback
            result += f"\n{traceback.format_exc()}"
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout

        is_small = is_small_test(input_data)
        save_test_result(i, description, input_data, result, expected, status, time_taken, memory_used, is_small)

    print(f"\n\nРезультаты:")
    print(f"Пройдено тестов: {passed_tests}/{total_tests}")
    if memory_violations > 0:
        print(f"❌ Нарушений памяти: {memory_violations}")
        print("   Решение ДОЛЖНО использовать внешние файлы, а не хранить все в ОЗУ!")
    else:
        print("✅ Нарушений памяти нет")

    return passed_tests, total_tests
