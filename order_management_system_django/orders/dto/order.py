from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List



@dataclass
class OrderDTO:

    order_id: int
    table_number: int | None
    items: List[int] | None
    updated: datetime | None
    status: int | None
    status_display: str | None
    total_price: Decimal | None
