from rest_framework import serializers

from carte.dto.dish import DishDTO
from carte.models import Dish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'title', 'price']


class DishQuantitySerializer(serializers.Serializer):
    dish_id = serializers.IntegerField()
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    quantity = serializers.IntegerField()

    def to_representation(self, instance: DishDTO):
        if not isinstance(instance, DishDTO):
            print(instance)
        data = {
            'dish_id': instance.dish_id,
            'title': instance.title,
            'price': instance.price,
            'quantity': instance.quantity
        }
        return super().to_representation(data)
