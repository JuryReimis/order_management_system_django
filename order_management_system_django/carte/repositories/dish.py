from typing import List

from django.db.models import Subquery, OuterRef

from carte.dto.dish import DishDTO
from carte.models import Dish
from orders.models import OrderItems


class DishRepository:
    r"""Дополнительный слой для взаимодействия с базой данных с помощью ORM Django"""

    def __init__(self, order_id: int):
        r"""Инициализация, сохранение id заказа, с которым будем работать"""
        self._order_id = order_id

    def _get_subquery(self):
        r"""Получение подзапроса, через который мы сможем за один запрос к бд получить количество блюд в заказе"""
        subquery = OrderItems.objects.filter(
            order_id=self._order_id,
            dish_id=OuterRef('pk')
        ).values('quantity')
        return subquery

    def _get_items(self):
        r"""Получение QuerySet с блюдами, которые относятся к заказу"""
        items = Dish.objects.filter(
            pk__in=OrderItems.objects.filter(order_id=self._order_id).values_list('dish_id', flat=True)
        ).annotate(
            quantity=Subquery(self._get_subquery())  # Добавляем данные о количестве блюд в заказе
        )

        return items

    def get_items_data(self) -> List[DishDTO]:
        r"""Возвращаем список объектов с данными о блюдах"""
        items = self._get_items()
        return [DishDTO(
            dish_id=item.pk,
            title=item.title,
            price=item.price,
            quantity=item.quantity
        ) for item in items]
