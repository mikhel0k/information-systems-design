from datetime import datetime
from typing import List, Any, Callable
from dataclasses import dataclass
import re


class ParsingError(Exception):
    """Пользовательское исключение для ошибок парсинга"""
    pass


@dataclass
class BaseProduct:
    """Базовый класс для всех продуктов"""
    name: str
    price: float

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Название продукта не может быть пустым")
        if self.price < 0:
            raise ValueError("Цена не может быть отрицательной")

    def __str__(self) -> str:
        return f"{self.name} ({self.price:.2f}Р)"


@dataclass
class Product(BaseProduct):
    """Класс для обычных продуктов"""
    provider: str

    def __post_init__(self):
        super().__post_init__()
        if not self.provider.strip():
            raise ValueError("Поставщик не может быть пустым")

    def __str__(self) -> str:
        return f"{super().__str__()}, поставщик: {self.provider}"


@dataclass
class Delivery:
    """Класс для информации о доставке"""
    date: str
    name: str
    count: int

    def __post_init__(self):
        if not re.match(r"^\d{4}\.\d{2}\.\d{2}$", self.date):
            raise ValueError("Неверный формат даты, ожидается YYYY.MM.DD")
        if not self.name.strip():
            raise ValueError("Название доставки не может быть пустым")
        if self.count <= 0:
            raise ValueError("Количество должно быть положительным")

    def __str__(self) -> str:
        return f"Доставка: {self.name} x{self.count} на {self.date}"


@dataclass
class Food(BaseProduct):
    """Класс для пищевых продуктов с сроком годности"""
    start_date: datetime
    end_date: datetime

    def __post_init__(self):
        super().__post_init__()
        if self.end_date <= self.start_date:
            raise ValueError("Дата окончания срока годности должна быть позже начальной")

    def __str__(self) -> str:
        return (f"{super().__str__()}, срок годности: "
                f"{self.start_date.strftime('%Y.%m.%d')}-{self.end_date.strftime('%Y.%m.%d')}")


@dataclass
class Drink(Food):
    """Класс для напитков (наследуется от Food)"""
    volume: float

    def __post_init__(self):
        super().__post_init__()
        if self.volume <= 0:
            raise ValueError("Объем должен быть положительным")

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
        try:
            parts = input_str.split('"')
            if len(parts) < 5:
                raise ParsingError("Неверный формат строки продукта, ожидается: \"name\" price \"provider\"")
            name = parts[1].strip()
            price = float(parts[2].strip())
            provider = parts[3].strip()
            product = Product(name=name, price=price, provider=provider)
            self.products.append(product)
            return product
        except (ValueError, IndexError) as e:
            raise ParsingError(f"Ошибка парсинга продукта: {e}")

    def parse_delivery(self, input_str: str) -> Delivery:
        """Парсит строку с информацией о доставке.

            Args:
                input_str: Строка для парсинга в формате "YYYY.MM.DD "name" quantity"

            Returns:
                Объект Delivery с полями: date, name, count
        """
        try:
            parts = input_str.split('"')
            if len(parts) < 3:
                raise ParsingError("Неверный формат строки доставки, ожидается: YYYY.MM.DD \"name\" quantity")
            date_str = parts[0].strip()
            name = parts[1].strip()
            count = int(parts[2].strip())
            delivery = Delivery(date=date_str, name=name, count=count)
            self.deliveries.append(delivery)
            return delivery
        except (ValueError, IndexError) as e:
            raise ParsingError(f"Ошибка парсинга доставки: {e}")

    def parse_food(self, input_str: str) -> Food:
        """Парсит строку с информацией о еде.

        Args:
            input_str: Строка для парсинга в формате "name" start_date end_date price

        Returns:
            Объект Food с полями: name, start_date, end_date, price
        """
        try:
            parts = input_str.split('"')
            if len(parts) < 3:
                raise ParsingError("Неверный формат строки еды, ожидается: \"name\" start_date end_date price")
            name = parts[1].strip()
            rest = parts[2].strip().split()
            if len(rest) < 3:
                raise ParsingError("Недостаточно данных для еды")
            start_date = datetime.strptime(rest[0], "%Y.%m.%d")
            end_date = datetime.strptime(rest[1], "%Y.%m.%d")
            price = float(rest[2])
            food = Food(name=name, price=price, start_date=start_date, end_date=end_date)
            self.foods.append(food)
            return food
        except (ValueError, IndexError) as e:
            raise ParsingError(f"Ошибка парсинга еды: {e}")

    def parse_drinks(self, input_str: str) -> Drink:
        """Парсит строку с информацией о напитках.

        Args:
            input_str: Строка для парсинга в формате "name" start_date end_date price volume

        Returns:
            Объект Drink с полями: name, start_date, end_date, price, volume
        """
        try:
            parts = input_str.split('"')
            if len(parts) < 3:
                raise ParsingError("Неверный формат строки напитка, ожидается:"
                                   " \"name\" start_date end_date price volume")
            name = parts[1].strip()
            rest = parts[2].strip().split()
            if len(rest) < 4:
                raise ParsingError("Недостаточно данных для напитка")
            start_date = datetime.strptime(rest[0], "%Y.%m.%d")
            end_date = datetime.strptime(rest[1], "%Y.%m.%d")
            price = float(rest[2])
            volume = float(rest[3])
            drink = Drink(name=name, price=price, start_date=start_date, end_date=end_date, volume=volume)
            self.drinks.append(drink)
            return drink
        except (ValueError, IndexError) as e:
            raise ParsingError(f"Ошибка парсинга напитка: {e}")

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
