
from typing import List

from carte.dto.dish_price import DishPriceDTO
from carte.repositories.dish_price_repository import DishPriceRepository
from orders.dto.order_items import OrderItemsDTO


class CalculateTotalPriceService:

    def _get_price_list(self, dto, repository) -> List[DishPriceDTO]:
        return repository.get_prices(dto)

    def _get_sum(self, price_list: List[DishPriceDTO]):
        total = 0
        for dish_price in price_list:
            total += dish_price.price
        return total

    def execute(self, order_items: OrderItemsDTO, repository: DishPriceRepository):
        price_list = self._get_price_list(order_items, repository)
        return self._get_sum(price_list)
