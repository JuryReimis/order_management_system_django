from django.db import transaction

from carte.repositories.dish_price_repository import DishPriceRepository
from orders.dto.order_items import OrderItemsDTO
from orders.repositories.update_order_items import UpdateOrderItemsRepository
from orders.services.calculate_total_price import CalculateTotalPriceService


class UpdateOrderService:

    def __init__(self, order_items_dto: OrderItemsDTO):
        self._order_items_dto = order_items_dto

    def execute(self):
        """Обновляет элементы заказа и пересчитывает общую стоимость."""

        with transaction.atomic():
            repository = UpdateOrderItemsRepository(self._order_items_dto)
            repository.update_items()

            price_repository = DishPriceRepository()
            total_price = CalculateTotalPriceService().execute(self._order_items_dto, price_repository)

            repository.update_order(total_price)
