import json
import logging

import pytest

from src.services import profitable_cashback_categories

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Фикстура для тестовых данных
@pytest.fixture
def sample_transactions():
    return [
        {"Дата": "2023-10-01", "Категория": "Супермаркеты", "Сумма": 1000},
        {"Дата": "2023-10-02", "Категория": "Рестораны", "Сумма": 500},
        {"Дата": "2023-10-03", "Категория": "Супермаркеты", "Сумма": 1500},
        {"Дата": "2023-09-30", "Категория": "Транспорт", "Сумма": 300},  # Транзакция за предыдущий месяц
        {"Дата": "2023-10-04", "Категория": "Рестораны", "Сумма": 700},
    ]


# Тест 1: Корректный расчет выгодных категорий
def test_profitable_cashback_categories_success(sample_transactions):
    year = 2023
    month = 10

    # Ожидаемый результат
    expected_result = {
        "year": year,
        "month": month,
        "profitable_categories": [
            {"category": "Супермаркеты", "total_spent": 2500},
            {"category": "Рестораны", "total_spent": 1200},
        ],
    }

    # Вызов функции
    result = profitable_cashback_categories(year, month, sample_transactions)

    # Проверка результата
    assert json.loads(result) == expected_result


# Тест 2: Нет транзакций за указанный месяц
def test_profitable_cashback_categories_no_transactions(sample_transactions):
    year = 2023
    month = 11  # Нет транзакций за этот месяц

    # Ожидаемый результат
    expected_result = {
        "year": year,
        "month": month,
        "profitable_categories": [],
    }

    # Вызов функции
    result = profitable_cashback_categories(year, month, sample_transactions)

    # Проверка результата
    assert json.loads(result) == expected_result


# Тест 3: Некорректный формат транзакций
def test_profitable_cashback_categories_invalid_transactions():
    year = 2023
    month = 10
    invalid_transactions = [
        {"Дата": "2023-10-01", "Категория": "Супермаркеты"},  # Нет поля "Сумма"
    ]

    # Проверка, что функция выбрасывает исключение
    with pytest.raises(Exception):
        profitable_cashback_categories(year, month, invalid_transactions)


# Тест 4: Некорректный формат даты
def test_profitable_cashback_categories_invalid_date_format():
    year = 2023
    month = 10
    invalid_transactions = [
        {"Дата": "2023/10/01", "Категория": "Супермаркеты", "Сумма": 1000},  # Неправильный формат даты
    ]

    # Проверка, что функция выбрасывает исключение
    with pytest.raises(Exception):
        profitable_cashback_categories(year, month, invalid_transactions)


# Тест 5: Пустой список транзакций
def test_profitable_cashback_categories_empty_transactions():
    year = 2023
    month = 10
    empty_transactions = []

    # Ожидаемый результат
    expected_result = {
        "year": year,
        "month": month,
        "profitable_categories": [],
    }

    # Вызов функции
    result = profitable_cashback_categories(year, month, empty_transactions)

    # Проверка результата
    assert json.loads(result) == expected_result
