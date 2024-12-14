'''import random
import time
import aiohttp
import asyncio

BASE_URL = "http://localhost:8000"

def generate_random_array():
    """Генерация случайного массива."""
    return [random.randint(1, 100) for _ in range(random.randint(5, 15))]

async def async_add_array(session, arr):
    """Отправка массива асинхронно."""
    async with session.post(f"{BASE_URL}/sort_array", json={"arr": arr}) as response:
        assert response.status == 200, f"Failed for array {arr}"

async def test_add_arrays_async(num_arrays):
    """Тест для добавления массивов в базу данных (асинхронно)."""
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [async_add_array(session, generate_random_array()) for _ in range(num_arrays)]
        await asyncio.gather(*tasks)
    elapsed_time = time.time() - start_time
    print(f"Test completed for {num_arrays} arrays in {elapsed_time:.2f} seconds")
    return {"success": True, "elapsed_time": elapsed_time}

async def async_clear_database(session):
    """Очистка базы данных асинхронно."""
    async with session.delete(f"{BASE_URL}/clear_database") as response:
        assert response.status == 200, "Failed to clear the database."

async def test_clear_database_async():
    """Тест для очистки базы данных (асинхронно)."""
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        await async_clear_database(session)
    elapsed_time = time.time() - start_time
    print(f"Database cleared in {elapsed_time:.2f} seconds")
    return {"success": True, "elapsed_time": elapsed_time}

async def async_retrieve_arrays(session):
    """Получение массивов из базы данных асинхронно."""
    async with session.get(f"{BASE_URL}/get_all_arrays") as response:
        assert response.status == 200, "Failed to retrieve arrays from the database."
        return await response.json()

async def test_retrieve_and_sort_async(num_arrays):
    """Тест для извлечения и сортировки массива (асинхронно)."""
    async with aiohttp.ClientSession() as session:
        arrays_data = await async_retrieve_arrays(session)
        arrays = arrays_data.get("arrays", [])
        assert len(arrays) >= num_arrays, "Not enough arrays in the database."
        
        selected_arrays = random.sample(arrays, num_arrays)
        start_time = time.time()
        
        # Параллельная сортировка в памяти
        tasks = [sorted(array['original_array']) for array in selected_arrays]
        elapsed_time = time.time() - start_time
        avg_time = elapsed_time / num_arrays
        print(f"Test completed for {num_arrays} arrays with average sorting time {avg_time:.5f} seconds per array")
        return {"success": True, "elapsed_time": elapsed_time, "average_time_per_array": avg_time}

async def run_tests_async():
    """Запуск всех тестов (асинхронно)."""
    print("\nRunning async test: Add 100 arrays...")
    result = await test_add_arrays_async(100)
    print(result)

    print("\nClearing database after 100 arrays...")
    result = await test_clear_database_async()
    print(result)

    print("\nRunning async test: Add 1000 arrays...")
    result = await test_add_arrays_async(1000)
    print(result)

    print("\nClearing database after 1000 arrays...")
    result = await test_clear_database_async()
    print(result)

    print("\nRunning async test: Retrieve and sort 100 arrays...")
    result = await test_retrieve_and_sort_async(100)
    print(result)

if __name__ == "__main__":
    asyncio.run(run_tests_async())
'''