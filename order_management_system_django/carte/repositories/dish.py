from typing import List

from django.db.models import Subquery, OuterRef

from carte.dto.dish import DishDTO
from carte.models import Dish
from orders.models import OrderItems


class DishRepository:

    def __init__(self, order_id: int):
        self._order_id = order_id

    def _get_subquery(self):
        subquery = OrderItems.objects.filter(
            order_id=self._order_id,
            dish_id=OuterRef('pk')
        ).values('quantity')
        return subquery

    def _get_items(self):
        items = Dish.objects.filter(
            pk__in=OrderItems.objects.filter(order_id=self._order_id).values_list('dish_id', flat=True)
        ).annotate(
            quantity=Subquery(self._get_subquery())
        )

        return items

    def get_items_data(self) -> List[DishDTO]:
        items = self._get_items()
        return [DishDTO(
            dish_id=item.pk,
            title=item.title,
            price=item.price,
            quantity=item.quantity
        ) for item in items]
