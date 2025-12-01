import sys

def minimal_palindrome_extension(s):
    n = len(s)
    if n == 0:
        return ""
    
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
    for i in range(n):
        if get_hash(i, n) == get_rev_hash(i, n):
            prefix_to_add = s[:i][::-1]
            return s + prefix_to_add
    
    return s + s[:-1][::-1]

def main():
    s = sys.stdin.readline().strip()
    print(minimal_palindrome_extension(s))

if __name__ == "__main__":
    main()
