from django.db import transaction

from orders.dto.order_items import OrderItemsDTO
from orders.services.calculate_total_price import CalculateTotalPriceService


class UpdateOrderService:
    r"""Сервис для обновления и создания заказа"""

    def __init__(self, order_items_dto: OrderItemsDTO, order_repository, update_order_items_repository,
                 dish_price_repository):
        self._update_order_items_repository = update_order_items_repository
        self._order_repository = order_repository
        self._price_repository = dish_price_repository
        self._order_items_dto = order_items_dto

    def execute(self):
        """Обновляет элементы заказа и пересчитывает общую стоимость."""

        with transaction.atomic():
            order_repository = self._order_repository(self._order_items_dto)

            update_items_repository = self._update_order_items_repository(self._order_items_dto)
            update_items_repository.save_items()

            price_repository = self._price_repository()
            total_price = CalculateTotalPriceService().execute(self._order_items_dto, price_repository)

            order_repository.update_order(total_price=total_price, new_status=self._order_items_dto.new_status)
