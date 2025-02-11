from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from carte.repositories.dish_price_repository import DishPriceRepository
from orders.dto.order_items import OrderItemsDTO
from orders.models import Order
from orders.services.calculate_total_price import CalculateTotalPriceService


@receiver(m2m_changed, sender=Order.items.through)
def update_order_total_price(sender, instance: Order, action, **kwargs):
    """
    Обновляет общую стоимость заказа при изменении связи m2m.
    """
    if action in ('post_add', 'post_remove', 'post_clear'):
        if instance.status == instance.PENDING:
            items = instance.order_items.order_by('-created')
            items_ids = [item.dish_id for item in items]
            last_update = items.first().created
            dto = OrderItemsDTO(
                order_id=instance.id,
                items_ids=items_ids,
                last_update=last_update
            )
            repository = DishPriceRepository()
            total_price = CalculateTotalPriceService().execute(dto, repository)
            instance.total_price = total_price
            instance.save()
