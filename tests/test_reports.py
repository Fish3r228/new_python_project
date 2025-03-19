import json
import logging
from datetime import datetime

import pandas as pd
import pytest

from src.reports import spending_by_weekday  # Замените на имя вашего модуля

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Фикстура для тестовых данных
@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "Дата": ["2023-10-01", "2023-10-02", "2023-10-03", "2023-10-04", "2023-10-05"],
            "Сумма": [1000, 500, 1500, 2000, 3000],
        }
    )


# Тест 1: Корректный расчет трат по дням недели
def test_spending_by_weekday_success(sample_data):
    # Вызов функции
    result = spending_by_weekday(sample_data, "2023-10-01")

    # Ожидаемый результат (дни недели на английском)
    expected_result = {
        "reference_date": "2023-10-01",
        "spending_by_weekday": [
            {"День недели": "Sunday", "Сумма": 1000},
            {"День недели": "Monday", "Сумма": 500},
            {"День недели": "Tuesday", "Сумма": 1500},
            {"День недели": "Wednesday", "Сумма": 2000},
            {"День недели": "Thursday", "Сумма": 3000},
        ],
    }

    # Преобразуем результат в словарь
    result_dict = json.loads(result)

    # Сортируем списки в обоих словарях по ключу "День недели"
    result_dict["spending_by_weekday"].sort(key=lambda x: x["День недели"])
    expected_result["spending_by_weekday"].sort(key=lambda x: x["День недели"])

    # Проверка результата
    assert result_dict == expected_result


# Тест 2: Расчет без указания даты (используется текущая дата)
def test_spending_by_weekday_default_date(sample_data):
    # Вызов функции без указания даты
    result = spending_by_weekday(sample_data)

    # Получаем текущую дату
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Проверяем, что дата в ответе соответствует текущей дате
    response = json.loads(result)
    assert response["reference_date"] == current_date


# Тест 3: Пустые данные
def test_spending_by_weekday_empty_data():
    empty_data = pd.DataFrame(columns=["Дата", "Сумма"])

    # Вызов функции
    result = spending_by_weekday(empty_data, "2023-10-01")

    # Ожидаемый результат
    expected_result = {"reference_date": "2023-10-01", "spending_by_weekday": []}

    # Проверка результата
    assert json.loads(result) == expected_result


# Тест 4: Некорректный формат даты
def test_spending_by_weekday_invalid_date_format(sample_data):
    # Некорректный формат даты
    invalid_date = "2023/10/01"

    # Проверка, что функция выбрасывает исключение
    with pytest.raises(Exception):
        spending_by_weekday(sample_data, invalid_date)


# Тест 5: Некорректные данные (отсутствие столбца 'Дата')
def test_spending_by_weekday_missing_date_column():
    invalid_data = pd.DataFrame({"Сумма": [1000, 500, 1500]})

    # Проверка, что функция выбрасывает исключение
    with pytest.raises(Exception):
        spending_by_weekday(invalid_data, "2023-10-01")


# Тест 6: Некорректные данные (отсутствие столбца 'Сумма')
def test_spending_by_weekday_missing_amount_column():
    invalid_data = pd.DataFrame({"Дата": ["2023-10-01", "2023-10-02", "2023-10-03"]})

    # Проверка, что функция выбрасывает исключение
    with pytest.raises(Exception):
        spending_by_weekday(invalid_data, "2023-10-01")
