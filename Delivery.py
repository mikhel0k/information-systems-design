from dataclasses import dataclass
import re


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
