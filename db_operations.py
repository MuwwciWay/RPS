import sqlite3
import json  # Для преобразования списков в JSON и обратно

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('arrays.db')
    conn.row_factory = sqlite3.Row
    return conn

# Функция для создания таблицы, если она еще не существует
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS arrays (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_array TEXT NOT NULL,
            sorted_array TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Функция для сохранения массива в базу данных

def save_array_to_db(original_array, sorted_array):
    # Проверка типа данных
    if not isinstance(original_array, list):
        raise ValueError("The original_array must be a list!")
    if not isinstance(sorted_array, list):
        raise ValueError("The sorted_array must be a list!")

    conn = sqlite3.connect("arrays.db")
    cursor = conn.cursor()
    
    # Преобразуем массивы в строки JSON
    original_array_str = json.dumps(original_array)
    sorted_array_str = json.dumps(sorted_array)
    
    cursor.execute(
        "INSERT INTO arrays (original_array, sorted_array) VALUES (?, ?)",
        (original_array_str, sorted_array_str)
    )
    conn.commit()
    conn.close()



# Функция для получения всех массивов из базы данных
def get_all_arrays():
    conn = sqlite3.connect("arrays.db")
    conn.row_factory = sqlite3.Row  # Для возврата строк в виде словарей
    cursor = conn.cursor()
    cursor.execute("SELECT id, original_array, sorted_array FROM arrays")
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row["id"],
            "original_array": json.loads(row["original_array"]),  # Преобразуем обратно в массив
            "sorted_array": json.loads(row["sorted_array"])
        })
    return result


# Функция для очистки базы данных
def clear_database():
    try:
        # Соединение с базой данных
        conn = sqlite3.connect("arrays.db")
        cursor = conn.cursor()

        # Выполнение SQL-запроса для удаления всех записей из таблицы
        cursor.execute("DELETE FROM arrays")

        # Сохраняем изменения и закрываем соединение
        conn.commit()
        conn.close()

        return True
    except Exception as e:
        print(f"Error clearing database: {e}")
        return False
