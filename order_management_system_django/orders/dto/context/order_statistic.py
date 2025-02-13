from dataclasses import dataclass
from decimal import Decimal


@dataclass
class OrderStatisticDTO:
    r"""DTO для передачи статистических данных по выборке заказов"""

    orders_amount: int
    sum_total_price: Decimal
    avg_total_price: Decimal
