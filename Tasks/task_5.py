import os
import sys
import json
from Algorithms_and_structures import HashTable


class ExternalMemoryDatabase:
    def __init__(self, data_file="database.dat", index_file="index.json"):
        self.data_file = data_file
        self.index_file = index_file
        self.index = HashTable()
        self.current_position = 0

        self._initialize_files()
        self._load_index()
        self._sync_current_position()

    def _initialize_files(self):
        # Создание файлов при первом запуске
        if not os.path.exists(self.data_file):
            open(self.data_file, 'wb').close()

    def _load_index(self):
        # Загрузка индекса из файла при старте программы
        try:
            if os.path.exists(self.index_file):
                with open(self.index_file, 'r') as f:
                    data = json.load(f)
                    for key, value in data['index'].items():
                        self.index.put(key, tuple(value))
                    self.current_position = data['current_position']
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
            # Если файл поврежден - начинаем с чистого листа
            self.index = HashTable()
            self.current_position = 0

    def _save_index(self):
        # Сохранение текущего состояния индекса в файл
        try:
            index_dict = {}
            for key in self.index:
                value = self.index.get(key)
                index_dict[key] = list(value) if value else []

            json_data = {
                'index': index_dict,
                'current_position': self.current_position
            }
            with open(self.index_file, 'w') as f:
                json.dump(json_data, f)
        except (IOError, TypeError):
            pass  # Игнорируем ошибки записи

    def _sync_current_position(self):
        # Синхронизация позиции с реальным размером файла
        try:
            self.current_position = os.path.getsize(self.data_file)
        except (OSError, FileNotFoundError):
            self.current_position = 0

    def _rebuild_database(self):
        # Полная перестройка файла данных без удаленных записей
        try:
            temp_file = self.data_file + ".tmp"
            new_index = HashTable()
            new_position = 0

            with open(temp_file, 'wb') as new_f:
                for key in self.index:
                    old_data = self.index.get(key)
                    if old_data is None:
                        continue
                    old_pos, key_size, value_size = old_data

                    # Чтение старой записи
                    with open(self.data_file, 'rb') as old_f:
                        old_f.seek(old_pos)
                        record_data = old_f.read(8 + key_size + value_size)

                    # Запись в новую позицию
                    new_f.write(record_data)
                    new_index.put(key, (new_position, key_size, value_size))
                    new_position += len(record_data)

            # Замена старого файла новым
            os.replace(temp_file, self.data_file)
            self.index = new_index
            self.current_position = new_position
            return True
        except (IOError, OSError, KeyError):
            return False

    def add(self, key, value):
        # Добавление новой записи
        if self.index.get(key) is not None:
            return False  # Ключ уже существует

        key_bytes = key.encode('utf-8')
        value_bytes = value.encode('utf-8')
        total_size = 8 + len(key_bytes) + len(value_bytes)  # 8 байт на размеры

        try:
            with open(self.data_file, 'ab') as f:
                position = self.current_position
                # Запись размера ключа (4 байта)
                f.write(len(key_bytes).to_bytes(4, byteorder='big'))
                f.write(key_bytes)
                # Запись размера значения (4 байта)
                f.write(len(value_bytes).to_bytes(4, byteorder='big'))
                f.write(value_bytes)

                self.index.put(key, (position, len(key_bytes), len(value_bytes)))
                self.current_position += total_size

            self._save_index()
            return True
        except (IOError, OSError):
            return False

    def delete(self, key):
        # Удаление записи по ключу
        if self.index.get(key) is None:
            return False  # Ключ не существует

        deleted_value = self.index.delete(key)
        if deleted_value is None:
            return False

        if self.index.size == 0:
            # Если удалили последнюю запись - очищаем файл
            try:
                with open(self.data_file, 'wb') as f:
                    f.truncate(0)
                self.current_position = 0
                if os.path.exists(self.index_file):
                    os.remove(self.index_file)
            except (IOError, OSError):
                return False
        else:
            # Перестраиваем базу без удаленной записи
            if not self._rebuild_database():
                return False
            self._save_index()

        return True

    def update(self, key, value):
        # Обновление значения существующей записи
        if self.index.get(key) is None:
            return False  # Ключ не существует

        old_data = self.index.get(key)
        # Удаляем старую запись и добавляем новую
        if not self.delete(key):
            return False

        if not self.add(key, value):
            # Откат в случае ошибки
            self.index.put(key, old_data)
            self._save_index()
            return False

        return True

    def print(self, key):
        # Вывод записи по ключу
        value = self.index.get(key)
        if value is None:
            return False  # Ключ не существует

        position, key_size, value_size = value

        try:
            with open(self.data_file, 'rb') as f:
                f.seek(position)
                # Чтение размера ключа
                stored_key_size = int.from_bytes(f.read(4), byteorder='big')
                stored_key = f.read(stored_key_size).decode('utf-8')
                # Чтение размера значения
                stored_value_size = int.from_bytes(f.read(4), byteorder='big')
                stored_value = f.read(stored_value_size).decode('utf-8')

                print(f"{stored_key} {stored_value}")
                return True
        except (IOError, OSError, UnicodeDecodeError, ValueError):
            return False


def main():
    database = ExternalMemoryDatabase()

    # Чтение количества команд
    n = int(sys.stdin.readline().strip())

    for _ in range(n):
        line = sys.stdin.readline().strip()
        parts = line.split()

        command = parts[0]

        if command == "ADD":
            if len(parts) == 3:
                if not database.add(parts[1], parts[2]):
                    print("ERROR")
            else:
                print("ERROR")

        elif command == "DELETE":
            if len(parts) == 2:
                if not database.delete(parts[1]):
                    print("ERROR")
            else:
                print("ERROR")

        elif command == "UPDATE":
            if len(parts) == 3:
                if not database.update(parts[1], parts[2]):
                    print("ERROR")
            else:
                print("ERROR")

        elif command == "PRINT":
            if len(parts) == 2:
                if not database.print(parts[1]):
                    print("ERROR")
            else:
                print("ERROR")


if __name__ == "__main__":
    main()
