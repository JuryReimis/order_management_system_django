from typing import List

from django.db.models import F, Subquery, Max, OuterRef

from carte.dto.dish_price import DishPriceDTO
from carte.models import DishPriceChanges
from orders.dto.order_items import OrderItemsDTO


class DishPriceRepository:

    def get_prices(self, order_items: OrderItemsDTO, ) -> List[DishPriceDTO]:
        items_ids = order_items.items_quantity_dict.keys()
        changed_date = order_items.last_update
        max_price_date_subquery = DishPriceChanges.objects.filter(
            dish=OuterRef('dish'),
            changed__lte=changed_date
        ).values('dish').annotate(
            max_changed=Max('changed')
        ).values('max_changed')

        price_list = DishPriceChanges.objects.filter(
            dish__in=items_ids,
            changed__lte=changed_date
        ).annotate(
            max_changed=Subquery(max_price_date_subquery)
        ).filter(
            changed=F('max_changed')
        ).values('dish_id', 'new_price', 'changed')
        return [DishPriceDTO(dish_id=value['dish_id'], price=value['new_price'], changed=value['changed'],
                             quantity=order_items.items_quantity_dict.get(value['dish_id'])) for value in price_list]
