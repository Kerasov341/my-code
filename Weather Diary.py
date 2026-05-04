import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

# Функция для сохранения данных в файл JSON
def save_to_file(data):
    with open("weather_diary.json", "w") as file:
        json.dump(data, file, indent=4)

# Функция для загрузки данных из файла JSON
def load_from_file():
    try:
        with open("weather_diary.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Функция добавления записи
def add_record():
    date = entry_date.get()
    temperature = entry_temperature.get()
    description = entry_description.get()
    precipitation = var_precipitation.get()

    # Проверка корректности ввода
    try:
        datetime.strptime(date, "%Y-%m-%d")  # Проверка формата даты
        temperature = float(temperature)       # Проверка температуры
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Некорректный ввод данных.")
        return

    if not description:
        messagebox.showerror("Ошибка ввода", "Описание не должно быть пустым.")
        return

    # Создание записи о погоде
    record = {
        "date": date,
        "temperature": temperature,
        "description": description,
        "precipitation": precipitation
    }

    # Добавление записи в список и сохранение
    records.append(record)
    save_to_file(records)
    update_records_view()
    clear_inputs()

# Функция обновления отображения записей
def update_records_view(filtered_records=None):
    # Очищаем таблицу перед обновлением
    for row in tree.get_children():
        tree.delete(row)

    records_to_display = filtered_records if filtered_records else records
    for record in records_to_display:
        tree.insert("", "end", values=(record["date"], record["temperature"], record["description"], record["precipitation"]))

# Функция фильтрации по дате
def filter_by_date():
    date = entry_filter_date.get()
    if not date:
        update_records_view()
        return
    filtered_records = [record for record in records if record["date"] == date]
    update_records_view(filtered_records)

# Функция фильтрации по температуре
def filter_by_temperature():
    try:
        temp_threshold = float(entry_filter_temperature.get())
        filtered_records = [record for record in records if record["temperature"] > temp_threshold]
        update_records_view(filtered_records)
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Температура должна быть числом.")
        return

# Функция очистки полей ввода
def clear_inputs():
    entry_date.delete(0, tk.END)
    entry_temperature.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    var_precipitation.set(False)

# Загрузка записей из файла при запуске приложения
records = load_from_file()

# Создаем основное окно
window = tk.Tk()
window.title("Weather Diary")
window.geometry("400x400")

# Поля ввода
tk.Label(window, text="Дата (YYYY-MM-DD):").pack(pady=5)
entry_date = tk.Entry(window)
entry_date.pack(pady=5)

tk.Label(window, text="Температура:").pack(pady=5)
entry_temperature = tk.Entry(window)
entry_temperature.pack(pady=5)

tk.Label(window, text="Описание погоды:").pack(pady=5)
entry_description = tk.Entry(window, width=40)
entry_description.pack(pady=5)

var_precipitation = tk.BooleanVar()
tk.Checkbutton(window, text="Осадки", variable=var_precipitation).pack(pady=5)

# Кнопка добавления записи
button_add = tk.Button(window, text="Добавить запись", command=add_record)
button_add.pack(pady=10)

# Поля фильтрации
tk.Label(window, text="Фильтр по дате (YYYY-MM-DD):").pack(pady=5)
entry_filter_date = tk.Entry(window)
entry_filter_date.pack(pady=5)

tk.Button(window, text="Фильтровать по дате", command=filter_by_date).pack(pady=5)

tk.Label(window, text="Фильтр по температуре (> X°C):").pack(pady=5)
entry_filter_temperature = tk.Entry(window)
entry_filter_temperature.pack(pady=5)

tk.Button(window, text="Фильтровать по температуре", command=filter_by_temperature).pack(pady=5)

# Таблица для отображения записей
tree = ttk.Treeview(window, columns=("date", "temperature", "description", "precipitation"), show="headings")
tree.heading("date", text="Дата")
tree.heading("temperature", text="Температура")
tree.heading("description", text="Описание")
tree.heading("precipitation", text="Осадки")
tree.pack(pady=10)

# Обновляем отображение на старте
update_records_view()

# Запускаем основной цикл приложения
window.mainloop()