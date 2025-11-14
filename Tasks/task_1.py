from Algorithms_and_structures import parser_numbers

def binary_search(arr, k):
    """Функция бинарного поиска для делителя."""    
    right = max(arr)
    left = 1
    while left <= right:
        mid = (left + right) // 2
        count = 0
        for el in arr:
            count += el // mid
        if count >= k:
            left = mid + 1
        else:
            right = mid - 1
    return right

def main():
    """Основаня функция программы."""
    n = parser_numbers(input())
    num_of_wires = n[0]
    k = n[1]

    arr = []
    for _ in range(num_of_wires):
        arr.append(int(input()))

    result = binary_search(arr, k)
    return result

if __name__ == "__main__":
    print(main())
