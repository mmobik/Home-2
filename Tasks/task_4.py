from Algorithms_and_structures import HashTable

def get_anagram_key(word):
    """Создает ключ анаграммы через подсчет букв за O(L) вместо O(L log L)"""
    # Создаем массив счетчиков для 26 букв A-Z
    count = [0] * 26
    
    # Подсчитываем частоты букв
    for char in word:
        count[ord(char) - ord('A')] += 1
    
    # Создаем ключ в формате "A5B3C1..." чтобы избежать коллизий
    key_parts = []
    for i in range(26):
        if count[i] > 0:
            key_parts.append(chr(ord('A') + i))
            key_parts.append(str(count[i]))
    
    return ''.join(key_parts)

def main():
    n = int(input().strip())
    
    anagram_groups = HashTable()
    
    for _ in range(n):
        word = input().strip()
        key = get_anagram_key(word)
        
        current_count = anagram_groups.get(key)
        if current_count is None:
            anagram_groups.put(key, 1)
        else:
            anagram_groups.put(key, current_count + 1)
    
    result = len(anagram_groups)
    return result

if __name__ == "__main__":
    print(main())
