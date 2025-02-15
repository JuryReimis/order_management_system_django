from rest_framework import serializers

from carte.api.v1.serializers import DishQuantitySerializer

from orders.dto.context.order_context import OrderContextDTO
from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    r"""Стандартный сериализатор для модели Order"""

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items', 'total_price', 'status', 'updated']
        read_only_fields = ['id', 'total_price', 'status', 'updated']


class OrderContextSerializer(serializers.Serializer):
    r"""Сериализатор для преобразования OrderContextDTO в json"""

    order_id = serializers.IntegerField()
    order_table = serializers.IntegerField()
    order_total_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    order_status = serializers.IntegerField()
    order_status_display = serializers.CharField()
    items = DishQuantitySerializer(many=True)

    def to_representation(self, instance: OrderContextDTO):

        # Присваиваем каждому item цены из словаря с актуальными ценами
        for item in instance.items:
            item.price = instance.item_price_dict.get(item.dish_id)

        data = {
            'order_id': instance.order_id,
            'order_table': instance.order_table,
            'order_total_price': instance.order_total_price,
            'order_status': instance.order_status,
            'order_status_display': instance.order_status_display,
            'items': instance.items
        }
        return super().to_representation(data)


