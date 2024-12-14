import tkinter as tk
from tkinter import ttk, messagebox
import requests
import random

# URL FastAPI-сервера
BASE_URL = "http://127.0.0.1:8000"

# Функция генерации случайного массива
def generate_random_array():
    return [random.randint(1, 100) for _ in range(random.randint(5, 15))]

# Создание основного окна
root = tk.Tk()
root.title("Array Sorting Application")
root.geometry("800x600")
root.configure(bg="#f9f9f9")

# Основной фрейм
main_frame = tk.Frame(root, bg="#f9f9f9")
main_frame.pack(fill=tk.BOTH, expand=True)

# Левое меню
menu_frame = tk.Frame(main_frame, bg="#f2f2f2", width=200)
menu_frame.pack(side=tk.LEFT, fill=tk.Y)

# Контент-фрейм (будет обновляться при каждом переходе)
content_frame = tk.Frame(main_frame, bg="#ffffff")
content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Заголовок
title_label = tk.Label(content_frame, text="Array Sorting Tool", bg="#ffffff", fg="#333333", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# Функция для вывода инструкций
def show_instructions():
    instructions = (
        "Инструкция:\n"
        "1. Нажмите 'Ввести массив', чтобы ввести массив вручную.\n"
        "2. Нажмите 'Сгенерировать массив', чтобы получить случайный массив.\n"
        "3. Нажмите 'Загрузить массив из БД', чтобы выбрать массив из базы данных.\n"
        "4. После ввода массива или генерации, вы можете сортировать его и сохранить в базу данных."
    )
    for widget in content_frame.winfo_children():
        widget.destroy()  # Удаляем все старые виджеты
    instructions_label = tk.Label(content_frame, text=instructions, bg="#ffffff", fg="#333333", font=("Arial", 12))
    instructions_label.pack(pady=10)

# Функции для работы с массивами

def sort_array(arr, sorted_array_var, save_buttons_frame):
    """Сортировка массива."""
    sorted_arr = sorted(arr)
    sorted_array_var.set(",".join(map(str, sorted_arr)))
    
    # Показать кнопки сохранения после сортировки
    for widget in save_buttons_frame.winfo_children():
        widget.pack_forget()  # Убираем старые кнопки

    save_unsorted_button = tk.Button(save_buttons_frame, text="Сохранить неотсортированный", bg="#ffcc99", font=("Arial", 12), command=lambda: save_unsorted_array(arr))
    save_unsorted_button.pack(side=tk.LEFT, padx=10, pady=10)

    save_sorted_button = tk.Button(save_buttons_frame, text="Сохранить отсортированный", bg="#ffcc99", font=("Arial", 12), command=lambda: save_sorted_array(arr, sorted_array_var))
    save_sorted_button.pack(side=tk.LEFT, padx=10, pady=10)

def save_unsorted_array(arr):
    """Сохранение неотсортированного массива в БД."""
    try:
        response = requests.post(f"{BASE_URL}/sort_array", json={"arr": arr})
        if response.status_code == 200:
            messagebox.showinfo("Success", "Unsorted array saved!")
        else:
            messagebox.showerror("Error", "Failed to save array!")
    except ValueError:
        messagebox.showerror("Input Error", "Invalid array input!")

def save_sorted_array(arr, sorted_array_var):
    """Сохранение отсортированного массива в БД."""
    try:
        # Извлекаем строковое представление отсортированного массива
        sorted_arr = list(map(int, sorted_array_var.get().split(",")))
        
        # Отправка на сервер
        response = requests.post(f"{BASE_URL}/sort_array", json={"arr": arr, "sorted_arr": sorted_arr})
        
        # Логирование полученного ответа
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.content}")
        
        if response.status_code == 200:
            messagebox.showinfo("Success", "Sorted array saved!")
        else:
            messagebox.showerror("Error", f"Failed to save array! Status Code: {response.status_code}")
    except ValueError as ve:
        print(f"ValueError: {ve}")
        messagebox.showerror("Input Error", "Invalid array input!")
    except Exception as e:
        print(f"Exception: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")



# Создание переменной для отсортированного массива
sorted_array_var = tk.StringVar()

