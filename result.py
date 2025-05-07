import csv
from collections import Counter
import statistics
from datetime import datetime

def analyze_csv(filename, filter_column=None, filter_value=None, sort_column=None, date_column=None):
    """
    Считывает CSV-файл, вычисляет и печатает базовую статистику для числовых столбцов,
    фильтрует и сортирует данные при необходимости, обрабатывает ошибки и работает с датами.
    """
    try:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            data = list(reader)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return

    # Фильтрация данных
    if filter_column and filter_value:
        try:
            filter_index = header.index(filter_column)
            data = [row for row in data if row[filter_index] == filter_value]
        except ValueError:
            print(f"Ошибка: Столбец '{filter_column}' не найден.")
            return

    # Сортировка данных
    if sort_column:
        try:
            sort_index = header.index(sort_column)
            data.sort(key=lambda row: row[sort_index])
        except ValueError:
            print(f"Ошибка: Столбец '{sort_column}' не найден.")
            return

    # Определяем числовые столбцы
    numerical_columns = []
    for i in range(len(header)):
        try:
            # Проверяем, является ли столбец числовым, пробуя преобразовать каждое значение
            float(data[0][i])
            numerical_columns.append(i)
        except ValueError:
            pass

    if not numerical_columns:
        print("В файле нет числовых столбцов для анализа.")
        return

    # Вычисляем статистику для числовых столбцов
    for i in numerical_columns:
        column_data = []
        for row in data:
            try:
                value = float(row[i])
                column_data.append(value)
            except ValueError:
                print(f"Предупреждение: Нечисловое значение '{row[i]}' в столбце '{header[i]}', строка пропущена.")
                continue  # Пропускаем нечисловое значение

        if not column_data:
            print(f"Предупреждение: Столбец '{header[i]}' не содержит числовых данных после обработки ошибок.")
            continue

        average = sum(column_data) / len(column_data)
        minimum = min(column_data)
        maximum = max(column_data)
        median = statistics.median(column_data)
        try:
            mode = statistics.mode(column_data)
        except statistics.StatisticsError:
            mode = "Нет моды"
        std_dev = statistics.stdev(column_data)

        print(f"Столбец '{header[i]}': Среднее = {average}, Минимум = {minimum}, Максимум = {maximum}, Медиана = {median}, Мода = {mode}, Стандартное отклонение = {std_dev}")

    # Работа с датами (если указан столбец с датами)
    if date_column:
        try:
            date_index = header.index(date_column)
            date_list = []
            for row in data:
                date_str = row[date_index]
                if date_str:  # Проверяем, что значение даты не пустое
                    try:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                        date_list.append(date_obj)
                    except ValueError:
                        print(f"Предупреждение: Неправильный формат даты '{date_str}' в строке, строка пропущена.")
                        continue
                else:
                    print(f"Предупреждение: Пропущена дата в строке, строка пропущена.")
                    continue

            if date_list:
                oldest_date = min(date_list)
                newest_date = max(date_list)
                print(f"Столбец '{date_column}': Самая старая дата = {oldest_date}, Самая новая дата = {newest_date}")
            else:
                print(f"Предупреждение: Нет корректных дат для анализа в столбце '{date_column}'.")

        except ValueError:
            print(f"Ошибка: Неправильный формат даты в столбце '{date_column}'. Ожидается формат 'YYYY-MM-DD'.")
        except KeyError:
            print(f"Ошибка: Столбец '{date_column}' не найден.")

# Пример использования
analyze_csv('data.csv', filter_column='City', filter_value='New York', sort_column='Age', date_column='Date')