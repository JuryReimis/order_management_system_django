from typing import List, Dict

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from carte.repositories.dish_price_repository import DishPriceRepository
from orders.api.v1.serializers import OrderSerializer, OrderContextSerializer
from orders.dto.order_items import OrderItemsDTO
from orders.mixins import GetOrdersListMixin, GetOrderDetailMixin
from orders.models import Order
from orders.repositories.order import OrderRepository
from orders.repositories.update_order_items import UpdateOrderItemsRepository
from orders.services.update_order import UpdateOrderService


class GetOrdersListAPIView(GetOrdersListMixin, ListAPIView):
    serializer_class = OrderSerializer


class GetOrderDetailAPIView(GetOrderDetailMixin, RetrieveAPIView):
    serializer_class = OrderContextSerializer

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as err:
            return Response(f"Произошла ошибка {err}", status=status.HTTP_400_BAD_REQUEST)


class CreateOrderAPIView(APIView):
    r"""Эндпоинт для создания заказа.
    На вход должен поступать table_number в формате int и список словарей {'dish_id': int, 'quantity': int}"""

    def post(self, request, *args, **kwargs):
        items: List[Dict[str, int]] = request.data.get('items')
        if items:
            order_repository = OrderRepository
            update_order_items_repository = UpdateOrderItemsRepository
            dish_price_repository = DishPriceRepository
            try:
                dto = OrderItemsDTO(
                    order_id=None,
                    items_quantity_dict={int(item.get('dish_id')): int(item.get('quantity')) for item in items},
                    last_update=None,
                    table_number=request.data.get('table_number')
                )
                service = UpdateOrderService(order_items_dto=dto, order_repository=order_repository,
                                             update_order_items_repository=update_order_items_repository,
                                             dish_price_repository=dish_price_repository)
                service.execute()
            except IntegrityError:
                return Response(f"Уже существует неоплаченный заказ для этого стола",
                                status=status.HTTP_400_BAD_REQUEST)
            except Exception as err:
                return Response(f"Непредвиденная ошибка {err}", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Заказ успешно создан", status=status.HTTP_201_CREATED)


class UpdateOrderItemsAPIView(UpdateAPIView):
    r"""Эндпоинт для обновления заказа.
    На вход ожидает несколько значений. items - список словарей {'dish_id': int, 'quantity': int}
    Список значений Dish, которые необходимо оставить в составе заказа.
    status: int - цифровое выражение статуса, который необходимо выставить заказу"""
    serializer_class = OrderSerializer

    def patch(self, request, *args, **kwargs):
        items: List[Dict[str, int]] = request.data.get('items')
        new_status = request.data.get('status')
        if items or new_status:
            try:
                self.update_order(items, new_status)
            except ValidationError as err:
                return Response(f"{err}", status=status.HTTP_400_BAD_REQUEST)
            except Exception as err:
                return Response(f"Произошла ошибка {err}", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(f"Заказ успешно изменен")
        else:
            return Response(f"Запрос должен содержать данные, для изменения: "
                            f"items - список словарей с ключами dish_id и quantity "
                            f"или status в разрешенных значениях {Order.STATUS}")

    def update_order(self, items, new_status):
        order_repository = OrderRepository
        update_order_items_repository = UpdateOrderItemsRepository
        dish_price_repository = DishPriceRepository
        if items:
            items_quantity_dict = {int(item.get('dish_id')): int(item.get('quantity')) for item in items}
        else:
            items_quantity_dict = {}
        dto = OrderItemsDTO(
            order_id=self.kwargs.get('pk'),
            items_quantity_dict=items_quantity_dict,
            last_update=None,
            new_status=new_status,
            table_number=None
        )
        service = UpdateOrderService(order_items_dto=dto, order_repository=order_repository,
                                     update_order_items_repository=update_order_items_repository,
                                     dish_price_repository=dish_price_repository)
        service.execute()


class DeleteOrderAPIView(DestroyAPIView):
    r"""Эндпоинт для удаления заказа"""
    queryset = Order.objects.all()
