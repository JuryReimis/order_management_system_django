from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, \
    DestroyAPIView

from carte.api.v1.serializers import DishSerializer
from carte.models import Dish


class CreateDishAPIView(CreateAPIView):
    serializer_class = DishSerializer


class GetDishesAPIView(ListAPIView):
    serializer_class = DishSerializer

    def get_queryset(self):
        queryset = Dish.objects.all()
        return queryset


class GetDishDetailAPIView(RetrieveAPIView):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()


class UpdateDishAPIView(UpdateAPIView):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()


class DeleteDishAPIView(DestroyAPIView):
    queryset = Dish.objects.all()
