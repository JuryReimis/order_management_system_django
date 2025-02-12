from dataclasses import dataclass
from decimal import Decimal
from typing import List, Dict

from carte.dto.dish import DishDTO


@dataclass
class OrderContextDTO:
    r"""Data Transfer Object для передачи контекста, который будет использоваться в шаблоне
    Передает:
        items: List[DishDTO] - список объектов, сформированных по данным модели Dish
        item_price_dict: Dict[int: Decimal] - Словарь. По ключу pk доступны цены для каждого item
        item_quantity_dict: Dict[int, int] - Словарь. По ключу pk доступно количество item в заказе
        order_id: int - id заказа
        order_table: int - Номер стола
        order_total_price: Decimal - Суммарная стоимость заказа
        order_status: int - Статус заказа в цифровом выражении
        order_status_display: str - Статус заказа в дисплейном виде
    """

    items: List[DishDTO]
    item_price_dict: Dict[int, Decimal]
    item_quantity_dict: Dict[int, int]
    order_id: int
    order_table: int
    order_total_price: Decimal
    order_status: int
    order_status_display: str
