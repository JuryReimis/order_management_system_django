from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from orders.forms import CreateNewOrderForm
from orders.models import Order


class CreateNewOrderView(generic.CreateView):
    template_name = 'orders/add-new-order.html'
    form_class = CreateNewOrderForm
    success_url = reverse_lazy('orders:create_order')


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

