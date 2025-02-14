from decimal import Decimal
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
            return Order.objects.get(pk=order_id)
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
        order.save()

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

    def update_order(self, total_price: Decimal):
        self._update_total_price(total_price)
