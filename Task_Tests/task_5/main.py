import time
from test_runner import run_tests_simple

if __name__ == "__main__":
    start = time.time()
    passed, total = run_tests_simple()
    end = time.time()
    
    print(f"\nОбщее время выполнения: {end - start:.2f} сек")
    print(f"Результат: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 Все тесты пройдены успешно!")
    else:
        print("❌ Некоторые тесты не пройдены.")
        print("Проверьте файлы в папке tests/")