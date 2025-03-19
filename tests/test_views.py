import json
import logging
from unittest.mock import patch

import pandas as pd
import pytest

from src.views import events_page, home_page  # Замените на имя вашего модуля

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Тесты для home_page
def test_home_page_success():
    date_time = "2023-10-01 12:00:00"

    # Фиктивные данные
    mock_data = pd.DataFrame(
        {
            "Дата": ["2023-10-01", "2023-10-02", "2023-10-01"],
            "Сумма": [1000, 500, 1500],
            "Категория": ["Супермаркеты", "Рестораны", "Супермаркеты"],
        }
    )

    # Ожидаемый результат
    expected_result = {
        "date": "2023-10-01",
        "total_spent": 2500,  # 1000 + 1500
        "operations": [
            {"Дата": "2023-10-01", "Сумма": 1000, "Категория": "Супермаркеты"},
            {"Дата": "2023-10-01", "Сумма": 1500, "Категория": "Супермаркеты"},
        ],
    }

    # Мокаем pd.read_excel
    with patch("pandas.read_excel", return_value=mock_data):
        result = home_page(date_time)

        # Проверка результата
        assert json.loads(result) == expected_result


def test_home_page_read_error():
    date_time = "2023-10-01 12:00:00"

    # Мокаем pd.read_excel, чтобы он выбрасывал исключение
    with patch("pandas.read_excel", side_effect=Exception("Ошибка чтения данных")):
        with pytest.raises(Exception):
            home_page(date_time)


# Тесты для events_page
def test_events_page_success():
    # Фиктивные данные
    mock_data = pd.DataFrame({"Категория": ["Супермаркеты", "Рестораны", "Супермаркеты"], "Сумма": [1000, 500, 1500]})

    # Ожидаемый результат
    expected_result = {
        "total_events": 3,
        "events_by_category": [
            {"Категория": "Рестораны", "Сумма": 500},
            {"Категория": "Супермаркеты", "Сумма": 2500},  # 1000 + 1500
        ],
    }

    # Вызов функции
    result = events_page(mock_data)

    # Проверка результата
    assert json.loads(result) == expected_result


def test_events_page_empty_data():
    # Пустые данные
    mock_data = pd.DataFrame(columns=["Категория", "Сумма"])

    # Проверка, что функция выбрасывает исключение
    with pytest.raises(ValueError):
        events_page(mock_data)


def test_events_page_missing_columns():
    # Данные без столбца 'Сумма'
    mock_data = pd.DataFrame({"Категория": ["Супермаркеты", "Рестораны"]})

    # Проверка, что функция выбрасывает исключение
    with pytest.raises(ValueError):
        events_page(mock_data)
