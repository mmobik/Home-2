import sys

def minimal_palindrome_extension(s):
    n = len(s)
    if n == 0:
        return ""
    
    # Особый случай: строка из одного символа
    if n == 1:
        return s + s  # S2 должно быть непустым, минимальный вариант - тот же символ
    
    base = 31
    mod = 10**9 + 7
    
    # Прямой хэш
    h = [0] * (n + 1)
    for i in range(n):
        h[i + 1] = (h[i] * base + ord(s[i])) % mod
    
    # Хэш перевёрнутой строки
    rev_s = s[::-1]
    rh = [0] * (n + 1)
    for i in range(n):
        rh[i + 1] = (rh[i] * base + ord(rev_s[i])) % mod
    
    # Степени основания
    p = [1] * (n + 1)
    for i in range(1, n + 1):
        p[i] = (p[i - 1] * base) % mod
    
    def get_hash(l, r):
        return (h[r] - h[l] * p[r - l]) % mod
    
    def get_rev_hash(l, r):
        rev_l = n - r
        rev_r = n - l
        return (rh[rev_r] - rh[rev_l] * p[rev_r - rev_l]) % mod
    
    # Ищем максимальный палиндромный суффикс
    # Начинаем с i=1, так как S2 должно быть непустым (i=0 дало бы S2 = "")
    for i in range(1, n):
        if get_hash(i, n) == get_rev_hash(i, n):
            # Нашли палиндромный суффикс, начинающийся с позиции i
            prefix_to_add = s[:i][::-1]
            return s + prefix_to_add
    
    # Если не нашли подходящий суффикс или строка уже палиндром
    # Добавляем всю строку кроме последнего символа
    return s + s[:-1][::-1]

def main():
    s = sys.stdin.readline().strip()
    print(minimal_palindrome_extension(s))

if __name__ == "__main__":
    main()
