def can_split(chapters, k, max_pages):
    """Проверяет, можно ли разбить главы на k томов с максимальной толщиной max_pages"""
    volumes = 1
    current_pages = 0
    
    for pages in chapters:
        if current_pages + pages <= max_pages:
            current_pages += pages
        else:
            volumes += 1
            current_pages = pages
            if volumes > k:
                return False
    return True

def main():
    # Чтение входных данных
    n = int(input().strip())
    chapters = list(map(int, input().split()))
    k = int(input().strip())
    
    # Границы бинарного поиска
    left = max(chapters)  # том не может быть меньше самой большой главы
    right = sum(chapters) # максимально возможный том
    
    # Бинарный поиск минимальной максимальной толщины
    while left < right:
        mid = (left + right) // 2
        if can_split(chapters, k, mid):
            right = mid
        else:
            left = mid + 1
    
    return left

if __name__ == "__main__":
    print(main())
