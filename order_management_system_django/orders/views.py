from datetime import datetime
from typing import List

from django.contrib import messages
from django.db import IntegrityError
from django.db.models import QuerySet
from django.forms import formset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic, View

from carte.models import Dish
from carte.repositories.dish_price_repository import DishPriceRepository
from orders.dto.dates_query import DatesQueryDTO
from orders.dto.order_items import OrderItemsDTO
from orders.forms import CreateNewOrderForm, UpdateOrderItemsForm, UpdateQuantityForm, DateRangeForm
from orders.mixins import GetOrdersListMixin, GetOrderDetailMixin
from orders.models import Order, OrderItems
from orders.repositories.order import OrderRepository
from orders.repositories.orders_filter import OrdersFilterRepository
from orders.repositories.update_order_items import UpdateOrderItemsRepository
from orders.services.compile_orders_stat import CompileOrdersStatService
from orders.services.update_order import UpdateOrderService


class CreateNewOrderView(generic.CreateView):
    template_name = 'orders/add-new-order.html'
    form_class = CreateNewOrderForm
    success_url = reverse_lazy('orders:create_order')

    def get(self, request, *args, **kwargs):
        dishes = Dish.objects.order_by('-price')
        self.extra_context = {
            'dishes': dishes
        }
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        items = request.POST.getlist('items')
        if items:
            order_repository = OrderRepository
            update_order_items_repository = UpdateOrderItemsRepository
            dish_price_repository = DishPriceRepository
            dto = OrderItemsDTO(
                order_id=None,
                items_quantity_dict={int(item): int(request.POST.get(f'item_{item}-quantity', 1)) for item in items},
                last_update=None,
                table_number=request.POST.get('table_number')
            )
            try:
                service = UpdateOrderService(order_items_dto=dto, order_repository=order_repository,
                                             update_order_items_repository=update_order_items_repository,
                                             dish_price_repository=dish_price_repository)
                service.execute()
            except IntegrityError:
                messages.error(request, "Уже существует неоплаченный заказ для этого стола", extra_tags='danger')
            except Exception as err:
                messages.error(request, f"Непредвиденная ошибка {err}")
            else:
                messages.success(request, "Заказ успешно создан")
        else:
            messages.error(request=request, message="Заказ не может быть пустым", extra_tags='danger')
        return self.get(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('table_number', "Для этого стола уже зарегистрирован неоплаченный заказ")
            return self.form_invalid(form)


class GetAllOrdersView(generic.ListView):
    paginate_by = 9
    context_object_name = 'orders'
    template_name = 'orders/orders-list.html'

    def get_queryset(self):
        orders = Order.objects.order_by('-created')
        return orders


class OrderDetailView(GetOrderDetailMixin, generic.DetailView):
    model = Order
    template_name = 'orders/order-detail.html'
    context_object_name = 'order'

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404 as err:
            raise Http404(err)
        except ValueError as err:
            messages.error(self.request, f"Произошла ошибка {err}", extra_tags='danger')
        except Exception as err:
            messages.error(self.request, f"Непредвиденная ошибка {err}", extra_tags='danger')
        return redirect('orders:get_all_orders')


class OrderDeleteView(generic.DeleteView):
    success_url = reverse_lazy('orders:get_all_orders')

    def get_object(self, queryset=None):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        return order


class OrderChangeItemsView(View):
    form_class = UpdateOrderItemsForm
    template_name = 'orders/update-order-items.html'
    model = Order

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        dishes = list(Dish.objects.exclude(pk__in=order.items.all().values_list('id', flat=True)))
        context = self.get_context_data(order=order, items=dishes)
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        order_id = kwargs['pk']
        items = request.POST.getlist('items')
        if order_id is not None and items is not None:
            dto = OrderItemsDTO(
                order_id=order_id,
                items_quantity_dict={int(item): int(request.POST.get(f'item_{item}-quantity', 1)) for item in items},
                last_update=None
            )
            try:
                order_repository = OrderRepository
                update_order_items_repository = UpdateOrderItemsRepository
                dish_price_repository = DishPriceRepository
                service = UpdateOrderService(order_items_dto=dto, order_repository=order_repository,
                                             update_order_items_repository=update_order_items_repository,
                                             dish_price_repository=dish_price_repository)
                service.execute()
            except ValueError as err:
                messages.error(request, f"Произошла ошибка {err}", extra_tags='danger')
            except Exception as err:
                messages.error(request, f"Произошла непредвиденная ошибка {err}", extra_tags='danger')
            else:
                messages.success(request, "Изменение заказа произошло успешно!")
        else:
            raise Http404(f"Не получены данные, необходимые для обновления id = {order_id}, выбранные блюда = {items}")

        return redirect(self.get_success_url())

    def get_context_data(self, order: Order, items: List[Dish], **kwargs):
        order_items = order.order_items.all()
        formset = self.get_formset(order_items)
        form_dict = {}
        for form in formset:
            dish_id = form.initial['dish_id']
            form.prefix = f"item_{dish_id}"
            form_dict[dish_id] = form
        context = {
            'order': order,
            'dishes': items,
            'form_dict': form_dict
        }
        return context

    @staticmethod
    def get_formset(order_items: QuerySet[OrderItems]):
        update_quantity_formset = formset_factory(UpdateQuantityForm, extra=0)
        return update_quantity_formset(
            initial=[{'quantity': item.quantity,
                      'dish_id': item.dish_id} for item in order_items]
        )

    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.kwargs.get('pk')})


class OrderChangeStatusView(View):

    def post(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            new_status = Order.PENDING
            if 'ready' in request.POST:
                new_status = Order.READY
            elif 'paid' in request.POST:
                new_status = Order.PAID
            self.save_new_status(obj, new_status)
        except IntegrityError as err:
            messages.warning(request, f"Уже имеется неоплаченный заказ на этом столе {err}")
        return redirect('orders:order_detail', pk=kwargs['pk'])

    @staticmethod
    def save_new_status(obj: Order, status: Order.STATUS):
        obj.status = status
        obj.save()

    def get_object(self):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        return order


class OrderSearchView(GetOrdersListMixin, generic.ListView):
    paginate_by = 9
    context_object_name = 'orders'
    template_name = 'orders/orders-list.html'


class GetOrdersStatsView(View):
    template_name = 'orders/orders_stats.html'
    form: DateRangeForm = DateRangeForm

    def get(self, request, *args, **kwargs):
        form = self.form(request.GET)
        context = {
            'form': form
        }

        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        if start_date_str and end_date_str:
            if form.is_valid():
                start_date = timezone.make_aware(datetime.fromisoformat(start_date_str))
                end_date = timezone.make_aware(datetime.fromisoformat(end_date_str))
                try:
                    dto = DatesQueryDTO(
                        start_date=start_date,
                        end_date=end_date
                    )
                    repository = OrdersFilterRepository()
                    service = CompileOrdersStatService(repository)
                    context['statistic'] = service.execute(dto)
                except Exception as err:
                    messages.error(request, f"Произошла ошибка\n{err}", extra_tags='danger')

        return render(request, self.template_name, context=context)
