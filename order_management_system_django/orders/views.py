from typing import List

from django.contrib import messages
from django.db import IntegrityError
from django.db.models import QuerySet
from django.forms import formset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic, View

from carte.models import Dish
from orders.dto.order_items import OrderItemsDTO
from orders.dto.search_query import SearchQueryDTO
from orders.forms import CreateNewOrderForm, UpdateOrderItemsForm, UpdateQuantityForm
from orders.models import Order, OrderItems
from orders.services.compile_order_filter import CompileOrderFilterService
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
            dto = OrderItemsDTO(
                order_id=None,
                items_quantity_dict={int(item): int(request.POST.get(f'item_{item}-quantity', 1)) for item in items},
                last_update=None
            )
            try:
                service = UpdateOrderService(dto)
                service.execute(request.POST.get('table_number'))
            except IntegrityError:
                messages.warning(request, "Уже существует неоплаченный заказ для этого стола")
            except Exception as err:
                messages.error(request, f"Непредвиденная ошибка {err}")
            finally:
                messages.success(request, "Заказ успешно создан")
        else:
            messages.error(request=request, message="Заказ не может быть пустым")
        return self.get(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('table_number', "Для этого стола уже зарегистрирован неоплаченный заказ")
            return self.form_invalid(form)


class GetAllOrdersView(generic.ListView):
    paginate_by = 10
    context_object_name = 'orders'
    template_name = 'orders/orders-list.html'

    def get_queryset(self):
        orders = Order.objects.order_by('-created')
        return orders


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'orders/order-detail.html'


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
                service = UpdateOrderService(dto)
                service.execute()
            except ValueError as err:
                messages.error(request, f"Произошла ошибка {err}")
            except Exception as err:
                messages.error(request, f"Произошла непредвиденная ошибка {err}")
            finally:
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

    def get_formset(self, order_items: QuerySet[OrderItems]):
        UpdateQuantityFormSet = formset_factory(UpdateQuantityForm, extra=0)
        return UpdateQuantityFormSet(
            initial=[{'quantity': item.quantity,
                      'dish_id': item.dish_id} for item in order_items]
        )

    def get_success_url(self):
        return reverse_lazy('orders:order_detail', kwargs={'pk': self.kwargs.get('pk')})


class OrderChangeStatusView(View):

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        new_status = Order.PENDING
        if 'ready' in request.POST:
            new_status = Order.READY
        elif 'paid' in request.POST:
            new_status = Order.PAID
        self.save_new_status(obj, new_status)
        return redirect('orders:order_detail', pk=kwargs.get('pk'))

    @staticmethod
    def save_new_status(obj: Order, status: Order.STATUS):
        obj.status = status
        obj.save()

    def get_object(self):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        return order


class OrderSearchView(generic.ListView):
    paginate_by = 10
    context_object_name = 'orders'
    template_name = 'orders/orders-list.html'

    def get(self, request, *args, **kwargs):
        table = request.GET.get('table')
        status = request.GET.get('status')
        service = CompileOrderFilterService()
        query = SearchQueryDTO(table=table, status=status)
        callback = service.execute(query)
        filter_opt = callback.filter
        self.kwargs['filter_opt'] = filter_opt
        return super().get(request, args, kwargs)

    def get_queryset(self):
        filter_opt = self.kwargs.pop('filter_opt')
        order = Order.objects.filter(filter_opt).order_by('-created')
        return order
