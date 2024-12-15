import time
import random
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def generate_random_array(size: int) -> list[int]:
    return [random.randint(0, 1000) for _ in range(size)]

# Тест добавления 100 массивов
def test_add_100_arrays():
    success_flag = True
    start_time = time.time()
    try:
        for _ in range(100):
            arr = generate_random_array(random.randint(1, 100))  # случайный размер массива
            sorted_arr = sorted(arr)
            response = client.post("/sort_array", json={"arr": arr})
            assert response.status_code == 200
    except Exception as e:
        success_flag = False
        print(f"Error during adding arrays: {e}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    return {"success": success_flag, "elapsed_time": elapsed_time}

# Тест добавления 1000 массивов
def test_add_1000_arrays():
    success_flag = True
    start_time = time.time()
    try:
        for _ in range(1000):
            arr = generate_random_array(random.randint(1, 100))  # случайный размер массива
            sorted_arr = sorted(arr)
            response = client.post("/sort_array", json={"arr": arr})
            assert response.status_code == 200
    except Exception as e:
        success_flag = False
        print(f"Error during adding arrays: {e}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    return {"success": success_flag, "elapsed_time": elapsed_time}

# Тест добавления 10000 массивов
def test_add_10000_arrays():
    success_flag = True
    start_time = time.time()
    try:
        for _ in range(10000):
            arr = generate_random_array(random.randint(1, 100))  # случайный размер массива
            sorted_arr = sorted(arr)
            response = client.post("/sort_array", json={"arr": arr})
            assert response.status_code == 200
    except Exception as e:
        success_flag = False
        print(f"Error during adding arrays: {e}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    return {"success": success_flag, "elapsed_time": elapsed_time}

# Тест выгрузки и сортировки 100 случайных массивов из базы данных
def test_sorting_100_random_arrays():
    success_flag = True
    start_time = time.time()
    try:
        response = client.get("/get_all_arrays")
        assert response.status_code == 200
        arrays = response.json()['arrays']
        random_arrays = random.sample(arrays, 100)
        for array in random_arrays:
            arr = array['original_array']
            sorted_arr = sorted(arr)
            # Пример сортировки (уже сохраненной) через API
            response = client.post("/sort_array", json={"arr": arr})
            assert response.status_code == 200
    except Exception as e:
        success_flag = False
        print(f"Error during sorting 100 arrays: {e}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    average_time_per_array = elapsed_time / 100
    return {
        "success": success_flag, 
        "elapsed_time": elapsed_time,
        "average_time_per_array": average_time_per_array
    }

# Тест очистки базы данных
def test_clear_database():
    success_flag = True
    start_time = time.time()
    try:
        response = client.delete("/clear_database")
        assert response.status_code == 200
    except Exception as e:
        success_flag = False
        print(f"Error during clearing the database: {e}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    return {"success": success_flag, "elapsed_time": elapsed_time}

# Запуск тестов для базы на 100, 1000 и 10000 записей
def run_tests():
    # Тест для 100 записей
    result_100 = test_add_100_arrays()
    print(f"Test 100 arrays: Success: {result_100['success']}, Elapsed Time: {result_100['elapsed_time']}")

    # Тест для 1000 записей
    result_1000 = test_add_1000_arrays()
    print(f"Test 1000 arrays: Success: {result_1000['success']}, Elapsed Time: {result_1000['elapsed_time']}")

    # Тест для 10000 записей
    result_10000 = test_add_10000_arrays()
    print(f"Test 10000 arrays: Success: {result_10000['success']}, Elapsed Time: {result_10000['elapsed_time']}")

    # Тест для выгрузки и сортировки 100 случайных массивов
    result_sorting_100 = test_sorting_100_random_arrays()
    print(f"Test sorting 100 random arrays: Success: {result_sorting_100['success']}, Elapsed Time: {result_sorting_100['elapsed_time']}, Average Time Per Array: {result_sorting_100['average_time_per_array']}")

    # Тест для очистки базы данных
    result_clear_db = test_clear_database()
    print(f"Test clear database: Success: {result_clear_db['success']}, Elapsed Time: {result_clear_db['elapsed_time']}")

if __name__ == "__main__":
    run_tests()
