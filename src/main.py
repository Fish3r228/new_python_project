import logging

from src.reports import spending_by_weekday
from src.utils import read_data_from_excel

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    try:
        # Чтение данных
        data = read_data_from_excel("data/operations.xlsx")

        # Анализ трат по дням недели
        report = spending_by_weekday(data)

        # Вывод отчета
        logging.info("Отчет о тратах по дням недели:\n%s", report)
    except Exception as e:
        logging.error("Ошибка в основном потоке выполнения: %s", e)


if __name__ == "__main__":
    main()
