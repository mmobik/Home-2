import sys

def unpack_generator(s):
    """Генератор, лениво распаковывающий строку."""
    # Вспомогательная функция полной распаковки
    def fully_unpack(s):
        stack = []
        result = []
        i = 0
        while i < len(s):
            if s[i].islower():
                result.append(s[i])
                i += 1
            elif s[i].isdigit():
                num = 0
                # Читаем число целиком
                while s[i].isdigit():
                    num = num * 10 + int(s[i])
                    i += 1
                i += 1  # Пропускаем '['
                # Сохраняем текущий контекст
                stack.append((result, num))
                result = []
            elif s[i] == ']':
                i += 1
                # Повторяем внутренний блок
                inner = ''.join(result)
                prev_result, repeat = stack.pop()
                prev_result.append(inner * repeat)
                result = prev_result
        return ''.join(result)
    
    # Возвращаем символы распакованной строки
    unpacked = fully_unpack(s)
    for ch in unpacked:
        yield ch

def main():
    n = int(sys.stdin.readline())
    strings = [sys.stdin.readline().strip() for _ in range(n)]
    
    # Создаём генераторы для каждой строки
    gens = [unpack_generator(s) for s in strings]
    prefix = []
    
    try:
        while True:
            # Берём символ из первой строки
            first_char = next(gens[0])
            # Сверяем с остальными
            for i in range(1, n):
                if next(gens[i]) != first_char:
                    print(''.join(prefix))
                    return
            prefix.append(first_char)
    except StopIteration:
        # Конец хотя бы одной строки
        print(''.join(prefix))

if __name__ == "__main__":
    main()
