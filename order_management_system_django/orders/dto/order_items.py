from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class OrderItemsDTO:
    r"""Data transfer object для передачи списка id блюд в заказе
    last_update должно быть присвоено значение последнего изменения списка блюд в заказе"""

    order_id: int
    items_ids: List[int]
    last_update: datetime
