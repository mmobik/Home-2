import time
import tracemalloc
import sys
import os
from io import StringIO
from tests.test_cases import generate_test_cases
import importlib.util

# Импорт main из Tasks/task_2.py через importlib
spec = importlib.util.spec_from_file_location("task_main", os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Tasks/task_2.py")))
task_main_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task_main_module)
main = task_main_module.main

def progress_bar(current, total, bar_length=40):
    """Прогресс-бар в консоли"""
    percent = float(current) * 100 / total
    arrow = '█' * int(percent / 100 * bar_length)
    spaces = '░' * (bar_length - len(arrow))
    sys.stdout.write(f'\r│{arrow}{spaces}│ {current}/{total} ({percent:.1f}%)')
    sys.stdout.flush()

def is_small_test(input_data, threshold=20):
    """
    Проверяет, является ли тест легким (по количеству глав N)
    """
    if not input_data:
        return True
    try:
        n = int(input_data.split('\n')[0])
        return n <= threshold
    except:
        # Если не удалось распарсить, считаем маленьким
        return True

def save_test_result(test_number, description, input_data, result, expected, status, time_taken, memory_used, is_small):
    """
    Сохраняет результат теста в файл внутри tests
    """
    result_dir = os.path.join(os.path.dirname(__file__), "tests")
    if is_small:
        filename = os.path.join(result_dir, 'results_small.txt')
        mode = 'a' if test_number > 1 else 'w'
    else:
        large_dir = os.path.join(result_dir, 'large_results')
        os.makedirs(large_dir, exist_ok=True)
        filename = os.path.join(large_dir, f'test_{test_number}_result.txt')
        mode = 'w'
    with open(filename, mode, encoding='utf-8') as f:
        if is_small and test_number == 1:
            f.write("ЛЕГКИЕ ТЕСТЫ (полный вывод)\n")
            f.write("=" * 80 + "\n\n")
        f.write(f"ТЕСТ {test_number}\n")
        f.write("-" * 60 + "\n")
        f.write(f"Описание: {description}\n")
        f.write(f"Статус: {status}\n")
        f.write(f"Время: {time_taken:.8f} сек\n")
        f.write(f"Память: {memory_used:.6f} МБ\n\n")
        f.write("ВХОДНЫЕ ДАННЫЕ:\n")
        f.write(input_data + "\n\n")
        f.write("ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:\n")
        f.write(str(expected) + "\n\n")
        f.write("ФАКТИЧЕСКИЙ РЕЗУЛЬТАТ:\n")
        f.write(str(result) + "\n\n")
        f.write("\n" + "=" * 60 + "\n\n")
    return filename

def run_tests_simple():
    test_cases = generate_test_cases()
    total_tests = len(test_cases)
    passed_tests = 0
    # Чистим старые результаты
    result_dir = os.path.join(os.path.dirname(__file__), "tests")
    small_file = os.path.join(result_dir, 'results_small.txt')
    large_dir = os.path.join(result_dir, 'large_results')
    if os.path.exists(small_file):
        os.remove(small_file)
    if os.path.exists(large_dir):
        for file in os.listdir(large_dir):
            os.remove(os.path.join(large_dir, file))
    else:
        os.makedirs(large_dir, exist_ok=True)
    print("Запуск тестов...")
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
            sys.stdin = StringIO(input_data)
            tracemalloc.start()
            start_time = time.perf_counter()
            result = main()
            end_time = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            time_taken = end_time - start_time
            memory_used = peak / (1024 * 1024)
            # Проверка результата
            if str(result) == str(expected):
                status = "✅ ПРОЙДЕН"
                passed_tests += 1
        except Exception as e:
            result = f"ОШИБКА: {e}"
        finally:
            sys.stdin = old_stdin
        is_small = is_small_test(input_data)
        save_test_result(i, description, input_data, result, expected, status, time_taken, memory_used, is_small)
    print(f"\n\nПройдено {passed_tests} из {total_tests} тестов.")

if __name__ == "__main__":
    start = time.time()
    run_tests_simple()
    print("\nОбщее время выполнения: {:.2f} сек".format(time.time() - start))

