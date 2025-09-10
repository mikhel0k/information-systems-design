from Drink import Drink
from Food import Food
from Delivery import Delivery
from Product import Product
from typing import List
from BaseProduct import BaseProduct
from ParsingError import ParsingError
from datetime import datetime


class Parser:
    def __init__(self):
        self.products: List[Product] = []
        self.deliveries: List[Delivery] = []
        self.foods: List[Food] = []
        self.drinks: List[Drink] = []

    def parse_product(self, input_str: str) -> Product:
        """Парсит строку с информацией о продукте."""
        try:
            parts = input_str.split('"')
            if len(parts) < 5:
                raise ParsingError(
                    "Неверный формат строки продукта, ожидается: \"name\" price \"provider\"",
                    input_str
                )
            name = parts[1].strip()
            price = float(parts[2].strip())
            provider = parts[3].strip()
            product = Product(name=name, price=price, provider=provider)
            self.products.append(product)
            return product
        except (ValueError, IndexError) as e:
            raise ParsingError(f"Ошибка парсинга продукта: {e}", input_str) from e

    def parse_delivery(self, input_str: str) -> Delivery:
        """Парсит строку с информацией о доставке."""
        try:
            parts = input_str.split('"')
            if len(parts) < 3:
                raise ParsingError(
                    "Неверный формат строки доставки, ожидается: YYYY.MM.DD \"name\" quantity",
                    input_str
                )
            date_str = parts[0].strip()
            name = parts[1].strip()
            count = int(parts[2].strip())
            delivery = Delivery(date=date_str, name=name, count=count)
            self.deliveries.append(delivery)
            return delivery
        except (ValueError, IndexError) as e:
            raise ParsingError(f"Ошибка парсинга доставки: {e}", input_str) from e

    def parse_food(self, input_str: str) -> Food:
        """Парсит строку с информацией о еде."""
        try:
            parts = input_str.split('"')
            if len(parts) < 3:
                raise ParsingError(
                    "Неверный формат строки еды, ожидается: \"name\" start_date end_date price",
                    input_str
                )
            name = parts[1].strip()
            rest = parts[2].strip().split()
            if len(rest) < 3:
                raise ParsingError("Недостаточно данных для еды", input_str)

            start_date = datetime.strptime(rest[0], "%Y.%m.%d")
            end_date = datetime.strptime(rest[1], "%Y.%m.%d")
            price = float(rest[2])

            food = Food(name=name, price=price, start_date=start_date, end_date=end_date)
            self.foods.append(food)
            return food
        except (ValueError, IndexError) as e:
            raise ParsingError(f"Ошибка парсинга еды: {e}", input_str) from e

    def parse_drinks(self, input_str: str) -> Drink:
        """Парсит строку с информацией о напитках."""
        try:
            parts = input_str.split('"')
            if len(parts) < 3:
                raise ParsingError(
                    "Неверный формат строки напитка, ожидается: \"name\" start_date end_date price volume",
                    input_str
                )
            name = parts[1].strip()
            rest = parts[2].strip().split()
            if len(rest) < 4:
                raise ParsingError("Недостаточно данных для напитка", input_str)

            start_date = datetime.strptime(rest[0], "%Y.%m.%d")
            end_date = datetime.strptime(rest[1], "%Y.%m.%d")
            price = float(rest[2])
            volume = float(rest[3])

            drink = Drink(name=name, price=price, start_date=start_date, end_date=end_date, volume=volume)
            self.drinks.append(drink)
            return drink
        except (ValueError, IndexError) as e:
            raise ParsingError(f"Ошибка парсинга напитка: {e}", input_str) from e

    def get_all_products(self) -> List[BaseProduct]:
        """Возвращает все продукты (включая еду и напитки)"""
        return self.products + self.foods + self.drinks

    def clear_data(self) -> None:
        """Очищает все данные"""
        self.products.clear()
        self.deliveries.clear()
        self.foods.clear()
        self.drinks.clear()