from typing import List

from django.db import transaction
from django.utils import timezone

from carte.models import Dish
from orders.dto.order_items import OrderItemsDTO
from orders.models import OrderItems


class UpdateOrderItemsRepository:
    def __init__(self, dto: OrderItemsDTO):
        self._order_items_dto = dto
        self._order_items_to_update = []
        self._order_items_to_create = []

    @staticmethod
    def _delete_unselected_items(order_id: int, items: List[int]):
        OrderItems.objects.filter(order_id=order_id).exclude(dish_id__in=items).delete()

    def _compile_items_lists(self, order_id: int, items: List[int]):
        dishes_to_add = Dish.objects.filter(pk__in=items)
        exciting_items = {item.dish_id: item for item in OrderItems.objects.filter(order_id=order_id)}
        exciting_dish_ids = exciting_items.keys()

        for dish in dishes_to_add:
            quantity = self._order_items_dto.items_quantity_dict.get(dish.pk)
            if dish.pk in exciting_dish_ids:
                order_item = exciting_items.get(dish.pk)
                order_item.quantity = quantity
                self._order_items_to_update.append(order_item)
            else:
                order_item = OrderItems(order_id=order_id, dish_id=dish.pk, quantity=quantity)
                self._order_items_to_create.append(order_item)

    def _bulk_update_or_create(self):
        if self._order_items_to_update:
            OrderItems.objects.bulk_update(self._order_items_to_update, ['quantity'])

        if self._order_items_to_create:
            OrderItems.objects.bulk_create(self._order_items_to_create)
        self._order_items_dto.last_update = timezone.now()

    def _update_items(self):
        order_id = self._order_items_dto.order_id
        if order_id is not None:
            items = list(self._order_items_dto.items_quantity_dict.keys())
            with transaction.atomic():
                self._delete_unselected_items(order_id, items)
                self._compile_items_lists(order_id, items)
                self._bulk_update_or_create()
        else:
            raise ValueError("Невозможно сохранить список без id заказа")

    def save_items(self):
        if self._order_items_dto.items_quantity_dict:
            self._update_items()
