from dataclasses import dataclass
from decimal import Decimal


@dataclass
class DishDTO:

    dish_id: int
    title: str
    price: Decimal
    quantity: int | None = None
