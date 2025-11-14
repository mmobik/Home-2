from Algorithms_and_structures import HashTable

class ExternalHashTable:
    def __init__(self, filename="database.bin"):
        self.filename = filename
        self.index = HashTable()
        
    def add(self, key, value):
        if self.index.get(key) is not None:
            return "ERROR"
        
        with open(self.filename, "ab") as f:
            position = f.tell()
            record = f"{len(key)}|{key}|{value}\n"
            f.write(record.encode())
            
        self.index.put(key, (position, len(value)))
        return None
    
    def get(self, key):
        index_data = self.index.get(key)
        if index_data is None:
            return "ERROR"
        
        position, value_len = index_data
        with open(self.filename, "rb") as f:
            f.seek(position)
            record = f.readline().decode().strip()
            parts = record.split('|', 2)
            return f"{key} {parts[2]}"
    
    def update(self, key, value):
        if self.index.get(key) is None:
            return "ERROR"
        
        self.delete(key)
        self.add(key, value)
        return None
    
    def delete(self, key):
        if self.index.get(key) is None:
            return "ERROR"
        self.index.delete(key)
        return None

def main():
    import sys
    
    n = int(sys.stdin.readline().strip())
    db = ExternalHashTable()
    
    for i in range(n):
        line = sys.stdin.readline().strip()
        if not line:
            continue
            
        parts = line.split()
        command = parts[0]
        
        if command == "ADD":
            key, value = parts[1], parts[2]
            result = db.add(key, value)
            if result:
                print(result)
                
        elif command == "DELETE":
            key = parts[1]
            result = db.delete(key)
            if result:
                print(result)
                
        elif command == "UPDATE":
            key, value = parts[1], parts[2]
            result = db.update(key, value)
            if result:
                print(result)
                
        elif command == "PRINT":
            key = parts[1]
            result = db.get(key)
            print(result)

if __name__ == "__main__":
    main()