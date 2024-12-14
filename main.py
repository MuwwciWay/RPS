from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
from tree_sort import generate_numbers, tree_sort, save_array  # Импортируем функции из файла tree_sort
from db_operations import create_table, save_array_to_db, get_all_arrays, clear_database  # Импортируем функции для работы с БД
import os
import sqlite3


app = FastAPI()



@app.delete("/clear_database")
def clear_database():
    try:
        print("Attempting to delete database file...")
        if os.path.exists("arrays.db"):
            os.remove("arrays.db")
            print("Database file deleted successfully.")
            return {"message": "Database cleared successfully"}
        else:
            print("Database file does not exist.")
            raise HTTPException(status_code=404, detail="Database file does not exist")
    except Exception as e:
        print(f"Error deleting the database: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting the database: {str(e)}")


# Инициализация базы данных и создание таблицы, если она еще не существует
create_table()

# Модель для ввода массива
class ArrayRequest(BaseModel):
    arr: list[int]

# Эндпоинт для создания случайного массива
@app.get("/generate_random_array")
def generate_random_array():
    arr = generate_numbers()
    return {"original_array": arr}

# Эндпоинт для сортировки массива
@app.post("/sort_array")
def sort_array(array_request: ArrayRequest):
    arr = array_request.arr
    sorted_arr = tree_sort(arr)
    # Сохранение массивов в базу данных
    save_array_to_db(arr, sorted_arr)
    return {"original_array": arr, "sorted_array": sorted_arr}

# Эндпоинт для получения всех сохраненных массивов
@app.get("/get_all_arrays")
def get_arrays():
    stored_arrays = get_all_arrays()
    result = []
    for row in stored_arrays:
        result.append({
            "id": row["id"],
            "original_array": row["original_array"],
            "sorted_array": row["sorted_array"]
        })
    return {"arrays": result}


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


@app.delete("/delete_array/{array_id}")
def delete_array(array_id: int):
    try:
        conn = sqlite3.connect("arrays.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM arrays WHERE id = ?", (array_id,))
        conn.commit()
        conn.close()
        return {"message": "Array deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting array: {e}")

