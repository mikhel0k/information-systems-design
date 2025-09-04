import unittest
from datetime import datetime
from unittest.mock import mock_open, patch
from io import StringIO
from typing import List
from dataclasses import dataclass

# Import the classes and functions to test
from work_file import BaseProduct, Product, Delivery, Food, Drink, Parser, read_file_lines, process_file_with_parser


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse_product(self):
        input_str = '"Apple" 1.99 "Fresh Farms"'
        product = self.parser.parse_product(input_str)

        self.assertEqual(product.name, "Apple")
        self.assertEqual(product.price, 1.99)
        self.assertEqual(product.provider, "Fresh Farms")
        self.assertEqual(str(product), "Apple ($1.99), поставщик: Fresh Farms")
        self.assertIn(product, self.parser.products)

    def test_parse_delivery(self):
        input_str = '2023.12.25 "Milk" 3'
        delivery = self.parser.parse_delivery(input_str)

        self.assertEqual(delivery.date, "2023.12.25")
        self.assertEqual(delivery.name, "Milk")
        self.assertEqual(delivery.count, 3)
        self.assertEqual(str(delivery), "Доставка: Milk x3 на 2023.12.25")
        self.assertIn(delivery, self.parser.deliveries)

    def test_parse_food(self):
        input_str = '"Cheese" 2023.01.01 2023.12.31 5.99'
        food = self.parser.parse_food(input_str)

        self.assertEqual(food.name, "Cheese")
        self.assertEqual(food.price, 5.99)
        self.assertEqual(food.start_date, datetime(2023, 1, 1))
        self.assertEqual(food.end_date, datetime(2023, 12, 31))
        self.assertEqual(str(food), "Cheese ($5.99), срок годности: 2023.01.01-2023.12.31")
        self.assertIn(food, self.parser.foods)

    def test_parse_drinks(self):
        input_str = '"Cola" 2023.01.01 2023.12.31 2.49 1.5'
        drink = self.parser.parse_drinks(input_str)

        self.assertEqual(drink.name, "Cola")
        self.assertEqual(drink.price, 2.49)
        self.assertEqual(drink.start_date, datetime(2023, 1, 1))
        self.assertEqual(drink.end_date, datetime(2023, 12, 31))
        self.assertEqual(drink.volume, 1.5)
        self.assertEqual(str(drink), "Cola ($2.49), срок годности: 2023.01.01-2023.12.31, объем: 1.5л")
        self.assertIn(drink, self.parser.drinks)

    def test_get_all_products(self):
        self.parser.parse_product('"Apple" 1.99 "Fresh Farms"')
        self.parser.parse_food('"Cheese" 2023.01.01 2023.12.31 5.99')
        self.parser.parse_drinks('"Cola" 2023.01.01 2023.12.31 2.49 1.5')

        all_products = self.parser.get_all_products()
        self.assertEqual(len(all_products), 3)
        self.assertTrue(any(isinstance(p, Product) for p in all_products))
        self.assertTrue(any(isinstance(p, Food) for p in all_products))
        self.assertTrue(any(isinstance(p, Drink) for p in all_products))

    def test_clear_data(self):
        self.parser.parse_product('"Apple" 1.99 "Fresh Farms"')
        self.parser.parse_delivery('2023.12.25 "Milk" 3')
        self.parser.parse_food('"Cheese" 2023.01.01 2023.12.31 5.99')
        self.parser.parse_drinks('"Cola" 2023.01.01 2023.12.31 2.49 1.5')

        self.parser.clear_data()

        self.assertEqual(len(self.parser.products), 0)
        self.assertEqual(len(self.parser.deliveries), 0)
        self.assertEqual(len(self.parser.foods), 0)
        self.assertEqual(len(self.parser.drinks), 0)

    @patch('builtins.open', new_callable=mock_open, read_data='2023.12.25 "Milk" 3')
    def test_read_file_lines(self, mock_file):
        lines = read_file_lines('dummy.txt')
        self.assertEqual(lines, ['2023.12.25 "Milk" 3'])

    @patch('builtins.open', new_callable=mock_open, read_data='2023.12.25 "Milk" 3')
    def test_process_file_with_parser(self, mock_file):
        with patch('sys.stdout', new=StringIO()) as mocked_output:
            process_file_with_parser('deliveries.txt', self.parser.parse_delivery, "Доставки")
            output = mocked_output.getvalue()
            print(f"Actual output: {repr(output)}")
            self.assertTrue("Доставка: Milk x3 на 2023.12.25\n" in output)

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_process_file_not_found(self, mock_file):
        with patch('sys.stdout', new=StringIO()) as mocked_output:
            process_file_with_parser('nonexistent.txt', self.parser.parse_delivery, "Доставки")
            output = mocked_output.getvalue()
            print(f"Actual output: {repr(output)}")
            self.assertTrue("Ошибка: Файл nonexistent.txt не найден\n" in output)


if __name__ == '__main__':
    unittest.main()