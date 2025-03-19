import logging
from unittest.mock import patch

import pandas as pd
import pytest

from src.utils import read_data_from_excel  # Замените на имя вашего модуля

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Фикстура для тестовых данных
@pytest.fixture
def sample_excel_file(tmp_path):
    """
    Создает временный Excel-файл с тестовыми данными.
    """
    data = pd.DataFrame(
        {"Дата": ["2023-10-01", "2023-10-02"], "Сумма": [1000, 500], "Категория": ["Супермаркеты", "Рестораны"]}
    )
    file_path = tmp_path / "test_data.xlsx"
    data.to_excel(file_path, index=False)
    return file_path


# Тест 1: Успешное чтение данных из Excel-файла
def test_read_data_from_excel_success(sample_excel_file):
    # Преобразуем Path в строку
    file_path = str(sample_excel_file)

    # Вызов функции
    result = read_data_from_excel(file_path)

    # Ожидаемый результат
    expected_data = pd.DataFrame(
        {"Дата": ["2023-10-01", "2023-10-02"], "Сумма": [1000, 500], "Категория": ["Супермаркеты", "Рестораны"]}
    )

    # Проверка результата
    pd.testing.assert_frame_equal(result, expected_data)


# Тест 2: Файл не существует
def test_read_data_from_excel_file_not_found():
    non_existent_file = "non_existent_file.xlsx"

    # Проверка, что функция выбрасывает исключение
    with pytest.raises(Exception):
        read_data_from_excel(non_existent_file)


# Тест 3: Некорректный формат файла
def test_read_data_from_excel_invalid_file_format(tmp_path):
    # Создаем файл с некорректным форматом (не Excel)
    invalid_file = tmp_path / "invalid_file.txt"
    with open(invalid_file, "w") as f:
        f.write("Это не Excel-файл")

    # Преобразуем Path в строку
    invalid_file = str(invalid_file)

    # Проверка, что функция выбрасывает исключение
    with pytest.raises(Exception):
        read_data_from_excel(invalid_file)


# Тест 4: Пустой файл
def test_read_data_from_excel_empty_file(tmp_path):
    # Создаем пустой Excel-файл
    empty_file = tmp_path / "empty_file.xlsx"
    pd.DataFrame().to_excel(empty_file, index=False)

    # Преобразуем Path в строку
    empty_file = str(empty_file)

    # Проверка, что функция возвращает пустой DataFrame
    result = read_data_from_excel(empty_file)
    assert result.empty


# Тест 5: Ошибка при чтении файла (мок)
def test_read_data_from_excel_read_error():
    file_path = "test_file.xlsx"

    # Мокаем pd.read_excel, чтобы он выбрасывал исключение
    with patch("pandas.read_excel", side_effect=Exception("Ошибка чтения файла")):
        with pytest.raises(Exception):
            read_data_from_excel(file_path)
