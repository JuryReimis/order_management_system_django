from typing import List

from django.db.models import F, Subquery, Max, OuterRef

from carte.dto.dish_price import DishPriceDTO
from carte.models import DishPriceChanges
from orders.dto.order_items import OrderItemsDTO


class DishPriceRepository:
    r"""Получаем список с данными об актуальных ценах и количестве блюд.
    У блюда актуальная цена - это цена блюда на момент последнего изменения состава заказа"""

    @staticmethod
    def _get_subquery(changed_date):
        r"""Получаем подзапрос с изменениями цен до момента последнего изменения состава заказа,
        после этого выбираем максимально близкую к дате изменения"""
        subquery = DishPriceChanges.objects.filter(
            dish=OuterRef('dish'),
            changed__lte=changed_date
        ).values('dish').annotate(
            max_changed=Max('changed')
        ).values('max_changed')
        return subquery

    @staticmethod
    def _get_price_list(items_ids, changed_date, max_price_date_subquery):
        r"""Получение списка блюд с их ценами, количеством и датой изменения"""
        return DishPriceChanges.objects.filter(
            dish__in=items_ids,
            changed__lte=changed_date
        ).annotate(
            max_changed=Subquery(max_price_date_subquery)
        ).filter(
            changed=F('max_changed')
        ).values('dish_id', 'new_price', 'changed')

    def get_prices(self, order_items: OrderItemsDTO, ) -> List[DishPriceDTO]:
        r"""Возвращает список с данными об актуальных ценах и количестве блюд"""
        items_ids = order_items.items_quantity_dict.keys()
        changed_date = order_items.last_update
        max_price_date_subquery = self._get_subquery(changed_date)
        price_list = self._get_price_list(items_ids, changed_date, max_price_date_subquery)
        return [DishPriceDTO(dish_id=value['dish_id'], price=value['new_price'], changed=value['changed'],
                             quantity=order_items.items_quantity_dict.get(value['dish_id'])) for value in price_list]
