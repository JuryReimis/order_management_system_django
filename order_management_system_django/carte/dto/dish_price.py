from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime


@dataclass
class DishPriceDTO:
    dish_id: int
    price: Decimal
    changed: datetime
