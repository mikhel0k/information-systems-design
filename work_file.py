from datetime import datetime
from typing import Dict, Any, Callable, List, Optional
from dataclasses import dataclass


@dataclass
class BaseProduct:
    """Базовый класс для всех продуктов"""
    name: str
    price: float

    def __str__(self) -> str:
        return f"{self.name} (${self.price})"


@dataclass
class Product(BaseProduct):
    """Класс для обычных продуктов"""
    provider: str

    def __str__(self) -> str:
        return f"{super().__str__()}, поставщик: {self.provider}"


@dataclass
class Delivery:
    """Класс для информации о доставке"""
    date: str
    name: str
    count: int

    def __str__(self) -> str:
        return f"Доставка: {self.name} x{self.count} на {self.date}"


@dataclass
class Food(BaseProduct):
    """Класс для пищевых продуктов с сроком годности"""
    start_date: datetime
    end_date: datetime

    def __str__(self) -> str:
        return (f"{super().__str__()}, срок годности: "
                f"{self.start_date.strftime('%Y.%m.%d')}-{self.end_date.strftime('%Y.%m.%d')}")


@dataclass
class Drink(Food):
    """Класс для напитков (наследуется от Food)"""
    volume: float

    def __str__(self) -> str:
        return f"{super().__str__()}, объем: {self.volume}л"


class Parser:
    def __init__(self):
        self.products: List[Product] = []
        self.deliveries: List[Delivery] = []
        self.foods: List[Food] = []
        self.drinks: List[Drink] = []

    def parse_product(self, input_str: str) -> Product:
        """Парсит строку с информацией о продукте.

            Args:
                input_str: Строка для парсинга в формате "name" price "provider"

            Returns:
                Объект Product с полями: name, price, provider
        """
        parts = input_str.split('"')[1:]
        name = parts[0].replace('"', '')
        price = float(parts[1])
        provider = parts[2].replace('"', '')

        product = Product(name=name, price=price, provider=provider)
        self.products.append(product)
        return product

    def parse_delivery(self, input_str: str) -> Delivery:
        """Парсит строку с информацией о доставке.

            Args:
                input_str: Строка для парсинга в формате "YYYY.MM.DD "name" quantity"

            Returns:
                Объект Delivery с полями: date, name, count
        """
        parts = input_str.split('"')
        date_str = parts[0].strip().split()[0]
        product_name = parts[1]
        quantity = int(parts[2])

        delivery = Delivery(date=date_str, name=product_name, count=quantity)
        self.deliveries.append(delivery)
        return delivery

    def parse_food(self, input_str: str) -> Food:
        """Парсит строку с информацией о еде.

        Args:
            input_str: Строка для парсинга в формате "name" start_date end_date price

        Returns:
            Объект Food с полями: name, start_date, end_date, price
        """
        parts = input_str.split('"')[1:]
        name = parts[0].replace('"', '')
        parts = parts[1].split(' ')
        start_date = datetime.strptime(parts[1], "%Y.%m.%d")
        end_date = datetime.strptime(parts[2], "%Y.%m.%d")
        price = float(parts[3])

        food = Food(name=name, price=price, start_date=start_date, end_date=end_date)
        self.foods.append(food)
        return food

    def parse_drinks(self, input_str: str) -> Drink:
        """Парсит строку с информацией о напитках.

        Args:
            input_str: Строка для парсинга в формате "name" start_date end_date price volume

        Returns:
            Объект Drink с полями: name, start_date, end_date, price, volume
        """
        parts = input_str.split('"')[1:]
        name = parts[0].replace('"', '')
        parts = parts[1].split(' ')
        start_date = datetime.strptime(parts[1], "%Y.%m.%d")
        end_date = datetime.strptime(parts[2], "%Y.%m.%d")
        price = float(parts[3])
        volume = float(parts[4])

        drink = Drink(name=name, price=price, start_date=start_date,
                      end_date=end_date, volume=volume)
        self.drinks.append(drink)
        return drink

    def get_all_products(self) -> List[BaseProduct]:
        """Возвращает все продукты (включая еду и напитки)"""
        return self.products + self.foods + self.drinks

    def clear_data(self) -> None:
        """Очищает все данные"""
        self.products.clear()
        self.deliveries.clear()
        self.foods.clear()
        self.drinks.clear()


def read_file_lines(file_path: str) -> List[str]:
    """Читает все строки из файла.

    Args:
        file_path: Путь к файлу

    Returns:
        Список строк файла
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]


def process_file_with_parser(
        file_path: str,
        parser_func: Callable[[str], Any],
        data_name: str
) -> None:
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
            parsed_obj = parser_func(line)
            print(parsed_obj)

        print()

    except FileNotFoundError:
        print(f"Ошибка: Файл {file_path} не найден")
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")


def main() -> None:
    parser = Parser()
    file_parsers = [
        ('1.txt', parser.parse_delivery, "Доставки"),
        ('2.txt', parser.parse_product, "Продукты"),
        ('3.txt', parser.parse_food, "Еда"),
        ('4.txt', parser.parse_drinks, "Напитки")
    ]

    # Обработка всех файлов
    for file_path, parser_func, data_name in file_parsers:
        process_file_with_parser(file_path, parser_func, data_name)

    # Демонстрация доступа к данным
    print("=== Сводная информация ===")
    print(f"Всего продуктов: {len(parser.products)}")
    print(f"Всего доставок: {len(parser.deliveries)}")
    print(f"Всего видов еды: {len(parser.foods)}")
    print(f"Всего напитков: {len(parser.drinks)}")
    print(f"Всего товаров: {len(parser.get_all_products())}")


if __name__ == '__main__':
    main()