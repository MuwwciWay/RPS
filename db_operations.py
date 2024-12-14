import sqlite3
import ast  # Для безопасного преобразования строки обратно в список

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
def save_array_to_db(original_arrays, sorted_arrays):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.executemany('''
            INSERT INTO arrays (original_array, sorted_array)
            VALUES (?, ?)
        ''', [(str(o), str(s)) for o, s in zip(original_arrays, sorted_arrays)])
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error during database insert: {e}")
    finally:
        conn.close()



# Функция для получения всех массивов из базы данных
def get_all_arrays():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM arrays')
    rows = cursor.fetchall()
    conn.close()
    
    # Преобразуем строки обратно в массивы
    arrays = []
    for row in rows:
        original_array = ast.literal_eval(row['original_array'])  # Преобразование строки в список
        sorted_array = ast.literal_eval(row['sorted_array'])      # Преобразование строки в список
        arrays.append({
            "id": row['id'],
            "original_array": original_array,
            "sorted_array": sorted_array
        })
    return arrays

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
