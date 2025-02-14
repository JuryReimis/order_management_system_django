from rest_framework import serializers

from carte.models import Dish


class DishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = ['id', 'title', 'price']
