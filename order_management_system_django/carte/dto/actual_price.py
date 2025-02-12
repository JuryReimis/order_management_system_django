from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ActualPriceDTO:
    dish_id: int
    actual_price: Decimal
