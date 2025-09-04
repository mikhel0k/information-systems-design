from argparse import ArgumentParser
from datetime import datetime
from typing import Dict, Any, Callable


class Parser:
    def parse_product(self, input_str: str) -> Dict[str, Any]:
        """Парсит строку с информацией о продукте.

            Args:
                input_str: Строка для парсинга в формате "name" price "provider"

            Returns:
                Словарь с ключами: name, price, provider
        """
        parts = input_str.split('"')[1:]
        name = parts[0].replace('"', '')
        price = float(parts[1])
        provider = parts[2].replace('"', '')

        return {'name': name, 'price': price, 'provider': provider}


    def parse_delivery(self, input_str: str) -> Dict[str, Any]:
        """Парсит строку с информацией о доставке.

            Args:
                input_str: Строка для парсинга в формате "YYYY.MM.DD "name" quantity"

            Returns:
                Словарь с ключами: date, name, count
        """
        parts = input_str.split('"')
        date_str = parts[0].strip().split()
        date_str = str(date_str[0])
        product_name = parts[1]
        quantity = int(parts[2])
        date = datetime.strptime(date_str, "%Y.%m.%d")

        return {"date": date.strftime('%Y.%m.%d'), "name": product_name, "count": quantity}


    def parse_food(self, input_str: str) -> Dict[str, Any]:
        """Парсит строку с информацией о еде.

        Args:
            input_str: Строка для парсинга в формате "name" start_date end_date price

        Returns:
            Словарь с ключами: name, start_date, end_date, price
        """
        parts = input_str.split('"')[1:]
        name = parts[0].replace('"', '')
        parts = parts[1].split(' ')
        start_date = datetime.strptime(parts[1], "%Y.%m.%d")
        end_date = datetime.strptime(parts[2], "%Y.%m.%d")
        price = float(parts[3])

        return {"name": name, "start_date": start_date, "end_date": end_date, "price": price}


    def parse_drinks(self, input_str: str) -> Dict[str, Any]:
        """Парсит строку с информацией о напитках.

        Args:
            input_str: Строка для парсинга в формате "name" start_date end_date price volume

        Returns:
            Словарь с ключами: name, start_date, end_date, price, volume
        """
        parts = input_str.split('"')[1:]
        name = parts[0].replace('"', '')
        parts = parts[1].split(' ')
        start_date = datetime.strptime(parts[1], "%Y.%m.%d")
        end_date = datetime.strptime(parts[2], "%Y.%m.%d")
        price = float(parts[3])
        volume = float(parts[4])

        return {"name": name, "start_date": start_date, "end_date": end_date, "price": price, "volume": volume}


def read_file_lines(file_path: str) -> list:
    """Читает все строки из файла.

    Args:
        file_path: Путь к файлу

    Returns:
        Список строк файла
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()


def process_file_with_parser(
        file_path: str,
        parser_func: Callable[[str], Dict[str, Any]]
) -> None:
    """Обрабатывает файл с использованием указанной функции-парсера.

    Args:
        file_path: Путь к файлу для обработки
        parser_func: Функция для парсинга строк
    """
    try:
        lines = read_file_lines(file_path)
        print(f"Данные из {file_path}:")

        for line in lines:
            parsed_data = parser_func(line.strip())
            print(parsed_data)

        print()

    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")

def main() -> None:
    parser = Parser()
    file_parsers = [
        ('1.txt', parser.parse_delivery),
        ('2.txt', parser.parse_product),
        ('3.txt', parser.parse_food),
        ('4.txt', parser.parse_drinks)
    ]

    for file_path, parser_func in file_parsers:
        process_file_with_parser(file_path, parser_func)


if __name__ == '__main__':
    main()
