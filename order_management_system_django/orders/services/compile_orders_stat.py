import decimal
from decimal import Decimal
from typing import List

from orders.dto.context.order_statistic import OrderStatisticDTO
from orders.dto.dates_query import DatesQueryDTO
from orders.dto.order import OrderDTO


class CompileOrdersStatService:
    def __init__(self, repository):
        self._repository = repository

    @staticmethod
    def _get_amount(orders: List[OrderDTO]) -> int:
        return len(orders)

    @staticmethod
    def _get_sum_total_price(orders: List[OrderDTO]) -> Decimal:
        sum_ = Decimal(0)
        for order in orders:
            sum_ += order.total_price
        return sum_

    @staticmethod
    def _get_avg_total_price(sum_price: Decimal, amount: int) -> Decimal:
        return (sum_price / amount).quantize(Decimal('0.00'), rounding=decimal.ROUND_HALF_UP)

    def _get_paid_order_stat(self, dates: DatesQueryDTO) -> List[OrderDTO]:
        return self._repository.get_paided_orders_range_dates(dates)

    def execute(self, dates: DatesQueryDTO) -> OrderStatisticDTO:
        orders = self._get_paid_order_stat(dates)
        orders_amount = self._get_amount(orders)
        sum_total_price = self._get_sum_total_price(orders)
        avg_total_price = self._get_avg_total_price(sum_total_price, orders_amount)

        return OrderStatisticDTO(
            orders_amount=orders_amount,
            sum_total_price=sum_total_price,
            avg_total_price=avg_total_price
        )
