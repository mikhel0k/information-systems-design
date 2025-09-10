from BaseProduct import BaseProduct
from dataclasses import dataclass
from datetime import datetime


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
