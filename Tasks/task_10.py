import sys

def z_function(s):
    """Вычисляет Z-функцию строки s.
    z[i] = длина наибольшего общего префикса строки s и её суффикса s[i:]"""
    n = len(s)
    z = [0] * n
    l = r = 0  # [l, r] - самый правый отрезок совпадения
    
    for i in range(1, n):
        if i <= r:
            # Используем ранее вычисленные значения
            z[i] = min(r - i + 1, z[i - l])
        # Расширяем вручную
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        # Обновляем самый правый отрезок
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z

def solve():
    s1 = sys.stdin.readline().strip()  # слово с забора
    s2 = sys.stdin.readline().strip()  # последнее слово
    n1, n2 = len(s1), len(s2)
    
    # Z-функция от s1#s2 покажет, какие префиксы s1 совпадают
    # с началами суффиксов s2
    concat = s1 + '#' + s2
    z = z_function(concat)
    
    # Динамика: dp[i] = можно ли разбить s2[0:i]
    dp = [False] * (n2 + 1)
    prev_len = [0] * (n2 + 1)  # для восстановления ответа
    dp[0] = True
    
    # Оптимизация: храним границу, до которой мы уже обновили dp
    max_reached = 0
    
    for i in range(n2):
        if not dp[i]:
            continue
        
        # Позиция начала s2[i:] в конкатенации
        pos = n1 + 1 + i
        max_len = z[pos]  # сколько символов можно взять как префикс s1
        
        if max_len == 0:
            continue

        # Нам нужно обновить dp[i+1 ... i+max_len]
        # Но обновляем только те, что еще не были обновлены (начиная с max_reached + 1)
        # Это гарантирует, что каждая ячейка dp обновляется только 1 раз -> O(N)
        start_update = max(i + 1, max_reached + 1)
        end_update = min(i + max_len, n2)
        
        for j in range(start_update, end_update + 1):
            dp[j] = True
            prev_len[j] = j - i
        
        max_reached = max(max_reached, end_update)
        
        # Если уже достигли конца, можно досрочно прервать (опционально, но полезно)
        if max_reached == n2:
            break
    
    if dp[n2]:
        # Восстанавливаем разбиение
        parts = []
        pos = n2
        while pos > 0:
            L = prev_len[pos]
            parts.append(s2[pos - L:pos])
            pos -= L
        parts.reverse()
        print("No")
        print(" ".join(parts))
    else:
        print("Yes")

if __name__ == "__main__":
    solve()
