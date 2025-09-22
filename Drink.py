from Food import Food
from dataclasses import dataclass


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
