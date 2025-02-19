import decimal
from decimal import Decimal
from typing import List

from carte.dto.dish_price import DishPriceDTO
from carte.repositories.dish_price_repository import DishPriceRepository
from orders.dto.order_items import OrderItemsDTO


class CalculateTotalPriceService:
    r"""Сервис для подсчета общей цены заказа"""

    def _get_price_list(self, dto, repository) -> List[DishPriceDTO]:
        return repository.get_prices(dto)

    def _get_sum(self, dish_list: List[DishPriceDTO]):
        total = 0
        for dish in dish_list:
            total += dish.price * dish.quantity
        return Decimal(total).quantize(Decimal('0.00'), rounding=decimal.ROUND_HALF_UP)

    def execute(self, order_items_dto: OrderItemsDTO, repository: DishPriceRepository) -> Decimal | None:
        if order_items_dto.items_quantity_dict:
            price_list = self._get_price_list(order_items_dto, repository)
            return self._get_sum(price_list)
        else:
            return None
