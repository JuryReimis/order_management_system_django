from typing import List

from carte.dto.actual_price import ActualPriceDTO
from carte.dto.dish import DishDTO
from carte.dto.dish_list_update_time import DishListUpdateTimeDTO
from orders.dto.context.order_context import OrderContextDTO
from orders.dto.order import OrderDTO


class GetDetailOrderContextService:
    r"""Формирование контекста для детального представления."""

    def __init__(self, order_repository, dish_repository, price_changes_repository):
        self._order_repository = order_repository
        self._dish_repository = dish_repository
        self._price_changes_repository = price_changes_repository

    def _get_order_context(self, order: OrderDTO) -> OrderDTO:
        return self._order_repository(order).get_order_data()

    def _get_items_context(self, order: OrderDTO) -> List[DishDTO]:
        return self._dish_repository(order.order_id).get_items_data()

    def _get_price_changes_context(self, ids: List[int], last_update) -> List[ActualPriceDTO]:
        dto = DishListUpdateTimeDTO(
            ids=ids,
            last_update=last_update
        )
        return self._price_changes_repository().get_actual_price_by_time(dto)

    def execute(self, order_dto: OrderDTO) -> OrderContextDTO:
        order_data = self._get_order_context(order_dto)
        items_data = self._get_items_context(order_dto)
        price_changes_data = self._get_price_changes_context(ids=order_data.items, last_update=order_data.updated)

        return OrderContextDTO(
            order_id=order_data.order_id,
            order_table=order_data.table_number,
            order_status=order_data.status,
            order_status_display=order_data.status_display,
            order_total_price=order_data.total_price,
            items=items_data,
            item_price_dict={item.dish_id: item.actual_price for item in price_changes_data},
            item_quantity_dict={item.dish_id: item.quantity for item in items_data}
        )
