import json
import logging
from datetime import datetime


def profitable_cashback_categories(year: int, month: int, transactions: list) -> str:
    """
    Функция сервиса «Выгодные категории повышенного кешбэка».
    """
    try:
        logging.info(f"Расчет выгодных категорий для {year}-{month}")

        # Фильтрация транзакций по году и месяцу
        filtered_transactions = [
            t
            for t in transactions
            if datetime.strptime(t["Дата"], "%Y-%m-%d").year == year
            and datetime.strptime(t["Дата"], "%Y-%m-%d").month == month
        ]

        # Группировка по категориям
        categories = {}
        for t in filtered_transactions:
            category = t["Категория"]
            if category not in categories:
                categories[category] = 0
            categories[category] += t["Сумма"]

        # Формирование JSON-ответа
        response = {
            "year": year,
            "month": month,
            "profitable_categories": [{"category": k, "total_spent": v} for k, v in categories.items()],
        }

        return json.dumps(response, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Ошибка в сервисе 'Выгодные категории': {e}")
        raise
