import sys

class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, index, delta):
        """Обновление элемента за O(log n)"""
        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i
    
    def query(self, index):
        """Запрос префиксной суммы [0..index] за O(log n)"""
        res = 0
        i = index + 1
        while i > 0:
            res += self.tree[i]
            i -= i & -i
        return res
    
    def range_sum(self, l, r):
        """Запрос суммы на отрезке [l, r] за O(log n)"""
        if l == 0:
            return self.query(r)
        return self.query(r) - self.query(l - 1)

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    m = int(data[1])
    
    # Чтение исходного массива
    arr = []
    idx = 2
    for i in range(n):
        arr.append(int(data[idx]))
        idx += 1
    
    # Инициализация дерева Фенвика
    fenw = FenwickTree(n)
    for i in range(n):
        fenw.update(i, arr[i])
    
    results = []
    
    # Обработка запросов
    for _ in range(m):
        code = int(data[idx]); idx += 1
        if code == 1:
            l = int(data[idx]); idx += 1
            r = int(data[idx]); idx += 1
            # Запрос суммы на отрезке [l, r]
            results.append(str(fenw.range_sum(l, r)))
        else:  # code == 2
            i = int(data[idx]); idx += 1
            new_val = int(data[idx]); idx += 1
            # Обновление элемента
            old_val = arr[i]
            delta = new_val - old_val
            fenw.update(i, delta)
            arr[i] = new_val
    
    # Возврат результатов запросов типа 1
    return "\n".join(results)

if __name__ == "__main__":
    print(main())
