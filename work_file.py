from ParsingError import ParsingError
from typing import List, Any, Callable
from Parser import Parser


def read_file_lines(file_path: str) -> List[str]:
    """Читает все строки из файла.

    Args:
        file_path: Путь к файлу

    Returns:
        Список строк файла
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        raise ParsingError(f"Файл {file_path} не найден")


def process_file_with_parser(file_path: str, parser_func: Callable[[str], Any], data_name: str) -> None:
    """Обрабатывает файл с использованием указанной функции-парсера.

    Args:
        file_path: Путь к файлу для обработки
        parser_func: Функция для парсинга строк
        data_name: Название типа данных для вывода
    """
    try:
        lines = read_file_lines(file_path)
        print(f"=== {data_name} из {file_path} ===")
        for line in lines:
            try:
                parsed_obj = parser_func(line)
                print(parsed_obj)
            except ParsingError as e:
                print(f"Ошибка обработки строки в файле {file_path}: {e}")
        print()
    except ParsingError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка при обработке файла {file_path}: {e}")


def main() -> None:
    parser = Parser()
    file_parsers = [
        ('1.txt', parser.parse_delivery, "Доставки"),
        ('2.txt', parser.parse_product, "Продукты"),
        ('3.txt', parser.parse_food, "Еда"),
        ('4.txt', parser.parse_drinks, "Напитки")
    ]

    for file_path, parser_func, data_name in file_parsers:
        process_file_with_parser(file_path, parser_func, data_name)

    print("=== Сводная информация ===")
    print(f"Всего продуктов: {len(parser.products)}")
    print(f"Всего доставок: {len(parser.deliveries)}")
    print(f"Всего видов еды: {len(parser.foods)}")
    print(f"Всего напитков: {len(parser.drinks)}")
    print(f"Всего товаров: {len(parser.get_all_products())}")


if __name__ == '__main__':
    main()
