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
                while i < len(s) and s[i].isdigit():  # проверка i < len(s)
                    num = num * 10 + int(s[i])
                    i += 1
                if i < len(s) and s[i] == '[':  # Проверяем, что есть '['
                    i += 1  # Пропускаем '['
                    # Сохраняем текущий контекст
                    stack.append((result, num))
                    result = []
                else:
                    # Если нет '[', то это просто цифры
                    result.append(str(num))
            elif s[i] == ']':
                i += 1
                if stack:  # Проверяем, что стек не пустой
                    # Повторяем внутренний блок
                    inner = ''.join(result)
                    prev_result, repeat = stack.pop()
                    prev_result.append(inner * repeat)
                    result = prev_result
                # Иначе игнорируем лишнюю ']'
            else:
                # Другие символы (пропускаем или обрабатываем)
                result.append(s[i])
                i += 1
        return ''.join(result)
    
    # Возвращаем символы распакованной строки
    unpacked = fully_unpack(s)
    for ch in unpacked:
        yield ch

def main():
    try:
        n_line = sys.stdin.readline()
        if not n_line:
            return
        n = int(n_line.strip())
    except ValueError:
        return
    
    strings = []
    for _ in range(n):
        line = sys.stdin.readline()
        if line:
            strings.append(line.strip())
        else:
            strings.append("")
    
    if n == 0:
        print("")
        return
    
    # Создаём генераторы для каждой строки
    gens = [unpack_generator(s) for s in strings]
    prefix = []
    
    try:
        while True:
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
