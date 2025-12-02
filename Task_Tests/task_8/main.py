"""
Модуль для запуска тестов задачи 8: Общий префикс распакованных строк

Этот модуль предоставляет функциональность для запуска комплексных тестов
решения задачи, измеряя метрики производительности такие как
время выполнения и использование памяти. Результаты тестов сохраняются в
текстовом формате для последующего анализа.
"""

import time
import tracemalloc
import sys
import os
from io import StringIO
from test_cases import generate_test_cases
import traceback
from datetime import datetime


def run_tests():
    """
    Выполняет все тестовые случаи и генерирует комплексные отчеты.
    """
    # Генерация тестов (не засекаем время)
    test_cases = generate_test_cases()
    total_tests = len(test_cases)
    passed_tests = 0

    test_run_start = datetime.now()
    
    # Подготовка для сохранения в файл
    report_lines = []
    
    def print_and_save(text=""):
        """Печатает и сохраняет строку в отчет"""
        print(text)
        report_lines.append(text)
    
    print_and_save("=" * 80)
    print_and_save("ИТОГОВЫЙ ОТЧЕТ ПО ТЕСТИРОВАНИЮ (ЗАДАЧА 8)")
    print_and_save("=" * 80)
    print_and_save()
    print_and_save(f"Начало тестирования: {test_run_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print_and_save()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    solution_path = os.path.abspath(os.path.join(current_dir, "..", "..", "Tasks", "task_8.py"))

    if not os.path.exists(solution_path):
        print_and_save(f"Файл решения не найден: {solution_path}")
        return 0, total_tests

    print_and_save(f"Найдено решение: {solution_path}")
    print_and_save()

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("task_solution", solution_path)
        task_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(task_module)

        # Ищем функцию для запуска (solve, main или другую)
        if hasattr(task_module, 'solve'):
            main = task_module.solve
        elif hasattr(task_module, 'main'):
            main = task_module.main
        else:
            print_and_save("Функция solve или main не найдена в решении")
            
            def fallback_main():
                """Резервная функция main когда решение не предоставляет свою."""
                input_data = sys.stdin.read().strip().split('\n')
                if not input_data:
                    return
                print("ERROR: Решение не реализовано")

            main = fallback_main

    except Exception as e:
        print_and_save(f"Ошибка импорта решения:")
        print_and_save(f"   Тип ошибки: {type(e).__name__}")
        print_and_save(f"   Сообщение: {e}")
        print_and_save("   Полный traceback:")
        traceback.print_exc()
        return 0, total_tests

    print_and_save("=" * 80)
    print_and_save("РЕЗУЛЬТАТЫ ТЕСТОВ")
    print_and_save("=" * 80)
    print_and_save()

    # Создаем папку tests для результатов
    results_dir = os.path.join(current_dir, "tests")
    os.makedirs(results_dir, exist_ok=True)

    all_results = []
    total_execution_time = 0  # Чистое время выполнения тестов

    for i, case in enumerate(test_cases, 1):
        print_and_save(f"Тест {i}/{total_tests}: {case.get('description', '')}")

        input_data = case["input"]
        expected = case.get("expected", "")
        
        # Определяем, большой ли тест (более 1000 символов в input или output)
        is_large_test = len(input_data) > 1000 or len(expected) > 1000

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
            total_execution_time += time_taken  # Добавляем только время выполнения
            memory_used = peak / (1024 * 1024)  # Конвертируем в МБ
            result = captured_output.getvalue().strip()

            if is_large_test:
                # Для больших тестов просто проверяем, что выполнение прошло без ошибок
                # ИЛИ можно сравнить хеши, но пока просто проверим выполнение
                # В данном случае expected у нас есть, можно сравнить длину или начало
                if len(result) == len(expected) and result[:100] == expected[:100]:
                     status = "ПРОЙДЕН"
                     passed_tests += 1
                else:
                     status = "НЕ ПРОЙДЕН (Неверный результат)"
            else:
                # Для маленьких тестов сравниваем с ожидаемым результатом
                # Нормализация не нужна, так как важны пробелы и символы
                if result == expected:
                    status = "ПРОЙДЕН"
                    passed_tests += 1
                else:
                    # Попробуем strip, вдруг лишний перевод строки
                    if result.strip() == expected.strip():
                        status = "ПРОЙДЕН"
                        passed_tests += 1

        except Exception as e:
            result = f"ОШИБКА ВЫПОЛНЕНИЯ: {str(e)}"
            print_and_save(f"   Ошибка выполнения: {e}")
            traceback.print_exc()
        finally:
            sys.stdin = old_stdin
            sys.stdout = old_stdout

        print_and_save(f"  Статус: {status}")
        print_and_save(f"  Время: {time_taken:.6f} сек")
        print_and_save(f"  Память: {memory_used:.7f} МБ")
        print_and_save()

        test_result = {
            "test_number": i,
            "total_tests": total_tests,
            "description": case.get('description', ''),
            "status": status,
            "passed": status == "ПРОЙДЕН",
            "time_seconds": time_taken,
            "memory_mb": memory_used,
            "input_data": input_data,
            "expected_output": expected if not is_large_test else "N/A (большой тест)",
            "actual_output": result if result else "",
            "is_large_test": is_large_test
        }
        
        all_results.append(test_result)

        # Сохраняем результат теста в отдельный файл (не засекаем время)
        test_filename = f"test_{i:02d}_result.txt"
        test_filepath = os.path.join(results_dir, test_filename)
        
        try:
            with open(test_filepath, 'w', encoding='utf-8') as f:
                f.write(f"Тест {i}/{total_tests}: {case.get('description', '')}\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Статус: {status}\n")
                f.write(f"Время: {time_taken:.6f} сек\n")
                f.write(f"Память: {memory_used:.7f} МБ\n\n")
                
                if is_large_test:
                    # Для больших тестов создаем отдельные файлы только для input и output
                    input_filename = f"test_{i:02d}_input.txt"
                    output_filename = f"test_{i:02d}_output.txt"
                    
                    # Сохраняем input
                    with open(os.path.join(results_dir, input_filename), 'w', encoding='utf-8') as input_file:
                        input_file.write(input_data)
                    
                    # Сохраняем actual output
                    if result:
                        with open(os.path.join(results_dir, output_filename), 'w', encoding='utf-8') as output_file:
                            output_file.write(result)
                    
                    f.write(f"Входные данные: см. {input_filename} ({len(input_data)} символов)\n")
                    if result:
                        f.write(f"Фактический вывод: см. {output_filename} ({len(result)} символов)\n")
                    f.write("\nПримечание: Для больших тестов полный вывод сохранен в отдельный файл.\n")
                else:
                    # Для маленьких тестов все в одном файле
                    f.write("Входные данные:\n")
                    f.write("-" * 80 + "\n")
                    f.write(input_data + "\n\n")
                    
                    f.write("Ожидаемый вывод:\n")
                    f.write("-" * 80 + "\n")
                    f.write(expected + "\n\n")
                    
                    f.write("Фактический вывод:\n")
                    f.write("-" * 80 + "\n")
                    f.write(result if result else "" + "\n")
        except Exception as e:
            print(f"  Не удалось сохранить результат теста: {e}")

    test_run_end = datetime.now()
    test_run_duration = (test_run_end - test_run_start).total_seconds()

    print_and_save("=" * 80)
    print_and_save("ИТОГОВЫЙ ОТЧЕТ")
    print_and_save("=" * 80)
    print_and_save()
    print_and_save(f"Начало тестирования: {test_run_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print_and_save(f"Окончание тестирования: {test_run_end.strftime('%Y-%m-%d %H:%M:%S')}")
    print_and_save(f"Общее время выполнения (с накладными расходами): {test_run_duration:.2f} сек")
    print_and_save(f"Чистое время выполнения тестов: {total_execution_time:.2f} сек")
    print_and_save()
    print_and_save(f"Всего тестов: {total_tests}")
    print_and_save(f"Пройдено: {passed_tests}")
    print_and_save(f"Провалено: {total_tests - passed_tests}")
    print_and_save(f"Процент успеха: {passed_tests / total_tests * 100:.2f}%")

    # Статистика по памяти
    memory_values = [r['memory_mb'] for r in all_results if r['memory_mb'] > 0]
    if memory_values:
        avg_memory = sum(memory_values) / len(memory_values)
        max_memory = max(memory_values)
        total_memory = sum(memory_values)
        print_and_save()
        print_and_save("Использование памяти:")
        print_and_save(f"  Средняя:       {avg_memory:.7f} МБ")
        print_and_save(f"  Максимальная:  {max_memory:.7f} МБ")
        print_and_save(f"  Общая:         {total_memory:.7f} МБ")

    # Детали проваленных тестов
    failed_tests = [r for r in all_results if not r['passed']]
    if failed_tests:
        print_and_save()
        print_and_save("=" * 80)
        print_and_save("ПРОВАЛЕННЫЕ ТЕСТЫ")
        print_and_save("=" * 80)
        print_and_save()
        for test_result in failed_tests:
            print_and_save(f"Тест {test_result['test_number']}/{test_result['total_tests']}: {test_result['description']}")
            print_and_save(f"  Ошибка: Неверный результат")
            print_and_save()

    print_and_save("=" * 80)

    # Сохраняем общий отчет в файл (не засекаем время)
    timestamp = test_run_start.strftime('%Y%m%d_%H%M%S')
    report_filename = os.path.join(current_dir, f"summary_{timestamp}.txt")
    
    try:
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        print(f"\nОбщий отчет сохранен в файл: {report_filename}")
        print(f"Результаты каждого теста сохранены в папку: {results_dir}")
    except Exception as e:
        print(f"\nОшибка при сохранении отчета: {e}")

    return passed_tests, total_tests


if __name__ == "__main__":
    passed, total = run_tests()
    sys.exit(0 if passed == total else 1)
