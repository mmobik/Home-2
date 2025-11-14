]import time
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
        f.write(f"Память: {memory_used:.2f} МБ\n\n")
        
        f.write("ВХОДНЫЕ ДАННЫЕ:\n")
        # Для больших тестов сохраняем полные данные в отдельные файлы
        if len(input_data) > 50000:  # Очень большие тесты
            input_filename = os.path.join(large_dir, f'test_{test_number}_input.txt')
            with open(input_filename, 'w', encoding='utf-8') as input_file:
                input_file.write(input_data)
            f.write(f"Сохранено в файл: {input_filename}\n")
            f.write(f"Размер: {len(input_data)} символов\n")
        elif len(input_data) > 1000:
            f.write(input_data[:1000] + f"\n... [еще {len(input_data) - 1000} символов]\n")
        else:
            f.write(input_data + "\n")
        f.write("\n")
        
        f.write("ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:\n")
        if len(str(expected)) > 50000:  # Очень большие ожидаемые результаты
            expected_filename = os.path.join(large_dir, f'test_{test_number}_expected.txt')
            with open(expected_filename, 'w', encoding='utf-8') as expected_file:
                expected_file.write(str(expected))
            f.write(f"Сохранено в файл: {expected_filename}\n")
            f.write(f"Размер: {len(str(expected))} символов\n")
        elif len(str(expected)) > 1000:
            f.write(str(expected)[:1000] + f"\n... [еще {len(str(expected)) - 1000} символов]\n")
        else:
            f.write(str(expected) + "\n")
        f.write("\n")
        
        f.write("ФАКТИЧЕСКИЙ РЕЗУЛЬТАТ:\n")
        if result is None:
            f.write("НЕТ ВЫВОДА\n")
        elif len(str(result)) > 50000:  # Очень большие фактические результаты
            result_filename = os.path.join(large_dir, f'test_{test_number}_actual.txt')
            with open(result_filename, 'w', encoding='utf-8') as result_file:
                result_file.write(str(result))
            f.write(f"Сохранено в файл: {result_filename}\n")
            f.write(f"Размер: {len(str(result))} символов\n")
        elif len(str(result)) > 1000:
            f.write(str(result)[:1000] + f"\n... [еще {len(str(result)) - 1000} символов]\n")
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
    small_file = os.path.join(result_dir, 'results_small.txt')
    large_dir = os.path.join(result_dir, 'large_results')
    
    # Создаем папки заранее
    os.makedirs(result_dir, exist_ok=True)
    os.makedirs(large_dir, exist_ok=True)
    
    if os.path.exists(small_file):
        os.remove(small_file)
    
    # Очищаем только файлы, не саму папку
    for file in os.listdir(large_dir):
        file_path = os.path.join(large_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    
    print("Запуск тестов для задачи с базой данных...")
    print(f"Всего тестов: {total_tests}")
    
    # Настройка main функции
    main = setup_task_main()
    
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
            
            # Сравниваем результат с ожидаемым
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
    
    print(f"\n\nПройдено {passed_tests} из {total_tests} тестов.")
    return passed_tests, total_tests