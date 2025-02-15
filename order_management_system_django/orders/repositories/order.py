from decimal import Decimal

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from orders.dto.order import OrderDTO
from orders.dto.order_items import OrderItemsDTO
from orders.models import Order


class OrderRepository:

    def __init__(self, order_items_dto: OrderItemsDTO):
        self._order_items_dto = order_items_dto
        self._order: Order | None = self._get_order()

    def _create_order(self, table_number):
        order = Order.objects.create(table_number=table_number)
        self._order_items_dto.order_id = order.pk
        return order

    def _get_order(self):
        order_id = self._order_items_dto.order_id
        if order_id is not None:
            return get_object_or_404(Order, pk=order_id)
        table_number = self._order_items_dto.table_number
        if table_number is None:
            raise ValueError("Произошла ошибка, в обработку не предано ни номера стола, ни id заказа")
        return self._create_order(table_number)

    def _update_total_price(self, new_total_price):
        last_update = self._order_items_dto.last_update
        if last_update is None:
            print("Время последнего обновления отсутствует в dto")
            last_update = timezone.now()
        order = self._order
        order.total_price = new_total_price
        order.updated = last_update

    def _update_status(self, new_status):
        order = self._order
        if new_status in list(map(lambda status_tuple: status_tuple[0], Order.STATUS)):
            order.status = new_status
        else:
            raise ValidationError(f"У заказа не может быть статуса {new_status}")

    def _order_save(self):
        self._order.save()

    def get_order_data(self) -> OrderDTO:
        if self._order:
            dto = OrderDTO(
                order_id=self._order.pk,
                table_number=self._order.table_number,
                items=[item.pk for item in self._order.items.all()],
                status=self._order.status,
                status_display=self._order.get_status_display(),
                updated=self._order.updated,
                total_price=self._order.total_price
            )
            return dto
        raise ValueError("Нет объекта")

    def update_order(self, total_price: Decimal | None, new_status: int | None):
        if new_status:
            self._update_status(new_status)
        if total_price:
            self._update_total_price(total_price)
        if total_price is None and new_status is None:
            raise ValidationError(f"Запрос должен содержать данные, для изменения: "
                                  f"items - список словарей с ключами dish_id и quantity "
                                  f"или status в разрешенных значениях {Order.STATUS}")
        self._order_save()
