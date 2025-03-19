import logging

import pandas as pd


def read_data_from_excel(file_path: str) -> pd.DataFrame:
    """
    Чтение данных из Excel-файла.
    """
    try:
        data = pd.read_excel(file_path)
        logging.info("Данные успешно загружены из файла: %s", file_path)
        return data
    except Exception as e:
        logging.error("Ошибка при чтении файла: %s", e)
        raise