# Функция генерации случайного массива и его отображение
def generate_and_display():
    """Генерация случайного массива и его отображение."""
    random_array = generate_random_array()
    for widget in content_frame.winfo_children():
        widget.destroy()  # Удаляем все старые виджеты

    # Отображение сгенерированного массива
    generated_array_label = tk.Label(content_frame, text=f"Generated Array: {random_array}", bg="#ffffff", font=("Arial", 12))
    generated_array_label.pack(pady=10)

    # Кнопки для перегенерации и сортировки
    regenerate_button = tk.Button(content_frame, text="Перегенерировать", bg="#ff9999", font=("Arial", 12), command=generate_and_display)
    regenerate_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Создание save_buttons_frame для сортировки
    save_buttons_frame = tk.Frame(content_frame, bg="#ffffff")
    save_buttons_frame.pack(pady=10, fill=tk.X)

    sort_button = tk.Button(content_frame, text="Сортировать массив", bg="#99ccff", font=("Arial", 12), command=lambda: sort_array(random_array, sorted_array_var, save_buttons_frame))
    sort_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Поле для вывода отсортированного массива с рамкой
    sorted_array_label_frame = tk.Frame(content_frame, bd=2, relief="solid", padx=10, pady=10, bg="#d4edda")
    sorted_array_label_frame.pack(pady=10, fill=tk.X)
    
    sorted_array_label = tk.Label(sorted_array_label_frame, text="Отсортированный массив:", bg="#d4edda", font=("Arial", 12, "bold"))
    sorted_array_label.pack(pady=5)

    sorted_array_label = tk.Label(sorted_array_label_frame, textvariable=sorted_array_var, bg="#d4edda", font=("Arial", 12))
    sorted_array_label.pack(pady=5)

class ArrayObject:
    def __init__(self, array_id, original_array):
        self.array_id = array_id
        self.original_array = original_array
    
    def sort_array(self):
        """Метод для сортировки массива."""
        return sorted(self.original_array)

def load_array_from_db():
    """Загрузка массива из базы данных."""
    response = requests.get(f"{BASE_URL}/get_all_arrays")
    if response.status_code == 200:
        arrays = response.json()["arrays"]
        for widget in content_frame.winfo_children():
            widget.destroy()  # Удаляем все старые виджеты
        
        if not arrays:
            messagebox.showinfo("Info", "База данных пуста.")
        else:
            # Отображение списка ID
            id_label = tk.Label(content_frame, text="Выберите ID массива:", bg="#ffffff", font=("Arial", 12))
            id_label.pack(pady=5)
            
            id_combobox = ttk.Combobox(content_frame, values=[str(arr['id']) for arr in arrays], width=50)
            id_combobox.pack(pady=5)
            
            def load_selected_array():
                array_id = id_combobox.get()
                selected_array = next((arr for arr in arrays if str(arr['id']) == array_id), None)
                if selected_array:
                    # Преобразуем массив в объект
                    array_object = ArrayObject(selected_array['id'], selected_array['original_array'])

                    # Define result_text widget for displaying the array
                    result_text = tk.Text(content_frame, height=4, width=50, wrap=tk.WORD)
                    result_text.pack(pady=10)

                    result_text.delete(1.0, tk.END)  # Clear the text area
                    result_text.insert(tk.END, f"Original Array: {array_object.original_array}\n")
                    
                    # Сортируем массив с помощью метода объекта
                    sorted_array = array_object.sort_array()
                    
                    # Добавление поля для вывода отсортированного массива
                    sorted_array_label_frame = tk.Frame(content_frame, bd=2, relief="solid", padx=10, pady=10, bg="#d4edda")
                    sorted_array_label_frame.pack(pady=10, fill=tk.X)
                    
                    sorted_array_label = tk.Label(sorted_array_label_frame, text="Отсортированный массив:", bg="#d4edda", font=("Arial", 12, "bold"))
                    sorted_array_label.pack(pady=5)
                    
                    # Отображаем отсортированный массив
                    sorted_array_label = tk.Label(sorted_array_label_frame, text=f"{sorted_array}", bg="#d4edda", font=("Arial", 12))
                    sorted_array_label.pack(pady=5)


            load_button = tk.Button(content_frame, text="Загрузить массив", bg="#99ccff", font=("Arial", 12), command=load_selected_array)
            load_button.pack(pady=10)

    else:
        messagebox.showerror("Error", "Failed to retrieve arrays!")



