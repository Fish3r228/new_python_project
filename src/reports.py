import json
import logging
from datetime import datetime

import pandas as pd


def spending_by_weekday(data: pd.DataFrame, reference_date: str = None) -> str:
    """
    Функция отчета «Траты по дням недели».
    """
    try:
        logging.info("Расчет трат по дням недели")

        # Преобразуем дату в формат datetime
        if reference_date:
            reference_date = datetime.strptime(reference_date, "%Y-%m-%d")
        else:
            reference_date = datetime.now()

        # Добавляем столбец с днем недели
        data["Дата"] = pd.to_datetime(data["Дата"])
        data["День недели"] = data["Дата"].dt.day_name()

        # Группировка по дням недели
        spending_by_day = data.groupby("День недели")["Сумма"].sum().reset_index()

        # Формирование JSON-ответа
        response = {
            "reference_date": reference_date.strftime("%Y-%m-%d"),
            "spending_by_weekday": spending_by_day.to_dict(orient="records"),
        }

        return json.dumps(response, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Ошибка в отчете 'Траты по дням недели': {e}")
        raise
