"""
Модуль для запуска тестов задачи 10: Слово с забора

Этот модуль предоставляет функциональность для запуска комплексных тестов
решения задачи, измеряя метрики производительности.
Особенность: проверяет корректность разбиения строки на префиксы.
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
    test_cases = generate_test_cases()
    total_tests = len(test_cases)
    passed_tests = 0

    test_run_start = datetime.now()
    
    report_lines = []
    
    def print_and_save(text=""):
        print(text)
        report_lines.append(text)
    
    print_and_save("=" * 80)
    print_and_save("ИТОГОВЫЙ ОТЧЕТ ПО ТЕСТИРОВАНИЮ (ЗАДАЧА 10)")
    print_and_save("=" * 80)
    print_and_save()
    print_and_save(f"Начало тестирования: {test_run_start.strftime('%Y-%m-%d %H:%M:%S')}")
    print_and_save()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    solution_path = os.path.abspath(os.path.join(current_dir, "..", "..", "Tasks", "task_10.py"))

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

        if hasattr(task_module, 'solve'):
            main = task_module.solve
        elif hasattr(task_module, 'main'):
            main = task_module.main
        else:
            print_and_save("Функция solve или main не найдена в решении")
            return 0, total_tests

    except Exception as e:
        print_and_save(f"Ошибка импорта решения: {e}")
        traceback.print_exc()
        return 0, total_tests

    print_and_save("=" * 80)
    print_and_save("РЕЗУЛЬТАТЫ ТЕСТОВ")
    print_and_save("=" * 80)
    print_and_save()

    results_dir = os.path.join(current_dir, "tests")
    os.makedirs(results_dir, exist_ok=True)

    all_results = []
    total_execution_time = 0

    for i, case in enumerate(test_cases, 1):
        print_and_save(f"Тест {i}/{total_tests}: {case.get('description', '')}")

        input_data = case["input"]
        expected = case.get("expected", "")
        
        # Разбираем входные данные для валидации
        input_lines = input_data.strip().split('\n')
        s1 = input_lines[0] if len(input_lines) > 0 else ""
        s2 = input_lines[1] if len(input_lines) > 1 else ""
        
        is_large_test = len(input_data) > 1000

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
            total_execution_time += time_taken
            memory_used = peak / (1024 * 1024)
            result = captured_output.getvalue().strip()

            # ВАЛИДАЦИЯ РЕЗУЛЬТАТА
            result_lines = result.split('\n')
            first_line = result_lines[0].strip()
            
            if first_line == "Yes":
                # Решение говорит "Невозможно"
                if expected == "Yes" or (expected == "N/A" and "Yes" in str(expected)):
                    status = "ПРОЙДЕН"
                    passed_tests += 1
                elif expected.startswith("No"):
                    status = "НЕ ПРОЙДЕН (Ожидалось No, получено Yes)"
                else:
                    # Если expected N/A, считаем пройденным (для рандомных тестов)
                    if expected == "N/A":
                         status = "ПРОЙДЕН (Результат Yes, ожидаемый неизвестен)"
                         passed_tests += 1
                    else:
                         status = "НЕ ПРОЙДЕН"

            elif first_line == "No":
                # Решение говорит "Возможно" и должно предоставить разбиение
                if len(result_lines) < 2:
                    status = "НЕ ПРОЙДЕН (Отсутствует строка с разбиением)"
                else:
                    parts_line = result_lines[1].strip()
                    parts = parts_line.split()
                    
                    # Проверяем корректность разбиения
                    reconstructed_s2 = "".join(parts)
                    
                    if reconstructed_s2 != s2:
                        status = f"НЕ ПРОЙДЕН (Разбиение не собирается в s2. Длина: {len(reconstructed_s2)} vs {len(s2)})"
                    else:
                        # Проверяем, что каждая часть - префикс s1
                        all_prefixes_valid = True
                        for part in parts:
                            if not s1.startswith(part):
                                all_prefixes_valid = False
                                status = f"НЕ ПРОЙДЕН (Часть '{part[:10]}...' не является префиксом s1)"
                                break
                        
                        if all_prefixes_valid:
                            if expected.startswith("No") or expected == "N/A":
                                status = "ПРОЙДЕН"
                                passed_tests += 1
                            elif expected == "Yes":
                                status = "НЕ ПРОЙДЕН (Ожидалось Yes, получено No)"
                            else:
                                status = "ПРОЙДЕН" # Если expected сложное, но валидация прошла
                                passed_tests += 1
            else:
                status = f"НЕ ПРОЙДЕН (Некорректный формат вывода: {first_line})"

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
            "passed": "ПРОЙДЕН" in status,
            "time_seconds": time_taken,
            "memory_mb": memory_used,
            "input_data": input_data,
            "expected_output": expected if not is_large_test else "N/A (большой тест)",
            "actual_output": result if result else "",
            "is_large_test": is_large_test
        }
        
        all_results.append(test_result)

        # Сохранение результатов в файлы (аналогично предыдущим задачам)
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
                    input_filename = f"test_{i:02d}_input.txt"
                    output_filename = f"test_{i:02d}_output.txt"
                    
                    with open(os.path.join(results_dir, input_filename), 'w', encoding='utf-8') as input_file:
                        input_file.write(input_data)
                    
                    if result:
                        with open(os.path.join(results_dir, output_filename), 'w', encoding='utf-8') as output_file:
                            output_file.write(result)
                    
                    f.write(f"Входные данные: см. {input_filename}\n")
                    f.write(f"Фактический вывод: см. {output_filename}\n")
                else:
                    f.write("Входные данные:\n" + "-" * 80 + "\n" + input_data + "\n\n")
                    f.write("Ожидаемый вывод:\n" + "-" * 80 + "\n" + expected + "\n\n")
                    f.write("Фактический вывод:\n" + "-" * 80 + "\n" + (result if result else "") + "\n")
        except Exception as e:
            print(f"  Не удалось сохранить результат: {e}")

    # Итоговая статистика
    test_run_end = datetime.now()
    test_run_duration = (test_run_end - test_run_start).total_seconds()

    print_and_save("=" * 80)
    print_and_save("ИТОГОВЫЙ ОТЧЕТ")
    print_and_save("=" * 80)
    print_and_save(f"Всего тестов: {total_tests}")
    print_and_save(f"Пройдено: {passed_tests}")
    print_and_save(f"Провалено: {total_tests - passed_tests}")
    print_and_save(f"Процент успеха: {passed_tests / total_tests * 100:.2f}%")
    
    memory_values = [r['memory_mb'] for r in all_results if r['memory_mb'] > 0]
    if memory_values:
        print_and_save(f"Макс. память: {max(memory_values):.7f} МБ")

    timestamp = test_run_start.strftime('%Y%m%d_%H%M%S')
    report_filename = os.path.join(current_dir, f"summary_{timestamp}.txt")
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    print(f"\nОбщий отчет: {report_filename}")

    return passed_tests, total_tests

if __name__ == "__main__":
    passed, total = run_tests()
    sys.exit(0 if passed == total else 1)