# Функция для отображения поля ввода массива
def show_input_array():
    """Показать форму для ввода массива вручную."""
    for widget in content_frame.winfo_children():
        widget.destroy()  # Удаляем все старые виджеты
    
    # Метка и поле ввода массива
    input_label = tk.Label(content_frame, text="Введите массив (через запятую):", bg="#ffffff", font=("Arial", 12))
    input_label.pack(pady=10)
    
    input_array_var = tk.StringVar()
    input_array_entry = tk.Entry(content_frame, textvariable=input_array_var, font=("Arial", 12))
    input_array_entry.pack(pady=5)
    
    sorted_array_var = tk.StringVar()  # Инициализация переменной для отсортированного массива
    
    save_buttons_frame = tk.Frame(content_frame, bg="#ffffff")
    save_buttons_frame.pack(pady=10, fill=tk.X)
    
    def on_sort_button_click():
        input_str = input_array_var.get().strip()
        
        # Проверка на пустой ввод или некорректные символы
        if not input_str:
            messagebox.showerror("Input Error", "Массив не может быть пустым!")
            return
        try:
            array = list(map(int, input_str.split(",")))
        except ValueError:
            messagebox.showerror("Input Error", "Массив должен содержать только числа!")
            return
        
        sort_array(array, sorted_array_var, save_buttons_frame)
    
    sort_button = tk.Button(content_frame, text="Сортировать массив", bg="#99ccff", font=("Arial", 12), command=on_sort_button_click)
    sort_button.pack(pady=10)

    # Поле для вывода отсортированного массива с рамкой
    sorted_array_label_frame = tk.Frame(content_frame, bd=2, relief="solid", padx=10, pady=10, bg="#d4edda")
    sorted_array_label_frame.pack(pady=10, fill=tk.X)
    
    sorted_array_label = tk.Label(sorted_array_label_frame, text="Отсортированный массив:", bg="#d4edda", font=("Arial", 12, "bold"))
    sorted_array_label.pack(pady=5)

    sorted_array_label = tk.Label(sorted_array_label_frame, textvariable=sorted_array_var, bg="#d4edda", font=("Arial", 12))
    sorted_array_label.pack(pady=5)


def show_all_arrays():
    """Загрузка всех массивов из базы данных и вывод их на экран."""
    try:
        response = requests.get(f"{BASE_URL}/get_all_arrays")
        if response.status_code == 200:
            arrays = response.json().get("arrays", [])
            
            # Очистить контент перед выводом новых данных
            for widget in content_frame.winfo_children():
                widget.destroy()

            if not arrays:
                messagebox.showinfo("Информация", "Нет массивов в базе данных.")
                return

            # Отображение всех массивов
            all_arrays_label = tk.Label(content_frame, text="Все массивы в базе данных:", bg="#ffffff", font=("Arial", 14, "bold"))
            all_arrays_label.pack(pady=10)

            # Отображение каждого массива
            for array in arrays:
                array_label = tk.Label(content_frame, text=f"ID: {array['id']}, Массив: {array['original_array']}", bg="#ffffff", font=("Arial", 12))
                array_label.pack(pady=5)
        else:
            messagebox.showerror("Ошибка", "Не удалось загрузить массивы.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка при загрузке данных: {str(e)}")


# Структура меню
menu_buttons = [
    ("Главная", show_instructions, "#ffe5b4"),
    ("Ввести массив", show_input_array, "#ffcc99"),
    ("Сгенерировать массив", generate_and_display, "#ffcc99"),
    ("Загрузить массив из БД", load_array_from_db, "#ffcc99"),
    ("Показать все массивы", show_all_arrays, "#ffcc99")  
]


# Кнопки меню
for text, command, color in menu_buttons:
    btn = tk.Button(menu_frame, text=text, command=command, font=("Arial", 12), fg="#333333", bg=color, activebackground="#e6e6e6", width=20, height=2)
    btn.pack(pady=10)

# Стартовое отображение инструкций
show_instructions()

root.mainloop()
