import sys
from Algorithms_and_structures import HashTable


def main():
    n = int(sys.stdin.readline().strip())
    hash_table = HashTable(capacity=100000)
    output_lines = []

    for _ in range(n):
        line = sys.stdin.readline().strip()
        if not line:
            continue

        parts = line.split()
        command = parts[0]

        if command == "put":
            key, value = int(parts[1]), int(parts[2])
            hash_table.put(key, value)

        elif command == "get":
            key = int(parts[1])
            result = hash_table.get(key)
            output_lines.append(str(result) if result is not None else "None")

        elif command == "delete":
            key = int(parts[1])
            result = hash_table.delete(key)
            output_lines.append(str(result) if result is not None else "None")

    # Выводим все результаты после обработки всех команд
    for line in output_lines:
        print(line)


if __name__ == "__main__":
    main()
