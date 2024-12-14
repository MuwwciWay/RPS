import random
import time
import aiohttp
import asyncio
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "http://localhost:8000"

def generate_random_array():
    """Генерация случайного массива."""
    array = [random.randint(1, 100) for _ in range(random.randint(5, 15))]
    return array

async def async_add_and_sort_array(session, arr):
    """Отправка массива, сортировка и удаление асинхронно."""
    try:
        # Сортировка массива
        start_time = time.time()
        sorted_array = sorted(arr)
        sorting_time = time.time() - start_time
        
        # Отправка отсортированного массива в базу данных
        start_time = time.time()
        async with session.post(f"{BASE_URL}/sort_array", json={"arr": sorted_array}) as response:
            response.raise_for_status()  # Это выбросит исключение при ошибке статуса
        db_post_time = time.time() - start_time

        # Удаление массива после его добавления
        start_time = time.time()
        async with session.delete(f"{BASE_URL}/delete_array/{sorted_array}") as response:
            response.raise_for_status()  # Это выбросит исключение при ошибке статуса
        db_delete_time = time.time() - start_time
        
        # Общая затраченное время
        total_time = sorting_time + db_post_time + db_delete_time
        return total_time
        
    except aiohttp.ClientResponseError as e:
        logging.error(f"Failed to process array {arr}. Status code: {e.status}, message: {e.message}")
    except Exception as e:
        logging.error(f"Error occurred while processing array {arr}: {e}")

async def test_add_and_process_arrays_async(num_arrays):
    """Тест для добавления и обработки массивов в базе данных (асинхронно)."""
    async with aiohttp.ClientSession() as session:
        times = []
        tasks = [async_add_and_sort_array(session, generate_random_array()) for _ in range(num_arrays)]
        results = await asyncio.gather(*tasks)
        
        # Собираем время для каждого массива
        times = [result for result in results if result is not None]
        
        # Среднее время
        average_time = sum(times) / len(times) if times else 0
        return average_time

async def test_clear_database_async():
    """Тест для очистки базы данных (асинхронно)."""
    async with aiohttp.ClientSession() as session:
        await async_clear_database(session)

async def async_clear_database(session):
    """Очистка базы данных асинхронно."""
    try:
        logging.debug("Sending request to clear the database.")
        async with session.delete(f"{BASE_URL}/clear_database") as response:
            response.raise_for_status()  # Это выбросит исключение при ошибке статуса
            logging.info("Database cleared successfully.")
    except aiohttp.ClientResponseError as e:
        logging.error(f"Failed to clear database. Status code: {e.status}, message: {e.message}")
    except Exception as e:
        logging.error(f"Error occurred while clearing database: {e}")

async def run_tests_async():
    """Запуск всех тестов (асинхронно)."""
    
    # Добавляем и обрабатываем 100 массивов
    logging.info("\nRunning async test: Add and process 100 arrays...")
    avg_time_100 = await test_add_and_process_arrays_async(100)
    logging.info(f"Average time for 100 arrays: {avg_time_100:.5f} seconds")

    # Очистка базы данных
    logging.info("\nClearing database after 100 arrays...")
    await test_clear_database_async()

    # Добавляем и обрабатываем 1000 массивов
    logging.info("\nRunning async test: Add and process 1000 arrays...")
    avg_time_1000 = await test_add_and_process_arrays_async(1000)
    logging.info(f"Average time for 1000 arrays: {avg_time_1000:.5f} seconds")

    # Очистка базы данных
    logging.info("\nClearing database after 1000 arrays...")
    await test_clear_database_async()

    # Добавляем и обрабатываем 10000 массивов
    logging.info("\nRunning async test: Add and process 10000 arrays...")
    avg_time_10000 = await test_add_and_process_arrays_async(10000)
    logging.info(f"Average time for 10000 arrays: {avg_time_10000:.5f} seconds")

    # Очистка базы данных
    logging.info("\nClearing database after 10000 arrays...")
    await test_clear_database_async()

if __name__ == "__main__":
    asyncio.run(run_tests_async())
