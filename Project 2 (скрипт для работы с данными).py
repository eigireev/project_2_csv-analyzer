import csv  # Импортируем модуль csv для работы с CSV-файлами

def analyze_csv(filename, filter_column='City', filter_value='NewYork', sort_column='Age'):
    """
    Считывает CSV-файл, вычисляет и печатает базовую статистику для числовых столбцов,
    фильтрует и сортирует данные при необходимости.
    """
    try:  # Пытаемся открыть и прочитать файл
        with open(filename, 'r') as file:  # Открываем файл для чтения
            reader = csv.reader(file)  # Создаем объект reader для чтения CSV-файла
            header = next(reader)  # Считываем первую строку файла, которая является заголовком
            data = list(reader)  # Считываем все остальные строки файла в список
    except FileNotFoundError:  # Если файл не найден
        print(f"Ошибка: Файл '{filename}' не найден.")  # Выводим сообщение об ошибке
        return  # Завершаем выполнение функции

    # Фильтрация данных
    if filter_column and filter_value:  # Если указаны столбец и значение для фильтрации
        try:  # Пытаемся отфильтровать данные
            filter_index = header.index(filter_column)  # Получаем индекс столбца для фильтрации
            data = [row for row in data if row[filter_index] == filter_value]  # Фильтруем строки, оставляем только те, у которых значение в указанном столбце соответствует заданному значению
        except ValueError:  # Если столбец для фильтрации не найден
            print(f"Ошибка: Столбец '{filter_column}' не найден.")  # Выводим сообщение об ошибке
            return  # Завершаем выполнение функции

    # Сортировка данных
    if sort_column:  # Если указан столбец для сортировки
        try:  # Пытаемся отсортировать данные
            sort_index = header.index(sort_column)  # Получаем индекс столбца для сортировки
            data.sort(key=lambda row: row[sort_index])  # Сортируем строки по значению в указанном столбце
        except ValueError:  # Если столбец для сортировки не найден
            print(f"Ошибка: Столбец '{sort_column}' не найден.")  # Выводим сообщение об ошибке
            return  # Завершаем выполнение функции

    # Определяем числовые столбцы
    numerical_columns = []  # Создаем пустой список для хранения индексов числовых столбцов
    for i in range(len(header)):  # Перебираем все столбцы
        try:  # Пытаемся преобразовать первый элемент столбца в число
            float(data[0][i])  # Пытаемся преобразовать значение в число
            numerical_columns.append(i)  # Если преобразование удалось, добавляем индекс столбца в список числовых столбцов
        except ValueError:  # Если преобразование не удалось
            pass  # Пропускаем столбец

    if not numerical_columns:  # Если нет числовых столбцов
        print("В файле нет числовых столбцов для анализа.")  # Выводим сообщение об отсутствии числовых столбцов
        return  # Завершаем выполнение функции

    # Вычисляем статистику для числовых столбцов
    for i in numerical_columns:  # Перебираем все числовые столбцы
        column_data = [float(row[i]) for row in data]  # Получаем данные из столбца и преобразуем их в числа
        average = sum(column_data) / len(column_data)  # Вычисляем среднее значение
        minimum = min(column_data)  # Вычисляем минимальное значение
        maximum = max(column_data)  # Вычисляем максимальное значение
        print(f"Столбец '{header[i]}': Среднее = {average}, Минимум = {minimum}, Максимум = {maximum}")  # Выводим статистику для столбца

# Пример использования
# analyze_csv('data.csv', filter_column='City', filter_value='New York', sort_column='Age')
analyze_csv('data/data.csv', filter_column='City', filter_value='New York', sort_column='Age')