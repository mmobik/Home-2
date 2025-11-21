import time
import tracemalloc
import sys
import os
from io import StringIO
from test_cases import generate_test_cases
import traceback


def run_tests():
    test_cases = generate_test_cases()
    total_tests = len(test_cases)
    passed_tests = 0

    print("Запуск тестов для задачи с базой данных...")
    print(f"Всего тестов: {total_tests}")

    # Правильный путь к решению
    solution_path = r"C:\Users\hak18\PycharmProjects\Home-2\Tasks\task_5.py"

    if not os.path.exists(solution_path):
        print(f"❌ Файл решения не найден: {solution_path}")
        return 0, total_tests

    print(f"✅ Найдено решение: {solution_path}")

    try:
        # Динамический импорт
        import importlib.util
        spec = importlib.util.spec_from_file_location("task_solution", solution_path)
        task_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(task_module)

        # Ищем функцию main
        if hasattr(task_module, 'main'):
            main = task_module.main
        else:
            # Если нет main, создаем обертку
            print("⚠️ Функция main не найдена, создаем обертку")

            # Проверяем какие классы/функции есть в модуле
            print("Доступные атрибуты в модуле:")
            for attr in dir(task_module):
                if not attr.startswith('_'):
                    print(f"  - {attr}")

            # Создаем простую обертку
            def fallback_main():
                # Читаем входные данные
                input_data = sys.stdin.read().strip().split('\n')
                if not input_data:
                    return

                n = int(input_data[0])
                # Здесь должна быть логика твоего решения
                # Это временная заглушка
                print("ERROR: Решение не реализовано")

            main = fallback_main

    except Exception as e:
        print(f"❌ Ошибка импорта решения:")
        print(f"   Тип ошибки: {type(e).__name__}")
        print(f"   Сообщение: {e}")
        print("   Полный traceback:")
        traceback.print_exc()
        return 0, total_tests

    for i, case in enumerate(test_cases, 1):
        print(f"\nТест {i}/{total_tests}: {case.get('description', '')}")

        input_data = case["input"]
        expected = case["expected"]

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
            if result == expected:
                status = "✅ ПРОЙДЕН"
                passed_tests += 1

        except Exception as e:
            result = f"ОШИБКА ВЫПОЛНЕНИЯ: {str(e)}"
            print(f"   Ошибка выполнения: {e}")
            traceback.print_exc()
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout

        print(f"  Статус: {status}")
        print(f"  Время: {time_taken:.6f} сек")
        print(f"  Память: {memory_used:.2f} МБ")

        if status == "❌ НЕ ПРОЙДЕН":
            print(f"  Ожидалось: {expected}")
            print(f"  Получено: {result}")

    print(f"\nИтог: Пройдено {passed_tests} из {total_tests} тестов.")
    return passed_tests, total_tests


if __name__ == "__main__":
    passed, total = run_tests()
    sys.exit(0 if passed == total else 1)
