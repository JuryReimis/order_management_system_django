from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class OrderItemsDTO:
    r"""Data transfer object для передачи списка id блюд в заказе
    last_update должно быть присвоено значение последнего изменения списка блюд в заказе"""

    order_id: int | None
    items_quantity_dict: Dict[int, int]
    last_update: datetime | None
    table_number: int | None = None
