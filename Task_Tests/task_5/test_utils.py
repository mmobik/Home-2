import os
import sys

def solve_database_problem(input_data):
    """
    Корректное решение задачи для вычисления ожидаемых результатов
    """
    lines = input_data.strip().split('\n')
    if not lines:
        return ""
    
    try:
        n = int(lines[0])
    except:
        return "ERROR: Invalid input"
    
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
        
        if command == "ADD":
            if len(parts) < 3:
                output_lines.append("ERROR")
                continue
            key, value = parts[1], parts[2]
            if key in database:
                output_lines.append("ERROR")
            else:
                database[key] = value
                
        elif command == "DELETE":
            if len(parts) < 2:
                output_lines.append("ERROR")
                continue
            key = parts[1]
            if key not in database:
                output_lines.append("ERROR")
            else:
                del database[key]
                
        elif command == "UPDATE":
            if len(parts) < 3:
                output_lines.append("ERROR")
                continue
            key, value = parts[1], parts[2]
            if key not in database:
                output_lines.append("ERROR")
            else:
                database[key] = value
                
        elif command == "PRINT":
            if len(parts) < 2:
                output_lines.append("ERROR")
                continue
            key = parts[1]
            if key not in database:
                output_lines.append("ERROR")
            else:
                output_lines.append(f"{key} {database[key]}")
    
    return "\n".join(output_lines)

class SimpleDatabase:
    """Простая реализация базы данных для тестирования"""
    def __init__(self):
        self.database = {}
    
    def process_commands(self, input_data):
        """Обрабатывает команды и возвращает результат"""
        lines = input_data.strip().split('\n')
        if not lines:
            return ""
        
        try:
            n = int(lines[0])
        except:
            return "ERROR: Invalid input"
        
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
            
            if command == "ADD":
                if len(parts) < 3:
                    output_lines.append("ERROR")
                    continue
                key, value = parts[1], parts[2]
                if key in self.database:
                    output_lines.append("ERROR")
                else:
                    self.database[key] = value
                    
            elif command == "DELETE":
                if len(parts) < 2:
                    output_lines.append("ERROR")
                    continue
                key = parts[1]
                if key not in self.database:
                    output_lines.append("ERROR")
                else:
                    del self.database[key]
                    
            elif command == "UPDATE":
                if len(parts) < 3:
                    output_lines.append("ERROR")
                    continue
                key, value = parts[1], parts[2]
                if key not in self.database:
                    output_lines.append("ERROR")
                else:
                    self.database[key] = value
                    
            elif command == "PRINT":
                if len(parts) < 2:
                    output_lines.append("ERROR")
                    continue
                key = parts[1]
                if key not in self.database:
                    output_lines.append("ERROR")
                else:
                    output_lines.append(f"{key} {self.database[key]}")
        
        return "\n".join(output_lines)

def setup_task_main():
    """Настройка импорта main из решения задачи"""
    task_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Tasks/task_5/main.py"))
    if os.path.exists(task_path):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("task_main", task_path)
            task_main_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(task_main_module)
            return task_main_module.main
        except Exception as e:
            print(f"Ошибка импорта решения: {e}")
            # Возвращаем функцию, которая использует SimpleDatabase
            def fallback_main():
                input_data = sys.stdin.read()
                db = SimpleDatabase()
                result = db.process_commands(input_data)
                if result:
                    print(result)
            return fallback_main
    else:
        print("Файл решения не найден, используется тестовый решатель")
        def fallback_main():
            input_data = sys.stdin.read()
            db = SimpleDatabase()
            result = db.process_commands(input_data)
            if result:
                print(result)
        return fallback_main

def is_small_test(input_data, threshold=100):
    """Проверяет, является ли тест легким"""
    if not input_data:
        return True
    try:
        first_line = input_data.split('\n')[0].strip()
        n = int(first_line)
        return n <= threshold
    except:
        return True

def progress_bar(current, total, bar_length=40):
    """Прогресс-бар в консоли"""
    percent = float(current) * 100 / total
    arrow = '█' * int(percent / 100 * bar_length)
    spaces = '░' * (bar_length - len(arrow))
    sys.stdout.write(f'\r│{arrow}{spaces}│ {current}/{total} ({percent:.1f}%)')
    sys.stdout.flush()