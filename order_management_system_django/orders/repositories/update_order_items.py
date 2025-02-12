from decimal import Decimal
from typing import List

from django.db import transaction
from django.utils import timezone

from carte.models import Dish
from orders.dto.order_items import OrderItemsDTO
from orders.models import Order, OrderItems


class UpdateOrderItemsRepository:
    def __init__(self, dto: OrderItemsDTO):
        self._order_items = dto
        self._order_items_to_update = []
        self._order_items_to_create = []
        self._order = self._get_order(self._order_items.order_id)

    @staticmethod
    def _get_order(order_id):
        if order_id is None:
            return None
        return Order.objects.get(pk=order_id)

    @staticmethod
    def _delete_unselected_items(order: Order, items: List[int]):
        OrderItems.objects.filter(order=order).exclude(dish_id__in=items).delete()

    def _compile_items_lists(self, order: Order, items: List[int]):
        dishes_to_add = Dish.objects.filter(pk__in=items)
        exciting_items = {item.dish_id: item for item in OrderItems.objects.filter(order=order)}
        exciting_dish_ids = exciting_items.keys()

        for dish in dishes_to_add:
            quantity = self._order_items.items_quantity_dict.get(dish.pk)
            if dish.pk in exciting_dish_ids:
                order_item = exciting_items.get(dish.pk)
                order_item.quantity = quantity
                self._order_items_to_update.append(order_item)
            else:
                order_item = OrderItems(order=order, dish_id=dish.pk, quantity=quantity)
                self._order_items_to_create.append(order_item)

    def _bulk_update(self):
        if self._order_items_to_update:
            OrderItems.objects.bulk_update(self._order_items_to_update, ['quantity'])

        if self._order_items_to_create:
            OrderItems.objects.bulk_create(self._order_items_to_create)
        self._order_items.last_update = timezone.now()

    def _update_total_price(self, total_price: Decimal):
        last_update = timezone.now()
        order = self._order
        order.total_price = total_price
        order.updated = last_update
        order.save()

    @staticmethod
    def _create_items(table_number):
        return Order.objects.create(table_number=table_number)

    def _update_items(self):
        order = self._order
        if order is not None:
            items = list(self._order_items.items_quantity_dict.keys())
            with transaction.atomic():
                self._delete_unselected_items(order, items)
                self._compile_items_lists(order, items)
                self._bulk_update()
        else:
            raise ValueError("Не передано ни номера стола, ни id заказа")

    def save_items(self, table_number: int = None):
        if table_number is not None:
            self._order = self._create_items(table_number)
        self._update_items()

    def update_order(self, total_price: Decimal):
        self._update_total_price(total_price)
