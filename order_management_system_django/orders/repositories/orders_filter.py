from typing import List

from orders.dto.dates_query import DatesQueryDTO
from orders.dto.order import OrderDTO
from orders.models import Order


class OrdersFilterRepository:

    def get_paided_orders_range_dates(self, dates: DatesQueryDTO) -> List[OrderDTO]:
        orders = Order.objects.filter(updated__range=[dates.start_date, dates.end_date], status=Order.PAID)
        return [OrderDTO(
            order_id=order.pk,
            total_price=order.total_price,
            status=None,
            table_number=None,
            updated=None,
            items=None,
            status_display=None
        ) for order in orders]
