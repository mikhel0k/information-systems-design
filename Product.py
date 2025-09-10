from BaseProduct import BaseProduct
from dataclasses import dataclass
from datetime import datetime


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