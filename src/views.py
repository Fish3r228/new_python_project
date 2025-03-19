import json
import logging
from datetime import datetime

import pandas as pd


def home_page(date_time: str) -> str:
    """
    Функция для страницы «Главная».
    """
    try:
        # Преобразуем строку в объект datetime
        dt = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        logging.info(f"Запрошена главная страница для даты: {dt}")

        # Чтение данных
        data = pd.read_excel("data/operations.xlsx")  # Переменная создана и используется

        # Фильтрация данных по дате
        filtered_data = data[data["Дата"] == dt.strftime("%Y-%m-%d")]

        # Преобразуем int64 в int
        total_spent = int(filtered_data["Сумма"].sum())

        # Формирование JSON-ответа
        response = {
            "date": dt.strftime("%Y-%m-%d"),
            "total_spent": total_spent,
            "operations": filtered_data.to_dict(orient="records"),
        }

        return json.dumps(response, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Ошибка на главной странице: {e}")
        raise


def events_page(data: pd.DataFrame) -> str:
    """
    Функция для страницы «События».
    """
    try:
        logging.info("Запрошена страница событий")

        # Проверка на пустые данные
        if data.empty:
            raise ValueError("Данные отсутствуют")

        # Проверка на наличие необходимых столбцов
        if "Категория" not in data.columns or "Сумма" not in data.columns:
            raise ValueError("Данные не содержат необходимых столбцов")

        # Группировка данных по категориям
        grouped_data = data.groupby("Категория")["Сумма"].sum().reset_index()

        # Преобразуем int64 в int
        grouped_data["Сумма"] = grouped_data["Сумма"].astype(int)

        # Формирование JSON-ответа
        response = {"total_events": len(data), "events_by_category": grouped_data.to_dict(orient="records")}

        return json.dumps(response, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Ошибка на странице событий: {e}")
        raise
