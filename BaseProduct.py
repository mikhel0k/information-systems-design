from dataclasses import dataclass


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
