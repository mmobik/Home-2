"""
Модуль для запуска тестов задачи 5 с базой данных.

Этот модуль предоставляет функциональность для запуска комплексных тестов
решения задачи с базой данных, измеряя метрики производительности такие как
время выполнения и использование памяти. Результаты тестов сохраняются в
форматах JSON и текстовом для последующего анализа.
"""

import time
import tracemalloc
import sys
import os
from io import StringIO
from test_cases import generate_test_cases
import traceback
import json
from datetime import datetime


def run_tests():
    """
    Выполняет все тестовые случаи и генерирует комплексные отчеты.
    
    Функция выполняет следующие операции:
    1. Загружает тестовые случаи из модуля test_cases
    2. Динамически импортирует модуль с решением
    3. Выполняет каждый тест с мониторингом производительности
    4. Сохраняет результаты отдельных тестов и итоговые отчеты
    
    Returns:
        tuple: Кортеж содержащий (passed_tests, total_tests)
            - passed_tests (int): Количество пройденных тестов
            - total_tests (int): Общее количество выполненных тестов
    
    Побочные эффекты:
        - Создает директорию 'tests/large_results' если она не существует
        - Генерирует JSON и текстовые файлы с результатами тестов
        - Удаляет временные файлы базы данных после каждого теста
    """
    test_cases = generate_test_cases()
    total_tests = len(test_cases)
    passed_tests = 0

    print("Запуск тестов для задачи с базой данных...")
    print(f"Всего тестов: {total_tests}")

    results_dir = os.path.join("tests", "large_results")
    os.makedirs(results_dir, exist_ok=True)
    
    all_results = []
    test_run_start = datetime.now()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    solution_path = os.path.abspath(os.path.join(current_dir, "..", "..", "Tasks", "task_5.py"))

    if not os.path.exists(solution_path):
        print(f"Файл решения не найден: {solution_path}")
        return 0, total_tests

    print(f"Найдено решение: {solution_path}")

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("task_solution", solution_path)
        task_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(task_module)

        if hasattr(task_module, 'main'):
            main = task_module.main
        else:
            print("Функция main не найдена, создаем обертку")

            print("Доступные атрибуты в модуле:")
            for attr in dir(task_module):
                if not attr.startswith('_'):
                    print(f"  - {attr}")

            def fallback_main():
                """Резервная функция main когда решение не предоставляет свою."""
                input_data = sys.stdin.read().strip().split('\n')
                if not input_data:
                    return

                n = int(input_data[0])
                print("ERROR: Решение не реализовано")

            main = fallback_main

    except Exception as e:
        print(f"Ошибка импорта решения:")
        print(f"   Тип ошибки: {type(e).__name__}")
        print(f"   Сообщение: {e}")
        print("   Полный traceback:")
        traceback.print_exc()
        return 0, total_tests

    for i, case in enumerate(test_cases, 1):
        print(f"\nТест {i}/{total_tests}: {case.get('description', '')}")

        input_data = case["input"]
        expected = case.get("expected", None)
        check_result_only = "result" in case

        test_data_file = f"test_{i}_database.dat"
        test_index_file = f"test_{i}_index.json"
        
        for old_file in [test_data_file, test_index_file, "database.dat", "index.json"]:
            if os.path.exists(old_file):
                try:
                    os.remove(old_file)
                except:
                    pass

        time_taken = 0
        memory_used = 0
        status = "НЕ ПРОЙДЕН"
        result = None

        try:
            old_stdin = sys.stdin
            old_stdout = sys.stdout
            
            sys.stdin = StringIO(input_data)
            captured_output = StringIO()
            sys.stdout = captured_output

            tracemalloc.start()
            start_time = time.perf_counter()

            main()

            end_time = time.perf_counter()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            time_taken = end_time - start_time
            memory_used = peak / (1024 * 1024)
            result = captured_output.getvalue().strip()

            if check_result_only:
                status = "ПРОЙДЕН (выполнение без ошибок)"
                passed_tests += 1
            elif result == expected:
                status = "ПРОЙДЕН"
                passed_tests += 1

        except Exception as e:
            result = f"ОШИБКА ВЫПОЛНЕНИЯ: {str(e)}"
            print(f"   Ошибка выполнения: {e}")
            traceback.print_exc()
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout
            
            for test_file in [test_data_file, test_index_file, "database.dat", "index.json"]:
                if os.path.exists(test_file):
                    try:
                        os.remove(test_file)
                    except:
                        pass

        print(f"  Статус: {status}")
        print(f"  Время: {time_taken:.6f} сек")
        print(f"  Память: {memory_used:.2f} МБ")

        if not status.startswith("ПРОЙДЕН"):
            if not check_result_only:
                print(f"  Ожидалось: {expected}")
            print(f"  Получено: {result}")

        test_result = {
            "test_number": i,
            "total_tests": total_tests,
            "description": case.get('description', ''),
            "status": status,
            "passed": status.startswith("ПРОЙДЕН"),
            "time_seconds": time_taken,
            "memory_mb": memory_used,
            "input_data": input_data,
            "expected_output": expected if not check_result_only else "N/A (проверка только выполнения)",
            "actual_output": result,
            "check_result_only": check_result_only
        }
        
        all_results.append(test_result)
        
        test_result_file = os.path.join(results_dir, f"test_{i:02d}_result.json")
        try:
            with open(test_result_file, 'w', encoding='utf-8') as f:
                json.dump(test_result, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"  Не удалось сохранить результат теста: {e}")
        
        test_result_txt = os.path.join(results_dir, f"test_{i:02d}_result.txt")
        try:
            with open(test_result_txt, 'w', encoding='utf-8') as f:
                f.write(f"Тест {i}/{total_tests}: {case.get('description', '')}\n")
                f.write(f"{'='*80}\n\n")
                f.write(f"Статус: {status}\n")
                f.write(f"Время: {time_taken:.6f} сек\n")
                f.write(f"Память: {memory_used:.2f} МБ\n\n")
                
                f.write(f"Входные данные (первые 1000 символов):\n")
                f.write(f"{'-'*80}\n")
                f.write(f"{input_data[:1000]}\n")
                if len(input_data) > 1000:
                    f.write(f"... (всего {len(input_data)} символов)\n")
                f.write(f"\n")
                
                if not check_result_only:
                    f.write(f"Ожидаемый вывод (первые 1000 символов):\n")
                    f.write(f"{'-'*80}\n")
                    expected_str = str(expected)
                    f.write(f"{expected_str[:1000]}\n")
                    if len(expected_str) > 1000:
                        f.write(f"... (всего {len(expected_str)} символов)\n")
                    f.write(f"\n")
                
                f.write(f"Фактический вывод (первые 1000 символов):\n")
                f.write(f"{'-'*80}\n")
                result_str = str(result)
                f.write(f"{result_str[:1000]}\n")
                if len(result_str) > 1000:
                    f.write(f"... (всего {len(result_str)} символов)\n")
        except Exception as e:
            print(f"  Не удалось сохранить текстовый результат теста: {e}")

    print(f"\nИтог: Пройдено {passed_tests} из {total_tests} тестов.")
    
    test_run_end = datetime.now()
    test_run_duration = (test_run_end - test_run_start).total_seconds()
    
    summary = {
        "test_run_start": test_run_start.isoformat(),
        "test_run_end": test_run_end.isoformat(),
        "total_duration_seconds": test_run_duration,
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": total_tests - passed_tests,
        "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
        "results": all_results
    }
    
    summary_file = os.path.join(results_dir, "summary.json")
    try:
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"\nРезультаты сохранены в: {results_dir}")
        print(f"   - summary.json - итоговый отчет")
        print(f"   - test_XX_result.json - результаты каждого теста (JSON)")
        print(f"   - test_XX_result.txt - результаты каждого теста (текст)")
    except Exception as e:
        print(f"\nНе удалось сохранить итоговый отчет: {e}")
    
    summary_txt = os.path.join(results_dir, "summary.txt")
    try:
        with open(summary_txt, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("ИТОГОВЫЙ ОТЧЕТ ПО ТЕСТИРОВАНИЮ\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Начало тестирования: {test_run_start.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Окончание тестирования: {test_run_end.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Общее время выполнения: {test_run_duration:.2f} сек\n\n")
            
            f.write(f"Всего тестов: {total_tests}\n")
            f.write(f"Пройдено: {passed_tests}\n")
            f.write(f"Провалено: {total_tests - passed_tests}\n")
            f.write(f"Процент успеха: {passed_tests / total_tests * 100:.2f}%\n\n")
            
            f.write("="*80 + "\n")
            f.write("РЕЗУЛЬТАТЫ ТЕСТОВ\n")
            f.write("="*80 + "\n\n")
            
            for result in all_results:
                f.write(f"Тест {result['test_number']}/{result['total_tests']}: {result['description']}\n")
                f.write(f"  Статус: {result['status']}\n")
                f.write(f"  Время: {result['time_seconds']:.6f} сек\n")
                f.write(f"  Память: {result['memory_mb']:.2f} МБ\n")
                f.write("\n")
    except Exception as e:
        print(f"Не удалось сохранить текстовый итоговый отчет: {e}")
    
    return passed_tests, total_tests


if __name__ == "__main__":
    passed, total = run_tests()
    sys.exit(0 if passed == total else 1)
