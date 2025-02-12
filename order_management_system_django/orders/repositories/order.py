from carte.dto.dish import DishDTO
from orders.dto.order import OrderDTO
from orders.models import Order


class OrderRepository:

    def __init__(self, order_id):
        self.order: Order | None = self._get_order(order_id)

    def _get_order(self, order_id):
        if order_id is not None:
            return Order.objects.get(pk=order_id)

    def get_order_data(self) -> OrderDTO:
        if self.order:
            dto = OrderDTO(
                order_id=self.order.pk,
                table_number=self.order.table_number,
                items=[item.pk for item in self.order.items.all()],
                status=self.order.status,
                status_display=self.order.get_status_display(),
                updated=self.order.updated,
                total_price=self.order.total_price
            )
            return dto
        raise ValueError("Нет объекта")
